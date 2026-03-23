![](_page_0_Picture_1.jpeg)

# Q. No. 1 – 25 Carry One Mark Each

| 1.    | Which of the following problems are decidable?  1) Does a given program ever produce an output? |                                                          |                                                   |                                             |  |  |  |
|-------|-------------------------------------------------------------------------------------------------|----------------------------------------------------------|---------------------------------------------------|---------------------------------------------|--|--|--|
|       |                                                                                                 | -                                                        | _ ^                                               |                                             |  |  |  |
|       | 2) If L is context-free language, then, is $\overline{L}$ also context-free?                    |                                                          |                                                   |                                             |  |  |  |
|       | 3) If L is regular la                                                                           | anguage, then, is $\overline{L}$                         | also regular?                                     |                                             |  |  |  |
|       | 4) If L is recursive language, then, is $\overline{L}$ also recursive?                          |                                                          |                                                   |                                             |  |  |  |
|       | (A) 1,2,3,4                                                                                     | (B) 1,2                                                  | (C) 2,3,4                                         | (D) 3,4                                     |  |  |  |
| Answe | er:- (D)                                                                                        |                                                          |                                                   |                                             |  |  |  |
| Exp:- | CFL's are not closunder complementa                                                             |                                                          | entation. Regular and                             | l recursive languages are closed            |  |  |  |
| 2.    | Given the language                                                                              | e L-{ab, aa, baa}, wh                                    | ich of the following s                            | trings are in L*?                           |  |  |  |
|       | 1) abaabaaabaa                                                                                  |                                                          |                                                   |                                             |  |  |  |
|       | 2) aaaabaaaa                                                                                    |                                                          |                                                   |                                             |  |  |  |
|       | 3) baaaaabaaaab                                                                                 |                                                          |                                                   |                                             |  |  |  |
|       | 4) baaaaabaa                                                                                    |                                                          |                                                   |                                             |  |  |  |
|       | (A) 1,2 and 3                                                                                   | (B) 2,3 and 4                                            | (C) 1,2 and 4                                     | (D) 1,3 and 4                               |  |  |  |
| Answe | er:-(C)                                                                                         |                                                          |                                                   |                                             |  |  |  |
| Exp:- | $L = \{ab, aa, baa\}$                                                                           | Engin                                                    | ooring                                            | Success                                     |  |  |  |
|       | Let S1 = ab, S2 = aa and S3 =baa INCESS                                                         |                                                          |                                                   |                                             |  |  |  |
|       | abaabaaabaa can be                                                                              | e written as S1S2S3S                                     | S1S2                                              |                                             |  |  |  |
|       | aaaabaaaa can be w                                                                              | written as S1S1S3S1                                      |                                                   |                                             |  |  |  |
|       | baaaaabaa can be w                                                                              | vritten as S3S2S1S2                                      |                                                   |                                             |  |  |  |
| 3.    | In the IPv4 address                                                                             | sing format, the num                                     | per of networks allow                             | ed under Class C addresses is               |  |  |  |
|       | (A) $2^{14}$                                                                                    | (B) $2^7$                                                | (C) $2^{21}$                                      | (B) $2^{24}$                                |  |  |  |
| Answe | er:-(C)                                                                                         |                                                          |                                                   |                                             |  |  |  |
| Exp:- |                                                                                                 | s, size of network fit works possible is 2 <sup>21</sup> |                                                   | est 3 bits are fixed as 110; hence          |  |  |  |
| 4.    | Which of the follow                                                                             | wing transport layer                                     | protocols is used to su                           | apport electronic mail?                     |  |  |  |
|       | (A) SMTP                                                                                        | (B) IP                                                   | (C) TCP                                           | (D) UDP                                     |  |  |  |
| Answe | er:-(C)                                                                                         |                                                          |                                                   |                                             |  |  |  |
| Exp:- | E-mail uses SMTP                                                                                | , application layer pr                                   | otocol which intern u                             | ses TCP transport layer protocol.           |  |  |  |
| 5.    |                                                                                                 |                                                          | tes values + 1 and -1 artion $F(x)$ at $x = -1$ a | 1 with probability 0.5 each. The and +1 are |  |  |  |
|       | (A) 0 and 0.5                                                                                   |                                                          | (B) 0 and 1                                       |                                             |  |  |  |

(C) 0.5 and 1

(D) 0.25 and 0.75

Answer:-(C)

Exp:- The cumulative distribution function

$$F(x) = P(X \le x)$$

$$F(-1) = P(X \le -1) = P(X = -1) = 0.5$$

$$F(+1) = P(X \le +1) = P(X = -1) + P(X = +1) = 0.5 + 0.5 = 1$$

- 6. Register renaming is done is pipelined processors
  - (A) as an alternative to register allocation at compile time
  - (B) for efficient access to function parameters and local variables
  - (C) to handle certain kinds of hazards
  - (D) as part of address translation

Answer:-(C)

Exp:- Register renaming is done to eliminate WAR/WAW hazards.

- 7. The amount of ROM needed to implement a 4 bit multiplier is
  - (A) 64 bits
- (B) 128 bits
- (C) 1 Kbits
- (D) 2 Kbits

Answer:-(D)

Exp:- For a 4 bit multiplier there are  $2^4 \times 2^4 = 2^8 = 256$  combinations.

Output will contain 8 bits.

So the amount of ROM needed is  $2^8 \times 8$  bits = 2 Kbits.

8. Let W(n) and A(n) denote respectively, the worst case and average case running time of an algorithm executed on an input of size n. Which of the following is **ALWAYS TRUE**?

(A) 
$$A(n) = \Omega(W(n))$$

(B) 
$$A(n) = \Theta(W(n))$$

(C) 
$$A(n) = O(W(n))$$

(D) 
$$A(n) = o(W(n))$$

Answer:-(C)

Exp:- The average case time can be lesser than or even equal to the worst case. So A(n) would be upper bounded by W(n) and it will not be strict upper bound as it can even be same (e.g. Bubble Sort and merge sort).

$$A(n) = O(W(n))$$

- 9. Let G be a simple undirected planar graph on 10 vertices with 15edges. If G is a connected graph, then the number of **bounded** faces in any embedding of G on the plane is equal to
  - (A) 3
- (B) 4
- (C) 5

(D) 6

Answer:-(D)

Exp:- We have the relation V-E+F=2, by this we will get the total number of faces,

F = 7. Out of 7 faces one is an unbounded face, so total 6 bounded faces.

10. The recurrence relation capturing the optimal execution time of the *Towers of Hanoi* problem with n discs is

(A) 
$$T(n) = 2T(n-2) + 2$$

(B) 
$$T(n) = 2T(n-1) + n$$

(C) 
$$T(n) = 2T(n/2) + 1$$

(D) 
$$T(n) = 2T(n-1)+1$$

Answer:-(D)

Exp:- Let the three pegs be A,B and C, the goal is to move n pegs from A to C using peg B

The following sequence of steps are executed recursively

1.move n-1 discs from A to B. This leaves disc n alone on peg A --- T(n-1)

2.move disc n from A to C-----1

3.move n-1 discs from B to C so they sit on disc n---- T(n-1)

So, T(n) = 2T(n-1) + 1

- 11. Which of the following statements are **TRUE** about an SQL query?
  - P: An SQL query can contain a HAVING clause even if it does not have a GROUP BY clause
  - Q: An SQL query can contain a HAVING clause only if it has GROUP BY clause
  - R: All attributes used in the GROUP BY clause must appear in the SELECT clause
  - S: Not all attributes used in the GROUP BY clause need to appear in the SELECT clause
  - (A) P and R
- (B) P and S
- (C) Q and R
- (D) Q and S

Answer:-(B)

Exp:- If we use a HAVING clause without a GROUP BY clause, the HAVING condition applies to all rows that satisfy the search condition. In other words, all rows that satisfy the search condition make up a single group. So, option P is true and Q is false.

S is also true as an example consider the following table and query.

| Id | Name   |
|----|--------|
| 1  | Ramesh |
| 2  | Ramesh |
| 3  | Rajesh |
| 4  | Suresh |

Select count (\*)

From student

Group by Name

Output will be

| Count (*) |  |
|-----------|--|
| 2         |  |
| 1         |  |

![](_page_3_Picture_1.jpeg)

1

- 12. Given the basic ER and relational models, which of the following is **INCORRECT**?
  - (A) An attribute of an entity can have more than one value
  - (B) An attribute of an entity can be composite
  - (C) In a row of a relational table, an attribute can have more than one value
  - (D) In a row of a relational table, an attribute can have exactly one value or a NULL value

Answer:-(C)

Exp:- The term 'entity' belongs to ER model and the term 'relational table' belongs to relational model.

Options A and B both are true since ER model supports both multivalued and composite attributes.

As multivalued attributes are not allowed in relational databases, in a row of a relational (table), an attribute cannot have more than one value.

13. What is the complement of the language accepted by the NFA show below? Assume  $\Sigma = \{a\}$  and  $\varepsilon$  is the empty string.

![](_page_3_Figure_13.jpeg)

Exp:- Language accepted by NFA is  $a^+$ , so complement of this language is  $\{\epsilon\}$ 

- 14. What is the correct translation of the following statement into mathematical logic? "Some real numbers are rational"
  - (A)  $\exists x (real(x) v rational(x))$
- (B)  $\forall x (real(x) \rightarrow rational(x))$
- (C)  $\exists x (real(x) \land rational(x))$
- (D)  $\exists x (rational(x) \rightarrow real(x))$

Answer:- (C)

Exp:- Option A: There exists x which is either real or rational and can be both.

Option B: All real numbers are rational

Option C: There exists a real number which is rational.

Option D: There exists some number which is not rational or which is real.

- 15. Let A be the 2 x 2 matrix with elements  $a_{11} = a_{12} = a_{21} = +1$  and  $a_{22} = -1$ . Then the eigen values of the matrix  $A^{19}$  are
  - (A) 1024 and -1024

(B)  $1024\sqrt{2}$  and  $-1024\sqrt{2}$ 

![](_page_4_Picture_1.jpeg)

(C) 
$$4\sqrt{2}$$
 and  $-4\sqrt{2}$ 

(D) 
$$512\sqrt{2}$$
 and  $-512\sqrt{2}$ 

Answer:-(D)

Exp:- Characteristic equation of A is  $|A - \lambda I| = 0$  where  $\lambda$  is the eigen value

$$\begin{vmatrix} 1 - \lambda & 1 \\ 1 & -1 - \lambda \end{vmatrix} = 0 \Rightarrow \lambda^2 - 2 = 0 \Rightarrow \lambda^2 = \pm \sqrt{2}$$

Every matrix satisfies its characteristic equation

Therefore 
$$A^2 - 2I = 0 \Rightarrow A^2 = 2I$$

$$A^{19} = A^{18} \times A = (A^2)^9 \times A = (2I)^9 \times A = 512 \times A$$

Hence eigen values of  $A^{19}$  are  $\pm 512\sqrt{2}$ 

- 16. The protocol data unit (PDU) for the application layer in the Internet stack is
  - (A) Segment
- (B) Datagram
- (C) Message
- (D) Frame

Answer:-(C)

Exp:- The PDU for Datalink layer, Network layer, Transport layer and Application layer are frame, datagram, segment and message respectively.

- 17. Consider the function  $f(x) = \sin(x)$  in the interval  $x \in [\pi/4, 7\pi/4]$ . The number and location (s) of the local minima of this function are
  - (A) One, at  $\pi/2$

- (B) One, at  $3\pi/2$
- (C) Two, at  $\pi/2$  and  $3\pi/2$
- (D) Two, at  $\pi/4$  and  $3\pi/2$

Answer:-(B)

Exp:- Sin x has a maximum value of 1 at  $\frac{\pi}{2}$ , and a minimum value of -1 at  $\frac{3\pi}{2}$  and at all angles conterminal with them.

The graph of  $f(x) = \sin x$  is

![](_page_4_Figure_26.jpeg)

 $\therefore$  In the interval  $\left[\frac{\pi}{4}, \frac{7\pi}{4}\right]$ , it has one local minimum at  $x = \frac{3\pi}{2}$ 

- 18. A process executes the code
  - fork();
  - fork();
  - fork();

The total number of **child** processes created is

- (A)3
- (B) 4
- (C) 7

(D) 8

Answer:- (C)

![](_page_5_Picture_1.jpeg)

Exp:- If fork is called n times, there will be total 2<sup>n</sup> running processes including the parent process. So, there will be 2<sup>n</sup>-1 child processes.

- 19. The decimal value 0.5 in IEEE single precision floating point representation has
  - (A) fraction bits of 000...000 and exponent value of 0
  - (B) fraction bits of 000...000 and exponent value of -1
  - (C) fraction bits of 100...000 and exponent value of 0
  - (D) no exact representation

Answer:-(B)

Exp:- 
$$(0.5)_{10} = (1.0)_2 \times 2^{-1}$$

So, exponent = -1 and fraction is 000 - - -000

20. The truth table

|       | X          | Y          | f(X,Y)      |
|-------|------------|------------|-------------|
|       | 0          | 0          | 0           |
|       | 0          | 1          | 0           |
|       | 1          | 0          | 1           |
|       | 1          | 1          | 1           |
|       | represents | the Boolea | an function |
|       | (A) X      |            | (B) X +     |
| Answe | r:- (A)    |            |             |
| Ехр:- | XY'+XY     | = X(Y'+Y)  | Y) = X      |

- 21. The worst case running time to search for an element in a balanced binary search tree with
  - (A)  $\Theta(n \log n)$

 $n2^n$  elements is

- (B)  $\Theta(n2^n)$  (C)  $\Theta(n)$
- (D)  $\Theta(\log n)$

Answer:-(C)

Exp:- The worst case search time in a balanced BST on 'x' nodes is logx. So, if  $x = n2^n$ , then  $\log(n2^n) = \log n + \log(2^n) = \log n + n = \theta(n)$ 

- 22. Assuming  $P \neq NP$ , which of the following is **TRUE**?
  - (A) NP-complete = NP

(B) NP-complete  $\cap P = \emptyset$ 

(C) NP-hard = NP

(D) P = NP-complete

Answer:-(B)

If P!=NP, then it implies that no NP-Complete problem can be solved in polynomialtime which implies that the set P and the set NPC are disjoint.

![](_page_6_Picture_1.jpeg)

23. What will be the output of the following C program segment?

```
Char inChar = 'A';

switch (inChar) {

case 'A': printf ("Choice A\n");

case 'B':

case 'C': print f("Choice B");

case 'D':

case 'E':

default: printf ("No Choice"); }
```

- (A) No choice
- (B) Choice A
- (C) Choice A

Choice B No choice

(D) Program gives no output as it is erroneous

# Answer:-(C)

Exp:- Since there is no 'break' statement, the program executes all the subsequent case statements after printing "choice A"

- 24. Which of the following is **TRUE?** 
  - (A) Every relation is 3NF is also in BCNF
  - (B) A relation R is in 3NF if every non-prime attribute of R is fully functionally dependent on every key of R
  - (C) Every relation in BCNF is also in 3NF
  - (D) No relation can be in both BCNF and 3NF

### Answer:-(C)

Exp:- Option A is false since BCNF is stricter than 3NF (it needs LHS of all FDs should be candidate key for 3NF condition)

Option B is false since the definition given here is of 2NF

Option C is true, since for a relation to be in BCNF it needs to be in 3NF, every relation in BCNF satisfies all the properties of 3NF.

Option D is false, since if a relation is in BCNF it will always be in 3NF.

- 25. Consider the following logical inferences.
  - $I_1$ : If it rains then the cricket match will not be played.

The cricket match was played.

**Inference:** There was no rain.

 $I_2$ : If it rains then the cricket match will not be played.

It did not rain.

**Inference:** The cricket match was played.

![](_page_7_Picture_1.jpeg)

Which of the following is **TRUE**?

- (A) Both I<sub>1</sub> and I<sub>2</sub> are correct inferences
- (B) I<sub>1</sub> is correct but I<sub>2</sub> is not a correct inference
- (C)  $I_1$  is not correct but  $I_2$  is a correct inference
- (D) Both I<sub>1</sub> and I<sub>2</sub> are not correct inferences

Answer:- (B)

Exp:-

$$I_{1}: \qquad R \rightarrow \sim C \approx \sim RV \sim C$$

$$C$$

$$-----$$

$$\sim R \qquad \text{(there was no rain)}$$

$$I_2: \qquad R \rightarrow \sim C \qquad \approx \sim Rv \sim C$$
 
$$\sim R \qquad \qquad \sim R$$
 
$$\sim RvC$$

(I<sub>1</sub> is correct and I<sub>2</sub> is not correct inference)

# Q. No. 26 – 51 Carry Two Marks Each

26. Consider the set of strings on {0,1} in which, every substring of 3 symbols has at most two zeros. For example, 001110 and 011001 are in the language, but 100010 is not. All strings of length less than 3 are also in the language. A partially completed DFA that accepts this language is shown below.

![](_page_7_Figure_14.jpeg)

![](_page_8_Picture_1.jpeg)

The missing arcs in the DFA are

(A)

| (B)       | 00 | 01 | 10 | 11 | q |
|-----------|----|----|----|----|---|
| (B)<br>00 | 1  | 0  |    |    |   |
| 01        |    |    |    | 1  |   |
| 10        | 0  |    |    |    |   |
| 11        |    |    | 0  |    |   |

|    | 00 | 01 | 10 | 11 | q |
|----|----|----|----|----|---|
| 00 |    | 0  |    |    | 1 |
| 01 |    | 1  |    |    |   |
| 10 |    |    |    | 0  |   |
| 11 |    | 0  |    |    |   |

(C)

|    | 00 | 01 | 10 | 11 | q |
|----|----|----|----|----|---|
| 00 |    | 1  |    |    | 0 |
| 01 |    | 1  |    |    |   |
| 10 |    |    | 0  |    |   |
| 11 |    | 0  |    |    |   |

(D)

|    | 00 | 01 | 10 | 11 | q |
|----|----|----|----|----|---|
| 00 |    | 1  |    |    | 0 |
| 01 |    |    |    | 1  |   |
| 10 | 0  |    |    |    |   |
| 11 |    |    | 0  |    |   |

Answer:-(D)

Exp:- The complete DFA is

![](_page_8_Figure_12.jpeg)

27. The height of a tree is defined as the number of edges on the longest path in the tree. The function shown in the pseudocode below is invoked as height (root) to compute the height of a binary tree rooted at the tree pointer root.

int height (treeptr n)

if 
$$(n \rightarrow left == NULL)$$

![](_page_9_Picture_1.jpeg)

```
if (n \rightarrow right = NULL) return 0;
              else return |BI|;
                                                                                             // Box 1
         else {h1 = height (n \rightarrow left);
               if (n \rightarrow right = NULL) return (1+h1);
              else \{h2 = height (n \rightarrow right);
                                     return B2;
                                                                                                  // Box 2
         }
         The appropriate expressions for the two boxes B1 and B2 are
         (A) B1: (1 + height(n \rightarrow right))
                                                                    (B) B1: \left( \text{height} \left( n \rightarrow \text{right} \right) \right)
               B2:(1+\max(h1,h2))
                                                                          B2:(1+\max(h1,h2))
         (C) B1: height (n \rightarrow right)
                                                                    (D) B1: (1 + \text{height } (n \rightarrow \text{right}))
              B2: max(h1,h2)
                                                                          B2: max(h1, h2)
Answer:-(A)
Exp:- int height (treeptr n)
                   if (n = = nu11) return -1;
                                                          If there is no node, return -1
                   if (n \rightarrow left = NULL) \rightarrow /* If there is no left child for node 'n'*/
                             if (n \rightarrow right = NULL) return O;
                                       → /*If no left child & no right child for 'n', return */
                             else return (1+height (n \rightarrow right));
                                       \rightarrow/* If no left child, but there is a right child, then compute height
                                       for right sub tree. Therefore total height is 1+ height (n \rightarrow right) */
                                       If there exist left child node for node 'n' */
                   else \{ \rightarrow / * \}
                             h_1 = height (n \rightarrow left);
                                       \rightarrow /* First Find the height of left sub tree for node 'n' */
                             If (n \rightarrow right == NULL) return (1+h1);
```

![](_page_10_Picture_1.jpeg)

28. Consider an instance of TCP's Additive Increase Multiplicative decrease (AIMD) algorithm where the window size at the start of the slow start phase is 2 MSS and the threshold at the start of the first transmission is 8 MSS. Assume that a timeout occurs during the fifth transmission. Find the congestion window size at the end of the tenth transmission.

![](_page_10_Figure_4.jpeg)

<sup>♦</sup> India's No.1 institute for GATE Training ♦ 1 Lakh+ Students trained till date ♦ 65+ Centers across India

![](_page_11_Picture_1.jpeg)

Given, initial threshold = 8

Time = 1, during 1st transmission, Congestion window size = 2 (slow start phase)

Time = 2, congestion window size = 4 (double the no. of acknowledgments)

Time = 3, congestion window size = 8 (Threshold meet)

Time = 4, congestion window size = 9, after threshold (increase by one Additive increase)

Time = 5, transmits 10 MSS, but time out occurs congestion window size = 10

Hence threshold = (Congestion window size)/2 =  $\frac{10}{2}$  = 5

Time = 6, transmits 2

Time = 7, transmits 4

Time = 8, transmits 5 (threshold is 5)

Time = 9, transmits 6, after threshold (increase by one Additive increase)

Time = 10, transmits 7

... During 10<sup>th</sup> transmission, it transmits 7 segments hence at the end of the tenth transmission the size of congestion window is 7 MSS.

- 29. Consider a source computer (S) transmitting a file of size  $10^6$  bits to a destination computer (D) over a network of two routers ( $R_1$  and  $R_2$ ) and three links ( $L_1$ ,  $L_2$ , and  $L_3$ ).  $L_1$  connects S to  $R_1$ ;  $L_2$  connects  $R_1$  to  $R_2$ ; and  $L_3$  connects  $R_2$  to D. Let each link be of length 100km. Assume signals travel over each line at a speed of  $10^8$  meters per second. Assume that the link bandwidth on each link is 1Mbps. Let the file be broken down into 1000 packets each of size 1000 bits. Find the total sum of transmission and propagation delays in transmitting the file from S to D?
  - (A) 1005ms
- (B) 1010ms
- (C) 3000ms
- (D) 3003ms

Answer:- (A)

Exp:-

![](_page_11_Figure_22.jpeg)

Transmission delay for 1 packet from each of S, R<sub>1</sub> and R<sub>2</sub> will take 1ms

Propagation delay on each link L<sub>1</sub>, L<sub>2</sub> and L<sub>3</sub> for one packet is 1ms

Therefore the sum of transmission delay and propagation delay on each link for one packet is 2ms.

The first packet reaches the destination at 6<sup>th</sup>ms

The second packet reaches the destination at 7<sup>th</sup>ms

So inductively we can say that 1000<sup>th</sup> packet reaches the destination at 1005<sup>th</sup> ms

- 30. Suppose R1 ( $\underline{A}$ , B) and R<sub>2</sub> ( $\underline{C}$ , D) are two relation schemas. Let  $r_1$  and  $r_2$  be the corresponding relation instances. B is a foreign key that refers to C in R<sub>2</sub>. If data in  $r_1$  and  $r_2$  satisfy referential integrity constrains, which of the following is **ALWAYS TRUE**?
  - (A)  $\Pi_{B}(r_{1}) \Pi_{C}(r_{2}) = \emptyset$

(B)  $\Pi_{C}(r_2) - \Pi_{B}(r_1) = \emptyset$ 

(C)  $\Pi_{\mathrm{B}}(\mathbf{r}_{1}) = \Pi_{\mathrm{C}}(\mathbf{r}_{2})$ 

(D)  $\Pi_{B}(r_{1}) - \Pi_{C}(r_{2}) \neq \emptyset$ 

Answer:-(A)

![](_page_12_Picture_1.jpeg)

- Exp:- Since B is a foreign key referring C,values under B will be subset of values under C  $(\Pi_B(r_1) \subseteq \Pi_C(r_2) \Rightarrow \Pi_B(r_1) \Pi_C(r_2) = \emptyset)$
- 31. Consider the virtual page reference string

1,2,3,2,4,1,3,2,4,1

on a demand paged virtual memory system running on a computer system that has main memory size of 3 page frames which are initially empty. Let LRU, FIFO and OPTIMAL denote the number of page faults under the corresponding page replacement policy. Then

- (A) OPTIMAL < LRU < FIFO
- (B) OPTIMAL < FIFO < LRU

(C) OPTIMAL = LRU

(D) OPTIMAL = FIFO

Answer:- (B)

Exp:- FIFO

1 1 1 4 4 4 2 2 2 1 1

3 3 3 2

 $\rightarrow$  (6) faults

**Optimal** 

1 1 1 1 1

![](_page_12_Figure_16.jpeg)

Optimal < FIFO < LRU

- 32. A file system with 300 GByte disk uses a file descriptor with 8 direct block addresses, 1 indirect block address and 1 doubly indirect block address. The size of each disk block is 128 Bytes and the size of each disk block address is 8 Bytes. The maximum possible file size in this file system is
  - (A) 3 KBytes

(B) 35 KBytes

(C) 280 KBytes

(D) dependent on the size of the disk

Answer:-(B)

Exp:- Each block size = 128 Bytes

Disk block address = 8 Bytes

 $\therefore$  Each disk can contain =  $\frac{128}{8}$  = 16 addresses

Size due to 8 direct block addresses: 8 x 128

Size due to 1 indirect block address: 16 x 128

Size due to 1 doubly indirect block address: 16 x 16 x 128 Size due to 1 doubly indirect block address: 16 x 16 x 128

![](_page_13_Picture_1.jpeg)

So, maximum possible file size:

```
= 8 \times 128 + 16 \times 128 + 16 \times 16 \times 128 = 1024 + 2048 + 32768 = 35840 Bytes = 35 KBytes
```

33. Consider the directed graph shown in the figure below. There are multiple shortest paths between vertices S and T. Which one will be reported by Dijkstra's shortest path algorithm? Assume that, in any iteration, the shortest path to a vertex  $\nu$  is updated only when a strictly shorter path to v is discovered.

![](_page_13_Figure_5.jpeg)

Answer:- (D)

Exp:- Let d[v] represent the shortest path distance computed from 'S' Initially d[S]=0,  $d[A]=\infty$ ,  $d[B]=\infty$ , ---,  $d[T]=\infty$ 

And let P[v] represent the predecessor of v in the shortest path from 'S' to 'v' and let P[v]=-1 denote that currently predecessor of 'v' has not been computed

- → Let Q be the set of vertices for which shortest path distance has not been computed
- → Let W be the set of vertices for which shortest path distance has not been computed
- $\rightarrow$  So initially, Q = {S, A, B, C, D, E, F, G, T}, W =  $\phi$

We will use the following procedure

Repeat until Q is empty

1 u = choose a vertex from O with minimum d[u] value

- 2. Q = Q u
- 3. update all the adjacent vertices of u
- 4.  $W = W U\{u\}$

$$d[S] = 0, d[A] = \infty, d[B] = \infty, \dots, d[T] = \infty$$

# **Iteration 1**

![](_page_14_Picture_1.jpeg)

Step 1: 
$$u = S$$
  
Step 2:  $Q = \{A, B, C, D, E, F, G, T\}$   
Step 3: final values after adjustment

$$d[S] = 0, d[A] = 4, d[B] = 3, d[C] = \infty, d[D] = 7, d[E] = \infty - \dots, d[T] = \infty$$
$$P[A] = S, P[B] = S, P[C] = -1, P[D] = S, P[E] = -1 - \dots, P[T] = -1$$

Step 4: 
$$W = \{S\}$$

#### **Iteration 2:**

Step 1: u = B

Step 
$$2: Q = \{A, C, D, E, F, G, T\}$$

step 3: final values after adjustment

$$d[S] = 0, d[A] = 4, d[B] = 3, d[C] = \infty, d[D] = 7, d[E] = \infty ---, d[T] = \infty$$

$$P[A] = S, P[B] = S, P[C] = -1, P[D] = S, P[E] = -1 ---, P[T] = -1$$

Step 4: 
$$W = \{S, B\}$$

# **Iteration 3:**

Step 1: 
$$u = A$$

Step 2: 
$$Q = \{C, D, E, F, G, T\}$$

step 3: final values after adjustment

$$d[S] = 0, d[A] = 4, d[B] = 3, d[C] = 5, d[D] = 7, d[E] = \infty - ---, d[T] = \infty$$

$$P[A] = S, P[B] = S, P[C] = A, P[D] = S, P[E] = -1 - ---, P[T] = -1$$

$$24: W = \{S, B, A\}$$

Step 4: 
$$W = \{S, B, A\}$$

# **Iteration 4:**

Step 1: 
$$u = C$$

Step 2: 
$$Q = \{D, E, F, G, T\}$$

step 3: final values after adjustment

$$d[S] = 0, d[A] = 4, d[B] = 3, d[C] = 5, d[D] = 7, d[E] = 6, ---, d[T] = \infty$$

$$P[A] = S, P[B] = S, P[C] = A, P[D] = S, P[E] = C, ---, P[T] = -1$$

Step 4: 
$$W = \{S, B, A, C\}$$

#### **Iteration 5:**

![](_page_15_Picture_1.jpeg)

Step 1: u = E

Step 2:  $Q = \{D, F, G, T\}$ 

step 3: final values after adjustment

$$d[S] = 0, d[A] = 4, d[B] = 3, d[C] = 5, d[D] = 7, d[E] = 6, d[F] = \infty, d[G] = 8, d[T] = 10$$

$$P[A] = S, P[B] = S, P[C] = A, P[D] = S, P[E] = C, P[F] = -1, P[G] = E, P[T] = E$$

Step 4:  $W = \{S, B, A, C, E\}$ 

After iteration 5, we can observe that P[T]=E, P[E]=C, P[C]=A, P[A]=S, So the shortest path from S to T is SACET

- 34. A list of n strings, each of length n, is sorted into lexicographic order using the merge-sort algorithm. The worst case running time of this computation is
  - (A)  $O(n \log n)$

(B)  $O(n^2 \log n)$ 

(C)  $O(n^2 + \log n)$ 

(D)  $O(n^2)$ 

Answer:-(B)

- Exp:- The height of the recursion tree using merge sort is logn and  $n^2$  comparisons are done at each level, where at most n pairs of strings are compared at each level and n comparisons are required to compare any two strings, So the worst case running time is  $O(n^2 \log n)$
- 35. Let G be a complete undirected graph on 6 vertices. If vertices of G are labeled, then the number of distinct cycles of length 4 in G is equal to

(A) 15

- (B) 30
- (C) 90

(D) 360

Answer:- No option matching (marks to all)

Exp:- 4 vertices from 6 vertices can be chosen in in  ${}^6c_4$ . Number of cycles of length 4 that can be formed from those selected vertices is (4-1)!/2 (left or right/ up or down does not matter), so total number of 4 length cycles are  $({}^6c_4.3!)/2 = 45$ .

- 36. How many onto (or surjective) functions are there from an n-element  $(n \ge 2)$  set to a 2-element set?
  - (A)  $2^{n}$
- (B)  $2^{n}-1$
- (C)  $2^n 2$
- (D)  $2(2^n-2)$

Answer:- (C)

Exp:- Total number of functions is  $2^n$ , out of which there will be exactly two functions where all elements map to exactly one element, so total number of onto functions is  $2^n-2$ 

37. Consider the program given below, in a block-structured pseudo-language with lexical scoping and nesting of procedures permitted.

Program main;

Var . . .

Procedure A1;

Var ....

<sup>→</sup> India's No.1 institute for GATE Training → 1 Lakh+ Students trained till date → 65+ Centers across India

![](_page_16_Picture_1.jpeg)

Call A2;
End A1
Procedure A2;
Var . . .
Procedure A21;
Var . . .
Call A1;
End A21
Call A21;
End A2
Call A1;

End main.

Consider the calling chain: Main  $\rightarrow$  A1  $\rightarrow$  A2  $\rightarrow$  A21  $\rightarrow$  A1

The correct set of activation records along with their access links is given by

![](_page_16_Figure_5.jpeg)

Answer:-(D)

<sup>♦</sup> India's No.1 institute for GATE Training ♦ 1 Lakh+ Students trained till date ♦ 65+ Centers across India

![](_page_17_Picture_1.jpeg)

- Exp:- Access link is defined as link to activation record of closest lexically enclosing block in program text, so the closest enclosing blocks respectively for A1 ,A2 and A21 are main , main and A2
- 38. Suppose a circular queue of capacity (n 1) elements is implemented with an array of n elements. Assume that the insertion and deletion operations are carried out using REAR and FRONT as array index variables, respectively. Initially, REAR = FRONT = 0. The conditions to detect queue full and queue empty are
  - (A) full: (REAR+1) mod n==FRONT empty: REAR ==FRONT
- (B) full:(REAR+1)mod n==FRONT empty: (FRONT+1)mod n==REAR
- (C) full: REAR==FRONT
  empty: (REAR+1) mod n ==FRONT
- (D) full:(FRONT+1)mod n==REAR empty: REAR ==FRONT

Answer:- (A)

Exp:- The *counter example* for the condition *full* : REAR = FRONT is

Initially when the Queue is empty REAR=FRONT=0 by which the above *full* condition is satisfied which is false

The *counter example* for the condition *full* : (FRONT+1)mod n =REAR is

Initially when the Queue is empty REAR=FRONT=0 and let n=3, so after inserting one element REAR=1 and FRONT=0, at this point the condition *full* above is satisfied, but still there is place for one more element in Queue, so this condition is also false

The *counter example* for the condition *empty* : (REAR+1) mod n = FRONT is

Initially when the Queue is empty REAR=FRONT=0 and let n=2, so after inserting one element REAR=1 and FRONT=0, at this point the condition *empty* above is satisfied, but the queue of capacity n-1 is full here

The *counter example* for the condition *empty*: (FRONT+1)mod n =REAR is

Initially when the Queue is empty REAR=FRONT=0 and let n=2, so after inserting one element REAR=1 and FRONT=0, at this point the condition *empty* above is satisfied, but the queue of capacity n-1 is full here

- 39. An Internet Service Provider (ISP) has the following chunk of CIDR-based IP addresses available with it: 245.248.128.0/20. The ISP wants to give half of this chunk of addresses to Organization A, and a quarter to Organization B, while retaining the remaining with itself. Which of the following is a valid allocation of address to A and B?
  - (A) 245.248.136.0/21 and 245.248.128.0/22
  - (B) 245.248.128.0/21 and 245.248.128.0/22
  - (C) 245.248.132.0/22 and 245.248.132.0/21
  - (D) 245.248.136.0/24 and 245.248.132.0/21

Answer:- (A)

Exp:- Network part host part  $11110101. \ 111111000.1000_{12\overline{13}} -. -- -- -- _{\overline{2}} -1$ 

![](_page_18_Picture_1.jpeg)

Since half of 4096 host addresses must be given to organization A, we can set 12<sup>th</sup> bit to 1 and include that bit into network part of organization A, so the valid allocation of addresses to A is 245.248.136.0/21

Now for organization B, 12<sup>th</sup> bit is set to '0' but since we need only half of 2048 addresses, 13<sup>th</sup> bit can be set to '0' and include that bit into network part of organization B so the valid allocation of addresses to B is 245.248.128.0/22

40. Suppose a fair six-sided die is rolled once. If the value on the die is 1, 2, or 3, the die is rolled a second time. What is the probability that the sum total of values that turn up is at least 6?

![](_page_18_Figure_5.jpeg)

41. Fetch\_And\_Add (X, i) is an atomic Read-Modify-Write instruction that reads the value of memory location X, increments it by the value i, and returns the old value of X. It is used in the pseudocode shown below to implement a busy-wait lock. L is an unsigned integer shared variable initialized to 0. The value of 0 corresponds to lock being available, while any non-zero value corresponds to the lock being not available.

```
AcquireLock(L)\{ \\ While (Fetch\_And\_Add(L,1)) \\ L = 1; \\ \} \\ Release Lock(L)\{ \\ L = 0; \\ \} \\ This implementation
```

- (A) fails as L can overflow
- (B) fails as L can take on a non-zero value when the lock is actually available

![](_page_19_Picture_1.jpeg)

- (C) works correctly but may starve some processes
- (D) works correctly without starvation

# Answer:- (B)

```
Exp:- 1. Acquire lock (L) {
2. While (Fetch_And_Add(L, 1))
3. L = 1.
}
4. Release Lock (L) {
5. L = 0;
6. }
```

Let P and Q be two concurrent processes in the system currently executing as follows

P executes 1,2,3 then Q executes 1 and 2 then P executes 4,5,6 then L=0 now Q executes 3 by which L will be set to 1 and thereafter no process can set

L to zero, by which all the processes could starve.

# 42. Consider the 3 process, P1, P2 and P3 shown in the table.

| Process | Arrival time | Time units Required |  |
|---------|--------------|---------------------|--|
| P1      | 0            | 5                   |  |
| P2      | 1, 1         | 7                   |  |
| P3      | 3            | 4                   |  |

The completion order of the 3 processes under the policies FCFS and RR2 (round robin scheduling with CPU quantum of 2 time units) are

(A) FCFS: P1, P2, P3 RR2: P1, P2, P3
(B) FCFS: P1, P3, P2 RR2: P1, P3, P2
(C) FCFS: P1, P2, P3 RR2: P1, P3, P2
(D) FCFS: P1, P3, P2 RR2: P1, P2, P3

### Answer:-(C)

Exp:- For FCFS Execution order will be order of Arrival time so it is P1,P2,P3

Next For RR with time quantum=2,the arrangement of Ready Queue will be as follows:

RQ: P1,P2,P1,P3,P2,P1,P3,P2

This RQ itself shows the order of execution on CPU(Using Gantt Chart) and here it gives the completion order as P1,P3,P2 in Round Robin algorithm.

![](_page_20_Picture_1.jpeg)

What is the minimal form of the Karnaugh map shown below? Assume that X denotes a don't 43. care term.

| ab<br>cd | 00 | 01 | 11 | 10 |
|----------|----|----|----|----|
| 00       | 1  | X  | X  | 1  |
| 01       | Х  |    |    | 1  |
| 11       |    |    |    |    |
| 10       | 1  |    |    | Х  |

 $(A) \overline{bd}$ 

(B)  $\overline{bd} + \overline{bc}$ 

(C)  $\overline{bd} + a\overline{bcd}$ 

(D)  $\overline{bd} + \overline{bc} + \overline{cd}$ 

![](_page_20_Figure_8.jpeg)

![](_page_20_Figure_9.jpeg)

- 44. Let G be a weighted graph with edge weights greater than one and G' be the graph constructed by squaring the weights of edges in G. Let T and T' be the minimum spanning trees of G and G' respectively, with total weights t and t'. Which of the following statements is **TRUE**?
  - (A) T' = T with total weight  $t' = t^2$
- (B) T' = T with total weight  $t' < t^2$
- (C) T'  $\neq$  T but total weight t' = t<sup>2</sup>
- (D) None of these

Answer:-(D)

Exp:-

![](_page_20_Picture_17.jpeg)

![](_page_20_Picture_18.jpeg)

Graph G is counter example for options (B) and (C) and Graph G<sub>1</sub> is counter example for option (A)

![](_page_21_Picture_1.jpeg)

- 45. The bisection method is applied to compute a zero of the function  $f(x) = x^4 x^3 x^2 4$  in the interval [1,9]. The method converges to a solution after \_\_\_\_\_\_ iterations.
  - (A) 1
- (B) 3
- (C) 5
- (D) 7

Answer:- (B)

Exp:-

$$f(x) = x^4 - x^3 - x^2 - 4$$

$$f(1) < 0$$
 and  $f(9) > 0$  :  $x_0 = \frac{1+9}{2} = 5$ 

f(5) > 0 : root lies in [1,5]

$$x_1 = \frac{1+5}{2} = 3$$

f(3) > 0 : root lies in [1,3]

$$x_2 = \frac{1+3}{2} = 2$$

f(2) = 0: root is 2

46. Which of the following graph is isomorphic to

![](_page_21_Picture_17.jpeg)

![](_page_21_Picture_18.jpeg)

![](_page_21_Picture_19.jpeg)

![](_page_21_Picture_20.jpeg)

![](_page_21_Picture_21.jpeg)

Answer:-(B)

Exp:- The graph in option (A) has a 3 length cycle whereas the original graph does not have a 3 length cycle

The graph in option (C) has vertex with degree 3 whereas the original graph does not have a vertex with degree 3

![](_page_22_Picture_1.jpeg)

The graph in option (D) has a 4 length cycle whereas the original graph does not have a 4 length cycle

47. Consider the following transactions with data items P and Q initialized to zero:

```
T<sub>1</sub>: read (P);

read (Q);

if P = 0 then Q : = Q + 1;

write (Q).

T<sub>2</sub>: read (Q);

read (P)

if Q = 0 then P : = P + 1;

write (P).
```

Any non-serial interleaving of T1 and T2 for concurrent execution leads to

- (A) a serializable schedule
- (B) a schedule that is not conflict serializable
- (C) a conflict serializable schedule
- (D) a schedule for which precedence graph cannot be drawn

# Answer:-(B)

Exp:- Let S be a non-serial schedule, without loss of generality assume that T1 has started earlier than T2. The first instruction of T1 is read(P) and the last instruction of T2 is write(P), so the precedence graph for S has an edge from T1 to T2, now since S is a non-serial schedule the first instruction of T2(read(Q)) should be executed before last instruction of T1(write(Q)) and since read and write are conflicting operations, the precedence graph for S also contains an edge from T2 to T1, So we will have a cycle in the precedence graph which implies that any non serial schedule with T1 as the earliest transaction will not be conflict serializable.

In a similar way we can show that if T2 is the earliest transaction then also the schedule is not conflict serializable.

# Common Data Questions: 48 & 49

Consider the following relations A, B and C:

A

| Id | Name   | Age |
|----|--------|-----|
| 12 | Arun   | 60  |
| 15 | Shreya | 24  |
| 99 | Rohit  | 11  |

В

| Id | Name   | Age |
|----|--------|-----|
| 15 | Shreya | 24  |
| 25 | Hari   | 40  |

![](_page_23_Picture_1.jpeg)

| 98 | Rohit | 20 |
|----|-------|----|
| 99 | Rohit | 11 |

 $\mathbf{C}$ 

| Id | Phone | Area |
|----|-------|------|
| 10 | 220   | 02   |
| 99 | 2100  | 01   |

48. How many tuples does the result of the following SQL query contain?

SELECT A.Id

FROM A

WHERE A.Age > ALL(SELECT B.Age

FROM B

WHERE B.Name = 'Arun')

(A) 4

(B) 3

(C) 0

(D) 1

Answer:-(B)

Exp:- As the result of subquery is an empty table, '>ALL' comparison is true. Therefore, all the three row id's of A will be selected from table A.

49. How many tuples does the result of the following relational algebra expression contain? Assume that the schema of  $A \cup B$  is the same as that of A.

 $(A \cup B) \triangleright \triangleleft_{A.Id>40 \text{ v. } C.Id<15} C$ 

(A)7

(B) 4

(C) 5

(D) 9

Answer:-(A)

Exp:- The final table is

| AUB . Id | Name   | Age | C.Id | Phone | Area |
|----------|--------|-----|------|-------|------|
| 12       | Arun   | 60  | 10   | 2200  | 02   |
| 15       | Shreya | 24  | 10   | 2200  | 02   |
| 25       | Hari   | 40  | 10   | 2200  | 02   |
| 98       | Rohit  | 20  | 10   | 2200  | 02   |
| 98       | Rohit  | 20  | 99   | 2100  | 01   |
| 99       | Rohit  | 11  | 10   | 2200  | 02   |
| 99       | Rohit  | 11  | 99   | 2100  | 01   |

Common Data Questions: 50 & 51

Consider the following C code segment:

int a, b, c = 0;

void prtFun(void);

<sup>♦</sup> India's No.1 institute for GATE Training ♦ 1 Lakh+ Students trained till date ♦ 65+ Centers across India

![](_page_24_Picture_1.jpeg)

```
main()
                                         /* Line 1 */
{
        static int a = 1;
        prtFun( );
        a + = 1;
        prtFun( )
        printf("\n %d %d ", a, b);
}
void prtFun(void)
{
        static int a=2;
                                         /* Line 2 */
        int b=1:
        a+=++b;
        printf("\n %d %d ", a, b);
}
```

50. What output will be generated by the given code segment if:

Line 1 is replaced by **auto int a = 1**;

Line 2 is replaced by **register int** a = 2;

![](_page_24_Figure_6.jpeg)

Answer:-(D)

Exp:- Static local variables: Scope is limited to function/block but life time is entire program.

# **Automatic local variables:**

Storage allocated on function entry and automatically deleted or freed when the function is exited.

**Register variables:** Same as automatic variables except that the register variables will not have addresses Hence may not take the address of a register variable.

$$\begin{array}{c|ccccccccccccccccccccccccccccccccccc$$

![](_page_25_Picture_1.jpeg)

51. What output will be generated by the given code segment?

![](_page_25_Figure_3.jpeg)

Answer:- (C)

# Exp:-

![](_page_25_Figure_6.jpeg)

Linked Answer Questions: Q.52 to Q.55 Carry Two Marks Each

**Statement for Linked Answer Questions: 52 & 53** 

A computer has a 256 KByte, 4-way set associative, write back data cache with block size of 32 Bytes. The processor sends 32 bit addresses to the cache controller. Each cache tag directory entry contains, in addition to address tag, 2 valid bits, 1 modified bit and 1 replacement bit.

52. The number of bits in the tag field of an address is

Answer:- (C)

Exp:- Number of blocks = 
$$\frac{256 \text{ KB}}{32 \text{ Bytes}} = \frac{2^{18}}{2^5} = 2^{13} \text{ blocks}$$

As it is 4-way set associative, number of sets =  $\frac{2^{13}}{2^2} = 2^{11}$ 

| <b>—</b>                       | 32 bits                       | <b>←</b>         |  |
|--------------------------------|-------------------------------|------------------|--|
| TAG                            | SET                           | Byte offset      |  |
|                                | offset                        |                  |  |
| $\overline{}$ 16 $\rightarrow$ | $\leftarrow$ 11 $\rightarrow$ | <del>←</del> 5 → |  |

![](_page_26_Picture_1.jpeg)

- 53. The size of the cache tag directory is
  - (A) 160 Kbits
- (B) 136 Kbits
- (C) 40 Kbits
- (D) 32 Kbits

Answer:-(A)

Exp:- TAG controller maintains 16 + 4 = 20 bits for every block

Hence, size of cache tag directory =  $20 \times 2^{13}$  bits = 160 K bits

# Statement for Linked Answer Questions: 54 & 55

For the grammar below, a partial LL(1) parsing table is also presented along with the grammar. Entries that need to be filled are indicated as **E1**, **E2**, and **E3**.  $\varepsilon$  is the empty string, \$ indicates end of input, and | separates alternate right hand sides of productions.

$$S \rightarrow aAbB|bAaB|\varepsilon$$

 $A \rightarrow S$ 

 $B \rightarrow S$ 

|   | a                 | b                 | \$               |
|---|-------------------|-------------------|------------------|
| S | <b>E</b> 1        | <b>E2</b>         | $S \to \epsilon$ |
| A | $A \rightarrow S$ | $A \rightarrow S$ | error            |
| В | $B \rightarrow S$ | $B \rightarrow S$ | E3               |

- 54. The First and Follow sets for the non-terminals A and B are
  - (A)  $FIRST(A) = \{a, b, \epsilon\} = FIRST(B)$

 $FOLLOW(A) = \{a, b\}$ 

 $FOLLOW(B) = \{a, b, \$\}$ 

(B)  $FIRST(A) = \{a, b, \$\}$ 

$$FIRST(B) = \{a, b, \epsilon\}$$

$$FOLLOW(A) = \{a, b\}$$

$$FOLLOW(B) = \{\$\}$$

(C)  $FIRST(A) = \{a, b, \epsilon\} = FIRST(B)$ 

$$FIRST(A) = \{a, b\}$$

$$FOLLOW(B) = \emptyset$$

(D)  $FIRST(A) = \{a, b,\} = FIRST(B)$ 

$$FIRST(A) = \{a, b\}$$

$$FOLLOW(B) = \{a, b\}$$

Answer:- (A)

Exp:- 
$$First(A) = First(S) = First(aAbB) \cup First(bAaB) \cup First(\in)$$

$$= \{a\} \cup \{b\} \cup \{\epsilon\} = \{\epsilon, a, b\}$$

$$First(B) = First(S) = \{ \in, a, b \}$$

Follow (A) = First (bB) 
$$\cup$$
 First (aB) = {a,b}

Follow (B) = Follow (S) = 
$$\{\$\} \cup \text{Follow}(A) = \{\$, a,b\}$$

<sup>→</sup> India's No.1 institute for GATE Training → 1 Lakh+ Students trained till date → 65+ Centers across India

![](_page_27_Picture_1.jpeg)

- 55. The appropriate entries for E1, E2, and E3 are
  - (A) E1:  $S \rightarrow aAbB$ ,  $A \rightarrow S$

(B) E1:  $S \rightarrow aAbB$ ,  $S \rightarrow \varepsilon$ 

E2:  $S \rightarrow bAaB$ ,  $B \rightarrow S$ 

E2:  $S \rightarrow bAaB$ ,  $S \rightarrow \varepsilon$ 

E3:  $B \rightarrow S$ 

E3:  $S \rightarrow \epsilon$ 

(C) E1:  $S \rightarrow aAbB$ ,  $S \rightarrow \varepsilon$ 

E2:  $S \rightarrow bAaB$ ,  $S \rightarrow \varepsilon$ 

E3: B $\rightarrow$ S

(D) E1:  $A \rightarrow S$ ,  $S \rightarrow \varepsilon$ 

E2: B  $\rightarrow$ S, S  $\rightarrow \epsilon$ 

E3: B  $\rightarrow$  S

# Answer:- (C)

Exp:-

First  $(S) = \{ \in, a, b \}$ , Follow  $(S) = \{ \$, a, b \}$ 

|   | a                    | b                    | \$                  |
|---|----------------------|----------------------|---------------------|
| S | $S \rightarrow aAbB$ | $S \rightarrow bAaB$ | $S \rightarrow \in$ |
|   | S→∈                  | S→∈                  |                     |

 $B \rightarrow S$  to be placed in LL(1) Parsing table as follows:-

First (S) =  $\{ \in, a, b \}$ , Follow (B) =  $\{ \$, a, b \}$ 

# $\begin{array}{c|ccccccccccccccccccccccccccccccccccc$

56. The cost function for a product in a firm is given by 5q<sup>2</sup>, where q is the amount of production. The firm can sell the product at a market price of Rs.50 per unit. The number of

units to be produced by the firm such that the profit is maximized is

- (A) 5
- (B) 10
- (C) 15
- (D) 25

Answer:- (A)

Exp:-

$$P = 50q - 5q^2$$

$$\frac{dp}{dq} = 50 - 10q$$
;  $\frac{d^2p}{dq^2} < 0$ 

 $\therefore$  p is maximum at 50-10q=0 or, q=5

Else check with options

57. Choose the most appropriate alternative from the options given below to complete the following sentence:

Suresh's dog is the one \_\_\_\_\_ was hurt in the stampede.

- (A) that
- (B) which
- (C) who
- (D) whom

Answer:- (A)

<sup>♦</sup> India's No.1 institute for GATE Training ♦ 1 Lakh+ Students trained till date ♦ 65+ Centers across India

![](_page_28_Picture_1.jpeg)

- 58. Choose the grammatically **INCORRECT** sentence:
  - (A) They gave us the money back less the service charges of Three Hundred rupees.
  - (B) This country's expenditure is not less than that of Bangladesh.
  - (C) The committee initially asked for a funding of Fifty Lakh rupees, but later settled for a lesser sum.
  - (D) This country's expenditure on educational reforms is very less

Answer:-(D)

59. Which one of the following options is the closest in meaning to the word given below?

Mitigate

- (A) Diminish
- (B) Divulge
- (C) Dedicate
- (D) Denote

Answer:- (A)

60. Choose the most appropriate alternative from the options given below to complete the following sentence:

\_ the mission succeeded in its attempt to resolve the conflict. Despite several \_

- (A) attempts
- (B) setbacks
- (C) meetings
- (D) delegations

Answer:- (B)

Q. No. 61 - 65 Carry Two Marks Each

- 61. Wanted Temporary, Part-time persons for the post of Field Interviewer to conduct personal interviews to collect and collate economic data. Requirements: High School-pass, must be available for Day, Evening and Saturday work. Transportation paid, expenses reimbursed.
  - Which one of the following is the best inference from the above advertisement?
  - (A) Gender-discriminatory
- (B) Xenophobic
- (C) Not designed to make the post attractive (D) Not gender-discriminatory

Answer:- (C)

Exp:- Gender is not mentioned in the advertisement and (B) clearly eliminated

- 62. Given the sequence of terms, AD CG FK JP, the next term is
  - (A) OV
- (B) OW
- (C) PV
- (D)PW

Exp:-

![](_page_28_Figure_36.jpeg)

- 63. Which of the following assertions are CORRECT?
  - P: Adding 7 to each entry in a list adds 7 to the mean of the list
  - Q: Adding 7 to each entry in a list adds 7 to the standard deviation of the list
  - R: Doubling each entry in a list doubles the mean of the list

![](_page_29_Picture_1.jpeg)

S: Doubling each entry in a list leaves the standard deviation of the list unchanged

- (A) P, Q
- (B) Q, R
- (C) P, R
- (D) R, S

Answer:-(C)

Exp:- P and R always hold true

Else consider a sample set {1, 2, 3, 4} and check accordingly

64. An automobile plant contracted to buy shock absorbers from two suppliers X and Y. X supplies 60% and Y supplies 40% of the shock absorbers. All shock absorbers are subjected to a quality test. The ones that pass the quality test are considered reliable Of X's shock absorbers, 96% are reliable. Of Y's shock absorbers, 72% are reliable.

The probability that a randomly chosen shock absorber, which is found to be reliable, is made by Y is

- (A) 0.288
- (B) 0.334
- (C) 0.667
- (D) 0.720

Answer:-(B)

$$P(x) = \frac{0.288}{0.576 + 0.288} = 0.334$$

- A political party orders an arch for the entrance to the ground in which the annual convention is being held. The profile of the arch follows the equation  $y = 2x 0.1x^2$  where y is the height of the arch in meters. The maximum possible height of the arch is
  - (A) 8 meters
- (B) 10 meters
- (C) 12 meters
- (D) 14 meters

Answer:-(B)

Exp:

$$y = 2x - 0.1x^{2}$$

$$\frac{dy}{dx} = 2 - 0.2x$$

$$\frac{d^{2}y}{dx^{2}} < 0 \therefore y \text{ max imises at } 2 - 0.2x = 0$$

$$\Rightarrow x = 10$$

$$\therefore y = 20 - 10 = 10 \text{ m}$$