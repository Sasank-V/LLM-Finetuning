![](_page_0_Picture_3.jpeg)

## Q. No. 1 - 25 Carry One Mark Each

- The simplified SOP (Sum of Product) form of the Boolean expression 1.  $(P + \overline{Q} + \overline{R}).(P + \overline{Q} + R).(P + Q + \overline{R})$  is
  - (A)  $(\overline{PQ} + \overline{R})$
- (B)  $(P + \overline{QR})$  (C)  $(\overline{PQ} + R)$  (D) (PQ + R)

Answer: - (B)

Exp: -

![](_page_0_Figure_12.jpeg)

$$f = (P + \overline{R})(P + \overline{Q})$$
$$= P + \overline{O}\overline{R}$$

Alternate method

$$\left(P+\overline{Q}+\overline{R}\right).\left(P+\overline{Q}+R\right).\left(P+Q+\overline{R}\right)=\overline{\left(\overline{P+\overline{Q}+\overline{R}}\right).\left(P+\overline{Q}+R\right).\left(P+Q+\overline{R}\right)}$$

$$=\overline{\overline{P}\ Q\ R}+\overline{\overline{P}\ Q\ \overline{R}}+\overline{\overline{P}\ \overline{Q}\ R}=\overline{\overline{\overline{P}\ Q\left(R+\overline{R}\right)}+\overline{\overline{P}\ \overline{Q}\ R}}=\overline{\overline{\overline{P}\ Q+\overline{P}\ \overline{Q}\ R}}=\overline{\overline{\overline{P}\ Q+\overline{P}\ \overline{Q}\ R}}$$

$$=\overline{\overline{P}(Q+R)}=P+\overline{Q}\overline{R}$$

Which one of the following circuits is NOT equivalent to a 2-input XNOR 2. (exclusive NOR) gate?

![](_page_0_Picture_20.jpeg)

(B)

![](_page_0_Picture_22.jpeg)

![](_page_0_Picture_23.jpeg)

Answer: - (D)

Exp: - All options except option 'D' gives EX-NOR gates

3. The minimum number of D flip-flops needed to design a mod-258 counter is

(A)9

- (B)8
- (C) 512
- (D) 258

Answer: - (A)

Exp:  $-2^n \ge 258 \Rightarrow n = 9$ 

4. A thread is usually defined as a 'light weight process' because an operating system (OS) maintains smaller data structures for a thread than for a process. In relation to this, which of the followings is TRUE?

![](_page_1_Picture_3.jpeg)

- (A) On per-thread basis, the OS maintains only CPU register state
- (B) The OS does not maintain a separate stack for each thread
- (C) On per-thread basis, the OS does not maintain virtual memory state
- (D)On per thread basis, the OS maintains only scheduling and accounting information

Answer: - (A)

5. K4 and Q3 are graphs with the following structures

![](_page_1_Picture_10.jpeg)

Which one of the following statements is TRUE in relation to these graphs?

- (A) K4 is planar while Q3 is not
- (B) Both K4 and Q3 are planar
- (C) Q3 is planar while K4 is not
- (D) Neither K4 not Q3 is planar

![](_page_1_Picture_16.jpeg)

- ∴ Both K<sub>4</sub> and Q<sub>3</sub> are planar
- 6. If the difference between the expectation of the square of random variable  $\left( \mathsf{E} \big[ \mathsf{X}^2 \big] \right)$  and the square of the expectation of the random variable  $\left( \mathsf{E} \big[ \mathsf{X}^2 \big] \right)$  is denoted by R then
  - (A) R = 0
- (B) R < 0
- (C)  $R \ge 0$
- (D)R>0

Answer: - (C)

- 7. The lexical analysis for a modern computer language such as Java needs the power of which one of the following machine models in a necessary and sufficient sense?
  - (A) Finite state automata
  - (B) Deterministic pushdown automata
  - (C) Non-Deterministic pushdown automata

![](_page_2_Picture_3.jpeg)

(D) Turing machine

Answer: - (A)

Exp: - Lexical Analysis is implemented by finite automata

- 8. Let the page fault service time be 10ms in a computer with average memory access time being 20ns. If one page fault is generated for every 10<sup>6</sup> memory accesses, what is the effective access time for the memory?
  - (A) 21ns
- (B) 30ns
- (C) 23ns
- (D)35ns

Answer: - (B)

Exp: - P = page fault rate

 $EA = p \times page fault service time$ 

 $+(1-p)\times Memory$  access time

$$= \frac{1}{10^6} \times 10 \times 10^6 + \left(1 - \frac{1}{10^6}\right) \times 20 \cong 29.9 \, \text{ns}$$

- 9. Consider a hypothetical processor with an instruction of type LW R1, 20(R2), which during execution reads a 32-bit word from memory and stores it in a 32-bit register R1. The effective address of the memory location is obtained by the addition of constant 20 and the contents of register R2. Which of the following best reflects the addressing mode implemented by this instruction for the operand in memory?
  - (A) Immediate Addressing
- (B) Register Addressing
- (C) Register Indirect Scaled Addressing (D) Base Indexed Addressing

Answer: - (D)

Exp: - Here 20 will act as base and content of R<sub>2</sub> will be index

10. What does the following fragment of C-program print?

- (A) GATE2011
- (B) E2011
- (C) 2011
- (D)011

Answer: - (C)

![](_page_3_Picture_3.jpeg)

11. A max-heap is a heap where the value of each parent is greater than or equal to the value of its children. Which of the following is a max-heap?

![](_page_3_Figure_5.jpeg)

![](_page_3_Figure_6.jpeg)

![](_page_3_Figure_7.jpeg)

![](_page_3_Figure_8.jpeg)

Answer: - (B)

Exp: - Heap is a complete binary tree

**FORUM** 

12. An algorithm to find the length of the longest monotonically increasing sequence of numbers in an array A[0:n-1] is given below.

Let  $L_i$  denote the length of the longest monotonically increasing sequence starting at index i in the array

Initialize  $L_{n-1} = 1$ 

For all i such that  $0 \le i \le n-2$ 

$$L_{_{i}} = \begin{cases} 1 + L_{_{i+1}} & \text{if A}\left[i\right] < A\left[i+1\right] \\ 1 & \text{Otherwise} \end{cases}$$

Finally the length of the longest monotonically increasing sequence is  $\text{Max}\left(L_{_{0}},L_{_{1}},...,L_{_{n-1}}\right)$ . Which of the following statements is TRUE?

- (A) The algorithm uses dynamic programming paradigm
- (B) The algorithm has a linear complexity and uses branch and bound paradigm
- (C) The algorithm has a non-linear polynomial complexity and uses branch and bound paradigm
- (D) The algorithm uses divide and conquer paradigm.

Answer: - (A)

13. Let P be a regular language and Q be a context free language such that  $Q \subseteq P$ . (For example, let P be the language represented by the regular expression p\*q\* and Q be  $\{p^nq^n \mid n \in N\}$ ). Then which of the following is ALWAYS regular?

(A) 
$$P \cap Q$$

(B) 
$$P - Q$$

(C) 
$$\Sigma * - P$$

(D) 
$$\Sigma * - Q$$

![](_page_4_Picture_0.jpeg)

**GATE 2011** 

www.gateforum.com

![](_page_4_Picture_3.jpeg)

Answer: - (C)

Exp: -  $\Sigma^*$  - P is the complement of P so it is always regular,

since regular languages are closed under complementation

- 14. In a compiler, keywords of a language are recognized during
  - (A) parsing of the program
- (B) the code generation
- (C) the lexical analysis of the program (D) dataflow analysis

Answer: - (C)

Exp: - Any identifier is also a token so it is recognized in lexical Analysis

- 15. A layer-4 firewall (a device that can look at all protocol headers up to the transport layer) CANNOT
  - (A) block entire HTTP traffic during 9:00PM and 5:00AM
  - (B) block all ICMP traffic
  - (C) stop incoming traffic from a specific IP address but allow outgoing traffic to the same IP address
  - (D) block TCP traffic from a specific user on a multi-user system during 9:00PM and 5:00AM

Answer: - (A)

Exp: - Since it is a layer 4 firewall it cannot block application layer protocol like HTTP.

16. If two fair coins are flipped and at least one of the outcomes is known to be a head, what is the probability that both outcomes are heads?

(A) 1/3

(B) 1/4

(C) 1/2

(D) 2/3

Answer: - (A)

Exp: - Sample space = {HH, HT, TH}

Required probability =  $\frac{1}{3}$ 

17. Consider different activities related to email.

m1: Send an email from a mail client to a mail server

m2: Download an email from mailbox server to a mail client

m3: Checking email in a web browser

Which is the application level protocol used in each activity?

(A) m1:HTTP m2:SMTP m3:POP (B) m1:SMTP m2:FTP m3:HTTP (C) m1: SMTP m2: POP m3: HTTP (D) m1: POP m2: SMTP m3:IMAP

Answer: - (C)

Exp: - Sending an email will be done through user agent and message transfer agent by SMTP, downloading an email from mail box is done through POP, checking email in a web browser is done through HTTP

![](_page_5_Picture_3.jpeg)

18. A company needs to develop a strategy for software product development for which it has a choice of two programming languages L1 and L2. The number of lines of code (LOC) developed using L2 is estimated to be twice the LOC developed with L1. the product will have to be maintained for five years. Various parameters for the company are given in the table below.

| Parameter                        | Language L1   | Language L2  |
|----------------------------------|---------------|--------------|
| Man years needed for development | LOC / 10000   | LOC / 10000  |
| Development Cost per year        | Rs. 10,00,000 | Rs. 7,50,000 |
| Maintenance time                 | 5 years       | 5 years      |
| Cost of maintenance per year     | Rs. 1,00,000  | Rs. 50,000   |

Total cost of the project includes cost of development and maintenance. What is the LOC for L1 for which the cost of the project using L1 is equal to the cost of the project using L2?

(A) 4000

(B) 5000

(C) 4333

(D)4667

Answer: - (B)

Exp: - LOC  $L_1 = X$ 

$$L_2 = 2x$$

Total cost of project

$$\frac{x}{10000} \times 1000000 + 5 \times 100000 = \frac{2x}{10000} \times 750000 + 50000 \times 5$$

$$100x + 500000 = 150x + 250000$$

$$\Rightarrow 50x = 500000 - 250000$$

$$\therefore x = \frac{250000}{50} \Rightarrow x = 5000$$

- 19. Let the time taken to switch between user and kernel modes of execution be  $t_1$  while the time taken to switch between two processes be  $t_2$ . Which of the following is TRUE?
  - (A)  $t_1 > t_2$
  - (B)  $t_1 = t_2$
  - (C)  $t_1 < t_2$
  - (D) Nothing can be said about the relation between t<sub>1</sub> and t<sub>2</sub>

Answer: - (C)

Exp: - Process switching also involves mode changing.

20. A company needs to develop digital signal processing software for one of its newest inventions. The software is expected to have 40000 lines of code. The company needs to determine the effort in person-months needed to develop this software using the basic COCOMO model. The multiplicative factor for this model is given as 2.8 for the software development on embedded systems, while the exponentiation factor is given as 1.20. What is the estimated effort in personmonths?

![](_page_6_Picture_3.jpeg)

(A) 234.25

(B) 932.50

(C) 287.80

(D) 122.40

Answer: - (A)

Exp: - Effort person per month

 $= \alpha.(kDSI)^B$ 

KDSI = Kilo LOC

- $=2.8\times(40)^{1.20}$
- $= 2.8 \times 83.6511$
- = 234.22 person per month
- 21. Which of the following pairs have DIFFERENT expressive power?
  - (A) Deterministic finite automata (DFA) and Non-deterministic finite automata (NFA)
  - (B) Deterministic push down automata (DPDA) and Non-deterministic push down automata (NPDA)
  - (C) Deterministic single-tape Turing machine and Non-deterministic single tape Turing machine
  - (D) Single-tape Turing machine and multi-tape Turing machine

Answer: - (B)

Exp: - NPDA is more powerful than DPDA.

Hence answer is (B)

- 22. HTML (Hyper Text Markup Language) has language elements which permit certain actions other than describing the structure of the web document. Which one of the following actions is NOT supported by pure HTML (without any server or client side scripting) pages?
  - (A) Embed web objects from different sites into the same page
  - (B) Refresh the page automatically after a specified interval
  - (C) Automatically redirect to another page upon download
  - (D) Display the client time as part of the page

Answer: - (D)

- 23. Which of the following is NOT desired in a good Software Requirement Specifications (SRS) document?
  - (A) Functional Requirements
  - (B) Non Functional Requirements
  - (C) Goals of Implementation
  - (D) Algorithms for Software Implementation

Answer: - (D)

24. A computer handles several interrupt sources of which the following are relevant for this question.

Interrupt from CPU temperature sensor

Interrupt from Mouse

![](_page_7_Picture_3.jpeg)

Interrupt from Keyboard

Interrupt from Hard Disk

- (A) Interrupt from Hard Disk
- (B) Interrupt from Mouse
- (C) Interrupt from Keyboard
- (D) Interrupt from CPU temp sensor

Answer: - (D)

- 25. Consider a relational table with a single record for each registered student with the following attributes.
  - 1. Registration\_Number: Unique registration number for each registered student
  - 2. UID: Unique Identity number, unique at the national level for each citizen
  - 3. BankAccount Number: Unique account number at the bank. A student can have multiple accounts or joint accounts. This attributes stores the primary account number
  - 4. Name: Name of the Student
  - 5. Hostel Room: Room number of the hostel

Which of the following options is INCORRECT?

- (A) BankAccount\_Number is a candidate key
- (B) Registration Number can be a primary key
- (C) UID is a candidate key if all students are from the same country
- (D) If S is a superkey such that  $S \cap UID$  is NULL then  $S \cup UID$  is also a superkey

Exp: - In case two students hold joint account then BankAccount\_Num will not uniquely determine other attributes.

# **41** . . i . . . . . . . . . . . . . Q. No. 26 - 51 Carry Two Marks Each

26. Which of the given options provides the increasing order of asymptotic complexityoffunctions  $f_1$ ,  $f_2$ ,  $f_3$  and  $f_4$ ?

$$f_1(n) = 2^n$$
;  $f_2(n) = n^{3/2}$ ;  $f_3(n) = n \log_2 n$ ;  $f_4(n) = n^{\log_2 n}$ 

(A)  $f_3$ ,  $f_2$ ,  $f_4$ ,  $f_1$  (B)  $f_3$ ,  $f_2$ ,  $f_1$ ,  $f_4$ 

(C)  $f_2$ ,  $f_3$ ,  $f_1$ ,  $f_4$  (D)  $f_2$ ,  $f_3$ ,  $f_4$ ,  $f_1$ 

Answer: - (A)

Let n = 1024

$$f_1(n) = 2^{1024}$$

$$f_2(n) = 2^{15}$$

$$f_3(n) = 10 \times 2^{10}$$

$$f_{4}(n) = 1024^{10} = 2^{100}$$

 $f_3$ ,  $f_2$ ,  $f_4$ ,  $f_1$  is the rquired increasing order

![](_page_8_Picture_3.jpeg)

27. Four matrices  $M_1$ ,  $M_2$ ,  $M_3$  and  $M_4$  are dimensions  $p \times q$ ,  $q \times r$ ,  $r \times s$  and  $s \times t$  respectively can be multiplied in several ways with different number of total scalar multiplications. For example When multiplied as  $((M_1 \times M_2) \times (M_3 \times M_4))$  the total number of scalar multiplications is pqr+rst+prt. When multiplied as  $(((M_1 \times M_2) \times M_3) \times M_4)$ , the total number of scalar multiplications is pqr+prs+pst.

If p=10, q=100, r=20, s=5 and t=80, then the minimum number of scalar multiplications needed is

- (A) 248000
- (B) 44000
- (C) 19000
- (D)25000

Answer: - (C)

Exp: - Multiply as 
$$(M_1 \times (M_2 \times M_3)) \times M_4$$

The total number of scalar multiplication is

- = qrs + pqs + pst
- = 10000 + 5000 + 4000 = 19000
- 28. Consider a relational table r with sufficient number of records, having attributes  $A_1$ ,  $A_2$ ,...,  $A_n$  and let  $1 \le p \le n$ . Two queries Q1 and Q2 are given below.

Q1:  $\pi_{A1...A_n} \left( \sigma_{A_p=c} \left( r \right) \right)$  where c is a const

Q2:  $\pi_{A_1...A_n}(\sigma_{c_1 \leq A_n \leq c_n}(r))$  where  $c_1$  and  $c_2$  are constants

The database can be configured to do ordered indexing on  $A_p$  or hashing on  $A_p$ . Which of the following statements is TRUE?

- (A) Ordered indexing will always outperform hashing for both queries
- (B) Hashing will always outperform ordered indexing for both queries
- (C) Hashing will outperform ordered indexing on Q1, but not on Q2
- (D) Hashing will outperform ordered indexing on Q2, but not on Q1.

Answer: - (C)

29. Consider the matrix as given below.

[1 2 3]

0 4 7

0 0 3

Which one of the following provides the CORRECT values of eigenvalues of the matrix?

(A) 1,4,3

(B)3,7,3

(C)7,3,2

(D)1,2,3

Answer: - (A)

Exp: - Given matrix is upper triangular matrix and its diagonal elements are its eigen values = 1, 4, 3

![](_page_9_Picture_3.jpeg)

30. Consider an instruction pipeline with four stages (S1, S2, S3 and S4) each with combinational circuit only. The pipeline registers are required between each stage and at the end of the last stage. Delays for the stages and for the pipeline registers are as given in the figure.

![](_page_9_Figure_5.jpeg)

What is the approximate speed up of the pipeline in steady state under ideal conditions when compared to the corresponding non-pipeline implementation?

- (A)4.0
- (B) 2.5
- (C) 1.1
- (D)3.0

Answer: - (B)

Exp: 
$$-\frac{(5+6+11+8)}{(11+1)} = \frac{30}{12} = 2.5$$

31. Definition of a language L with alphabet  $\{a\}$  is given as following  $L = \{a^{nk} \mid k > 0, \text{ and n is a positive integer constant}\}$ 

What is the minimum number of states needed in a DFA to recognize L?

- (A)k+1
- (B) n+1
- (C)  $2^{n+1}$
- (D)  $2^{k+1}$

Answer: - (B)

Exp: - Let n = 3 and k=1

![](_page_9_Figure_21.jpeg)

(n+1) states

- 32. An 8KB direct mapped write-back cache is organized as multiple blocks, each of size 32-bytes. The processor generates 32-bit addresses. The cache controller maintains the tag information for each cache block comprising of the following.
  - 1 Valid bit
  - 1 Modified bit

As many bits as the minimum needed to identify the memory block mapped in the cache.

What is the total size of memory needed at the cache controller to store metadata (tags) for the cache?

- (A) 4864 bits
- (B) 6144bits
- (C) 6656bits
- (D) 5376bits

Answer: - (D)

![](_page_10_Picture_3.jpeg)

Exp: -

![](_page_10_Figure_5.jpeg)

Required answer =  $256 \times (19 + 2) = 5376$  bits

33. An application loads 100 libraries at startup. Loading each library requires exactly one disk access. The seek time of the disk to a random location is given as 10ms. Rotational speed of disk is 6000rpm. If all 100 libraries are loaded from random locations on the disk, how long does it take to load all libraries? (The time to transfer data from the disk block once the head has been positioned at the start of the block may be neglected)

(A) 0.50s

(B) 1.50s

(C) 1.25s

(D)1.00s

Answer: - (B)

Exp: - 6000 rotations \_\_\_\_\_ 60 sec

1 rotation\_\_\_\_\_10 ms

∴ Rotational latency = 5ms

Time for one disk access = 15 ms

Time to load all libraries =  $15 \times 100 = 1500 \, \text{ms} = 1.5 \, \text{sec}$ 

34. A deterministic finite automation (DFA)D with alphabet  $\Sigma = \{a, b\}$  is given below

![](_page_10_Figure_19.jpeg)

Which of the following finite state machines is a valid minimal DFA which accepts the same language as D?

![](_page_10_Figure_21.jpeg)

![](_page_11_Picture_3.jpeg)

![](_page_11_Picture_4.jpeg)

(D) p b q b

Answer: - (A)

Exp: - Options B and C will accept the string b
Option - D will accept the string "bba"
Both are invalid strings.
So the minimized DFA is option A

35. The following is comment written for a C function

/\* This function computes the roots of a quadratic equation  $a.x^2+b.x+c=0$ . The function stores two real roots in \*root1 and \*root2 and returns the status of validity of roots. It handles four different kinds of cases.

- (i) When coefficient a is zero irrespective of discriminant
- (ii) When discriminant is positive
- (iii) When discrimanant is zero
- (iv) When discrimanant is negative

Only in cases (ii) and (iii), the stored roots are valid.

Otherwise 0 is stored in the roots. the function returns 0 when the roots are valid and -1 otherwise.

The functin also ensures root1>=root2.

int get\_QuadRoots (float a, float b, float c, float \*root1, float \*root2);

\*/

A software test engineer is assigned the job of doing black box testing. He comes up with the following test cases, many of which are redundant.

|           | Input set |       |      | Expected Output set |       |                 |
|-----------|-----------|-------|------|---------------------|-------|-----------------|
| Test Case | а         | b     | С    | Root1               | Root2 | Return<br>Value |
| T1        | 0.0       | 0.0   | 7.0  | 0.0                 | 0.0   | -1              |
| T2        | 0.0       | 1.0   | 3.0  | 0.0                 | 0.0   | -1              |
| Т3        | 1.0       | 2.0   | 1.0  | -1.0                | -1.0  | 0               |
| T4        | 4.0       | -12.0 | 9.0  | 1.5                 | 1.5   | 0               |
| T5        | 1.0       | -2.0  | -3.0 | 3.0                 | -1.0  | 0               |
| Т6        | 1.0       | 1.0   | 4.0  | 0.0                 | 0.0   | -1              |

Which one of the following options provide the set of non-redundant tests using equivalence class partitioning approach from input perspective for black box testing?

(A) T1,T2,T3,T6

(B) T1, T3, T4, T5

(C) T2,T4,T5,T6

(D)T2,T3,T4,T5

Answer: - (C)

![](_page_12_Picture_3.jpeg)

Exp: -  $T_1$  and  $T_2$  checking same condition a = 0 hence, any one of  $T_1$  and  $T_2$  is redundant.

 $T_3$ ,  $T_4$ : in both case discriminant (D)= $b^2 - 4ac = 0$ . Hence any one of it is redundant.

 $T_5: D>0$  $T_6 : D < 0$ 

36. Database table by name Loan\_Records is given below.

| Borrow                                                                            | ver 💮        | Bank_Manager                         | Loan_ Amount      |
|-----------------------------------------------------------------------------------|--------------|--------------------------------------|-------------------|
| Rames                                                                             | sh           | Sunderajan                           | 10000.00          |
| Sures                                                                             | h            | Ramgopal                             | 5000.00           |
| Mahes                                                                             | sh           | Sunderajan                           | 7000.00           |
| What is the outpu<br>SELECT count(*)<br>FROM(<br>(SELECT Borrower<br>NATURAL JOIN |              | owing SQL query?<br>nager FROM Loan_ | Records) AS S     |
| · -                                                                               | anager, Loar | n_Amount FROM L                      | oan_Records) AS T |
| );<br>(A) 3<br>nswer: - (C)                                                       | (B) 9        | (C) 5                                | (D) 6             |

| Borrower | Bank _ Manager | Bank _ Manager | Loan _ Amount |
|----------|----------------|----------------|---------------|
| Ramesh   | Sunderajan     | Sunderajan     | 10000.00      |
| Suresh   | Ramgqpal       | Ramgopal       | 5000.00       |
| Mahesh   | Sunderjan      | Sunderjan      | 7000.00       |

After executing the given query, the output would be

| Borrower | Bank_Manager | Load_Amount |
|----------|--------------|-------------|
| Ramesh   | Sunderajan   | 10000.00    |
| Ramesh   | Sunderajan   | 7000.00     |
| Suresh   | Ramgopal     | 5000.00     |
| Mahesh   | Sunderajan   | 10000.00    |
| Mahesh   | Sunderajan   | 7000.00     |

![](_page_13_Picture_3.jpeg)

37. Consider two binary operators ' $\uparrow$ ' and ' $\downarrow$ ' with the precedence of operator  $\downarrow$  being lower than that of the operator  $\uparrow$ . Operator  $\uparrow$  is right associative while operator  $\downarrow$ , is left associative. Which one of the following represents the parse tree for expression  $(7 \downarrow 3 \uparrow 4 \uparrow 3 \downarrow 2)$ ?

![](_page_13_Figure_5.jpeg)

![](_page_13_Picture_6.jpeg)

![](_page_13_Figure_7.jpeg)

![](_page_13_Figure_8.jpeg)

Answer: - (B) Exp: -  $7 \downarrow 3 \uparrow 4 \uparrow 3 \downarrow 2$ 

- $\Rightarrow$  7 \( \d\ 3 \) \( (4 \) \( 3 \) \( \d\ 2 \) as \( \lambda \) is right associative
- $\Rightarrow$  7 \( \lambda \) (3 \( \hat{1} \) (4 \( \hat{3} \) ) \( \lambda \) 2
- $\Rightarrow$   $(7 \downarrow (3 \uparrow (4 \uparrow 3))) \downarrow 2$  as  $\downarrow$  is left associative
- 38. Consider the languages L1, L2 and L3 as given below

$$L1 = \{0^p1^q \mid p, q \in N\}$$

$$L2 = \{0^p1^q \mid p, q \in N \text{ and } p = q\}$$
 and

L3 = 
$$\{0^p1^q0^r \mid p, q, r \in N \text{ and } p = q = r\}$$

Which of the following statements is NOT TRUE?

- (A) Push Down Automata (PDA) can be used to recognize L1 and L2
- (B) L1 is a regular language
- (C) All the three languages are context free
- (D) Turing machines can be used to recognize all the languages

![](_page_14_Picture_3.jpeg)

Answer: - (C)

Exp: - L1: regular language

L2: context free language

L3: context sensitive language

39. On a non-pipelined sequential processor, a program segment, which is a part of the interrupt service routine, is given to transfer 500 bytes from an I/O device to memory.

Initialize the address register

Initialize the count to 500

LOOP: Load a byte from device

Store in memory at address given by address register

Increment the address register

Decrement the count

If count != 0 go to LOOP

Assume that each statement in this program is equivalent to a machine instruction which takes one clock cycle to execute if it is a non-load/store instruction. The load-store instructions take two clock cycles to execute.

The designer of the system also has an alternate approach of using the DMA controller to implement the same transfer. The DMA controller requires 20 clock cycles for initialization and other overheads. Each DMA transfer cycle takes two clock cycles to transfer one byte of data from the device to the memory.

What is the approximate speedup when the DMA controller based design is used in place of the interrupt driven program based input-output?

Answer: - (A)

Exp: - No. of clock cycles required by using load-store approach =  $2 + 500 \times 7 = 3502$  and that of by using DMA =  $20 + 500 \times 2 = 1020$ 

Required speed up = 
$$\frac{3502}{1020}$$
 = 3.4

- 40. We are given a set of n distinct elements and an unlabeled binary tree with n nodes. In how many ways can we populate the tree with the given set so that it becomes a binary search tree?
  - (A)0
- (B) 1
- (C) n!
- (D)  $\frac{1}{n+1}$ .  ${}^{2n}C_n$

Answer: - (D)

41. Which one of the following options is CORRECT given three positive integers x, y and z, and a predicate

$$P(x) = \neg(x = 1) \land \forall y (\exists z (x = y * z) \Rightarrow (y = x) \lor (y = 1))$$

(A) P(x) being true means that x is a prime number

![](_page_15_Picture_3.jpeg)

- (B) P(x) being true means that x is a number other than 1
- (C) P(x) is always true irrespective of the value of x
- (D)P(x) being true means that x has exactly two factors other than 1 and x

Answer: - (A)

42. Given  $i = \sqrt{-1}$ , what will be the evaluation of the definite integral  $\int\limits_0^{\pi/2} \frac{\cos x + i \sin x}{\cos x - i \sin x} dx ?$ 

(A)0

(B) 2

(C) -i

(D)i

Answer: - (D)

Exp:  $-\int_0^{\pi/2} \frac{e^{ix}}{e^{-ix}} dx = \int_0^{\pi/2} e^{2ix} dx$ 

 $= \left(\frac{e^{2ix}}{2i}\right)_0^{\pi/2} = \frac{1}{2i}\left[e^{i\pi} - 1\right] = \frac{1}{2i}\left[\cos\pi + i\sin\pi - 1\right] = \frac{1}{2i}\left[-1 + 0 - 1\right] = \frac{-2}{2i} = \frac{-1}{i} \times \frac{i}{i} = \frac{-i}{-1} = i$ 

43. Consider a database table T containing two columns X and Y each of type integer. After the creation of the table, one record (X = 1, Y = I) is inserted in the table.

Let MX and MY denote the respective maximum values of X and Y among all records in the table at any point in time. Using MX and MY, new records are inserted in the table 128 times with X and Y values being MX+1, 2\*MY+1 respectively. It may be noted that each time after the insertion, values of MX and MY change.

What will be the output of the following SQL query after the steps mentioned above are carried out?

SELECT Y FROM T WHERE X=7;

(A) 127

(B) 255

(C) 129

(D) 257

Answer: - (A)

Exp: -

| Х | Y   |
|---|-----|
| 1 | 1   |
| 2 | 3   |
| 3 | 7   |
| 4 | 15  |
| 5 | 31  |
| 6 | 63  |
| 7 | 127 |

![](_page_16_Picture_0.jpeg)

**GATE 2011** 

![](_page_16_Picture_3.jpeg)

- 44. Consider a finite sequence of random values  $X = [x_1, x_2, ... x_n]$ . Let  $\mu_x$  be the mean and  $\sigma_x$  be the standard deviation of X. Let another finite sequence Y of equal length be derived from this as  $y_i = a * x_i + b$ , where a and b are positive constants. Let  $\mu_y$  be the mean and  $\sigma_y$  be the standard deviation of this sequence. Which one of the following statements is INCORRECT?
  - (A) Index position of mode of X in X is the same as the index position of mode of Y in Y.
  - (B) Index position of median of X in X is the same as the index position of median of Y in Y.

(C) 
$$\mu_{v} = a\mu_{x} + b$$

(D) 
$$\sigma_v = a\sigma_v + b$$

Answer: - (D)

- 45. A deck of 5 cards (each carrying a distinct number from 1 to 5) is shuffled thoroughly. Two cards are then removed one at a time from the deck. What is the probability that the two cards are selected with the number on the first card being one higher than the number on the second card?
  - (A) 1/5
- (B) 4/25
- (C) 1/4
- (D)2/5

Answer: - (A)

Exp: - (2,1), (3,2), (4,3), (5,4)

Required probability = 
$$\frac{4}{5 \times 4} = \frac{4}{20} = \frac{1}{5}$$

Success

46. Consider the following table of arrival time and burst time for three processes P0, P1 and P2.

| Process | <b>Arrival time</b> | <b>Burst Time</b> |
|---------|---------------------|-------------------|
| P0      | 0 ms                | 9 ms              |
| P1      | 1 ms                | 4ms               |
| P2      | 2 ms                | 9ms               |

The pre-emptive shortest job first scheduling algorithm is used. Scheduling is carried out only at arrival or completion of processes. What is the average waiting time for the three processes?

- (A) 5.0 ms
- (B) 4.33 ms
- (C) 6.33 ms
- (D) 7.33 ms

Answer: - (A)

![](_page_17_Picture_3.jpeg)

Exp: -

|   | $P_0$ | P <sub>1</sub> | P <sub>0</sub> |    | P <sub>2</sub> |    |
|---|-------|----------------|----------------|----|----------------|----|
| 0 | 1     |                | 5              | 13 |                | 22 |

Average waiting time =  $\frac{4+11}{3}$  = 5 ms

47. Consider evaluating the following expression tree on a machine with load-store architecture in which memory can be accessed only through load and store instructions. The variables a, b, c, d and e are initially stored in memory. The binary operators used in this expression tree can be evaluated by the machine only when the operands are in registers. The instructions produce result only in a register. If no intermediate results can be stored in memory, what is the minimum number of registers needed to evaluate this expression?

![](_page_17_Figure_8.jpeg)

(A)2

(B) 9

(C) 5

(D)3

Exp: - Load  $R_1$ , a;  $R_1 \leftarrow M[a]$ 

Load 
$$R_2$$
, b;  $R_2 \leftarrow M[b]$ 

Sub 
$$R_1, R_2$$
;  $R_1 \leftarrow R_1 - R_2$ 

$$Load R_2, c ; R_2 \leftarrow M[c]$$

Load 
$$R_3$$
, d;  $R_3 \leftarrow M[d]$ 

Add 
$$R_2$$
,  $R_3$ ;  $R_2 \leftarrow R_2 + R_3$ 

Load 
$$R_3$$
, e;  $R_3 \leftarrow M[e]$ 

Sub 
$$R_3$$
,  $R_2$ :  $R_3 \leftarrow R_3 - R_2$ 

Add 
$$R_1,R_3$$
 ;  $R_1 \leftarrow R_1 + R_3$ 

Total 3 Registers are required minimum

### Common Data Questions: 48 & 49

Consider the following recursive C function that takes two arguments

```
unsigned int foo(unsigned int n, unsigned int r) { if (n > 0) return (n\%r) + foo(n/r, r)); else return 0; }
```

- 48. What is the return value of the function foo when it is called as foo (513, 2)?
  - (A)9
- (B)8
- (C)5
- (D)2

Answer: - (D)

![](_page_18_Figure_13.jpeg)

- What is the return value of the function foo when it is called as foo (345, 10)?
  - (A) 345
- (B) 12
- (C) 5
- (D) 3

Answer: - (B)

![](_page_18_Figure_20.jpeg)

![](_page_19_Picture_3.jpeg)

## Common Data Questions: 50 & 51

Consider the following circuit involving three D-type flip-flops used in a certain type of counter configuration.

![](_page_19_Picture_6.jpeg)

50. If all the flip-flops were reset to 0 at power on, what is the total number of distinct outputs (states) represented by PQR generated by the counter?

(A) 3
Answer: - (B)
Exp: 
(B) 4

(C) 5

(D) 6

Engineering Success

| CLOCK | Inputs    |                            |                        | Outputs |   |   |
|-------|-----------|----------------------------|------------------------|---------|---|---|
|       | $D_1 = R$ | $D_2 = \overline{(P + R)}$ | $D_3 = Q \overline{R}$ | Р       | Q | R |
| 1     | 0         | 1                          | 0                      | 0       | 1 | 0 |
| 2     | 0         | 1                          | 1                      | 0       | 1 | 1 |
| 3     | 1         | 0                          | 0                      | 1       | 0 | 0 |
| 4     | 0         | 0                          | 0                      | 0       | 0 | 0 |

So Total number of distinct outputs is 4

51. If at some instance prior to the occurrence of the clock edge, P. Q and R have a value 0, 1 and 0 respectively, what shall be the value of PQR after the clock edge?

(A)000

(B) 001

(C) 010

(D)011

![](_page_20_Picture_3.jpeg)

Answer: - (D)

Exp: -From the Table Shown in the explanation of question 50, if first state is 010 next State is 011

### Linked Answer Questions: Q.52 to Q.55 Carry Two Marks Each

#### Statement for Linked Answer Questions: 52 & 53

An undirected graph G(V,E) contains n(n > 2) nodes named  $v_1, v_2, .... v_n$ . Two nodes  $v_i$ ,  $v_j$  are connected if and only if  $0 < |i - j| \le 2$ . Each edge  $(v_i, v_j)$  is assigned a weight i + j. A sample graph with n = 4 is shown below

![](_page_20_Figure_9.jpeg)

52. What will be the cost of the minimum spanning tree (MST) of such a graph with n nodes?

(A) 
$$\frac{1}{12} (11n^2 - 5n)$$

(B) 
$$n^2 - n + 1$$

(C) 
$$6n - 11$$

Answer: - (B)

- 53. The length of the path from  $v_5$  to  $v_6$  in the MST of previous question with n = 10
  - (A) 11
- (B) 25
- (C) 31
- (D)41

Answer: - (C)

![](_page_20_Figure_22.jpeg)

$$12 + 8 + 4 + 3 + 6 + 10 = 31$$

![](_page_21_Picture_3.jpeg)

## **Statement for Linked Answer Questions: 54 & 55**

Consider a network with five nodes, N1 to N5, as shown below

![](_page_21_Figure_6.jpeg)

The net work uses a Distance Vector Routing protocol. Once the routes have stabilized, the distance vectors at different nodes are as following

N1:(0,1,7,8,4)

N2:(1,0,6,7,3)

N3:(7,6,0,2,6)

N4:(8,7,2,0,4)

N5:(4,3,6,4,0)

Each distance vector is the distance of the best known path at that instance to nodes, N1 to N5, where the distance to itself is 0. Also, all links are symmetric and the cost is identical in both directions. In each round, all nodes exchange their distance vectors with their respective neighbors. Then all nodes update their distance vectors. In between two rounds, any change in cost of a link will cause the two incident nodes to change only that entry in their distance vectors

54. The cost of link N2-N3 reduces to 2 in (both directions). After the next round of updates, what will be the new distance vector at node, N3?

Answer: - (A)

Exp: -

$$\begin{array}{c|c} N_3 \\ N_1 & 3 \\ N_2 & 2 \\ N_3 & 0 \\ N_4 & 2 \\ N_5 & 5 & \rightarrow 2+3 \end{array}$$

- 55. After the update in the previous question, the link N1-N2 goes down. N2 will reflect this change immediately in its distance vector as cost,  $\infty$ . After the NEXT ROUND of update, what will be the cost to N1 in the distance vector of N3?
  - (A)3
- (B)
- (C) 10
- (D)∞

![](_page_22_Picture_3.jpeg)

Answer: - (C)

Exp: - N<sub>3</sub> has neighbors N<sub>2</sub> and N<sub>4</sub>

 $N_2$  has made entry  $\infty$ 

N<sub>4</sub> has the distance of 8 to N<sub>1</sub>

N<sub>3</sub> has the distance of 2 to N<sub>4</sub>

So 2 + 8 = 10

### Q. No. 56 - 60 Carry One Mark Each

56. If Log (P) = (1/2)Log (Q) = (1/3) Log (R), then which of the following options is TRUE?

(A)  $P^2 = Q^3R^2$  (B)  $Q^2 = PR$  (C)  $Q^2 = R^3P$  (D)  $R = P^2Q^2$ 

Answer: - (B)

Exp:-  $\log P = \frac{1}{2} \log Q = \frac{1}{3} \log (R) = k$ 

 $\therefore P = b^k, Q = b^{2k}, R = b^{3k}$ 

Now,  $Q^2 = b^{4k} = b^{3k} b^k = PR$ 

57. Choose the most appropriate word(s) from the options given below to complete the following sentence.

I contemplated\_\_\_\_\_Singapore for my vacation but decided against

(A) To visit

(B) having to visit (C) visiting

(D)for a visit

Answer: - (C)

Exp: - Contemplate is a transitive verb and hence is followed by a gerund Hence the correct usage of contemplate is verb+ ing form.

58. Choose the most appropriate word from the options given below to complete the following sentence.

If you are trying to make a strong impression on your audience, you cannot do so by being understated, tentative or

(A) Hyperbolic

(B) Restrained

(C) Argumentative

(D) Indifferent

Answer: - (B)

Exp: - The tone of the sentence clearly indicates a word that is similar to understated is needed for the blank. Alternatively, the word should be antonym of strong (fail to make strong impression). Therefore, the best choice is restrained which means controlled/reserved/timid.

59. Choose the word from the options given below that is most nearly opposite in meaning to the given word: Amalgamate

(A) Merge

(B) Split

(C) Collect

(D) Separate

Answer: - (B)

![](_page_23_Picture_3.jpeg)

- Exp: Amalgamate means combine or unite to form one organization or structure. So the best option here is split. Separate on the other hand, although a close synonym, it is too general to be the best antonym in the given question while Merge is the synonym; Collect is not related.
- 60. Which of the following options is the closest in the meaning to the word below:

### **Inexplicable**

(A) Incomprehensible

(B) Indelible

(C) Inextricable

(D) Infallible

Answer: - (A)

Exp: - Inexplicable means not explicable; that cannot be explained, understood, or accounted for. So the best synonym here is incomprehensible.

#### Q. No. 61 - 65 Carry Two Marks Each

61. P, Q, R and S are four types of dangerous microbes recently found in a human habitat. The area of each circle with its diameter printed in brackets represents the growth of a single microbe surviving human immunity system within 24 hours of entering the body. The danger to human beings varies proportionately with the toxicity, potency and growth attributed to a microbe shown in the figure below

![](_page_23_Figure_15.jpeg)

(Probability that microbe will overcome human immunity system)

A pharmaceutical company is contemplating the development of a vaccine against the most dangerous microbe. Which microbe should the company target in its first attempt?

(A) P

(B) Q

(C) R

(D)S

Answer: - (D)

Exp: - By observation of the table, we can say S

|             | Р   | Q   | R   | S   |
|-------------|-----|-----|-----|-----|
| Requirement | 800 | 600 | 300 | 200 |
| Potency     | 0.4 | 0.5 | 0.4 | 0.8 |

- 62. The variable cost (V) of manufacturing a product varies according to the equation V= 4q, where q is the quantity produced. The fixed cost (F) of production of same product reduces with q according to the equation F = 100/q. How many units should be produced to minimize the total cost (V+F)?
  - (A) 5
- (B) 4
- (C) 7

(D)6

Answer: (A)

Exp: - Checking with all options in formula: (4q+100/q) i.e. (V+F). Option A gives the minimum cost.

63. A transporter receives the same number of orders each day. Currently, he has some pending orders (backlog) to be shipped. If he uses 7 trucks, then at the end of the 4th day he can clear all the orders. Alternatively, if he uses only 3 trucks, then all the orders are cleared at the end of the 10th day. What is the minimum number of trucks required so that there will be no pending order at the end of the 5th day?

(A) 4

(C)6 | | (D)7

Answer: - (C)

Exp: - Let each truck carry 100 units.

$$2800 = 4n + e$$
  $n = normal$ 

$$3000 = 10n + e$$

3000 = 10n + e e = excess/pending

$$\therefore n = \frac{100}{3}, e = \frac{8000}{3}$$

$$5 days \Rightarrow 500x = \frac{5.100}{3} + \frac{8000}{3}$$

$$\Rightarrow 500x = \frac{8500}{3}17 \Rightarrow x > 5$$

#### Minimum possible = 6

- 64. A container originally contains 10 litres of pure spirit. From this container 1 litre of spirit is replaced with 1 litre of water. Subsequently, 1 litre of the mixture is again replaced with 1 litre of water and this process is repeated one more time. How much spirit is now left in the container?
  - (A) 7.58 litres
- (B) 7.84 litres
- (C) 7 litres
- (D) 7.29 litres

![](_page_25_Picture_0.jpeg)

Answer: - (D)

Exp:- 
$$10\left(\frac{10-1}{10}\right)^3 = 10\left(\frac{9}{10}\right)^3 = \frac{729}{1000}$$
  
 $\therefore \frac{729}{1000} \times 1 = 7.29 \text{ litres}$ 

65. Few school curricula include a unit on how to deal with bereavement and grief, and yet all students at some point in their lives suffer from losses through death and parting.

Based on the above passage which topic would not be included in a unit on bereavement?

- (A) how to write a letter of condolence
- (B) what emotional stages are passed through in the healing process
- (C) what the leading causes of death are
- (D) how to give support to a grieving friend

Answer: - (C)

Exp: - The given passage clearly deals with how to deal with bereavement and grief and so after the tragedy occurs and not about precautions. Therefore, irrespective of the causes of death, a school student rarely gets into details of causes—which is beyond the scope of the context. Rest all are important in dealing with grief.

![](_page_25_Picture_13.jpeg)