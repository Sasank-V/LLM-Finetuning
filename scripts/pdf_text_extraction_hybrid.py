#!/usr/bin/env python
# coding: utf-8

# # Hybrid PDF Text Extraction (Multi-Parser + Datalab Marker Fallback)
#
#
#
# This notebook extracts text page-by-page from PDFs using a robust hybrid strategy:
#
# 1. Multiple primary parsers per page: PyMuPDF, pdfplumber, and pypdf.
#
# 2. Rich garble detection metrics (symbol ratio, dictionary OOV ratio, language confidence, encoding artifacts, token structure).
#
# 3. Best-parser selection by quality score and threshold gating.
#
# 4. Automatic fallback to Datalab Marker markdown when quality is poor.
#
# 5. Per-page CSV output with diagnostics and source used.
#

# In[1]:


get_ipython().run_line_magic(
    "pip",
    "install pymupdf pdfplumber pypdf pandas tqdm requests python-dotenv langdetect chardet wordfreq openai",
)


# In[2]:


import base64
import csv
import gc
import json
import os
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

import chardet
import fitz
import pandas as pd
import pdfplumber
import requests
from dotenv import load_dotenv
from langdetect import DetectorFactory, detect_langs
from openai import OpenAI
from pypdf import PdfReader
from tqdm.auto import tqdm
from wordfreq import zipf_frequency


# In[3]:


load_dotenv()
DetectorFactory.seed = 0


def find_workspace_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "datasets" / "training" / "Books").exists():
            return candidate
    return start.resolve()


WORKSPACE_ROOT = find_workspace_root(Path.cwd())
# BOOKS_DIR = WORKSPACE_ROOT / "datasets" / "training" / "Books"
# OUTPUT_DIR = WORKSPACE_ROOT / "datasets" / "training"
BOOKS_DIR = WORKSPACE_ROOT / "Books"
OUTPUT_DIR = WORKSPACE_ROOT
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DATALAB_MARKER_URL = os.getenv(
    "DATALAB_MARKER_URL", "http://localhost:8001/marker/upload"
).strip()
MARKER_TIMEOUT_SEC = int(os.getenv("MARKER_TIMEOUT_SEC", "120"))

VISION_LLM_MODEL = os.getenv(
    "VISION_LLM_MODEL_NAME", "Qwen/Qwen3-VL-8B-Instruct"
).strip()
VISION_LLM_BASE_URL = os.getenv(
    "VISION_LLM_API_URL", "http://localhost:8002/v1"
).strip()
VISION_LLM_API_KEY = os.getenv("VISION_LLM_API_KEY", "").strip()


def make_vision_client(base_url: str, api_key: str):
    if not base_url:
        return None
    try:
        return OpenAI(base_url=base_url, api_key=api_key or "EMPTY")
    except Exception:
        return None


VISION_CLIENT = make_vision_client(VISION_LLM_BASE_URL, VISION_LLM_API_KEY)

print(f"Workspace root: {WORKSPACE_ROOT}")
print(f"Books dir: {BOOKS_DIR}")
print(f"Output dir: {OUTPUT_DIR}")
print(f"Marker URL configured: {bool(DATALAB_MARKER_URL)}")
print(f"Vision model configured: {bool(VISION_LLM_MODEL and VISION_CLIENT)}")


# In[4]:


NOISE_PATTERNS = [
    r"^\s*\d+\s*$",
    r"^\s*page\s+\d+\s*$",
    r"^\s*chapter\s+\d+\s*$",
    r"^\s*contents\s*$",
    r"^\s*copyright\b.*$",
    r"^\s*all rights reserved\b.*$",
    r"^\s*isbn\b.*$",
    r"^\s*www\..*$",
    r"^\s*https?://.*$",
    r"^\s*\.{4,}\s*\d+\s*$",
]


def normalize_text(text: str) -> str:
    text = text or ""
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u00ad", "")
    text = re.sub(r"-\n(?=[a-z])", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def should_drop_line(line: str) -> bool:
    clean = line.strip()
    if not clean:
        return True
    if len(clean) <= 2:
        return True
    for pat in NOISE_PATTERNS:
        if re.match(pat, clean, flags=re.IGNORECASE):
            return True
    if sum(ch.isdigit() for ch in clean) > 10 and len(clean) < 30:
        return True
    return False


def deep_clean_text(raw_text: str) -> str:
    lines = [ln.rstrip() for ln in (raw_text or "").splitlines()]
    cleaned: List[str] = []
    for line in lines:
        if should_drop_line(line):
            continue
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            cleaned.append(line)

    merged: List[str] = []
    for line in cleaned:
        if (
            merged
            and len(line) < 80
            and line[0].islower()
            and not merged[-1].endswith((".", ":", ";", "?", "!"))
        ):
            merged[-1] = f"{merged[-1]} {line}"
        else:
            merged.append(line)

    text = "\n".join(merged)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_page_text_pymupdf(doc: fitz.Document, page_idx: int) -> str:
    page = doc[page_idx]
    h = page.rect.height
    blocks = page.get_text("blocks")

    filtered = []
    for b in blocks:
        x0, y0, x1, y1, txt, block_no, block_type = b
        if block_type != 0:
            continue
        if y0 <= h * 0.04 or y1 >= h * 0.96:
            continue
        t = (txt or "").strip()
        if not t:
            continue
        filtered.append((y0, x0, t))

    filtered.sort(key=lambda x: (round(x[0], 1), round(x[1], 1)))
    joined = "\n".join(t for _, _, t in filtered)
    return deep_clean_text(joined)


def single_page_pdf_bytes(doc: fitz.Document, page_idx: int) -> bytes:
    temp = fitz.open()
    temp.insert_pdf(doc, from_page=page_idx, to_page=page_idx)
    data = temp.tobytes()
    temp.close()
    return data


# In[5]:


# Marker API fix: use documented upload params and parse only real content fields.

_MARKER_META_KEYS = {
    "output_format",
    "page_range",
    "force_ocr",
    "paginate_output",
    "status",
    "success",
    "filename",
    "file",
    "message",
}


def _marker_upload_url(url: str) -> str:
    u = (url or "").strip().rstrip("/")
    if not u:
        return u
    if u.endswith("/marker/upload"):
        return u
    if u.endswith("/marker"):
        return f"{u}/upload"
    return f"{u}/marker/upload"


def _extract_marker_content(payload: Any) -> str:
    if isinstance(payload, str):
        t = payload.strip()
        if not t:
            return ""
        if t.lower() in {"markdown", "json", "html"}:
            return ""
        return t

    if isinstance(payload, list):
        parts: List[str] = []
        for item in payload:
            got = _extract_marker_content(item)
            if got:
                parts.append(got)
        return "\n\n".join(parts).strip()

    if isinstance(payload, dict):
        # Prefer explicit content keys first.
        for key in [
            "markdown",
            "text",
            "content",
            "page_markdown",
            "page_text",
            "full_text",
            "result",
            "output",
        ]:
            if key in payload:
                got = _extract_marker_content(payload.get(key))
                if got:
                    return got

        # If paginated structure exists, collect per-page bodies.
        for key in ["pages", "page_outputs", "items", "data"]:
            if key in payload and isinstance(payload.get(key), list):
                got = _extract_marker_content(payload.get(key))
                if got:
                    return got

        # Fallback over values but skip metadata keys.
        parts: List[str] = []
        for k, v in payload.items():
            if str(k).strip().lower() in _MARKER_META_KEYS:
                continue
            got = _extract_marker_content(v)
            if got:
                parts.append(got)
        return "\n\n".join(parts).strip()

    return ""


def extract_page_markdown_marker(
    file_bytes: bytes, filename: str, marker_url: str, timeout_sec: int = 120
) -> str:
    if not marker_url:
        return ""

    files = {"file": (filename, file_bytes, "application/pdf")}
    data = {
        "output_format": "markdown",
        "paginate_output": "false",
        "force_ocr": "false",
    }
    headers = {"Accept": "application/json"}

    primary = _marker_upload_url(marker_url)
    candidates = [primary]
    if marker_url.strip() and marker_url.strip() not in candidates:
        candidates.append(marker_url.strip())

    last_error = None
    for endpoint in candidates:
        try:
            resp = requests.post(
                endpoint, files=files, data=data, headers=headers, timeout=timeout_sec
            )
            resp.raise_for_status()
            try:
                payload = resp.json()
                extracted = _extract_marker_content(payload)
                if extracted:
                    return deep_clean_text(extracted)
            except Exception:
                pass

            raw = (resp.text or "").strip()
            if not raw:
                continue
            try:
                payload = json.loads(raw)
                extracted = _extract_marker_content(payload)
                if extracted:
                    return deep_clean_text(extracted)
            except Exception:
                # If server returns plain markdown/text directly.
                if raw.lower() not in {"markdown", "json", "html"}:
                    return deep_clean_text(raw)

        except Exception as exc:
            last_error = exc
            continue

    if last_error:
        raise last_error
    return ""


# In[6]:


# Multi-parser quality engine override (PyMuPDF + pdfplumber + pypdf + Vision LaTeX fallback)
MOJIBAKE_RE = re.compile(r"(?:Ã.|Â.|â€|â€™|â€œ|â€\x9d|�)")
WORD_RE = re.compile(r"[A-Za-z]{2,}")
SUSPICIOUS_CHARS = {"�", "□", "■", "◻", "◼", "¤"}
FIGURE_PLACEHOLDER_RE = re.compile(
    r"!\[[^\]]*\]\([^\)]+\)|<img\b[^>]*>|\[\s*figure\s*\]|\{\{\s*figure[^\}]*\}\}",
    flags=re.IGNORECASE,
)


@dataclass
class ExtractionConfig:
    use_marker_fallback: bool = True
    marker_timeout_sec: int = MARKER_TIMEOUT_SEC
    prefer_marker_if_better: bool = True
    use_vision_latex_fallback: bool = True
    vision_timeout_sec: int = 120


def extract_page_text_pdfplumber(pdf_doc: pdfplumber.PDF, page_idx: int) -> str:
    page = pdf_doc.pages[page_idx]
    raw = page.extract_text(layout=True, x_tolerance=1, y_tolerance=3) or ""
    return deep_clean_text(raw)


def extract_page_text_pypdf(pdf_reader: PdfReader, page_idx: int) -> str:
    raw = pdf_reader.pages[page_idx].extract_text() or ""
    return deep_clean_text(raw)


def detect_language_confidence(text: str) -> Tuple[str, float]:
    t = (text or "").strip()
    if len(t) < 40:
        return "unknown", 0.0
    try:
        langs = detect_langs(t[:4000])
        if not langs:
            return "unknown", 0.0
        top = langs[0]
        return str(top.lang), float(top.prob)
    except Exception:
        return "unknown", 0.0


def dictionary_unknown_ratio(text: str, language_hint: str = "en") -> float:
    tokens = [tok.lower() for tok in WORD_RE.findall(text or "")]
    if not tokens:
        return 1.0

    language = (
        language_hint if language_hint in {"en", "de", "fr", "es", "it", "pt"} else "en"
    )
    unknown = 0
    for tok in tokens:
        if zipf_frequency(tok, language) < 2.0:
            unknown += 1
    return unknown / max(1, len(tokens))


def suspicious_char_metrics(text: str) -> Dict[str, float]:
    t = text or ""
    if not t:
        return {
            "mojibake_hits": 0.0,
            "replacement_char_count": 0.0,
            "explicit_suspicious_count": 0.0,
            "non_printable_count": 0.0,
            "suspicious_char_total": 0.0,
            "suspicious_char_ratio": 0.0,
        }

    mojibake_hits = len(MOJIBAKE_RE.findall(t))
    replacement_char_count = t.count("�")
    explicit_suspicious_count = sum(ch in SUSPICIOUS_CHARS for ch in t)
    non_printable_count = sum(
        (ord(ch) < 32 and ch not in {"\n", "\t", "\r"}) for ch in t
    )

    suspicious_char_total = (
        mojibake_hits
        + replacement_char_count
        + explicit_suspicious_count
        + non_printable_count
    )
    suspicious_char_ratio = suspicious_char_total / max(1, len(t))

    return {
        "mojibake_hits": float(mojibake_hits),
        "replacement_char_count": float(replacement_char_count),
        "explicit_suspicious_count": float(explicit_suspicious_count),
        "non_printable_count": float(non_printable_count),
        "suspicious_char_total": float(suspicious_char_total),
        "suspicious_char_ratio": float(suspicious_char_ratio),
    }


def encoding_artifact_metrics(text: str) -> Dict[str, float]:
    t = text or ""
    if not t:
        return {
            "encoding_confidence": 0.0,
            "encoding_artifact_ratio": 1.0,
            "replacement_char_ratio": 0.0,
        }

    mojibake_hits = len(MOJIBAKE_RE.findall(t))
    replacement_chars = t.count("�")
    probe = chardet.detect(t.encode("utf-8", errors="ignore"))
    conf = float(probe.get("confidence") or 0.0)
    token_count = max(1, len(re.findall(r"\S+", t)))

    return {
        "encoding_confidence": conf,
        "encoding_artifact_ratio": float(mojibake_hits / token_count),
        "replacement_char_ratio": float(replacement_chars / max(1, len(t))),
    }


def text_quality_metrics(text: str) -> Dict[str, float]:
    t = text or ""
    n = len(t)
    if n == 0:
        return {
            "length": 0.0,
            "alpha_ratio": 0.0,
            "digit_ratio": 0.0,
            "symbol_ratio": 1.0,
            "non_alnum_ratio": 1.0,
            "avg_word_len": 0.0,
            "short_word_ratio": 1.0,
            "alnum_mixed_token_ratio": 1.0,
            "dictionary_unknown_ratio": 1.0,
            "language_confidence": 0.0,
            "encoding_confidence": 0.0,
            "encoding_artifact_ratio": 1.0,
            "replacement_char_ratio": 0.0,
            "suspicious_char_total": 0.0,
            "suspicious_char_ratio": 0.0,
            "quality_score": 0.0,
        }

    alpha = sum(ch.isalpha() for ch in t)
    digit = sum(ch.isdigit() for ch in t)
    spaces = sum(ch.isspace() for ch in t)
    symbol = max(0, n - alpha - digit - spaces)
    non_alnum = sum((not ch.isalnum()) and (not ch.isspace()) for ch in t)

    tokens = [tok for tok in re.split(r"\s+", t) if tok]
    words = [tok for tok in tokens if re.search(r"[A-Za-z]", tok)]
    avg_word_len = sum(len(w) for w in words) / max(1, len(words))
    short_word_ratio = sum(len(w) < 3 for w in words) / max(1, len(words))
    alnum_mixed = sum(
        bool(re.search(r"[A-Za-z]", tok) and re.search(r"\d", tok)) for tok in tokens
    )
    alnum_mixed_ratio = alnum_mixed / max(1, len(tokens))

    language, lang_conf = detect_language_confidence(t)
    dict_unknown = dictionary_unknown_ratio(t, language_hint=language)
    enc = encoding_artifact_metrics(t)
    suspicious = suspicious_char_metrics(t)

    alpha_ratio = alpha / n
    digit_ratio = digit / n
    symbol_ratio = symbol / n
    non_alnum_ratio = non_alnum / n
    len_norm = min(1.0, n / 1200.0)
    word_len_score = 1.0 - min(1.0, abs(avg_word_len - 5.2) / 5.2)
    strict_garble_penalty = min(0.60, suspicious["suspicious_char_total"] * 0.20)

    quality_score = (
        0.20 * alpha_ratio
        + 0.15 * (1.0 - non_alnum_ratio)
        + 0.15 * (1.0 - dict_unknown)
        + 0.15 * lang_conf
        + 0.10 * len_norm
        + 0.10 * word_len_score
        + 0.10 * (1.0 - alnum_mixed_ratio)
        + 0.05 * (1.0 - enc["encoding_artifact_ratio"])
        - strict_garble_penalty
    )

    return {
        "length": float(n),
        "alpha_ratio": float(alpha_ratio),
        "digit_ratio": float(digit_ratio),
        "symbol_ratio": float(symbol_ratio),
        "non_alnum_ratio": float(non_alnum_ratio),
        "avg_word_len": float(avg_word_len),
        "short_word_ratio": float(short_word_ratio),
        "alnum_mixed_token_ratio": float(alnum_mixed_ratio),
        "dictionary_unknown_ratio": float(dict_unknown),
        "language_confidence": float(lang_conf),
        "encoding_confidence": float(enc["encoding_confidence"]),
        "encoding_artifact_ratio": float(enc["encoding_artifact_ratio"]),
        "replacement_char_ratio": float(enc["replacement_char_ratio"]),
        "suspicious_char_total": float(suspicious["suspicious_char_total"]),
        "suspicious_char_ratio": float(suspicious["suspicious_char_ratio"]),
        "quality_score": float(quality_score),
    }


def should_fallback_to_marker(metrics: Dict[str, float]) -> Tuple[bool, str]:
    if metrics["suspicious_char_total"] >= 1:
        return True, "single_suspicious_char_detected"

    if metrics["length"] < 220:
        return True, "too_short"

    if metrics["non_alnum_ratio"] > 0.15:
        return True, "high_non_alnum_ratio"

    if metrics["dictionary_unknown_ratio"] > 0.24:
        return True, "high_dictionary_unknown_ratio"

    if metrics["language_confidence"] < 0.65:
        return True, "low_language_confidence"

    if metrics["encoding_artifact_ratio"] > 0.0:
        return True, "encoding_artifacts_detected"

    if metrics["avg_word_len"] < 3.2:
        return True, "low_average_word_length"

    if metrics["alnum_mixed_token_ratio"] > 0.20:
        return True, "high_alnum_mixed_token_ratio"

    if metrics["quality_score"] < 0.65:
        return True, "low_quality_score"

    return False, "best_parser_ok"


def _best_parser_choice(
    parser_outputs: Dict[str, str],
) -> Tuple[str, str, Dict[str, float], Dict[str, Dict[str, float]]]:
    parser_metrics: Dict[str, Dict[str, float]] = {}
    best_name = ""
    best_text = ""
    best_score = -1.0

    for parser_name, txt in parser_outputs.items():
        m = text_quality_metrics(txt)
        parser_metrics[parser_name] = m
        if m["quality_score"] > best_score:
            best_score = m["quality_score"]
            best_name = parser_name
            best_text = txt

    if not best_name:
        best_name = "none"
        best_text = ""
        parser_metrics["none"] = text_quality_metrics("")

    return best_name, best_text, parser_metrics[best_name], parser_metrics


def page_to_base64_png(doc: fitz.Document, page_idx: int, max_dim: int = 1600) -> str:
    page = doc[page_idx]
    zoom = 2.0
    max_side = max(page.rect.width, page.rect.height)
    if max_side > 0:
        zoom = min(2.0, max_dim / max_side)
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    return base64.b64encode(pix.tobytes("png")).decode("utf-8")


def _coerce_message_text(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: List[str] = []
        for item in content:
            if isinstance(item, dict):
                txt = (item.get("text") or "").strip()
                if txt:
                    parts.append(txt)
        return "\n".join(parts).strip()
    return ""


def vision_page_to_latex(
    client: Any,
    model: str,
    page_image_b64: str,
    extracted_text: str,
    timeout_sec: int = 120,
) -> str:
    if not client or not model:
        return ""

    prompt_text = (
        "You are given a textbook page image and extracted OCR text. "
        "Return a corrected LaTeX representation of the page content. "
        "Preserve equations and symbols accurately. "
        "Return only valid LaTeX content, no markdown fences, no explanation."
    )

    response = client.chat.completions.create(
        model=model,
        temperature=0,
        timeout=timeout_sec,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_text
                        + "\n\nOCR text:\n"
                        + (extracted_text or ""),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{page_image_b64}"},
                    },
                ],
            }
        ],
    )

    message = response.choices[0].message
    return _coerce_message_text(getattr(message, "content", ""))


# In[7]:


# Markdown-specific quality evaluation for Vision fallback decisions.
MD_CODE_BLOCK_RE = re.compile(r"```[\s\S]*?```", flags=re.MULTILINE)
MD_INLINE_CODE_RE = re.compile(r"`[^`]+`")
MD_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^\)]+\)")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^\)]+\)")
MD_HTML_TAG_RE = re.compile(r"<[^>]+>")
MD_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+", flags=re.MULTILINE)
MD_LIST_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+\.\s+)", flags=re.MULTILINE)
MD_TABLE_RE = re.compile(r"\|.+\|")
_LAST_MARKDOWN_TEXT_FOR_EVAL = ""


def markdown_to_text_for_quality(markdown_text: str) -> str:
    md = markdown_text or ""
    md = MD_CODE_BLOCK_RE.sub(" ", md)
    md = MD_INLINE_CODE_RE.sub(" ", md)
    md = MD_IMAGE_RE.sub(" ", md)
    md = MD_LINK_RE.sub(r"\1", md)
    md = MD_HTML_TAG_RE.sub(" ", md)
    md = re.sub(r"^\s{0,3}>\s?", "", md, flags=re.MULTILINE)
    md = re.sub(r"^\s{0,3}#{1,6}\s+", "", md, flags=re.MULTILINE)
    md = re.sub(r"^\s*(?:[-*+]\s+|\d+\.\s+)", "", md, flags=re.MULTILINE)
    md = md.replace("|", " ")
    md = re.sub(r"\s+", " ", md)
    return md.strip()


def markdown_quality_metrics(markdown_text: str) -> Dict[str, float]:
    md = markdown_text or ""
    plain = markdown_to_text_for_quality(md)
    base = text_quality_metrics(plain)

    char_count = max(1, len(md))
    heading_count = len(MD_HEADING_RE.findall(md))
    list_count = len(MD_LIST_RE.findall(md))
    image_count = len(MD_IMAGE_RE.findall(md))
    table_count = len(MD_TABLE_RE.findall(md))
    code_block_count = len(MD_CODE_BLOCK_RE.findall(md))

    markdown_symbol_count = sum(
        md.count(ch) for ch in ["#", "*", "_", "`", "|", "[", "]", "(", ")"]
    )
    markdown_symbol_ratio = markdown_symbol_count / char_count

    words = [w for w in re.findall(r"[A-Za-z]{2,}", plain)]
    unique_ratio = (len(set(words)) / max(1, len(words))) if words else 0.0
    lexical_score = min(1.0, unique_ratio / 0.55)

    structural_bonus = min(
        0.08, (heading_count * 0.01) + (list_count * 0.005) + (table_count * 0.01)
    )
    formatting_penalty = min(0.10, markdown_symbol_ratio * 0.7)

    md_quality_score = max(
        0.0,
        min(
            1.0,
            (0.86 * base["quality_score"])
            + (0.08 * lexical_score)
            + structural_bonus
            - formatting_penalty,
        ),
    )

    return {
        "markdown_quality_score": float(md_quality_score),
        "markdown_symbol_ratio": float(markdown_symbol_ratio),
        "heading_count": float(heading_count),
        "list_count": float(list_count),
        "table_count": float(table_count),
        "image_count": float(image_count),
        "code_block_count": float(code_block_count),
        "lexical_score": float(lexical_score),
        "plain_quality_score": float(base["quality_score"]),
        "plain_non_alnum_ratio": float(base["non_alnum_ratio"]),
        "plain_dictionary_unknown_ratio": float(base["dictionary_unknown_ratio"]),
        "plain_language_confidence": float(base["language_confidence"]),
    }


def markdown_has_figure_placeholder(text: str) -> bool:
    global _LAST_MARKDOWN_TEXT_FOR_EVAL
    t = (text or "").strip()
    _LAST_MARKDOWN_TEXT_FOR_EVAL = t
    if not t:
        return False
    return bool(FIGURE_PLACEHOLDER_RE.search(t) or MD_IMAGE_RE.search(t))


def should_use_vision_for_markdown(
    metrics: Dict[str, float], has_figure_placeholder: bool
) -> Tuple[bool, str]:
    md_metrics = markdown_quality_metrics(_LAST_MARKDOWN_TEXT_FOR_EVAL)

    if has_figure_placeholder:
        return True, "markdown_contains_figure_placeholder"

    if md_metrics["markdown_quality_score"] < 0.62:
        return True, "markdown_low_quality_score"

    if md_metrics["plain_language_confidence"] < 0.60:
        return True, "markdown_low_language_confidence"

    if md_metrics["plain_dictionary_unknown_ratio"] > 0.30:
        return True, "markdown_high_dictionary_unknown_ratio"

    if (
        md_metrics["plain_non_alnum_ratio"] > 0.22
        and md_metrics["code_block_count"] == 0
    ):
        return True, "markdown_high_non_alnum_ratio"

    return False, "markdown_ok"


# In[8]:


def extract_book_pages_hybrid(
    pdf_path: Path, config: ExtractionConfig, start_page: int = 0
):
    with fitz.open(pdf_path) as fitz_doc, pdfplumber.open(str(pdf_path)) as plumber_doc:
        best_text = None
        marker_text = None
        vision_latex_text = None
        final_text = None
        pypdf_reader = PdfReader(str(pdf_path))
        total_pages = len(fitz_doc)
        start_page = max(0, min(start_page, total_pages))
        for page_idx in tqdm(
            range(start_page, total_pages), desc=f"Extract::{pdf_path.name}"
        ):
            page_no = page_idx + 1
            parser_outputs = {
                "pymupdf": extract_page_text_pymupdf(fitz_doc, page_idx),
                "pdfplumber": extract_page_text_pdfplumber(plumber_doc, page_idx),
                "pypdf": extract_page_text_pypdf(pypdf_reader, page_idx),
            }

            best_parser, best_text, best_metrics, all_parser_metrics = (
                _best_parser_choice(parser_outputs)
            )
            fallback_needed, fallback_reason = should_fallback_to_marker(best_metrics)

            marker_text = ""
            marker_error = ""
            marker_metrics = text_quality_metrics("")
            markdown_eval_text = best_text
            markdown_eval_metrics = best_metrics
            markdown_has_placeholder = markdown_has_figure_placeholder(
                markdown_eval_text
            )

            vision_latex_text = ""
            vision_error = ""
            vision_trigger_reason = "markdown_ok"

            # Step 1: Always try to retrieve page markdown first when Marker is configured.
            if config.use_marker_fallback and DATALAB_MARKER_URL:
                try:
                    one_page_pdf = single_page_pdf_bytes(fitz_doc, page_idx)
                    marker_text = extract_page_markdown_marker(
                        file_bytes=one_page_pdf,
                        filename=f"{pdf_path.stem}_page_{page_no}.pdf",
                        marker_url=DATALAB_MARKER_URL,
                        timeout_sec=config.marker_timeout_sec,
                    )
                    marker_metrics = text_quality_metrics(marker_text)
                except Exception as exc:
                    marker_error = str(exc)

            if marker_text:
                markdown_eval_text = marker_text
                markdown_eval_metrics = marker_metrics
                markdown_has_placeholder = markdown_has_figure_placeholder(marker_text)

            # Step 2: Grade markdown + placeholder check to decide Vision usage.
            need_vision, vision_trigger_reason = should_use_vision_for_markdown(
                markdown_eval_metrics,
                markdown_has_placeholder,
            )

            if (
                config.use_vision_latex_fallback
                and need_vision
                and VISION_CLIENT
                and VISION_LLM_MODEL
            ):
                try:
                    page_png_b64 = page_to_base64_png(fitz_doc, page_idx)
                    vision_latex_text = vision_page_to_latex(
                        client=VISION_CLIENT,
                        model=VISION_LLM_MODEL,
                        page_image_b64=page_png_b64,
                        extracted_text=markdown_eval_text,
                        timeout_sec=config.vision_timeout_sec,
                    )
                except Exception as exc:
                    vision_error = str(exc)

            final_source = best_parser
            final_text = best_text
            decision_reason = f"best_primary_parser::{best_parser}"

            if marker_text:
                if config.prefer_marker_if_better:
                    if marker_metrics["quality_score"] >= best_metrics["quality_score"]:
                        final_source = "marker"
                        final_text = marker_text
                        decision_reason = "marker_better_or_equal"
                    else:
                        decision_reason = f"{best_parser}_scored_higher_than_marker"
                else:
                    final_source = "marker"
                    final_text = marker_text
                    decision_reason = "marker_forced_on_fallback"

            if vision_latex_text:
                final_source = "vision_latex"
                final_text = vision_latex_text
                decision_reason = f"vision_latex::{vision_trigger_reason}"

            row = {
                "book_name": pdf_path.name,
                "page_number": page_no,
                "primary_best_parser": best_parser,
                "source_used": final_source,
                "decision_reason": decision_reason,
                "fallback_triggered": bool(fallback_needed),
                "fallback_reason": fallback_reason,
                "best_quality": round(best_metrics["quality_score"], 4),
                "marker_quality": round(marker_metrics["quality_score"], 4),
                "best_length": int(best_metrics["length"]),
                "marker_length": int(marker_metrics["length"]),
                "best_non_alnum_ratio": round(best_metrics["non_alnum_ratio"], 4),
                "best_dictionary_unknown_ratio": round(
                    best_metrics["dictionary_unknown_ratio"], 4
                ),
                "best_language_confidence": round(
                    best_metrics["language_confidence"], 4
                ),
                "best_encoding_artifact_ratio": round(
                    best_metrics["encoding_artifact_ratio"], 4
                ),
                "best_avg_word_len": round(best_metrics["avg_word_len"], 4),
                "best_alnum_mixed_token_ratio": round(
                    best_metrics["alnum_mixed_token_ratio"], 4
                ),
                "best_suspicious_char_total": int(
                    best_metrics["suspicious_char_total"]
                ),
                "best_suspicious_char_ratio": round(
                    best_metrics["suspicious_char_ratio"], 6
                ),
                "parser_metrics_json": json.dumps(
                    all_parser_metrics, ensure_ascii=False
                ),
                "marker_error": marker_error,
                "vision_error": vision_error,
                "text": final_text,
            }
            yield row

            del parser_outputs
            del best_text
            del final_text
            del marker_text
            del vision_latex_text
            if "one_page_pdf" in locals():
                del one_page_pdf
            if "page_png_b64" in locals():
                del page_png_b64
            if page_idx % 5 == 0:
                gc.collect()


# In[9]:


# NOT USED
# Figure-aware Vision enrichment for markdown outputs

FIGURE_MD_RE = re.compile(r"!\[[^\]]*\]\([^\)]+\)")
FIGURE_HTML_RE = re.compile(r"<img\b[^>]*>", flags=re.IGNORECASE)


def _page_image_base64_list(
    doc: fitz.Document, page_idx: int, max_images: int = 6
) -> List[str]:
    page = doc[page_idx]
    images = page.get_images(full=True) or []
    payloads: List[str] = []

    for img_info in images[:max_images]:
        xref = img_info[0]
        try:
            img_data = doc.extract_image(xref)
            blob = img_data.get("image", b"")
            if not blob:
                continue
            payloads.append(base64.b64encode(blob).decode("utf-8"))
        except Exception:
            continue

    return payloads


def vision_describe_or_latex_image(
    client: Any,
    model: str,
    image_b64: str,
    page_text: str,
    timeout_sec: int = 120,
) -> str:
    if not client or not model:
        return ""

    prompt = (
        "Analyze this textbook figure image together with nearby page text. "
        "If the figure contains equations/symbol-heavy math, return a corrected LaTeX representation. "
        "Otherwise return a detailed but concise technical caption. "
        "Return only the final content text (no markdown fences, no explanation)."
    )

    response = client.chat.completions.create(
        model=model,
        temperature=0,
        timeout=timeout_sec,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt + "\n\nPage text context:\n" + (page_text or ""),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_b64}"},
                    },
                ],
            }
        ],
    )

    msg = response.choices[0].message
    return _coerce_message_text(getattr(msg, "content", ""))


def replace_figure_placeholders(markdown_text: str, replacements: List[str]) -> str:
    text = markdown_text or ""
    if not replacements:
        return text

    idx = 0

    def _next_replacement(prefix: str = "") -> str:
        nonlocal idx
        if idx >= len(replacements):
            return prefix + "[Figure content unavailable]"
        val = replacements[idx]
        idx += 1
        return prefix + val

    text = FIGURE_MD_RE.sub(lambda _: _next_replacement("\n"), text)
    text = FIGURE_HTML_RE.sub(lambda _: _next_replacement("\n"), text)

    if idx == 0:
        # No explicit placeholders; append figure interpretations at the end.
        extra = "\n\nFigure Insights:\n" + "\n".join(f"- {r}" for r in replacements)
        return (text + extra).strip()

    return text.strip()


def extract_book_pages_hybrid_with_figure_vision(
    pdf_path: Path, config: ExtractionConfig, start_page: int = 0
):
    with fitz.open(pdf_path) as fitz_doc:
        for page_idx, row in enumerate(
            extract_book_pages_hybrid(pdf_path, config, start_page=start_page),
            start=start_page,
        ):
            if not (
                config.use_vision_latex_fallback and VISION_CLIENT and VISION_LLM_MODEL
            ):
                yield row
                continue

            image_payloads = _page_image_base64_list(fitz_doc, page_idx)
            if not image_payloads:
                yield row
                continue

            figure_outputs: List[str] = []
            figure_errors: List[str] = []
            for image_b64 in image_payloads:
                try:
                    figure_out = vision_describe_or_latex_image(
                        client=VISION_CLIENT,
                        model=VISION_LLM_MODEL,
                        image_b64=image_b64,
                        page_text=row.get("text", ""),
                        timeout_sec=getattr(config, "vision_timeout_sec", 120),
                    )
                    if figure_out:
                        figure_outputs.append(figure_out)
                except Exception as exc:
                    figure_errors.append(str(exc))
                finally:
                    del image_b64

            if not figure_outputs:
                if figure_errors:
                    row["vision_error"] = (
                        row.get("vision_error", "") + " | " + " ; ".join(figure_errors)
                    ).strip(" |")
                del image_payloads
                del figure_outputs
                del figure_errors
                gc.collect()
                yield row
                continue

            row["text"] = replace_figure_placeholders(
                row.get("text", ""), figure_outputs
            )
            row["decision_reason"] = (
                row.get("decision_reason", "") + "|figure_vision_replaced"
            ).strip("|")

            # Preserve main source when it is already vision-driven; otherwise mark enrichment.
            if row.get("source_used") not in {"vision_latex", "vision_figure_enriched"}:
                row["source_used"] = "vision_figure_enriched"

            if figure_errors:
                row["vision_error"] = (
                    row.get("vision_error", "") + " | " + " ; ".join(figure_errors)
                ).strip(" |")

            del image_payloads
            del figure_outputs
            del figure_errors
            gc.collect()
            yield row


# In[ ]:


import csv

CFG = ExtractionConfig(
    use_marker_fallback=True,
    marker_timeout_sec=MARKER_TIMEOUT_SEC,
    prefer_marker_if_better=True,
    use_vision_latex_fallback=True,
    vision_timeout_sec=120,
)

pdf_files = sorted(BOOKS_DIR.glob("*.pdf"))
if not pdf_files:
    raise FileNotFoundError(f"No PDF files found in {BOOKS_DIR}")

# Per-book CSV outputs are stored here.
PER_BOOK_DIR = OUTPUT_DIR / "pdf_page_text_by_book"
PER_BOOK_DIR.mkdir(parents=True, exist_ok=True)

write_columns = ["book_name", "page_number", "source_used", "decision_reason", "text"]
all_books = len(pdf_files)
already_done = 0


def get_last_extracted_page(csv_path: Path) -> int:
    if not csv_path.exists() or csv_path.stat().st_size == 0:
        return 0

    last_page = 0
    try:
        with csv_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames or "page_number" not in reader.fieldnames:
                return 0

            for row in reader:
                raw_page = str(row.get("page_number", "")).strip()
                if not raw_page:
                    continue
                try:
                    page_number = int(float(raw_page))
                except Exception:
                    continue
                if page_number > last_page:
                    last_page = page_number
    except Exception:
        return 0

    return last_page


for pdf in pdf_files:
    book_csv = PER_BOOK_DIR / f"{pdf.stem}_pages_cleaned.csv"

    with fitz.open(pdf) as doc:
        expected_pages = len(doc)

    last_page = get_last_extracted_page(book_csv)
    start_page = max(0, min(last_page, expected_pages))

    if start_page >= expected_pages and expected_pages > 0:
        already_done += 1
        print(f"\nSkipping (already extracted): {pdf.name}")
        gc.collect()
        continue

    if start_page > 0:
        print(f"\nResuming {pdf.name} from page {start_page + 1} of {expected_pages}.")
    else:
        if book_csv.exists() and book_csv.stat().st_size > 0:
            print(
                f"\nResuming {pdf.name} from the first page because no valid checkpoint row was found."
            )
        else:
            print(f"\nProcessing: {pdf.name}")

    batch: List[Dict[str, Any]] = []
    batch_size = 20
    wrote_header = book_csv.exists() and book_csv.stat().st_size > 0

    # Stream rows in small batches to keep RAM usage bounded.
    for row in extract_book_pages_hybrid(pdf, CFG, start_page=start_page):
        batch.append(row)
        if len(batch) >= batch_size:
            df = pd.DataFrame(batch, columns=write_columns)
            df.to_csv(
                book_csv,
                mode="a",
                header=not wrote_header,
                index=False,
                encoding="utf-8",
                quoting=csv.QUOTE_MINIMAL,
                quotechar='"',
                escapechar="\\",
            )
            wrote_header = True

            del df
            del batch
            batch = []
            gc.collect()

    if batch:
        df = pd.DataFrame(batch, columns=write_columns)
        df.to_csv(
            book_csv,
            mode="a",
            header=not wrote_header,
            index=False,
            encoding="utf-8",
            quoting=csv.QUOTE_MINIMAL,
            quotechar='"',
            escapechar="\\",
        )

        del df
        del batch
        batch = []

    gc.collect()
    if book_csv.exists():
        print(f"  per-book CSV: {book_csv}")
    else:
        print(f"  warning: no CSV written for {pdf.name}")

print(f"\nSummary: skipped {already_done}/{all_books} books with complete CSV outputs.")
gc.collect()
