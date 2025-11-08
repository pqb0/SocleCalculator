# Calculation for $k$-th Socle Filtration using Sum of 4 partition Little Wood Coefficients.

This is the code I have developed using formula for filtration. Based on work with professor penkov at 

This is the code I have developed using formula for filtration. it combines the use of math.sage library for python and a simple algorithm developed by me!

## Method for Algorithm

We want to solve the problem of calculating the *$k$-th socle filtration*:  given by the sum: 

$$\left[ \text{soc}^k \ \mathcal{I}^{ \ \lambda , F, \mu} : V^{\lambda',F, \mu'}\right] = \sum_{2|\gamma| + |\delta| + p + q \ = \ k} N^\lambda_{\lambda', \gamma, \delta, 1^p} \ N^\mu_{\mu', \gamma, \delta, 1^q}$$
for given partitions: $\lambda, \lambda' \mu, \mu'$ such that:

$$ (I) : \quad
\begin{cases} 
      |\lambda| - |\lambda'| = |\gamma|+|\delta| + p \\
      |\mu| - |\mu'| = |\gamma|+|\delta| + q \\
      2|\gamma| + |\delta| + p + q \ = \ k 
\end{cases}
$$

To solve for possible partitions $\gamma, \delta, 1^p, 1^q$
where $1^q = (1, 1, ..., 1)$ is the partition with $q$ number of ones.
To do so generate the following sets:

$$\Lambda_1 = \lbrace \ \lambda' \ \text{  partitions: } |\lambda'| \le |\lambda| \ \rbrace$$
$$\mathcal{M}_1 = \lbrace \ \mu' \ \text{  partitions: } |\mu'| \le |\mu| \ \rbrace  $$


denote 

$$|\lambda|= k_1 \quad |\lambda'| = k_2 \quad |\mu| = k_3 \quad|\mu'| = k_4 $$

$$|\delta|= x_1 \quad |\gamma| = x_2 \quad p = x_3 \quad q = x_4 $$

And transform $(I)$ into:



We define function ``SolveOne()`` (Short for Solve System One) which takes as input $\lambda, \lambda' \mu, \mu'$

And solves the system $(I)$ to produce $\mathcal{L}_1$ defined by:

$$\mathcal{L}_1 := \lbrace \ \vec{x} = (\gamma, \delta, p, q) , \quad A\vec{x} = b \ \rbrace$$



_Explanation to be completed..._

