
## Part I — Socle Layers and Littlewood–Richardson Coefficients

### 1. Overview

This part of the repository investigates the combinatorial structure of socle-layer multiplicities expressed through generalized Littlewood–Richardson (LR) coefficients.

The project began with a SageMath implementation, `hoyt.ipynb`, designed to compute these multiplicities and generate LaTeX tables describing the corresponding layers. We subsequently developed optimized implementations, verification tools, and interactive notebooks for examining individual LR contributions.

The computational investigation motivated a broader mathematical question:

**Can the highest nonzero layer be determined directly from the shapes of two partitions, without explicitly evaluating every Littlewood–Richardson coefficient?**

Our work has led to:

- An optimized algorithm for computing generalized LR multiplicities.
- Exact formulas for the maximum nonzero layer when one partition has at most two rows.
- General bounds and structural properties for arbitrary partitions.
- An exact recursive formulation using characters of symmetric groups.
- Superadditivity and stability results.
- A finite-generation framework for common LR supports.
- An asymptotic theory for stretched partitions.
- Computational investigations of intersection participation and common-factor saturation.

The research is ongoing. Established mathematical statements are distinguished below from computational observations and open questions.

---

### 2. Mathematical Background

#### 2.1. Partitions and Young diagrams

A partition of a nonnegative integer $n$ is a weakly decreasing sequence of positive integers

$$
\lambda=(\lambda_1,\ldots,\lambda_r),
\qquad
\lambda_1\ge\cdots\ge\lambda_r>0,
$$

satisfying

$$
|\lambda|=\sum_{i=1}^r\lambda_i=n.
$$

The empty partition is denoted by $\varnothing$.

The length of a partition, denoted by $\ell(\lambda)$, is its number of nonzero parts.

A partition can be represented by a Young diagram containing $\lambda_i$ boxes in its $i$-th row.

For two partitions $\mu,\lambda$, we write

$$
\mu\subseteq\lambda
$$

if $\mu_i\le\lambda_i$ for every $i$, padding both partitions with zeros when necessary.

The intersection of two partitions is defined componentwise:

$$
\lambda\cap\mu
=
\bigl(
\min(\lambda_1,\mu_1),
\min(\lambda_2,\mu_2),
\ldots
\bigr),
$$

with trailing zeros omitted.

The conjugate partition $\lambda^{\mathsf T}$ is obtained by transposing its Young diagram:

$$
\lambda_j^{\mathsf T}
=
\#\{i:\lambda_i\ge j\}.
$$

Thus, conjugation exchanges rows and columns.

#### 2.2. Littlewood–Richardson coefficients

Let $s_\lambda$ denote the Schur function associated with $\lambda$.

The ordinary Littlewood–Richardson coefficients are defined by

$$
s_\alpha s_\beta
=
\sum_\lambda
c_{\alpha,\beta}^{\lambda}s_\lambda.
$$

The coefficient $c_{\alpha,\beta}^{\lambda}$ is a nonnegative integer counting LR tableaux of the appropriate skew shape and content.

In particular,

$$
c_{\alpha,\beta}^{\lambda}>0
$$

implies

$$
|\lambda|=|\alpha|+|\beta|,
\qquad
\alpha,\beta\subseteq\lambda.
$$

Associativity of Schur-function multiplication allows us to define generalized LR coefficients. In the three-factor case,

$$
N_{\delta,\gamma,\lambda'}^\lambda
=
\sum_\nu
c_{\delta,\gamma}^{\nu}
c_{\nu,\lambda'}^\lambda.
$$

Equivalently, this is the coefficient of $s_\lambda$ in

$$
s_\delta s_\gamma s_{\lambda'}.
$$

#### 2.3. The layer multiplicity formula

For partitions $\lambda,\mu$ and an index $k$, the quantity computed throughout this investigation is

$$
\boxed{
S_k^{\lambda,\mu}(\lambda',\mu')
=
\sum_{\substack{\delta,\gamma\\
|\delta|+|\gamma|=k}}
N_{\delta,\gamma,\lambda'}^\lambda
N_{\delta,\gamma,\mu'}^\mu.
}
$$

The sum is over ordered pairs $(\delta,\gamma)$, including the empty partition.

The degree constraints imply

$$
|\lambda'|=|\lambda|-k,
\qquad
|\mu'|=|\mu|-k.
$$

The associated formal layer decomposition is

$$
\mathcal L_k^{\lambda,\mu}
=
\bigoplus_{\lambda',\mu'}
S_k^{\lambda,\mu}(\lambda',\mu')
V^{\lambda',\mu'}.
$$

The maximum nonzero layer index is

$$
\boxed{
k_{\max}(\lambda,\mu)
=
\max\left\{
k:
\exists\,\lambda',\mu'
\text{ with }
S_k^{\lambda,\mu}(\lambda',\mu')>0
\right\}.
}
$$

Here $k=0$ corresponds to the initial layer in the notebook's zero-based indexing. If the representation-theoretic socle filtration is indexed starting at one, the corresponding layer number is shifted by one.

Our research concerns both the complete multiplicities $S_k$ and the simpler question of determining $k_{\max}$.

---

### 3. The Original Hoyt Implementation

**Primary file:** `hoyt.ipynb`

The original notebook provides a direct implementation of the generalized LR multiplicity formula in SageMath.

It uses SageMath's `lrcalc` implementation to evaluate ordinary LR coefficients and combines them through explicit enumeration.

#### 3.1. Partition generation

The function

`generate_partitions(n, max_part=None)`

recursively generates every partition of a specified integer $n$.

The function

`subset_partitions(partition)`

generates all partitions whose degrees are at most the degree of the input partition.

Despite its name, this function does **not** restrict the generated partitions to Young diagrams contained in the input diagram. Consequently, the original implementation considers many candidate partitions whose LR coefficients must eventually vanish.

This is one source of unnecessary computation.

#### 3.2. Degree constraints

The function

`solveTwo(k, k1, k2, k3, k4)`

determines possible degree assignments for the two common LR factors.

For fixed $\lambda,\lambda',\mu,\mu'$, a nonzero contribution requires

$$
k
=
|\lambda|-|\lambda'|
=
|\mu|-|\mu'|.
$$

The function enumerates the possible degree splittings

$$
|\delta|=j,
\qquad
|\gamma|=k-j,
\qquad
0\le j\le k.
$$

These constraints eliminate some impossible terms before the LR coefficients are evaluated.

#### 3.3. Generalized LR coefficients

The function

`lrcoef3(mu1, mu2, mu3, lam)`

computes a three-factor LR coefficient using associativity:

$$
N_{\alpha,\beta,\gamma}^{\lambda}
=
\sum_{\nu\vdash|\alpha|+|\beta|}
c_{\alpha,\beta}^{\nu}
c_{\nu,\gamma}^{\lambda}.
$$

The implementation generates possible intermediate partitions $\nu$ and evaluates the two ordinary LR coefficients for each one.

#### 3.4. Socle multiplicities

The principal function

`CalcSoc(k, lam, lamP, mu, muP)`

implements the defining multiplicity formula.

For every admissible degree splitting, it generates the corresponding partitions $\delta,\gamma$ and calculates

$$
N_{\delta,\gamma,\lambda'}^\lambda
N_{\delta,\gamma,\mu'}^\mu.
$$

All these products are summed to obtain

$$
S_k^{\lambda,\mu}(\lambda',\mu').
$$

The original function also prints the ordered pairs $(\delta,\gamma)$ giving nonzero contributions.

This is mathematically useful because it identifies the factorizations responsible for a particular summand.

#### 3.5. Layer decomposition and LaTeX generation

The original notebook includes several formatting functions:

- `DirectSumMethod(k, lam, mu)` constructs the formal direct-sum decomposition for one layer.
- `MakeTable(k, lam, mu)` prints a LaTeX table.
- `MakeTable_tex(lam, mu, filename)` writes a table to a file.
- `generateTables(n, m)` computes tables for partitions of specified degrees.
- `le_generateTables(max_m, max_n)` iterates over degree pairs and invokes the table generator.

The original `MakeTable_tex` starts at $k=0$ and stops when it encounters an empty row. Thus it assumes that a zero row marks the end of the relevant decomposition.

The optimized implementation removes this stopping assumption and explicitly examines all admissible degrees.

#### 3.6. Main limitations

The original algorithm is transparent and follows the mathematical definition closely, but it is computationally expensive.

Its main costs arise from repeated enumeration of:

1. Candidate partitions $\lambda'$ and $\mu'$.
2. Degree splittings for $\delta$ and $\gamma$.
3. Partitions $\delta,\gamma$ for every splitting.
4. Intermediate partitions required by generalized LR coefficients.
5. LR coefficients that have already been computed elsewhere.

Many candidates necessarily produce zero coefficients.

The original implementation remains valuable as a reference for understanding the defining sum and validating alternative algorithms.

---

### 4. Optimizing the Computation

**Primary file:** `hoyt_optimized.ipynb`

The optimized implementation uses associativity and the Schur-function coproduct to reorganize the original calculation.

Rather than independently recomputing every generalized LR coefficient, it separates the calculation into reusable components.

#### 4.1. Factorization of the multiplicity formula

Recall that

$$
N_{\delta,\gamma,\lambda'}^\lambda
=
\sum_{\nu\vdash k}
c_{\delta,\gamma}^{\nu}
c_{\nu,\lambda'}^\lambda.
$$

Substituting this identity into the multiplicity formula gives

$$
\begin{aligned}
S_k^{\lambda,\mu}(\lambda',\mu')
={}&
\sum_{\nu,\omega\vdash k}
c_{\nu,\lambda'}^\lambda
c_{\omega,\mu'}^\mu\\
&\quad\cdot
\sum_{|\delta|+|\gamma|=k}
c_{\delta,\gamma}^{\nu}
c_{\delta,\gamma}^{\omega}.
\end{aligned}
$$

Define the common LR kernel

$$
\boxed{
K_k(\nu,\omega)
=
\sum_{|\delta|+|\gamma|=k}
c_{\delta,\gamma}^{\nu}
c_{\delta,\gamma}^{\omega}.
}
$$

Then

$$
\boxed{
S_k^{\lambda,\mu}(\lambda',\mu')
=
\sum_{\nu,\omega\vdash k}
c_{\nu,\lambda'}^\lambda
K_k(\nu,\omega)
c_{\omega,\mu'}^\mu.
}
$$

The important observation is that $K_k(\nu,\omega)$ depends only on the two intermediate partitions, not on the outer partitions or the residual summands.

It can therefore be computed once and reused.

#### 4.2. Sparse coproducts

The Schur coproduct satisfies

$$
\Delta(s_\lambda)
=
\sum_{\alpha,\beta}
c_{\alpha,\beta}^{\lambda}
s_\alpha\otimes s_\beta.
$$

The optimized notebook obtains these coefficients through SageMath's `lrcalc.coprod` implementation.

Only nonzero coefficients are stored.

For each partition $\lambda$, its coproduct is represented as a sparse mapping

$$
(\alpha,\beta)\longmapsto c_{\alpha,\beta}^{\lambda}.
$$

The core functions are:

`coproduct(p)`: returns the sparse LR coproduct of $p$.

`coproduct_by_right(p, k)`: groups nonzero coproduct entries according to their right-hand factor, restricting the left-hand factor to degree $k$.

`kernel(nu, omega)`: evaluates the common LR kernel as a sparse dot product.

`row_data(k, lam, mu)`: constructs the nonzero summand multiplicities in layer $k$.

`max_degree(lam, mu)`: finds the largest index with a nonzero row.

The implementation uses memoization to avoid repeating previously computed coproducts and kernels.

#### 4.3. Why the optimized version is more efficient

The optimization relies on three ideas.

**Sparse evaluation.** Only LR coefficients that are nonzero are propagated through the calculation.

**Reusable intermediate data.** Coproducts and kernels are cached across different outer partitions and layers.

**Algebraic factorization.** The computation follows the factorized formula instead of repeatedly evaluating the original nested sums.

These changes reduce redundant LR evaluations, particularly when generating many tables involving partitions of similar degrees.

The asymptotic or practical speedup depends on the input partitions and cache state; it should be measured rather than assumed to have a fixed factor.

#### 4.4. Table generation

The optimized version includes:

`direct_sum(k, lam, mu)`

`table_tex(lam, mu, include_zeros=False)`

`write_table(lam, mu, filename, ...)`

`generate_tables(max_lam_degree, max_mu_degree, filename, ...)`

Unlike the original table generator, the optimized implementation scans

$$
0\le k\le\min(|\lambda|,|\mu|)
$$

rather than stopping at the first empty row.

The `include_zeros` option controls whether zero layers are displayed.

The `exploit_symmetry` option avoids some duplicate calculations using the symmetry between $\lambda$ and $\mu$.

#### 4.5. Standalone LaTeX output

**File:** `hoyt_optimized_compilable_latex.ipynb`

This notebook extends the optimized implementation with complete LaTeX document generation.

Instead of exporting isolated table fragments, it can generate a standalone article containing the required preamble, title, author, tables, and document environment.

This is useful for producing collections of examples that can be compiled directly or imported into Overleaf.

---

### 5. Validation and Benchmarking

Several additional notebooks were developed to ensure that the optimization preserves the original mathematical quantities.

**Relevant files:**

- `hoyt_targeted_optimizations.ipynb`
- `hoyt_large_scale_regression.ipynb`
- `hoyt_three_way_table_benchmark.ipynb`
- `hoyt_with_verification.ipynb`

The targeted implementation retains the structure and interfaces of the original code while introducing caching, more selective partition enumeration, and other local improvements.

The redesigned implementation instead uses the sparse coproduct factorization described above.

The three-way benchmark compares:

1. The original implementation.
2. The targeted optimized implementation.
3. The redesigned coproduct-based implementation.

The benchmark distinguishes cold and warm execution, since memoization changes performance substantially.

It also compares actual multiplicities, including zero and nonzero entries, rather than treating matching output formatting as mathematical verification.

These checks establish agreement for tested inputs, not a universal correctness proof. The general factorization identity above supplies the mathematical justification for the redesigned algorithm.

---

### 6. Investigating the Highest Nonzero Layer

**Primary file:** `hoyt_optimized_top_layer_beta_explorer.ipynb`

Once full layer tables could be computed more efficiently, the research shifted toward understanding their highest nonzero layer.

For a fixed pair $(\lambda,\mu)$, we want to determine:

- The value of $k_{\max}(\lambda,\mu)$.
- Which pairs $(\lambda',\mu')$ occur in that layer.
- Their multiplicities.
- Which ordered LR factor pairs $(\delta,\gamma)$ contribute to each summand.
- Whether particular partitions occur among those factors.

#### 6.1. Top-layer explorer

The explorer provides functions including:

`show_top_layer(lam, mu)`: displays all nonzero summands in the maximum layer.

`inspect_top_pair(lam, mu, ...)`: examines one selected summand.

`pair_contributions(lam, mu, lp, mp, ...)`: returns the nonzero ordered LR-factor contributions.

`beta_membership(selection, beta)`: checks whether a proposed partition occurs as $\delta$ or $\gamma$.

`check_beta(lam, mu, beta, ...)`: combines selection and membership inspection.

Each contribution has the form

$$
N_{\delta,\gamma,\lambda'}^\lambda
N_{\delta,\gamma,\mu'}^\mu.
$$

The explorer verifies that the sum of the displayed contributions equals the optimized multiplicity.

#### 6.2. The intersection-participation question

An early conjecture concerned the intersection

$$
\rho=\lambda\cap\mu.
$$

We considered whether $\rho$ necessarily appears as one of the common factors in the highest nonzero layer.

Two versions were distinguished.

**Strong intersection property:** For every nonzero summand $(\lambda',\mu')$ in the highest layer, at least one contributing pair satisfies

$$
\delta=\rho
\qquad\text{or}\qquad
\gamma=\rho.
$$

**Weak intersection property:** At least one summand in the highest layer admits such a pair.

These questions concern the *individual factors* contributing at the maximum layer. They are different from asking whether $\rho$ guarantees some nonzero layer.

The strong property does not hold universally. The weak property is also false in general.

For example, consider

$$
\lambda=(2,2,2),
\qquad
\mu=(3,3).
$$

Their intersection is

$$
\rho=(2,2),
$$

but

$$
k_{\max}(\lambda,\mu)=6.
$$

At degree six, the pair

$$
\delta=\gamma=(2,1)
$$

contributes positively, since

$$
c_{(2,1),(2,1)}^{(2,2,2)}>0,
\qquad
c_{(2,1),(2,1)}^{(3,3)}>0.
$$

Neither factor equals $\rho$.

This observation motivated the transition from intersection-based descriptions toward common LR-factor supports.

---

### 7. The Common LR-Factor Formulation

The main conceptual simplification is that nonvanishing of a layer can be characterized entirely through ordinary LR coefficients.

Define

$$
\mathcal C(\nu,\omega)
=
\sum_{\delta,\gamma}
c_{\delta,\gamma}^{\nu}
c_{\delta,\gamma}^{\omega},
$$

for partitions $\nu,\omega$ of equal degree.

Because LR coefficients are nonnegative,

$$
\mathcal C(\nu,\omega)>0
$$

if and only if $\nu$ and $\omega$ admit at least one common ordered LR-factor pair.

Associativity gives the exact characterization

$$
\boxed{
k_{\max}(\lambda,\mu)
=
\max\left\{
k:
\begin{array}{l}
\exists\,\nu\subseteq\lambda,\;
\omega\subseteq\mu,\\
|\nu|=|\omega|=k,\\
\mathcal C(\nu,\omega)>0
\end{array}
\right\}.
}
$$

This reformulation no longer requires the intersection partition to occur as an LR factor.

It asks instead whether two Young-diagram containment regions support a common LR factorization at a given degree.

---

### 8. Established Results for the Maximum Layer

#### 8.1. Universal bounds

Let

$$
\rho=\lambda\cap\mu.
$$

Then

$$
\boxed{
|\rho|
\le
k_{\max}(\lambda,\mu)
\le
\min\{|\lambda|,|\mu|,2|\rho|\}.
}
$$

The lower bound follows by taking

$$
\delta=\rho,
\qquad
\gamma=\varnothing.
$$

The upper bound follows because any common LR factors must individually be contained in both outer partitions.

In particular, if either outer partition contains the other, then

$$
\boxed{
k_{\max}(\lambda,\mu)
=
\min\{|\lambda|,|\mu|\}.
}
$$

This does not imply that the intersection occurs as a factor at the maximum layer for arbitrary incomparable partitions.

#### 8.2. Conjugation symmetry

The LR conjugation identity implies

$$
\boxed{
k_{\max}(\lambda,\mu)
=
k_{\max}(\lambda^{\mathsf T},\mu^{\mathsf T}).
}
$$

The maximum layer is also symmetric under exchanging the two input partitions:

$$
k_{\max}(\lambda,\mu)
=
k_{\max}(\mu,\lambda).
$$

#### 8.3. One-row formula

If $\lambda=(a)$, then

$$
\boxed{
k_{\max}((a),\mu)
=
\min\{a,\mu_1+\mu_2\}.
}
$$

This follows from Pieri's rule:

$$
s_{(d)}s_{(g)}
=
\sum_{j=0}^{\min(d,g)}
s_{(d+g-j,j)}.
$$

The product of two single-row Schur functions has only constituents with at most two rows.

Conversely, every two-row partition of a given degree can be obtained in an appropriate such product.

By conjugation, if $\lambda=(1^a)$,

$$
\boxed{
k_{\max}((1^a),\mu)
=
\min\{a,\mu_1^{\mathsf T}+\mu_2^{\mathsf T}\}.
}
$$

#### 8.4. Two-row formula

For

$$
\lambda=(a,b),
\qquad a\ge b\ge0,
$$

the constructive two-row result is

$$
\boxed{
k_{\max}((a,b),\mu)
=
\min\left\{
a+b,\,
\mu_1+\mu_2+
\min(b,\mu_3+\mu_4)
\right\}.
}
$$

The proof uses a common-factor criterion.

For $\nu=(A,B)$ and $|\omega|=A+B$, a common pair of LR factors exists precisely when

$$
\ell(\omega)\le4
$$

and

$$
\omega_3+\omega_4\le B.
$$

Necessity follows from LR containment and row-tail inequalities.

The constructive sufficiency argument decomposes the columns of $\omega$ into elementary blocks and combines explicit LR witnesses using the LR semigroup property.

The accompanying file

`hoyt_two_row_constructive_proof.py`

contains the finite base-case witnesses and checks the construction on small partitions.

In particular, if both $\lambda$ and $\mu$ have at most two rows,

$$
\boxed{
k_{\max}(\lambda,\mu)
=
\min\{|\lambda|,|\mu|\}.
}
$$

The two-row result is supported by a constructive argument and finite verification. A publication-level presentation should retain the complete base-witness table and the interval-combination justification, rather than relying on numerical checks alone.

#### 8.5. General row-tail bounds

Define

$$
P_t(\lambda)=\sum_{i=1}^{t}\lambda_i,
\qquad
R_t(\lambda)=\sum_{i>t}\lambda_i.
$$

For every integer $t\ge0$,

$$
\boxed{
k_{\max}(\lambda,\mu)
\le
P_{2t}(\mu)+R_t(\lambda).
}
$$

By symmetry, we also obtain

$$
k_{\max}(\lambda,\mu)
\le
P_{2t}(\lambda)+R_t(\mu).
$$

Applying these inequalities after conjugation provides analogous column-based bounds.

They are not always exact.

For example,

$$
\lambda=(3,3,3),
\qquad
\mu=(6,1,1,1)
$$

has

$$
k_{\max}(\lambda,\mu)=8,
$$

while the row-tail bounds permit degree nine.

This shows that the geometry of LR factorizations cannot always be captured by simple row-capacity inequalities.

---

### 9. Superadditivity and Stability

#### 9.1. Superadditivity

For componentwise partition addition,

$$
\boxed{
k_{\max}(\lambda+\alpha,\mu+\beta)
\ge
k_{\max}(\lambda,\mu)
+
k_{\max}(\alpha,\beta).
}
$$

The proof follows from the LR semigroup property.

If two common-factor witnesses exist for $(\lambda,\mu)$ and $(\alpha,\beta)$, then their componentwise sums give a valid witness for $(\lambda+\alpha,\mu+\beta)$.

This property provides a useful algebraic structure for studying maximum layers under stretching and decomposition.

#### 9.2. One-box stability

Suppose $\Lambda$ is obtained from $\lambda$ by adding one box.

Then

$$
\boxed{
0
\le
k_{\max}(\Lambda,\mu)-k_{\max}(\lambda,\mu)
\le1.
}
$$

Monotonicity follows from containment.

The upper bound is obtained by removing the added corner from an appropriate LR constituent and applying Schur-function branching to shorten one common factor.

Iterating gives

$$
0\le
k_{\max}(\Lambda,\mu)-k_{\max}(\lambda,\mu)
\le|\Lambda|-|\lambda|
$$

whenever $\lambda\subseteq\Lambda$.

This makes $k_{\max}$ a stable function on the Young lattice.

#### 9.3. Consecutive nonzero layers

If a nonzero common-factor witness exists at degree $k>0$, LR branching can be used to remove a corner from one of its factors and produce a common-factor witness at degree $k-1$.

Consequently, the set of nonzero layer indices is an initial interval:

$$
\{k:\mathcal L_k^{\lambda,\mu}\neq0\}
=
\{0,1,\ldots,k_{\max}(\lambda,\mu)\}.
$$

This also justifies using monotone feasibility tests to locate the maximum layer.

---

### 10. Exact Character-Theoretic Computation

**File:** `hoyt_inductive_top_layer.py`

We developed an independent formulation using irreducible characters of symmetric groups.

For partitions $\nu,\omega$ of degree $n$,

$$
\boxed{
\mathcal C(\nu,\omega)
=
\sum_{\pi\vdash n}
\frac{2^{\ell(\pi)}}{z_\pi}
\chi^\nu(\pi)\chi^\omega(\pi),
}
$$

where $\chi^\nu$ is the irreducible character of $S_n$ indexed by $\nu$, and

$$
z_\pi
=
\prod_{j\ge1}
j^{m_j(\pi)}m_j(\pi)!.
$$

The formula follows from the Schur coproduct, orthogonality under the Hall inner product, and the Frobenius character expansion.

The characters can be evaluated recursively through the Murnaghan–Nakayama rule:

$$
\chi^\nu((q,\widehat\pi))
=
\sum_{\substack{\tau\subseteq\nu\\
\nu/\tau\text{ a rim hook of size }q}}
(-1)^{\operatorname{ht}(\nu/\tau)}
\chi^\tau(\widehat\pi).
$$

The base case is

$$
\chi^\varnothing(\varnothing)=1.
$$

This gives an exact recursive method for computing common LR overlaps and therefore $k_{\max}$ for arbitrary partitions.

It is an induction on partition degree, not a closed formula for every possible row count.

The character formulation also provides an independent way to check the coproduct-based computations.

---

### 11. Finite Generation and Asymptotic Behavior

#### 11.1. Common LR-support semigroup

For a fixed row bound $r$, define

$$
\mathfrak C_r
=
\left\{
(\nu,\omega):
\begin{array}{l}
\ell(\nu),\ell(\omega)\le r,\\
|\nu|=|\omega|,\\
\mathcal C(\nu,\omega)>0
\end{array}
\right\}.
$$

The LR semigroup property implies that $\mathfrak C_r$ is closed under componentwise addition.

Using the rational polyhedral description of LR positivity through Horn or hive inequalities, together with LR saturation and Gordan's lemma, one obtains finite generation for fixed $r$.

Thus there is a finite collection of common-factor pairs

$$
G_r
=
\{(u_1,v_1),\ldots,(u_s,v_s)\}
$$

whose nonnegative integer combinations generate $\mathfrak C_r$.

This provides a different perspective on the maximum-layer problem: rather than directly enumerating all LR factorizations for every input, one can study generators of the common-support semigroup.

#### 11.2. Integer optimization formulation

Let

$$
w_j=|u_j|=|v_j|.
$$

For a sufficiently large fixed row bound, the maximum layer can be expressed as

$$
\boxed{
k_{\max}(\lambda,\mu)
=
\max_{\mathbf t\in\mathbb Z_{\ge0}^s}
\sum_{j=1}^s w_jt_j
}
$$

subject to the componentwise constraints

$$
\sum_{j=1}^s t_j u_j\subseteq\lambda,
\qquad
\sum_{j=1}^s t_j v_j\subseteq\mu.
$$

The difficulty shifts to identifying efficient generating sets, especially when the number of rows grows.

#### 11.3. Asymptotic maximum layer

Define the stretched partitions

$$
N\lambda=(N\lambda_1,N\lambda_2,\ldots).
$$

Superadditivity gives

$$
k_{\max}((N+M)\lambda,(N+M)\mu)
\ge
k_{\max}(N\lambda,N\mu)
+
k_{\max}(M\lambda,M\mu).
$$

Since the sequence grows at most linearly, Fekete's lemma implies that

$$
\boxed{
\kappa(\lambda,\mu)
=
\lim_{N\to\infty}
\frac{k_{\max}(N\lambda,N\mu)}{N}
}
$$

exists.

The finite-generation formulation further identifies this limit with the optimum of a rational linear-programming relaxation.

In particular,

$$
\boxed{
\kappa(\lambda,\mu)\in\mathbb Q.
}
$$

For a fixed input pair and a fixed finite generating set, the integer and relaxed optima also differ by a bounded additive amount under stretching.

This suggests that asymptotic maximum layers may be more amenable to polyhedral methods than exact finite-degree layers.

---

### 12. Computational Research and Experiments

**Relevant files:**

- `hoyt_top_layer_pattern_study.py`
- `hoyt_two_row_formula_study.py`
- `hoyt_two_row_constructive_proof.py`
- `hoyt_ten_research_tracks.py`
- `hoyt_ten_research_tracks_results.json`
- `hoyt_inductive_study_9.json`

We conducted several finite-degree investigations to test possible formulas and identify counterexamples.

These include:

**Intersection bounds.** Comparing the exact maximum layer with

$$
\min\{|\lambda|,|\mu|,2|\lambda\cap\mu|\}.
$$

**Two-row formulas.** Exhaustively testing the proposed formula for partitions with at most two rows against LR positivity calculations.

**Three-row behavior.** Searching for cases where row-tail inequalities fail to determine the maximum.

**Stability.** Checking how the maximum changes when a single box is added.

**Superadditivity.** Testing the componentwise partition-addition inequality.

**Stretching and saturation.** Comparing common-factor support before and after scaling partitions.

**Common-factor diversity.** Investigating the different LR factorizations that can attain the same maximum layer.

The exact degree ranges and case counts are recorded in the experiment scripts and JSON output.

These computations are finite tests. They are useful for discovering and falsifying conjectures but are not substitutes for proofs.

---

### 13. Common-Factor Saturation

One of our principal open questions concerns saturation of common LR support.

Suppose $\nu,\omega$ are partitions of equal degree.

We ask whether

$$
\boxed{
\mathcal C(N\nu,N\omega)>0
\quad\Longrightarrow\quad
\mathcal C(\nu,\omega)>0
}
$$

holds for every positive integer $N$.

The reverse implication follows from the LR semigroup property.

The question is therefore whether common-factor positivity is invariant under simultaneous stretching.

Ordinary LR coefficients satisfy the Knutson–Tao saturation theorem:

$$
c_{N\alpha,N\beta}^{N\lambda}>0
\iff
c_{\alpha,\beta}^{\lambda}>0.
$$

However, this does not immediately settle common-factor saturation, because the common factors found for $N\nu$ and $N\omega$ need not be multiples of $N$.

Likewise, finite generation of the common-support semigroup does not automatically imply that the semigroup is saturated.

The common-factor saturation question remains open within this investigation.

A potential approach is to study the projection of the intersection of two LR/Horn cones and determine whether the integer points in that projection always lift to integral common factors.

---

### 14. Additional Questions Beyond the Maximum Layer

Although most of the theoretical investigation has focused on $k_{\max}$, the complete multiplicity data supports several other research directions.

#### 14.1. Number of distinct top-layer summands

Define

$$
D(\lambda,\mu)
=
\#\left\{
(\lambda',\mu'):
S_{k_{\max}}^{\lambda,\mu}(\lambda',\mu')>0
\right\}.
$$

Can $D(\lambda,\mu)$ be characterized in terms of the outer partition shapes?

Which partitions yield exactly one top-layer summand?

#### 14.2. Multiplicity-free top layers

For which pairs $(\lambda,\mu)$ do we have

$$
S_{k_{\max}}^{\lambda,\mu}(\lambda',\mu')
\in\{0,1\}
$$

for every $\lambda',\mu'$?

This is a natural classification problem related to multiplicity-free representation-theoretic decompositions.

#### 14.3. Number of common LR factorizations

For fixed $\nu,\omega$, define

$$
F(\nu,\omega)
=
\#\left\{
(\delta,\gamma):
c_{\delta,\gamma}^{\nu}
c_{\delta,\gamma}^{\omega}>0
\right\}.
$$

Unlike $\mathcal C(\nu,\omega)$, this counts distinct ordered common-factor pairs without weighting them by their LR multiplicities.

Studying $F$ could reveal patterns not visible from the maximum degree alone.

#### 14.4. Equality in superadditivity

Determine when

$$
k_{\max}(\lambda+\alpha,\mu+\beta)
=
k_{\max}(\lambda,\mu)+k_{\max}(\alpha,\beta).
$$

Characterizing equality may reveal how optimal common LR factorizations combine.

#### 14.5. Stability and Young-lattice geometry

Classify the circumstances under which adding one box increases the maximum layer:

$$
k_{\max}(\Lambda,\mu)
=
k_{\max}(\lambda,\mu)+1.
$$

Alternatively, determine when the maximum remains unchanged.

#### 14.6. Minimal semigroup generators

Compute or characterize minimal generating sets for $\mathfrak C_r$.

The three-row case is a particularly interesting target, because simple row-tail formulas first fail there.

---

### 15. Current Research Priorities

Our immediate research program has several complementary objectives.

**Priority A — Common-factor saturation**

Attempt to prove or disprove saturation of the common LR-support relation, beginning with small row bounds and translating the problem into Horn or hive feasibility.

**Priority B — Three-row common LR supports**

Determine which additional compatibility conditions are needed when one constituent has three rows.

Use the known counterexamples to test any proposed criterion.

**Priority C — Finite generation and optimization**

Compute explicit common-support semigroup generators for small row bounds.

Study whether they lead to efficient integer-programming algorithms or new formulas for $k_{\max}$.

**Priority D — Asymptotic theory**

Investigate the rational stretching limit, equality cases, and quantitative bounds on the difference between finite-degree maxima and their linear-programming approximations.

**Priority E — Top-layer multiplicities**

Move beyond the maximum degree to study the number, shape, and multiplicities of the representations appearing in the highest layer.

---

### 16. Repository File Guide

| File | Purpose |
|---|---|
| `hoyt.ipynb` | Original direct SageMath implementation |
| `hoyt_targeted_optimizations.ipynb` | Local optimizations preserving the original approach |
| `hoyt_optimized.ipynb` | Redesigned sparse-coproduct implementation |
| `hoyt_optimized_compilable_latex.ipynb` | Standalone LaTeX table generation |
| `hoyt_large_scale_regression.ipynb` | Regression testing against the original calculation |
| `hoyt_three_way_table_benchmark.ipynb` | Comparison of original, targeted, and redesigned implementations |
| `hoyt_optimized_top_layer_explorer.ipynb` | Inspection of highest-layer summands |
| `hoyt_optimized_top_layer_beta_explorer.ipynb` | Investigation of individual LR factors and intersection participation |
| `hoyt_top_layer_pattern_study.py` | Exhaustive maximum-layer pattern searches |
| `hoyt_two_row_formula_study.py` | Computational study of the two-row formula |
| `hoyt_two_row_constructive_proof.py` | Finite LR witnesses for the constructive two-row argument |
| `hoyt_inductive_top_layer.py` | Character-based exact recursive calculation |
| `hoyt_ten_research_tracks.py` | Multiple computational investigations of structural properties |
| `hoyt_ten_research_tracks_results.json` | Recorded results of the research tracks |
| `lr_research_team/` | Research briefs, audits, and coordinated proof-development notes |
| `lr_paper/` | Formal mathematical manuscript and LaTeX source |

Several notebooks have additional corrected or presentation-specific variants. These preserve the same general research workflow but address particular output, interface, or benchmarking requirements.

The notebook calculations involving `lrcalc` require SageMath. The separate pure-Python research scripts can be run without a SageMath kernel, subject to their individual dependencies.

---

### 17. Mathematical Status and Verification

The project distinguishes four kinds of results.

**Proved mathematical statements:** Results accompanied by mathematical arguments, such as the common-factor reduction, general bounds, transposition symmetry, one-row formula, superadditivity, and one-box stability.

**Constructively established results:** Results supported by explicit finite LR witnesses and a general construction, notably the two-row formula.

**Computational observations:** Statements verified for specified finite degree ranges but not established universally.

**Open questions:** Statements for which no complete proof or counterexample has yet been obtained, notably common-factor saturation and a general closed formula for three-row or arbitrary-row partitions.

The project also contains a plan for formal verification in Lean. The current proofs have not been machine-checked in Lean.

The Python tests and SageMath comparisons provide independent computational evidence, but this should not be described as formal proof verification.

For publication, the proof arguments, computational claims, and assertions of novelty should be reviewed separately against the relevant literature.

---

### 18. References and Further Reading

The mathematical background draws on the theory of symmetric functions, Littlewood–Richardson coefficients, and representation theory.

Useful starting points include:

1. W. Fulton, *Young Tableaux: With Applications to Representation Theory and Geometry*.
2. I. G. Macdonald, *Symmetric Functions and Hall Polynomials*.
3. A. Knutson and T. Tao, *The Honeycomb Model of GL(n) Tensor Products I: Proof of the Saturation Conjecture*.
4. A. S. Buch, *The Saturation Conjecture (after A. Knutson and T. Tao)*.
5. A. Knutson, T. Tao, and C. Woodward, *A Positive Proof of the Littlewood–Richardson Rule Using the Octahedron Recurrence*.

The formal manuscript in `lr_paper/` develops the principal statements and their proofs in more detail.

---

### 19. Summary

This investigation began as a computational problem: evaluate generalized Littlewood–Richardson multiplicities and generate the associated layer decompositions efficiently.

The optimized Hoyt implementation made it practical to study much larger families of partition pairs, inspect their highest nonzero layers, and identify the LR factorizations responsible for individual summands.

The mathematical investigation then developed beyond direct computation.

We obtained exact formulas in the one-row and two-row cases, general structural inequalities, stability and superadditivity properties, a character-theoretic recursion, and a finite-generation framework with asymptotic consequences.

The current emphasis is no longer exclusively on determining the maximum nonzero layer. It is on understanding the structure of common Littlewood–Richardson supports, the multiplicities within the highest layer, and the algebraic and polyhedral properties governing their behavior.

These questions provide several independent directions for further research and connect the computational experiments to broader problems in algebraic combinatorics and representation theory.

---
