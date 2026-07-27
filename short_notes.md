# 🎓 GATE Data Science & AI (DA) Topper Short Notes

This formula sheet compiles all critical equations, definitions, and theorems across the GATE DA syllabus. Use it for active recall, quick reference, and final revisions.

---

## 1. Linear Algebra

### System of Equations & Rank
*   **System Form:** $Ax = b$, where $A$ is $m \times n$.
*   **Rank-Nullity Theorem:** $\text{rank}(A) + \text{nullity}(A) = n$ (number of columns).
*   **Consistency:** $Ax = b$ is consistent if and only if $\text{rank}(A) = \text{rank}([A \mid b])$.
    *   Unique solution: $\text{rank}(A) = n$.
    *   Infinitely many solutions: $\text{rank}(A) < n$.

### Eigenvalues & Eigenvectors
*   **Characteristic Equation:** $\det(A - \lambda I) = 0$.
*   **Trace & Determinant:**
    *   $\sum \lambda_i = \text{trace}(A)$ (sum of diagonal elements).
    *   $\prod \lambda_i = \det(A)$.
*   **Symmetric Matrix:** Eigenvalues are always real. Eigenvectors corresponding to distinct eigenvalues are orthogonal.

### Matrix Decompositions
*   **LU Decomposition:** $A = LU$ (Lower and Upper triangular).
*   **QR Decomposition:** $A = QR$, where $Q$ is orthogonal ($Q^T Q = I$) and $R$ is upper triangular.
*   **Singular Value Decomposition (SVD):** $A = U \Sigma V^T$.
    *   Columns of $U$: Eigenvectors of $A A^T$ (left singular vectors).
    *   Columns of $V$: Eigenvectors of $A^T A$ (right singular vectors).
    *   Singular values $\sigma_i = \sqrt{\lambda_i}$ (eigenvalues of $A^T A$).

---

## 2. Probability & Statistics

### Probability Rules
*   **Bayes' Theorem:**
    $$P(A \mid B) = \frac{P(B \mid A) P(A)}{P(B)} = \frac{P(B \mid A) P(A)}{\sum_i P(B \mid E_i) P(E_i)}$$

### Random Variables (Discrete & Continuous)
*   **Expectation:** $\mathbb{E}[X] = \sum x p(x)$ or $\int x f(x) dx$.
*   **Variance:** $\text{Var}(X) = \mathbb{E}[X^2] - (\mathbb{E}[X])^2$.
*   **Covariance:** $\text{Cov}(X, Y) = \mathbb{E}[XY] - \mathbb{E}[X]\mathbb{E}[Y]$.

### Standard Distributions
| Distribution | PMF / PDF | Mean | Variance |
| :--- | :--- | :--- | :--- |
| **Binomial** | $P(X=k) = \binom{n}{k} p^k (1-p)^{n-k}$ | $np$ | $np(1-p)$ |
| **Poisson** | $P(X=k) = \frac{e^{-\lambda} \lambda^k}{k!}$ | $\lambda$ | $\lambda$ |
| **Normal** | $f(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$ | $\mu$ | $\sigma^2$ |
| **Exponential** | $f(x) = \lambda e^{-\lambda x}$ ($x \ge 0$) | $1/\lambda$ | $1/\lambda^2$ |

### Hypothesis Testing
*   **Type I Error ($\alpha$):** Rejecting $H_0$ when it is true (False Positive).
*   **Type II Error ($\beta$):** Failing to reject $H_0$ when it is false (False Negative).
*   **Z-Test Statistic:** $z = \frac{\bar{x} - \mu_0}{\sigma / \sqrt{n}}$.
*   **t-Test Statistic:** $t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}$ (with $n-1$ degrees of freedom).

---

## 3. Calculus & Optimization

### Derivatives & Taylor Series
*   **Taylor Series of $f(x)$ at $a$:**
    $$f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!} (x-a)^n$$
*   **Gradient Vector:** $\nabla f = \left[ \frac{\partial f}{\partial x_1}, \frac{\partial f}{\partial x_2}, \dots, \frac{\partial f}{\partial x_k} \right]^T$.
*   **Hessian Matrix:** $H_{ij} = \frac{\partial^2 f}{\partial x_i \partial x_j}$.
    *   Positive Definite ($H > 0$): Local Minimum.
    *   Negative Definite ($H < 0$): Local Maximum.
    *   Indefinite: Saddle Point.

### Gradient Descent Updates
*   **Update Rule:** $x^{(t+1)} = x^{(t)} - \eta \nabla f(x^{(t)})$, where $\eta$ is the learning rate.

---

## 4. Machine Learning

### Loss Functions & Regularization
*   **Linear Regression MSE:** $J(w, b) = \frac{1}{2n} \sum_{i=1}^n (y_i - (w x_i + b))^2$.
*   **L2 Regularization (Ridge):** Penalty term $+ \lambda \|w\|_2^2$ (shrinks coefficients smoothly).
*   **L1 Regularization (Lasso):** Penalty term $+ \lambda \|w\|_1$ (creates sparse solutions, feature selection).

### Classification Metrics
*   **Precision:** $\frac{TP}{TP + FP}$
*   **Recall:** $\frac{TP}{TP + FN}$
*   **F1-Score:** $\frac{2 \times \text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$

### Activation Functions
*   **Sigmoid:** $\sigma(z) = \frac{1}{1 + e^{-z}}$
*   **ReLU:** $f(z) = \max(0, z)$
*   **Leaky ReLU:** $f(z) = \max(\alpha z, z)$ ($0 < \alpha < 1$)

---

## 5. DBMS & Warehousing

### Normalization Constraints
*   **1NF:** Atomic values only.
*   **2NF:** 1NF + no partial dependencies (non-prime attribute depending on subset of candidate key).
*   **3NF:** 2NF + no transitive dependencies (non-prime attribute depending on another non-prime attribute).
*   **BCNF:** For every FD $X \to Y$, $X$ must be a superkey.

---

## 6. Artificial Intelligence

### Search Complexity
*   **BFS:** Time $O(b^d)$, Space $O(b^d)$ (complete and optimal if step costs are equal).
*   **DFS:** Time $O(b^m)$, Space $O(bm)$ (not complete, not optimal).
*   **A* Heuristic Conditions:**
    *   **Admissibility:** $h(n) \le h^*(n)$ (never overestimates real cost).
    *   **Consistency:** $h(n) \le c(n, a, n') + h(n')$ (monotonically non-decreasing along paths).

### Propositional Logic Rules
*   **Modus Ponens:** $\frac{P, \;\; P \to Q}{Q}$
*   **Modus Tollens:** $\frac{\neg Q, \;\; P \to Q}{\neg P}$
*   **Disjunctive Syllogism:** $\frac{P \lor Q, \;\; \neg P}{Q}$
