# %%
# !pip install pymupdf pandas tqdm openai python-dotenv rapidfuzz

# %%
import json
import os
import re
import threading
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from tqdm.auto import tqdm

load_dotenv()


def find_workspace_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "datasets" / "training" / "pdf_page_text_by_book").exists():
            return candidate
    return start.resolve()


WORKSPACE_ROOT = find_workspace_root(Path.cwd())
CSV_PAGES_DIR = WORKSPACE_ROOT / "pdf_page_text_by_book"
OUTPUT_DIR = WORKSPACE_ROOT / "datasets"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# QWEN provider for question generation
QWEN_BASE_URL = os.getenv("QWEN_LLM_API_URL", "http://localhost:9000/v1").strip()
QWEN_MODEL = os.getenv("QWEN_LLM_MODEL_NAME", "Qwen/Qwen3.5-27B").strip()
QWEN_API_KEY = (
    os.getenv("QWEN_LLM_API_KEY", "").strip()
    or os.getenv("OPENAI_LLM_API_KEY", "").strip()
    or os.getenv("OPENAI_API_KEY", "").strip()
)

# OPENAI provider for eligibility/context validation
OPENAI_BASE_URL = os.getenv("OPENAI_LLM_API_URL", "http://localhost:8000/v1").strip()
OPENAI_MODEL = os.getenv("OPENAI_LLM_MODEL_NAME", "openai/gpt-oss-20b").strip()
OPENAI_API_KEY = (
    os.getenv("OPENAI_LLM_API_KEY", "").strip()
    or os.getenv("OPENAI_API_KEY", "").strip()
)

WINDOW_SIZE = 5
WINDOW_STRIDE = 3
QUESTIONS_PER_WINDOW = 30  # robust profile: 6 Bloom levels x 5 formats
MAX_CONTEXT_CHARS = 18000
MIN_CONTEXT_CHARS = 450
GENERATION_MAX_RETRIES = 3
VALIDATION_MAX_RETRIES = 2
DEDUP_THRESHOLD = 90
SEED = 42

print(f"Workspace root: {WORKSPACE_ROOT}")
print(f"CSV pages dir: {CSV_PAGES_DIR}")
print(f"Output dir: {OUTPUT_DIR}")
print(f"QWEN model: {QWEN_MODEL} | URL set: {bool(QWEN_BASE_URL)}")
print(f"OPENAI model: {OPENAI_MODEL} | URL set: {bool(OPENAI_BASE_URL)}")

# %%
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


def _to_int(v: Any, default: int = 0) -> int:
    try:
        if pd.isna(v):
            return default
        return int(float(v))
    except Exception:
        return default


def infer_page_data_type(source_used: str, decision_reason: str, text: str) -> str:
    src = normalize_text(str(source_used)).lower()
    reason = normalize_text(str(decision_reason)).lower()
    body = text or ""

    if "vision_latex" in src or "vision_latex" in reason:
        return "latex"
    if "marker" in src or "markdown" in reason:
        return "markdown"
    if src in {"pymupdf", "pdfplumber", "pypdf"}:
        return "plain_text"
    if re.search(r"\\[a-zA-Z]+|\$\$|\$[^$]+\$", body):
        return "latex"
    if re.search(
        r"^\s*#{1,6}\s+|!\[[^\]]*\]\([^\)]+\)|\[[^\]]+\]\([^\)]+\)",
        body,
        flags=re.MULTILINE,
    ):
        return "markdown"
    return "plain_text"


def load_book_pages_from_csv(csv_path: Path) -> pd.DataFrame:
    required_cols = [
        "book_name",
        "page_number",
        "source_used",
        "decision_reason",
        "text",
    ]
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing CSV file: {csv_path}")

    df = pd.read_csv(csv_path)
    for col in required_cols:
        if col not in df.columns:
            if col == "book_name":
                df[col] = csv_path.stem.replace("_pages_cleaned", "")
            elif col == "page_number":
                df[col] = 0
            else:
                df[col] = ""

    df = df[required_cols].copy()
    df["page_number"] = df["page_number"].apply(lambda x: _to_int(x, 0))
    df = df[df["page_number"] > 0].copy()
    df["text"] = df["text"].fillna("").astype(str)
    df = df[df["text"].str.strip() != ""].copy()
    df["source_used"] = df["source_used"].fillna("").astype(str)
    df["decision_reason"] = df["decision_reason"].fillna("").astype(str)
    df["book_name"] = df["book_name"].fillna("").astype(str)

    # CSV text is already cleaned by extraction pipeline; no additional cleaning here.
    df["page_data_type"] = [
        infer_page_data_type(src, reason, txt)
        for src, reason, txt in zip(
            df["source_used"], df["decision_reason"], df["text"]
        )
    ]

    return df.sort_values("page_number").reset_index(drop=True)


def get_book_total_pages(book_pages_df: pd.DataFrame) -> int:
    if book_pages_df.empty:
        return 0
    return int(book_pages_df["page_number"].max())


def build_context_from_pages(
    book_pages_df: pd.DataFrame, page_start: int, page_end: int
) -> Tuple[str, List[Dict[str, Any]]]:
    if book_pages_df.empty:
        return "", []

    chunk = book_pages_df[
        (book_pages_df["page_number"] >= page_start)
        & (book_pages_df["page_number"] <= page_end)
    ].copy()

    if chunk.empty:
        return "", []

    chunk = chunk.sort_values("page_number")
    parts: List[str] = []
    metadata_rows: List[Dict[str, Any]] = []

    for _, row in chunk.iterrows():
        page_no = _to_int(row.get("page_number"), 0)
        page_text = str(row.get("text", "") or "").strip()
        page_type = str(row.get("page_data_type", "plain_text") or "plain_text")
        source_used = str(row.get("source_used", "") or "")

        if not page_text:
            continue

        parts.append(
            f"[Page {page_no} | data_type={page_type} | source={source_used}]\n{page_text}"
        )
        metadata_rows.append(
            {
                "page_number": page_no,
                "source_used": source_used,
                "decision_reason": str(row.get("decision_reason", "") or ""),
                "page_data_type": page_type,
            }
        )

    return "\n\n".join(parts).strip(), metadata_rows


# %%
def build_qwen_client() -> OpenAI:
    if not QWEN_BASE_URL:
        raise ValueError(
            "Set QWEN_LLM_API_URL and QWEN_LLM_API_KEY (or OPENAI_LLM_API_KEY) in environment/.env"
        )
    return OpenAI(base_url=QWEN_BASE_URL, api_key=QWEN_API_KEY)


def build_openai_validation_client() -> OpenAI:
    if not OPENAI_BASE_URL:
        raise ValueError(
            "Set OPENAI_LLM_API_URL and OPENAI_LLM_API_KEY in environment/.env"
        )
    return OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)


DIFFICULTY_SNIPPETS: Dict[str, str] = {
    "Remember": (
        "Target faithful retrieval of explicitly stated facts, definitions, symbols, constraints, or step names from the given context. "
        "Use action intent such as identify, list, recall, or state. "
        "Do not require inference beyond direct textual evidence. "
        "Answers should be short, exact, and traceable to a specific statement in the passage."
    ),
    "Understand": (
        "Target comprehension of meaning, relationships, and interpretation. "
        "Use intents like explain, summarize, classify, compare at a basic level, or interpret in plain language. "
        "Questions should verify that the learner can restate the concept accurately without adding external assumptions. "
        "Answers should include brief conceptual linkage, not mere copying."
    ),
    "Apply": (
        "Target transfer of a concept, rule, or procedure to a concrete mini-scenario consistent with the context. "
        "Use intents such as apply, compute, determine, execute, or choose based on stated rules. "
        "Require 1-2 explicit reasoning steps grounded in given conditions. "
        "Answers should demonstrate how the rule is used, not only the final outcome."
    ),
    "Analyze": (
        "Target decomposition and structural reasoning: part-whole relationships, assumptions, causal pathways, and distinctions. "
        "Use intents like differentiate, infer structure, diagnose, or compare mechanisms with evidence. "
        "Questions should require multi-part reasoning and discrimination between similar options. "
        "Answers should cite the decisive evidence from context."
    ),
    "Evaluate": (
        "Target judgment using explicit criteria present in the context, such as correctness, efficiency, robustness, or trade-offs. "
        "Use intents such as justify, critique, defend, prioritize, or assess alternatives. "
        "Questions must force a choice under constraints and require rationale for rejecting competing choices. "
        "Answers should present criterion-based justification, not opinion-only claims."
    ),
    "Create": (
        "Target synthesis of ideas into a new but context-consistent artifact: design choice, algorithm sketch, improved formulation, or structured plan. "
        "Use intents such as design, construct, propose, formulate, or compose. "
        "Questions should combine multiple concepts from the passage while preserving constraints and factual consistency. "
        "Answers should present a coherent constructed solution with concise rationale."
    ),
}

FORMAT_SNIPPETS: Dict[str, str] = {
    "MCQ": (
        "Include exactly four options (A-D), one unambiguously correct answer, "
        "and plausible distractors derived from common misconceptions in the same context."
    ),
    "Fill_blank": (
        "Use a single meaningful blank whose completion depends on conceptual understanding, "
        "not rote memorization of a random token."
    ),
    "Assertion": (
        "Use assertion-reason style with a clear verdict in the answer. "
        "The rationale must explicitly explain whether the reason supports the assertion."
    ),
    "Analytical": (
        "Ask for structured analysis or comparison (e.g., mechanism vs outcome, choice vs trade-off). "
        "Answer should be concise but logically sequenced."
    ),
    "Conceptual": (
        "Ask a self-contained explanatory question that tests understanding of principles, "
        "causality, or interpretation from the provided context."
    ),
}

SUBFORMAT_FOR_MAIN = {
    "Objective": ["MCQ", "Fill_blank", "Assertion", "Analytical"],
    "Subjective": ["Conceptual"],
}

DIFFICULTY_ORDER: List[str] = [
    "Remember",
    "Understand",
    "Apply",
    "Analyze",
    "Evaluate",
    "Create",
]
SUBFORMAT_ORDER: List[str] = [
    "MCQ",
    "Fill_blank",
    "Assertion",
    "Analytical",
    "Conceptual",
]
SUBFORMAT_TO_MAIN_FORMAT: Dict[str, str] = {
    "MCQ": "Objective",
    "Fill_blank": "Objective",
    "Assertion": "Objective",
    "Analytical": "Objective",
    "Conceptual": "Subjective",
}

ALL_QUESTION_COMBINATIONS: List[Tuple[str, str, str]] = [
    (difficulty, SUBFORMAT_TO_MAIN_FORMAT[sub_format], sub_format)
    for sub_format in SUBFORMAT_ORDER
    for difficulty in DIFFICULTY_ORDER
]
DEFAULT_QUESTIONS_PER_VALID_WINDOW = len(ALL_QUESTION_COMBINATIONS)

# Per-thread trace buffers keep parallel book runs isolated.
_TRACE_LOCAL = threading.local()
QWEN_RAW_RESPONSE_LOG = os.getenv("QWEN_RAW_RESPONSE_LOG", "1").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}


def _get_llm_trace_logs() -> List[Dict[str, Any]]:
    logs = getattr(_TRACE_LOCAL, "logs", None)
    if logs is None:
        logs = []
        _TRACE_LOCAL.logs = logs
    return logs


def reset_llm_trace_logs() -> None:
    _TRACE_LOCAL.logs = []


def get_llm_trace_logs() -> List[Dict[str, Any]]:
    return _get_llm_trace_logs()


def _preview(text: str, n: int = 180) -> str:
    text = (text or "").replace("\n", " ").strip()
    return text[:n] + ("..." if len(text) > n else "")


def _append_llm_trace(entry: Dict[str, Any]) -> None:
    _get_llm_trace_logs().append(entry)
    payload_txt = " | ".join(f"{k}={v}" for k, v in entry.items())
    print(f"[llm::summary] {payload_txt}")


def _log_qwen_raw_response(
    response_type: str,
    window_tag: str,
    attempt: int,
    variant_idx: int,
    finish_reason: Any,
    raw: str,
    reasoning: str,
) -> None:
    if not QWEN_RAW_RESPONSE_LOG:
        return
    print("[qwen::raw] ----- begin -----")
    print(
        f"[qwen::raw] type={response_type} window={window_tag or 'na'} attempt={attempt} variant={variant_idx} finish_reason={finish_reason}"
    )
    print(
        f"[qwen::raw] content_chars={len(raw or '')} reasoning_chars={len(reasoning or '')}"
    )
    print("[qwen::raw] content:")
    print(raw if raw else "<EMPTY>")
    if reasoning:
        print("[qwen::raw] reasoning_content:")
        print(reasoning)
    print("[qwen::raw] ----- end -----")


def _strip_qwen_think_blocks(text: str) -> str:
    # Qwen reasoning may appear as <think>...</think> OR as free-form text ending with </think>.
    t = text or ""
    t = re.sub(r"<think\b[^>]*>.*?</think>", "", t, flags=re.DOTALL | re.IGNORECASE)
    if "</think>" in t:
        # Handle malformed/orphan close-tag output by keeping only the post-think payload.
        t = t.split("</think>", 1)[1]
    return t.strip()


def _extract_qwen_thinking_text(content_text: str, reasoning_text: str) -> str:
    # Prefer explicit reasoning_content when present.
    rt = (reasoning_text or "").strip()
    if rt:
        m = re.search(r"<think>(.*?)</think>", rt, flags=re.DOTALL | re.IGNORECASE)
        if m:
            return m.group(1).strip()
        return rt

    blob = content_text or ""
    m = re.search(r"<think>(.*?)</think>", blob, flags=re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()

    # Handle outputs like: 'Thinking Process: ... </think>\n\n{json}'
    if "</think>" in blob:
        return blob.split("</think>", 1)[0].strip()

    return ""


def _extract_json_candidate(raw: str) -> str:
    cleaned = re.sub(r"```(?:json)?", "", (raw or "")).replace("```", "").strip()
    if not cleaned:
        return ""

    cleaned = _strip_qwen_think_blocks(cleaned)

    # Prefer object blocks first.
    m_obj = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if m_obj:
        return m_obj.group(0).strip()

    # Some models may emit a top-level list.
    m_list = re.search(r"\[.*\]", cleaned, flags=re.DOTALL)
    if m_list:
        return m_list.group(0).strip()

    return cleaned


def _extract_balanced_json_span(text: str) -> str:
    if not text:
        return ""
    start = -1
    stack: List[str] = []
    in_str = False
    esc = False
    for i, ch in enumerate(text):
        if start == -1 and ch in "[{":
            start = i
            stack = [ch]
            in_str = False
            esc = False
            continue
        if start == -1:
            continue
        if in_str:
            if esc:
                esc = False
                continue
            if ch == "\\":
                esc = True
                continue
            if ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
            continue
        if ch in "[{":
            stack.append(ch)
            continue
        if ch in "]}":
            if not stack:
                continue
            opener = stack[-1]
            if (opener == "[" and ch == "]") or (opener == "{" and ch == "}"):
                stack.pop()
                if not stack and start != -1:
                    return text[start : i + 1].strip()
    return ""


def _strip_trailing_commas(text: str) -> str:
    prev = None
    cur = text
    while prev != cur:
        prev = cur
        cur = re.sub(r",\s*([}\]])", r"\1", cur)
    return cur


def _close_unbalanced_json(text: str) -> str:
    if not text:
        return text
    stack: List[str] = []
    in_str = False
    esc = False
    for ch in text:
        if in_str:
            if esc:
                esc = False
                continue
            if ch == "\\":
                esc = True
                continue
            if ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
            continue
        if ch in "[{":
            stack.append(ch)
        elif ch in "]}" and stack:
            opener = stack[-1]
            if (opener == "[" and ch == "]") or (opener == "{" and ch == "}"):
                stack.pop()
    closers = []
    for opener in reversed(stack):
        closers.append("]" if opener == "[" else "}")
    return text + "".join(closers)


def _extract_items_object_fallback(text: str) -> Dict[str, Any]:
    # Last-resort parser: pull per-item JSON objects from malformed arrays.
    items: List[Dict[str, Any]] = []
    for m in re.finditer(r"\{[^{}]*\}", text, flags=re.DOTALL):
        chunk = m.group(0).strip()
        if '"question"' not in chunk or '"answer"' not in chunk:
            continue
        chunk = _strip_trailing_commas(_close_unbalanced_json(chunk))
        try:
            obj = json.loads(chunk)
            if isinstance(obj, dict):
                items.append(obj)
        except Exception:
            continue
    return {"items": items}


def _parse_json_payload(candidate: str, response_type: str) -> Dict[str, Any]:
    if not candidate:
        raise ValueError("empty_response")

    attempts: List[str] = []
    attempts.append(candidate)
    span = _extract_balanced_json_span(candidate)
    if span:
        attempts.append(span)
    attempts.append(_strip_trailing_commas(candidate))
    attempts.append(_strip_trailing_commas(_close_unbalanced_json(candidate)))

    seen: set = set()
    for payload in attempts:
        payload = (payload or "").strip()
        if not payload or payload in seen:
            continue
        seen.add(payload)
        try:
            parsed = json.loads(payload)
        except Exception:
            continue

        if isinstance(parsed, dict):
            return parsed
        if isinstance(parsed, list) and response_type == "generation":
            return {"items": parsed}

    if response_type == "generation":
        fallback = _extract_items_object_fallback(candidate)
        if fallback.get("items"):
            return fallback

    raise ValueError("unparseable_json_payload")


def get_question_combinations(question_count: int) -> List[Tuple[str, str, str]]:
    base = list(ALL_QUESTION_COMBINATIONS)
    if question_count <= 0:
        return []
    if question_count <= len(base):
        return base[:question_count]

    expanded: List[Tuple[str, str, str]] = []
    while len(expanded) < question_count:
        expanded.extend(base)
    return expanded[:question_count]


def _combo_key(difficulty: str, main_format: str, sub_format: str) -> str:
    return f"{difficulty}|{main_format}|{sub_format}"


BLOOMS_ALIAS_MAP: Dict[str, str] = {
    "remember": "Remember",
    "knowledge": "Remember",
    "understand": "Understand",
    "understanding": "Understand",
    "comprehend": "Understand",
    "apply": "Apply",
    "application": "Apply",
    "analyze": "Analyze",
    "analysis": "Analyze",
    "analyse": "Analyze",
    "evaluate": "Evaluate",
    "evaluation": "Evaluate",
    "create": "Create",
    "creation": "Create",
    "synthesize": "Create",
    "synthesis": "Create",
}


def normalize_blooms_level(value: str) -> str:
    v = normalize_text(value).lower()
    return BLOOMS_ALIAS_MAP.get(v, "Understand")


GENERATION_ENABLE_THINKING = os.getenv("QWEN_ENABLE_THINKING", "0").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}


def _message_text(msg: Any) -> str:
    content = getattr(msg, "content", None)
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: List[str] = []
        for p in content:
            if isinstance(p, dict):
                t = p.get("text") or p.get("content") or ""
                if t:
                    parts.append(str(t))
        return "\n".join(parts).strip()
    return ""


def chat_json(
    client: OpenAI,
    model: str,
    system_prompt: str,
    user_prompt: str,
    max_tokens: Optional[int] = None,
    temperature: float = 0.2,
    response_type: str = "generic",
    window_tag: str = "",
    max_retries: int = 2,
) -> Dict[str, Any]:
    last_error: Optional[Exception] = None

    for attempt in range(max_retries + 1):
        strict_suffix = ""
        if attempt > 0:
            strict_suffix = "\n\nIMPORTANT: Return ONLY valid JSON with no prose, no markdown, no code fences."

        # First try with configured mode.
        variants: List[Dict[str, Any]] = []
        base_req: Dict[str, Any] = {
            "model": model,
            "temperature": 0.0 if attempt > 0 else temperature,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt + strict_suffix},
            ],
        }
        if max_tokens is not None:
            base_req["max_tokens"] = (
                max_tokens if attempt == 0 else max(1800, min(max_tokens * 2, 4096))
            )
        if response_type == "generation" and GENERATION_ENABLE_THINKING:
            base_req["extra_body"] = {"chat_template_kwargs": {"enable_thinking": True}}
        variants.append(base_req)

        # Fallback for generation: hard-disable thinking and give larger completion budget.
        if response_type == "generation":
            gen_fallback: Dict[str, Any] = {
                "model": model,
                "temperature": 0.0,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt + strict_suffix},
                ],
            }
            if max_tokens is not None:
                gen_fallback["max_tokens"] = max(2400, min(max_tokens * 2, 4096))
            variants.append(gen_fallback)

        for variant_idx, request_kwargs in enumerate(variants, start=1):
            try:
                resp = client.chat.completions.create(**request_kwargs)
            except Exception as exc:
                last_error = exc
                _append_llm_trace(
                    {
                        "type": response_type,
                        "window": window_tag or "na",
                        "model": model,
                        "status": "request_error",
                        "attempt": attempt + 1,
                        "variant": variant_idx,
                        "error": str(exc),
                    }
                )
                continue

            choice = resp.choices[0]
            msg = choice.message
            finish_reason = getattr(choice, "finish_reason", None)
            raw = _message_text(msg)
            reasoning_content = str(getattr(msg, "reasoning_content", None) or "")
            thinking_text = _extract_qwen_thinking_text(raw, reasoning_content)
            if model == QWEN_MODEL:
                _log_qwen_raw_response(
                    response_type=response_type,
                    window_tag=window_tag,
                    attempt=attempt + 1,
                    variant_idx=variant_idx,
                    finish_reason=finish_reason,
                    raw=raw,
                    reasoning=thinking_text,
                )
            candidate = _extract_json_candidate(raw)

            if not candidate:
                last_error = ValueError("empty_response")
                _append_llm_trace(
                    {
                        "type": response_type,
                        "window": window_tag or "na",
                        "model": model,
                        "status": "empty_content",
                        "attempt": attempt + 1,
                        "variant": variant_idx,
                        "finish_reason": finish_reason,
                        "raw_chars": len(raw),
                        "reasoning_chars": len(thinking_text),
                    }
                )
                continue

            try:
                data = _parse_json_payload(candidate, response_type=response_type)
            except Exception as exc:
                last_error = exc
                _append_llm_trace(
                    {
                        "type": response_type,
                        "window": window_tag or "na",
                        "model": model,
                        "status": "parse_error",
                        "attempt": attempt + 1,
                        "variant": variant_idx,
                        "finish_reason": finish_reason,
                        "raw_chars": len(raw),
                        "reasoning_chars": len(thinking_text),
                        "raw_preview": _preview(raw),
                        "error": str(exc),
                    }
                )
                continue

            _append_llm_trace(
                {
                    "type": response_type,
                    "window": window_tag or "na",
                    "model": model,
                    "status": "ok",
                    "attempt": attempt + 1,
                    "variant": variant_idx,
                    "finish_reason": finish_reason,
                    "raw_chars": len(raw),
                    "reasoning_chars": len(thinking_text),
                }
            )
            return data

    raise ValueError(f"json_parse_failed_after_retries::{last_error}")


def ask_eligibility(
    validation_client: OpenAI,
    context_text: str,
    window_tag: str = "",
    max_questions_per_page: int = 1,
    window_pages: int = WINDOW_SIZE,
    validation_retries: int = VALIDATION_MAX_RETRIES,
) -> Dict[str, Any]:
    system_prompt = (
        "You are a strict textbook-content gatekeeper for QA dataset creation. "
        "Your job is to reject noisy/non-teachable pages and allow only concept-rich instructional content. "
        "Return strict JSON only."
    )
    max_questions_per_page = max(1, int(max_questions_per_page))
    window_pages = max(1, int(window_pages))
    max_questions_for_window = max_questions_per_page * window_pages

    user_prompt = f"""
Context (trimmed):
{context_text[:MAX_CONTEXT_CHARS]}

Return JSON with keys:
- eligible: true/false
- reason: short snake_case reason
- recommended_questions: integer between 0 and {max_questions_for_window}

Primary objective:
- We run this validation mainly to remove noisy book sections (author index, acknowledgements, references, glossary, publication metadata, copyright pages, TOC pages, and similar non-teaching content).

Eligibility rules:
- Mark eligible=false when the context is primarily structural/noisy matter: author index entries, acknowledgements, bibliography/references, table of contents, preface-only notes, appendices that are lists/tables only, page headers/footers, or OCR garbage.
- Mark eligible=true only if the passage contains enough teachable material: definitions, explanations, procedures, comparisons, worked reasoning, or conceptual discussion that can support self-contained QA generation.
- If mixed content appears, prefer eligible=false unless at least ~60% of the text is instructional and concept-bearing.
- Keep reason concise and specific, e.g., author_index_page, acknowledgements_page, toc_page, bibliography_page, noisy_ocr, concept_rich_text.
- For eligible windows, use this ceiling rule:
  max_questions_per_page = {max_questions_per_page}
  window_pages = {window_pages}
  max_questions_for_window = {max_questions_for_window}
- Keep recommended_questions <= max_questions_for_window.
"""
    try:
        result = chat_json(
            client=validation_client,
            model=OPENAI_MODEL,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=280,
            temperature=0.0,
            response_type="validation",
            window_tag=window_tag,
            max_retries=max(1, int(validation_retries)),
        )
    except Exception as exc:
        _append_llm_trace(
            {
                "type": "validation",
                "window": window_tag or "na",
                "model": OPENAI_MODEL,
                "status": "fallback",
                "reason": str(exc),
            }
        )
        return {
            "eligible": True,
            "reason": f"eligibility_fallback::{exc}",
            "recommended_questions": max_questions_for_window,
        }

    return {
        "eligible": bool(result.get("eligible", True)),
        "reason": str(result.get("reason", "unknown")),
        "recommended_questions": int(
            result.get("recommended_questions", max_questions_for_window)
            or max_questions_for_window
        ),
    }


def _chunked(
    seq: List[Tuple[str, str, str]], size: int
) -> List[List[Tuple[str, str, str]]]:
    return [seq[i : i + size] for i in range(0, len(seq), size)]


def _has_mcq_options(question_text: str) -> bool:
    q = normalize_text(question_text)
    return bool(
        re.search(r"(?:^|\s)A\)", q)
        and re.search(r"(?:^|\s)B\)", q)
        and re.search(r"(?:^|\s)C\)", q)
        and re.search(r"(?:^|\s)D\)", q)
    )


def _is_valid_item_for_format(
    sub_format: str, question: str, answer: str, item: Dict[str, Any]
) -> bool:
    if sub_format == "MCQ":
        has_inline = _has_mcq_options(question)
        has_structured = all(
            normalize_text(str(item.get(k, "")))
            for k in ["option_a", "option_b", "option_c", "option_d"]
        )
        has_correct = bool(
            re.match(r"^\s*[ABCD]\)", normalize_text(answer), flags=re.IGNORECASE)
            or normalize_text(str(item.get("correct_option", "")))
            in {"A", "B", "C", "D"}
        )
        return (has_inline or has_structured) and has_correct
    if sub_format == "Fill_blank":
        return question.count("____") == 1
    if sub_format == "Assertion":
        q = normalize_text(question)
        return bool(
            re.search(r"Assertion\s*[:\-]", q, flags=re.IGNORECASE)
            and re.search(r"Reason\s*[:\-]", q, flags=re.IGNORECASE)
        )
    return True


def generate_window_questions(
    generation_client: OpenAI,
    context_text: str,
    question_count: int,
    window_tag: str = "",
    combination_plan: Optional[List[Tuple[str, str, str]]] = None,
    generation_retries: int = GENERATION_MAX_RETRIES,
) -> List[Dict[str, Any]]:
    system_prompt = (
        "You are an expert computer science educator creating rigorous study QA data. "
        "Use internal reasoning, but return only strict JSON in the final content."
    )

    full_plan = combination_plan or get_question_combinations(question_count)
    if not full_plan:
        return []

    # Keep generation prompts lighter than full window context to reduce backend truncation risk.
    trimmed_context = (context_text or "")[:7000]

    # Combination plan is executed in batches of 5 to keep prompts stable.
    batch_size = 5 if len(full_plan) > 5 else len(full_plan)
    plan_batches = _chunked(full_plan, batch_size)

    all_rows: List[Dict[str, Any]] = []
    missing_total: List[str] = []

    for b_idx, batch_plan in enumerate(plan_batches, start=1):
        batch_tag = f"{window_tag}::batch{b_idx}/{len(plan_batches)}"
        user_prompt = build_dynamic_prompt(
            context_text=trimmed_context, combination_plan=batch_plan
        )
        expected_keys = {
            _combo_key(diff, main_fmt, sub_fmt)
            for diff, main_fmt, sub_fmt in batch_plan
        }

        retries = max(1, int(generation_retries))
        for batch_attempt in range(1, retries + 1):
            data = chat_json(
                client=generation_client,
                model=QWEN_MODEL,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.1,
                response_type="generation",
                window_tag=f"{batch_tag}::retry{batch_attempt}",
                max_retries=max(1, int(generation_retries)),
            )

            items = data.get("items", [])
            if not isinstance(items, list):
                _append_llm_trace(
                    {
                        "type": "generation",
                        "window": batch_tag,
                        "model": QWEN_MODEL,
                        "status": "invalid_items_payload",
                        "batch_attempt": batch_attempt,
                    }
                )
                items = []

            normalized: List[Dict[str, Any]] = []
            for item in items:
                if not isinstance(item, dict):
                    continue

                q = normalize_text(str(item.get("question", "")))
                a = normalize_text(str(item.get("answer", "")))
                r = normalize_text(str(item.get("reasoning", "")))
                if not q or not a:
                    continue

                difficulty = normalize_blooms_level(
                    str(item.get("difficulty", "Understand"))
                )

                sub_format = str(item.get("sub_format", "Conceptual"))
                if sub_format not in SUBFORMAT_TO_MAIN_FORMAT:
                    sub_format = "Conceptual"

                if not _is_valid_item_for_format(sub_format, q, a, item):
                    _append_llm_trace(
                        {
                            "type": "generation",
                            "window": batch_tag,
                            "model": QWEN_MODEL,
                            "status": "invalid_format_item",
                            "batch_attempt": batch_attempt,
                            "sub_format": sub_format,
                            "question_preview": _preview(q),
                        }
                    )
                    continue

                mapped_main_format = SUBFORMAT_TO_MAIN_FORMAT[sub_format]
                combo_key = _combo_key(difficulty, mapped_main_format, sub_format)

                normalized.append(
                    {
                        "combo_id": str(item.get("combo_id", "")) or "",
                        "combo_key": combo_key,
                        "question": q,
                        "answer": a,
                        "reasoning": r,
                        "difficulty": difficulty,
                        "main_topic": str(item.get("main_topic", "DSA")) or "DSA",
                        "sub_topic": str(item.get("sub_topic", "General")) or "General",
                        "main_format": mapped_main_format,
                        "sub_format": sub_format,
                        "option_a": normalize_text(str(item.get("option_a", ""))),
                        "option_b": normalize_text(str(item.get("option_b", ""))),
                        "option_c": normalize_text(str(item.get("option_c", ""))),
                        "option_d": normalize_text(str(item.get("option_d", ""))),
                        "correct_option": normalize_text(
                            str(item.get("correct_option", ""))
                        ).upper(),
                    }
                )

            selected_by_combo: Dict[str, Dict[str, Any]] = {}
            for row in normalized:
                key = row["combo_key"]
                if key not in expected_keys:
                    continue
                if key in selected_by_combo:
                    continue
                selected_by_combo[key] = row

            missing_batch: List[str] = []
            tentative_rows: List[Dict[str, Any]] = []
            for diff, main_fmt, sub_fmt in batch_plan:
                key = _combo_key(diff, main_fmt, sub_fmt)
                row = selected_by_combo.get(key)
                if row:
                    row = dict(row)
                    row.pop("combo_key", None)
                    tentative_rows.append(row)
                else:
                    missing_batch.append(key)

            if not missing_batch:
                all_rows.extend(tentative_rows)
                break

            _append_llm_trace(
                {
                    "type": "generation",
                    "window": batch_tag,
                    "model": QWEN_MODEL,
                    "status": "batch_retry_validation_failed",
                    "batch_attempt": batch_attempt,
                    "missing_combos": len(missing_batch),
                }
            )

            if batch_attempt == retries:
                all_rows.extend(tentative_rows)
                missing_total.extend(missing_batch)

    _append_llm_trace(
        {
            "type": "generation",
            "window": window_tag or "na",
            "model": QWEN_MODEL,
            "status": "batched_normalized",
            "requested": len(full_plan),
            "normalized_items": len(all_rows),
            "missing_combos": len(missing_total),
            "batches": len(plan_batches),
        }
    )

    if missing_total:
        print(
            f"[window] {window_tag} missing_combinations={len(missing_total)} details={missing_total}"
        )

    return all_rows


# %%
# Deep smoke matrix (v2): parse orphan </think> consistently with main pipeline.
# This cell is the canonical smoke check for current parser behavior.

from pprint import pprint


def _msg_to_text_v2(msg: Any) -> str:
    content = getattr(msg, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: List[str] = []
        for p in content:
            if isinstance(p, dict):
                t = p.get("text") or p.get("content") or ""
                if t:
                    parts.append(str(t))
            elif hasattr(p, "text"):
                t = getattr(p, "text", "")
                if t:
                    parts.append(str(t))
        return "\n".join(parts).strip()
    return ""


def _extract_thinking_block_v2(content_text: str, reasoning_text: str) -> str:
    # Reuse the exact main-pipeline parser to avoid divergence.
    return _extract_qwen_thinking_text(content_text, reasoning_text)


qwen_client = build_qwen_client()
base_messages = [
    {"role": "system", "content": "Return strict JSON only."},
    {"role": "user", "content": 'Return exactly: {"ok": true, "source": "qwen_smoke"}'},
]

cases = [
    {"name": "think_on_temp00_unbounded", "temperature": 0.0, "enable_thinking": True},
    {
        "name": "think_off_temp00_unbounded",
        "temperature": 0.0,
        "enable_thinking": False,
    },
    {
        "name": "think_off_temp02_unbounded",
        "temperature": 0.2,
        "enable_thinking": False,
    },
]

results: List[Dict[str, Any]] = []

for cfg in cases:
    req = {
        "model": QWEN_MODEL,
        "messages": base_messages,
        "temperature": cfg["temperature"],
    }
    if cfg["enable_thinking"]:
        req["extra_body"] = {"chat_template_kwargs": {"enable_thinking": True}}

    try:
        resp = qwen_client.chat.completions.create(**req)
        choice = resp.choices[0]
        msg = choice.message

        content_text = _msg_to_text_v2(msg)
        provider_reasoning = str(getattr(msg, "reasoning_content", None) or "")
        thinking_text = _extract_thinking_block_v2(content_text, provider_reasoning)

        _log_qwen_raw_response(
            response_type="smoke_v2",
            window_tag=cfg["name"],
            attempt=1,
            variant_idx=1,
            finish_reason=getattr(choice, "finish_reason", None),
            raw=content_text,
            reasoning=thinking_text,
        )

        usage = getattr(resp, "usage", None)
        row = {
            "case": cfg["name"],
            "finish_reason": getattr(choice, "finish_reason", None),
            "content_len": len(content_text),
            "reasoning_len": len(thinking_text),
            "provider_reasoning_len": len(provider_reasoning),
            "thinking_len": len(thinking_text),
            "content_preview": content_text[:120],
            "reasoning_preview": thinking_text[:120],
            "provider_reasoning_preview": provider_reasoning[:120],
            "thinking_preview": thinking_text[:120],
            "usage": usage.model_dump() if hasattr(usage, "model_dump") else str(usage),
        }
        results.append(row)

        print("\n===", cfg["name"], "===")
        print("finish_reason:", row["finish_reason"])
        print(
            "content_len:",
            row["content_len"],
            "| reasoning_len:",
            row["reasoning_len"],
            "| provider_reasoning_len:",
            row["provider_reasoning_len"],
            "| thinking_len:",
            row["thinking_len"],
        )
        print("content_preview:", repr(row["content_preview"]))
        print("reasoning_preview:", repr(row["reasoning_preview"]))
        print("provider_reasoning_preview:", repr(row["provider_reasoning_preview"]))
        print("thinking_preview:", repr(row["thinking_preview"]))
        print("thinking_block:")
        print(thinking_text if thinking_text else "<EMPTY>")

        if row["content_len"] == 0:
            print("raw_message_dump:")
            if hasattr(msg, "model_dump"):
                pprint(msg.model_dump())
            else:
                pprint(str(msg))

    except Exception as exc:
        results.append({"case": cfg["name"], "error": str(exc)})
        print("\n===", cfg["name"], "===")
        print("error:", exc)

print("\nSummary:")
for r in results:
    print(r)

# %%
from rapidfuzz import fuzz


def build_windows(
    total_pages: int, window_size: int = WINDOW_SIZE, stride: int = WINDOW_STRIDE
) -> List[Tuple[int, int]]:
    if total_pages <= 0:
        return []
    windows: List[Tuple[int, int]] = []
    start = 1
    while start <= total_pages:
        end = min(total_pages, start + window_size - 1)
        windows.append((start, end))
        if end == total_pages:
            break
        start += stride
    return windows


def summarize_page_data_types_from_context(context_text: str) -> Dict[str, int]:
    counts: Dict[str, int] = {"plain_text": 0, "markdown": 0, "latex": 0}
    for m in re.finditer(
        r"data_type\s*=\s*(plain_text|markdown|latex)",
        context_text or "",
        flags=re.IGNORECASE,
    ):
        k = m.group(1).lower()
        counts[k] = counts.get(k, 0) + 1
    return counts


def normalize_for_dedup(text: str) -> str:
    text = normalize_text(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def deduplicate_rows(
    rows: List[Dict[str, Any]], threshold: int = 92
) -> List[Dict[str, Any]]:
    kept: List[Dict[str, Any]] = []
    seen: List[str] = []
    for row in rows:
        q_norm = normalize_for_dedup(row.get("question", ""))
        if not q_norm:
            continue

        if q_norm in seen:
            continue

        duplicate = False
        for prev in seen:
            if fuzz.token_set_ratio(q_norm, prev) >= threshold:
                duplicate = True
                break

        if duplicate:
            continue

        seen.append(q_norm)
        kept.append(row)
    return kept


def _format_specific_rules(sub_format: str) -> List[str]:
    if sub_format == "MCQ":
        return [
            "Include exactly four options (A-D), one unambiguously correct answer, and plausible distractors.",
            "Provide option_a, option_b, option_c, option_d, and correct_option fields.",
            "Set answer to start with the correct label (A/B/C/D) and a brief rationale.",
        ]
    if sub_format == "Fill_blank":
        return [
            "Use exactly one blank token in question: ____.",
            "Answer should be the expected fill with a short rationale.",
        ]
    if sub_format == "Assertion":
        return [
            "Use assertion-reason structure in question text.",
            "Answer must include the verdict and whether reason supports assertion.",
        ]
    if sub_format == "Analytical":
        return [
            "Ask for structured analysis or comparison grounded in context.",
            "Answer should be concise and logically sequenced.",
        ]
    return [
        "Ask a self-contained conceptual question that tests principles/causality.",
        "Answer should explain the concept clearly and briefly.",
    ]


def build_dynamic_prompt(
    context_text: str, combination_plan: List[Tuple[str, str, str]]
) -> str:
    question_count = len(combination_plan)
    required_combo_lines = []
    combo_instruction_lines: List[str] = []
    any_mcq = False

    page_type_counts = summarize_page_data_types_from_context(context_text)
    page_type_summary = (
        f"plain_text={page_type_counts.get('plain_text', 0)}, "
        f"markdown={page_type_counts.get('markdown', 0)}, "
        f"latex={page_type_counts.get('latex', 0)}"
    )

    for idx, (diff, main_fmt, sub_fmt) in enumerate(combination_plan, start=1):
        combo_id = f"combo_{idx:02d}_{diff.lower()}_{sub_fmt.lower()}"
        required_combo_lines.append(
            f"- {combo_id}: difficulty={diff}, main_format={main_fmt}, sub_format={sub_fmt}"
        )
        fmt_rules = _format_specific_rules(sub_fmt)
        any_mcq = any_mcq or (sub_fmt == "MCQ")
        combo_instruction_lines.append(f"- {combo_id}:")
        combo_instruction_lines.append(f"  cognitive_goal: {DIFFICULTY_SNIPPETS[diff]}")
        combo_instruction_lines.append(f"  format_goal: {FORMAT_SNIPPETS[sub_fmt]}")
        for r in fmt_rules:
            combo_instruction_lines.append(f"  rule: {r}")

    extra_schema = ""
    if any_mcq:
        extra_schema = (
            '\n      "option_a": "optional_for_mcq",'
            '\n      "option_b": "optional_for_mcq",'
            '\n      "option_c": "optional_for_mcq",'
            '\n      "option_d": "optional_for_mcq",'
            '\n      "correct_option": "A|B|C|D (optional_for_mcq)"'
        )

    return f"""
Generate exactly {question_count} high-quality QA items from the context.

Context:
{context_text[:MAX_CONTEXT_CHARS]}

Page data profile for this window: {page_type_summary}
- plain_text: manually extracted prose-like text.
- markdown: marker-converted content, may include headings/lists/code blocks/links.
- latex: vision-latex converted content, may include equations and symbolic notation.

Data-type parsing rules:
1) Respect page-level [Page X | data_type=...] tags while interpreting evidence.
2) For markdown pages, ignore markdown syntax markers and use semantic text content.
3) For latex pages, parse equations/symbols faithfully; preserve technical notation in answers where needed.
4) Do not misread formatting tokens as concepts (e.g., '#', '*', '\\section', raw delimiters).

Hard constraints:
1) The examnee will NOT be given the source context; every question must be fully self-contained and understandable on its own.
2) Do not reference location markers like 'line 7', 'above paragraph', 'this page', 'in the figure', or 'section 1.2'.
3) Do not use arbitrary numeric references unless the context contains executable code/pseudocode and the number is semantically necessary.
4) Use only facts present in context. No external facts.
5) Avoid duplicates and near-duplicates.
6) Keep answers concise but complete.
7) Include a short reasoning field for each item that justifies why the answer is correct from context.
8) Keep reasoning concise (1-3 sentences), evidence-grounded, and free of chain-of-thought style hidden deliberations.
9) Produce exactly one item for each required combination below. Do not skip any combination.
10) Output compact valid JSON only. Do not add markdown, comments, trailing commas, or extra keys.
11) Each item must include all required keys and valid enum values.
12) Keep question and answer concise to avoid truncation; avoid long paragraphs.

Required combinations (exactly one item each):
{chr(10).join(required_combo_lines)}

Per-combination generation guidance:
{chr(10).join(combo_instruction_lines)}

Field rules:
- combo_id must exactly match one required combo_id above.
- difficulty/main_format/sub_format must match the required combination for that combo_id.
- reasoning must be 1-2 short evidence-grounded sentences.
- Include option_a/option_b/option_c/option_d/correct_option only when the combo sub_format is MCQ.

Return strict JSON with shape:
{{
  "items": [
    {{
      "combo_id": "combo_01_remember_mcq",
      "question": "...",
      "answer": "...",
      "reasoning": "brief grounded rationale",
      "difficulty": "...",
      "main_topic": "DSA",
      "sub_topic": "...",
      "main_format": "...",
      "sub_format": "..."{extra_schema}
    }}
  ]
}}
"""


def _extract_mcq_fields(question: str, answer: str) -> Dict[str, Any]:
    q = normalize_text(question)
    m = re.search(
        r"\bA\)\s*(.*?)\s*B\)\s*(.*?)\s*C\)\s*(.*?)\s*D\)\s*(.*)$",
        q,
        flags=re.IGNORECASE,
    )
    if not m:
        return {
            "question_stem": q,
            "option_a": "",
            "option_b": "",
            "option_c": "",
            "option_d": "",
            "correct_option": "",
        }

    stem = q[: m.start()].strip(" :-")
    ans_match = re.match(r"^\s*([ABCD])\)", normalize_text(answer), flags=re.IGNORECASE)
    return {
        "question_stem": stem,
        "option_a": normalize_text(m.group(1)),
        "option_b": normalize_text(m.group(2)),
        "option_c": normalize_text(m.group(3)),
        "option_d": normalize_text(m.group(4)),
        "correct_option": ans_match.group(1).upper() if ans_match else "",
    }


def _extract_assertion_fields(question: str) -> Dict[str, Any]:
    q = normalize_text(question)
    m = re.search(
        r"Assertion\s*[:\-]\s*(.*?)\s*Reason\s*[:\-]\s*(.*)$", q, flags=re.IGNORECASE
    )
    if m:
        return {
            "assertion_statement": normalize_text(m.group(1)),
            "reason_statement": normalize_text(m.group(2)),
        }
    return {
        "assertion_statement": q,
        "reason_statement": "",
    }


def _clean_reasoning_field(text: str) -> str:
    """Clean reasoning field: strip think blocks and normalize whitespace."""
    text = str(text or "").strip()
    # Remove <think>...</think> blocks
    text = _strip_qwen_think_blocks(text)
    # Normalize multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _count_reasoning_chars(text: str) -> int:
    """Count reasoning characters after cleaning think blocks."""
    cleaned = _clean_reasoning_field(text)
    return len(cleaned)


def _enrich_row_for_jsonl(row: Dict[str, Any]) -> Dict[str, Any]:
    r = dict(row)
    sub_format = str(r.get("sub_format", "")).strip()
    question = str(r.get("question", ""))
    answer = str(r.get("answer", ""))
    reasoning = str(r.get("reasoning", ""))

    # Clean reasoning field: strip think blocks and normalize
    r["reasoning"] = _clean_reasoning_field(reasoning)
    r["reasoning_char_count"] = _count_reasoning_chars(reasoning)

    if sub_format == "MCQ":
        parsed = _extract_mcq_fields(question, answer)
        for fld in [
            "question_stem",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "correct_option",
        ]:
            existing = normalize_text(str(r.get(fld, "")))
            if existing:
                parsed[fld] = existing
        if not parsed.get("correct_option"):
            m = re.match(r"^\s*([ABCD])\)", normalize_text(answer), flags=re.IGNORECASE)
            parsed["correct_option"] = m.group(1).upper() if m else ""
        r.update(parsed)
    elif sub_format == "Assertion":
        r.update(_extract_assertion_fields(question))
    elif sub_format == "Fill_blank":
        r["question_stem"] = question
        r["blank_count"] = question.count("____")
        r["expected_fill"] = normalize_text(answer)
    else:
        r["question_stem"] = question

    return r


def append_jsonl_rows(jsonl_path: Path, rows: List[Dict[str, Any]]) -> int:
    if not rows:
        return 0
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    with jsonl_path.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(_enrich_row_for_jsonl(r), ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())
    return len(rows)


def append_llm_trace(
    trace_path: Path, entries: List[Dict[str, Any]], start_index: int = 0
) -> int:
    if start_index >= len(entries):
        return start_index
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    with trace_path.open("a", encoding="utf-8") as f:
        for e in entries[start_index:]:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())
    return len(entries)


def _window_key(page_start: int, page_end: int) -> str:
    return f"{int(page_start)}-{int(page_end)}"


def load_stream_checkpoint_index(
    stream_jsonl_path: Optional[Path], input_csv_file: str
) -> Dict[str, set]:
    index: Dict[str, set] = {}
    if not stream_jsonl_path or not stream_jsonl_path.exists():
        return index

    with stream_jsonl_path.open("r", encoding="utf-8") as f:
        for line in f:
            raw = (line or "").strip()
            if not raw:
                continue
            try:
                row = json.loads(raw)
            except Exception:
                continue

            if str(row.get("input_csv_file", "")).strip() != input_csv_file:
                continue

            p_start = _to_int(row.get("page_start"), 0)
            p_end = _to_int(row.get("page_end"), 0)
            if p_start <= 0 or p_end <= 0:
                continue

            difficulty = normalize_blooms_level(str(row.get("difficulty", "")))
            sub_format = str(row.get("sub_format", "")).strip()
            if sub_format not in SUBFORMAT_TO_MAIN_FORMAT:
                continue

            inferred_main = SUBFORMAT_TO_MAIN_FORMAT[sub_format]
            main_format = (
                str(row.get("main_format", inferred_main)).strip() or inferred_main
            )
            if main_format not in {"Objective", "Subjective"}:
                main_format = inferred_main

            wk = _window_key(p_start, p_end)
            index.setdefault(wk, set()).add(
                _combo_key(difficulty, main_format, sub_format)
            )

    return index


def save_outputs(rows: List[Dict[str, Any]], stem: str) -> Dict[str, Path]:
    jsonl_path = OUTPUT_DIR / f"{stem}.jsonl"
    structured_rows = [_enrich_row_for_jsonl(r) for r in rows]

    with jsonl_path.open("w", encoding="utf-8") as f:
        for r in structured_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    trace_logs = get_llm_trace_logs()
    if trace_logs:
        trace_jsonl_path = OUTPUT_DIR / f"{stem}_llm_trace.jsonl"
        with trace_jsonl_path.open("w", encoding="utf-8") as f:
            for e in trace_logs:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
        print(f"[trace] wrote_llm_trace={trace_jsonl_path} rows={len(trace_logs)}")

    return {"jsonl": jsonl_path}


# %%
# Override: per-combination parallel generation (one request per question-combo).
PARALLEL_COMBO_REQUESTS = max(
    1, int(os.getenv("QWEN_PARALLEL_COMBO_REQUESTS", "8") or 8)
)


def _normalize_generated_item(
    item: Dict[str, Any],
    expected_combo: Tuple[str, str, str],
    batch_tag: str,
    batch_attempt: int,
) -> Optional[Dict[str, Any]]:
    if not isinstance(item, dict):
        return None

    q = normalize_text(str(item.get("question", "")))
    a = normalize_text(str(item.get("answer", "")))
    r = normalize_text(str(item.get("reasoning", "")))
    if not q or not a:
        return None

    difficulty = normalize_blooms_level(str(item.get("difficulty", "Understand")))
    sub_format = str(item.get("sub_format", "Conceptual"))
    if sub_format not in SUBFORMAT_TO_MAIN_FORMAT:
        sub_format = "Conceptual"

    if not _is_valid_item_for_format(sub_format, q, a, item):
        _append_llm_trace(
            {
                "type": "generation",
                "window": batch_tag,
                "model": QWEN_MODEL,
                "status": "invalid_format_item",
                "batch_attempt": batch_attempt,
                "sub_format": sub_format,
                "question_preview": _preview(q),
            }
        )
        return None

    mapped_main_format = SUBFORMAT_TO_MAIN_FORMAT[sub_format]
    combo_key = _combo_key(difficulty, mapped_main_format, sub_format)
    expected_key = _combo_key(expected_combo[0], expected_combo[1], expected_combo[2])
    if combo_key != expected_key:
        return None

    return {
        "combo_id": str(item.get("combo_id", "")) or "",
        "combo_key": combo_key,
        "question": q,
        "answer": a,
        "reasoning": r,
        "difficulty": difficulty,
        "main_topic": str(item.get("main_topic", "DSA")) or "DSA",
        "sub_topic": str(item.get("sub_topic", "General")) or "General",
        "main_format": mapped_main_format,
        "sub_format": sub_format,
        "option_a": normalize_text(str(item.get("option_a", ""))),
        "option_b": normalize_text(str(item.get("option_b", ""))),
        "option_c": normalize_text(str(item.get("option_c", ""))),
        "option_d": normalize_text(str(item.get("option_d", ""))),
        "correct_option": normalize_text(str(item.get("correct_option", ""))).upper(),
    }


def _request_single_combo(
    generation_client: OpenAI,
    context_text: str,
    combo: Tuple[str, str, str],
    window_tag: str,
    generation_retries: int,
) -> Optional[Dict[str, Any]]:
    system_prompt = (
        "You are an expert computer science educator creating rigorous study QA data. "
        "Use internal reasoning, but return only strict JSON in the final content."
    )
    combo_key = _combo_key(combo[0], combo[1], combo[2])

    # Keep prompt payload compact to reduce truncation risk.
    trimmed_context = (context_text or "")[:7000]
    user_prompt = build_dynamic_prompt(
        context_text=trimmed_context, combination_plan=[combo]
    )

    retries = max(1, int(generation_retries))
    for attempt in range(1, retries + 1):
        batch_tag = f"{window_tag}::{combo_key}::retry{attempt}"
        try:
            data = chat_json(
                client=generation_client,
                model=QWEN_MODEL,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.1,
                response_type="generation",
                window_tag=batch_tag,
                max_retries=1,
            )
        except Exception as exc:
            _append_llm_trace(
                {
                    "type": "generation",
                    "window": batch_tag,
                    "model": QWEN_MODEL,
                    "status": "request_or_parse_error",
                    "batch_attempt": attempt,
                    "error": str(exc),
                }
            )
            continue

        items = data.get("items", [])
        if not isinstance(items, list):
            _append_llm_trace(
                {
                    "type": "generation",
                    "window": batch_tag,
                    "model": QWEN_MODEL,
                    "status": "invalid_items_payload",
                    "batch_attempt": attempt,
                }
            )
            continue

        for item in items:
            normalized = _normalize_generated_item(
                item, combo, batch_tag=batch_tag, batch_attempt=attempt
            )
            if normalized:
                return normalized

        _append_llm_trace(
            {
                "type": "generation",
                "window": batch_tag,
                "model": QWEN_MODEL,
                "status": "combo_not_found_in_response",
                "batch_attempt": attempt,
                "expected_combo": combo_key,
            }
        )

    _append_llm_trace(
        {
            "type": "generation",
            "window": window_tag or "na",
            "model": QWEN_MODEL,
            "status": "combo_failed_after_retries",
            "expected_combo": combo_key,
            "retries": retries,
        }
    )
    return None


def generate_window_questions(
    generation_client: OpenAI,
    context_text: str,
    question_count: int,
    window_tag: str = "",
    combination_plan: Optional[List[Tuple[str, str, str]]] = None,
    generation_retries: int = GENERATION_MAX_RETRIES,
) -> List[Dict[str, Any]]:
    full_plan = combination_plan or get_question_combinations(question_count)
    if not full_plan:
        return []

    max_workers = min(len(full_plan), PARALLEL_COMBO_REQUESTS)
    print(
        f"[window] {window_tag} parallel_combo_requests={max_workers} planned_questions={len(full_plan)}"
    )

    selected_by_combo: Dict[str, Dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_combo = {
            executor.submit(
                _request_single_combo,
                generation_client,
                context_text,
                combo,
                window_tag,
                generation_retries,
            ): combo
            for combo in full_plan
        }

        for future in as_completed(future_to_combo):
            combo = future_to_combo[future]
            key = _combo_key(combo[0], combo[1], combo[2])
            try:
                row = future.result()
            except Exception as exc:
                _append_llm_trace(
                    {
                        "type": "generation",
                        "window": window_tag or "na",
                        "model": QWEN_MODEL,
                        "status": "parallel_future_error",
                        "expected_combo": key,
                        "error": str(exc),
                    }
                )
                continue

            if row:
                selected_by_combo[key] = row

    all_rows: List[Dict[str, Any]] = []
    missing_total: List[str] = []
    for diff, main_fmt, sub_fmt in full_plan:
        key = _combo_key(diff, main_fmt, sub_fmt)
        row = selected_by_combo.get(key)
        if row:
            out = dict(row)
            out.pop("combo_key", None)
            all_rows.append(out)
        else:
            missing_total.append(key)

    _append_llm_trace(
        {
            "type": "generation",
            "window": window_tag or "na",
            "model": QWEN_MODEL,
            "status": "parallel_combo_normalized",
            "requested": len(full_plan),
            "normalized_items": len(all_rows),
            "missing_combos": len(missing_total),
            "parallel_workers": max_workers,
        }
    )

    if missing_total:
        print(
            f"[window] {window_tag} missing_combinations={len(missing_total)} details={missing_total}"
        )

    return all_rows


# %%
@dataclass
class RunConfig:
    questions_per_window: int = QUESTIONS_PER_WINDOW
    window_size: int = WINDOW_SIZE
    stride: int = WINDOW_STRIDE
    dedup_threshold: int = DEDUP_THRESHOLD
    min_context_chars: int = MIN_CONTEXT_CHARS
    generation_retries: int = GENERATION_MAX_RETRIES
    validation_retries: int = VALIDATION_MAX_RETRIES


RUN_CFG = RunConfig(
    questions_per_window=min(30, len(ALL_QUESTION_COMBINATIONS)),
    window_size=5,
    stride=2,
    dedup_threshold=90,
    min_context_chars=450,
    generation_retries=3,
    validation_retries=2,
)

print("Run configuration:")
print(RUN_CFG)

# %%
import builtins
from typing import Optional

# Global debug flag: when False, suppress CLI prints while still writing llm_trace JSONL.
DEBUG_CLI = os.getenv("QA_DEBUG_CLI", "0").strip().lower() in {"1", "true", "yes", "on"}
_RAW_PRINT = builtins.print


def debug_print(*args, **kwargs):
    if DEBUG_CLI:
        _RAW_PRINT(*args, **kwargs)


# Route notebook-level print calls through debug flag.
print = debug_print


def _read_last_valid_jsonl_row(jsonl_path: Optional[Path]) -> Optional[Dict[str, Any]]:
    if not jsonl_path or not jsonl_path.exists():
        return None

    # Read from file end to quickly find the last valid JSON row.
    with jsonl_path.open("rb") as f:
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        if file_size <= 0:
            return None

        chunk_size = 8192
        pos = file_size
        carry = b""

        while pos > 0:
            take = min(chunk_size, pos)
            pos -= take
            f.seek(pos)
            block = f.read(take)
            buf = block + carry
            lines = buf.splitlines()

            if pos > 0:
                carry = lines[0] if lines else b""
                lines = lines[1:] if len(lines) > 1 else []
            else:
                carry = b""

            for raw in reversed(lines):
                text = raw.decode("utf-8", errors="ignore").strip()
                if not text:
                    continue
                try:
                    obj = json.loads(text)
                except Exception:
                    continue
                if isinstance(obj, dict):
                    return obj

    return None


def load_last_stream_progress(
    stream_jsonl_path: Optional[Path], input_csv_file: str
) -> Dict[str, Any]:
    row = _read_last_valid_jsonl_row(stream_jsonl_path)
    if not row:
        return {}

    row_csv = str(row.get("input_csv_file", "")).strip()
    if row_csv and row_csv != input_csv_file:
        return {}

    p_start = _to_int(row.get("page_start"), 0)
    p_end = _to_int(row.get("page_end"), 0)
    b_no = _to_int(row.get("batch_number"), 1)
    w_idx = _to_int(row.get("window_index"), 0)
    q_no = _to_int(row.get("question_number"), 0)

    if p_start <= 0 or p_end <= 0:
        page_range = str(row.get("page_number_range", "")).strip()
        m = re.match(r"\s*(\d+)\s*[-:]\s*(\d+)\s*$", page_range)
        if m:
            p_start, p_end = int(m.group(1)), int(m.group(2))

    if p_start <= 0 or p_end <= 0:
        return {}

    return {
        "page_start": p_start,
        "page_end": p_end,
        "batch_number": max(1, b_no),
        "window_index": w_idx,
        "question_number": q_no,
    }


def generate_for_book(
    generation_client: OpenAI,
    validation_client: OpenAI,
    csv_path: Path,
    questions_per_window: int = QUESTIONS_PER_WINDOW,
    window_size: int = WINDOW_SIZE,
    stride: int = WINDOW_STRIDE,
    batch_number: int = 1,
    dedup_threshold: int = DEDUP_THRESHOLD,
    min_context_chars: int = MIN_CONTEXT_CHARS,
    generation_retries: int = GENERATION_MAX_RETRIES,
    validation_retries: int = VALIDATION_MAX_RETRIES,
    stream_jsonl_path: Optional[Path] = None,
    stream_trace_path: Optional[Path] = None,
    flush_every_windows: int = 1,
) -> List[Dict[str, Any]]:
    book_pages_df = load_book_pages_from_csv(csv_path)
    if book_pages_df.empty:
        print(f"[book] skip={csv_path.name} reason=empty_csv_content")
        return []

    book_name = str(book_pages_df["book_name"].iloc[0]) or csv_path.stem.replace(
        "_pages_cleaned", ""
    )
    total_pages = get_book_total_pages(book_pages_df)
    windows = build_windows(
        total_pages=total_pages, window_size=window_size, stride=stride
    )
    rows: List[Dict[str, Any]] = []
    batch_buffer: List[Dict[str, Any]] = []
    trace_offset = 0

    target_questions_per_window = max(
        1, min(int(questions_per_window), len(ALL_QUESTION_COMBINATIONS))
    )
    flush_every_windows = max(1, int(flush_every_windows))
    checkpoint_index = load_stream_checkpoint_index(stream_jsonl_path, csv_path.name)

    # Resume anchor from the LAST row in stream JSONL for this CSV.
    last_progress = (
        load_last_stream_progress(stream_jsonl_path, csv_path.name)
        if stream_jsonl_path
        else {}
    )
    resume_key = ""
    resume_reached = False
    effective_batch_number = int(batch_number)

    if last_progress:
        resume_key = _window_key(last_progress["page_start"], last_progress["page_end"])
        effective_batch_number = max(
            effective_batch_number,
            int(last_progress.get("batch_number", effective_batch_number)),
        )
        print(
            f"[resume] book={book_name} from_last_row page_range={last_progress['page_start']}-{last_progress['page_end']} "
            f"batch={effective_batch_number}"
        )

    resumed_complete = 0
    resumed_partial = 0

    print(
        f"[book] start={book_name} csv={csv_path.name} total_pages={total_pages} windows={len(windows)}"
    )

    for w_idx, (p_start, p_end) in enumerate(
        tqdm(windows, desc=f"Windows::{book_name}"), start=1
    ):
        wk = _window_key(p_start, p_end)

        # Skip everything before the last persisted window.
        if resume_key and not resume_reached:
            if wk != resume_key:
                continue
            resume_reached = True

        window_tag = f"{book_name}:{p_start}-{p_end}"
        context_text, page_meta = build_context_from_pages(
            book_pages_df, page_start=p_start, page_end=p_end
        )
        if not context_text or len(context_text) < max(200, int(min_context_chars)):
            print(
                f"[window] {window_tag} context_valid=False reason=insufficient_context chars={len(context_text or '')}"
            )
            continue

        print(f"[window] {window_tag} context_valid=True chars={len(context_text)}")
        window_pages = max(1, p_end - p_start + 1)
        max_questions_per_page = max(
            1,
            (target_questions_per_window + max(1, window_size) - 1)
            // max(1, window_size),
        )
        full_plan = list(get_question_combinations(target_questions_per_window))
        existing_combo_keys = (
            checkpoint_index.get(wk, set()) if stream_jsonl_path else set()
        )
        pending_plan = [
            combo
            for combo in full_plan
            if _combo_key(combo[0], combo[1], combo[2]) not in existing_combo_keys
        ]

        if stream_jsonl_path and not pending_plan:
            resumed_complete += 1
            print(
                f"[resume] skip_complete window={window_tag} combos={len(existing_combo_keys)}"
            )
            continue

        if stream_jsonl_path and existing_combo_keys and pending_plan:
            resumed_partial += 1
            gate = {
                "eligible": True,
                "reason": "resume_partial_window",
                "recommended_questions": len(full_plan),
            }
            print(
                f"[resume] partial window={window_tag} existing={len(existing_combo_keys)} pending={len(pending_plan)}"
            )
        else:
            gate = ask_eligibility(
                validation_client,
                context_text,
                window_tag=window_tag,
                max_questions_per_page=max_questions_per_page,
                window_pages=window_pages,
                validation_retries=validation_retries,
            )
            if not gate["eligible"]:
                print(
                    f"[window] {window_tag} eligible=False reason={gate.get('reason', 'unknown')}"
                )
                continue

        combination_plan = pending_plan if pending_plan else full_plan
        q_count = len(combination_plan)
        page_types = sorted(
            {str(pm.get("page_data_type", "plain_text")) for pm in page_meta}
        )
        page_sources = sorted(
            {
                str(pm.get("source_used", ""))
                for pm in page_meta
                if str(pm.get("source_used", "")).strip()
            }
        )

        print(
            f"[window] {window_tag} eligible=True "
            f"recommended={gate.get('recommended_questions', 'na')} "
            f"requested_questions={q_count} "
            f"data_types={page_types}"
        )

        try:
            items = generate_window_questions(
                generation_client,
                context_text=context_text,
                question_count=q_count,
                window_tag=window_tag,
                combination_plan=combination_plan,
                generation_retries=generation_retries,
            )
        except Exception as exc:
            print(
                f"[warn] generation failed for {book_name} pages {p_start}-{p_end}: {exc}"
            )
            continue

        print(f"[window] {window_tag} generated_items={len(items)}")

        for i, item in enumerate(items, start=1):
            existing_count = len(existing_combo_keys)
            row = {
                **item,
                "book_name": book_name,
                "page_number_range": f"{p_start} - {p_end}",
                "page_start": p_start,
                "page_end": p_end,
                "window_index": w_idx,
                "window_size": window_size,
                "window_stride": stride,
                "question_number": existing_count + i,
                "batch_number": effective_batch_number,
                "context_char_len": len(context_text),
                "eligibility_reason": gate.get("reason", "unknown"),
                "recommended_questions": int(
                    gate.get("recommended_questions", q_count) or q_count
                ),
                "window_page_metadata": page_meta,
                "window_page_types": page_types,
                "window_page_sources": page_sources,
                "input_csv_file": csv_path.name,
            }
            rows.append(row)
            batch_buffer.append(row)
            checkpoint_index.setdefault(wk, set()).add(
                _combo_key(
                    row.get("difficulty", ""),
                    row.get("main_format", ""),
                    row.get("sub_format", ""),
                )
            )

        if stream_jsonl_path and (
            (w_idx % flush_every_windows == 0) or (w_idx == len(windows))
        ):
            wrote = append_jsonl_rows(stream_jsonl_path, batch_buffer)
            if wrote:
                print(f"[stream] wrote_rows={wrote} path={stream_jsonl_path}")
            batch_buffer = []

        if stream_trace_path:
            trace_offset = append_llm_trace(
                stream_trace_path, get_llm_trace_logs(), start_index=trace_offset
            )

    if batch_buffer and stream_jsonl_path:
        wrote = append_jsonl_rows(stream_jsonl_path, batch_buffer)
        if wrote:
            print(f"[stream] wrote_rows={wrote} path={stream_jsonl_path}")

    pre_dedup = len(rows)
    deduped = deduplicate_rows(rows, threshold=dedup_threshold)
    if stream_jsonl_path:
        print(
            f"[resume] complete_windows_skipped={resumed_complete} partial_windows_resumed={resumed_partial}"
        )
    print(
        f"[book] complete={book_name} pre_dedup={pre_dedup} post_dedup={len(deduped)} removed={pre_dedup - len(deduped)}"
    )

    return deduped


# %% [markdown]
# ## Section A: Single-CSV Generation
#
# Uses the shared API + eligibility + sliding-window pipeline to generate QA rows for one selected page-text CSV in the pdf_page_text_by_book folder.

# %%
# # Section A: Generate QA for one selected CSV in CSV_PAGES_DIR

# generation_client = build_qwen_client()
# validation_client = build_openai_validation_client()

# csv_candidates = sorted(CSV_PAGES_DIR.glob("*_pages_cleaned.csv"))
# if not csv_candidates:
#     raise FileNotFoundError(f"No *_pages_cleaned.csv files found in {CSV_PAGES_DIR}")

# TARGET_CSV = csv_candidates[0]  # change this to any specific file in CSV_PAGES_DIR
# print(f"Selected CSV: {TARGET_CSV.name}")

# stream_jsonl = OUTPUT_DIR / f"qa_{TARGET_CSV.stem}_stream.jsonl"
# stream_trace = OUTPUT_DIR / f"qa_{TARGET_CSV.stem}_stream_llm_trace.jsonl"

# single_rows = generate_for_book(
#     generation_client=generation_client,
#     validation_client=validation_client,
#     csv_path=TARGET_CSV,
#     questions_per_window=RUN_CFG.questions_per_window,
#     window_size=RUN_CFG.window_size,
#     stride=RUN_CFG.stride,
#     batch_number=1,
#     dedup_threshold=RUN_CFG.dedup_threshold,
#     min_context_chars=RUN_CFG.min_context_chars,
#     generation_retries=RUN_CFG.generation_retries,
#     validation_retries=RUN_CFG.validation_retries,
#     stream_jsonl_path=stream_jsonl,
#     stream_trace_path=stream_trace,
#     flush_every_windows=1,
# )

# single_paths = save_outputs(single_rows, stem=f"qa_{TARGET_CSV.stem}_single_csv")

# print("Single-CSV generation complete.")
# print(f"Rows: {len(single_rows)}")
# print(f"- stream_jsonl: {stream_jsonl}")
# print(f"- stream_trace: {stream_trace}")
# for k, v in single_paths.items():
#     print(f"- {k}: {v}")

# %% [markdown]
# ## Section B: All-CSV Dataset Build
#
# Reuses the exact same functions from Section A, iterates all page-text CSV files in the pdf_page_text_by_book folder, and exports one deduplicated combined dataset.

# %%
# Section B: Generate QA for selected book groups (parallel workers + per-book isolated traces)

import gc

# Set selected groups here. Example: ["DSA"], ["CN", "OS"], or [] for all books.
BOOK_GROUPS: List[str] = ["DSA"]


def _normalize_group_token(text: str) -> str:
    t = normalize_text(str(text or "")).lower()
    return re.sub(r"[^a-z0-9]+", "", t)


def _book_group_prefix_from_stem(csv_stem: str) -> str:
    # Example stems: "DSA - 1_pages_cleaned", "CN - 2_pages_cleaned" -> "dsa", "cn"
    book_label = csv_stem.replace("_pages_cleaned", "")
    m = re.match(r"\s*([A-Za-z]+)", book_label)
    if m:
        return _normalize_group_token(m.group(1))
    return _normalize_group_token(book_label)


def filter_csv_candidates_by_groups(
    csv_files: List[Path], groups: List[str]
) -> List[Path]:
    if not groups:
        return csv_files

    wanted = {_normalize_group_token(g) for g in groups if str(g).strip()}
    if not wanted:
        return csv_files

    out: List[Path] = []
    for p in csv_files:
        prefix = _book_group_prefix_from_stem(p.stem)
        if prefix in wanted:
            out.append(p)
    return out


all_csv_candidates = sorted(CSV_PAGES_DIR.glob("*_pages_cleaned.csv"))
csv_candidates = filter_csv_candidates_by_groups(all_csv_candidates, BOOK_GROUPS)

if not csv_candidates:
    raise FileNotFoundError(
        f"No matching *_pages_cleaned.csv files found for groups={BOOK_GROUPS} in {CSV_PAGES_DIR}"
    )

# Configure based on provider limits and machine capacity.
MAX_PARALLEL_BOOKS = min(13, len(csv_candidates))
BATCH_FLUSH_WINDOWS = 5

book_run_summaries: List[Dict[str, Any]] = []

print(
    f"Selected groups: {BOOK_GROUPS if BOOK_GROUPS else 'ALL'} | "
    f"books_selected={len(csv_candidates)} / total_books={len(all_csv_candidates)}"
)


def process_single_book(task: Tuple[int, Path]) -> Dict[str, Any]:
    batch_idx, csv_path = task
    reset_llm_trace_logs()

    generation_client = build_qwen_client()
    validation_client = build_openai_validation_client()

    stream_jsonl = OUTPUT_DIR / f"qa_{csv_path.stem}_stream.jsonl"
    stream_trace = OUTPUT_DIR / f"qa_{csv_path.stem}_stream_llm_trace.jsonl"

    book_rows = generate_for_book(
        generation_client=generation_client,
        validation_client=validation_client,
        csv_path=csv_path,
        questions_per_window=RUN_CFG.questions_per_window,
        window_size=RUN_CFG.window_size,
        stride=RUN_CFG.stride,
        batch_number=batch_idx,
        dedup_threshold=RUN_CFG.dedup_threshold,
        min_context_chars=RUN_CFG.min_context_chars,
        generation_retries=RUN_CFG.generation_retries,
        validation_retries=RUN_CFG.validation_retries,
        stream_jsonl_path=stream_jsonl,
        stream_trace_path=stream_trace,
        flush_every_windows=BATCH_FLUSH_WINDOWS,
    )

    output_stem = f"qa_{csv_path.stem}_sliding_window"
    book_paths = save_outputs(book_rows, stem=output_stem)

    summary = {
        "status": "ok",
        "input_csv_file": csv_path.name,
        "rows_after_dedup": len(book_rows),
        "stream_jsonl": str(stream_jsonl),
        "stream_trace": str(stream_trace),
        "output_jsonl": str(book_paths.get("jsonl", "")),
        "error": "",
    }

    del book_rows
    del book_paths
    gc.collect()

    return summary


print(
    f"Running {len(csv_candidates)} selected books with up to {MAX_PARALLEL_BOOKS} parallel workers"
)
tasks: List[Tuple[int, Path]] = list(enumerate(csv_candidates, start=1))

with ThreadPoolExecutor(max_workers=MAX_PARALLEL_BOOKS) as executor:
    future_to_task = {
        executor.submit(process_single_book, task): task for task in tasks
    }
    for future in tqdm(
        as_completed(future_to_task), total=len(future_to_task), desc="Books"
    ):
        batch_idx, csv_path = future_to_task[future]
        try:
            summary = future.result()
            book_run_summaries.append(summary)
            print(
                f"\nCompleted {batch_idx}/{len(csv_candidates)}: {csv_path.name} "
                f"| rows_after_dedup={summary['rows_after_dedup']}"
            )
        except Exception as exc:
            print(
                f"\nFailed {batch_idx}/{len(csv_candidates)}: {csv_path.name} | error={exc}"
            )
            book_run_summaries.append(
                {
                    "status": "failed",
                    "input_csv_file": csv_path.name,
                    "rows_after_dedup": 0,
                    "stream_jsonl": str(
                        OUTPUT_DIR / f"qa_{csv_path.stem}_stream.jsonl"
                    ),
                    "stream_trace": str(
                        OUTPUT_DIR / f"qa_{csv_path.stem}_stream_llm_trace.jsonl"
                    ),
                    "output_jsonl": "",
                    "error": str(exc),
                }
            )

print("\nPer-book generation complete.")

if book_run_summaries:
    summary_df = pd.DataFrame(book_run_summaries)
    summary_df = summary_df.sort_values(["status", "input_csv_file"]).reset_index(
        drop=True
    )
    summary_csv = OUTPUT_DIR / "qa_per_book_generation_summary.csv"
    summary_df.to_csv(summary_csv, index=False)

    print("\nRun summary:")
    print(
        summary_df[["status", "input_csv_file", "rows_after_dedup"]].to_string(
            index=False
        )
    )
    failed_count = int((summary_df["status"] == "failed").sum())
    print(f"\nFailed books: {failed_count}")
    print(f"Summary CSV: {summary_csv}")
