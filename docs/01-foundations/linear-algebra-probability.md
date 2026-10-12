---
title: Linear Algebra, Probability, Optimization
---

# Math Foundations

## Linear algebra

| Concept | Key facts |
|---|---|
| Vector space, basis, rank | rank = dim(column space); `rank(A)+nullity(A)=n` |
| Eigen-decomposition | $A v=\lambda v$; symmetric $A=Q\Lambda Q^\top$ with real λ, orthogonal Q |
| SVD | $A=U\Sigma V^\top$ for any matrix; singular values = √eig($A^\top A$); gives pseudo-inverse $A^+=V\Sigma^{+}U^\top$, low-rank approx (Eckart–Young), PCA |
| Positive definite | $x^\top A x>0$; all λ>0; Cholesky exists; covariance matrices are PSD |
| Orthogonal / rotation | $R^\top R=I$, $\det R=1$ (SO(3)) |
| Norms | $\ell_1$ sparsity, $\ell_2$ energy, Frobenius for matrices |
| Matrix calculus | $\nabla_x (a^\top x)=a$, $\nabla_x x^\top A x=(A+A^\top)x$, $\nabla_W \|Wx-y\|^2=2(Wx-y)x^\top$ |
| Condition number | $\kappa=\sigma_{max}/\sigma_{min}$; large → ill-posed (near-singular Jacobian!) |
| Least squares | $\min\|Ax-b\|^2 \Rightarrow x=(A^\top A)^{-1}A^\top b = A^+b$ |

**Robotics links:** Jacobian singularities = rank loss; SVD of Jacobian gives manipulability ellipsoid; EKF/Kalman use covariance algebra; ICP uses SVD (Kabsch).

## Probability & statistics

- **Bayes:** $p(\theta|D)=\dfrac{p(D|\theta)p(\theta)}{p(D)}$
- **Gaussian:** $\mathcal N(x;\mu,\Sigma)=\frac{1}{\sqrt{(2\pi)^n|\Sigma|}}\exp(-\tfrac12 (x-\mu)^\top\Sigma^{-1}(x-\mu))$. Closed under linear maps, marginalization, conditioning, product — *why Kalman filters work*.
- **Linear-Gaussian map:** $y=Ax+b \Rightarrow y\sim\mathcal N(A\mu+b,\ A\Sigma A^\top)$.
- **Expectation tricks:** $\mathrm{Var}(X)=E[X^2]-E[X]^2$; law of total variance; linearity of expectation.
- **MLE vs MAP:** MLE maximizes $p(D|\theta)$; MAP adds a prior (= regularization: Gaussian prior ↔ L2, Laplace ↔ L1).
- **KL divergence:** $D_{KL}(p\|q)=\sum p\log\frac pq\ge0$, asymmetric. Cross-entropy $H(p,q)=H(p)+D_{KL}(p\|q)$.
- **Entropy:** $H(p)=-\sum p\log p$; mutual information $I(X;Y)=H(X)-H(X|Y)$.
- **CLT / LLN**, confidence intervals, hypothesis tests (p-value = P(data at least this extreme | H0)), A/B tests.
- **Important distributions:** Bernoulli, Binomial, Poisson, Categorical, Gaussian, Beta (conjugate to Bernoulli), Dirichlet, von Mises (angles), Wishart.
- **Monte-Carlo:** $E[f(x)]\approx\frac1N\sum f(x_i)$, error $\propto 1/\sqrt N$. Importance sampling weights $w=p/q$. Particle filters = sequential importance resampling.
- **Markov chain / MDP basics:** stationary distribution, ergodicity, detailed balance (MCMC, Metropolis–Hastings).

## Optimization

| Topic | Notes |
|---|---|
| Convexity | f convex ⇒ every local min is global. Check Hessian ⪰ 0. |
| Gradient descent | $x\leftarrow x-\eta\nabla f$; converges at rate O(1/k) convex, linear if strongly convex. |
| Momentum / Nesterov | accelerate along consistent directions. |
| Newton | $x\leftarrow x-H^{-1}\nabla f$ — quadratic convergence, expensive. Quasi-Newton: BFGS / L-BFGS. |
| Gauss–Newton / LM | for $\min\|r(x)\|^2$: $(J^\top J+\lambda I)\delta=-J^\top r$ — **core of bundle adjustment, SLAM back-ends, IK** |
| Lagrangian / KKT | stationarity, primal/dual feasibility, complementary slackness. |
| LP / QP / SOCP / SDP | QP drives MPC & whole-body control; SDP drives SOS & quantum relaxations. |
| Non-convex deep nets | saddle points dominate; SGD noise helps; Adam adapts per-parameter lr. |
| Constrained NLP | SQP, interior point (IPOPT), ADMM; trajectory optimization uses these. |
| Black-box | CMA-ES, Bayesian optimization, random search (domain randomization tuning). |

### Quick derivation to know cold: Linear regression closed form

$L(w)=\tfrac12\|Xw-y\|^2 \Rightarrow \nabla L=X^\top(Xw-y)=0 \Rightarrow w=(X^\top X)^{-1}X^\top y$. With ridge: $(X^\top X+\lambda I)^{-1}X^\top y$ — always invertible.

## Interview Q&A

**Why is covariance symmetric PSD?** $\Sigma=E[(x-\mu)(x-\mu)^\top]$; for any v, $v^\top\Sigma v=\mathrm{Var}(v^\top x)\ge0$.

**When does least squares fail?** Rank-deficient $X^\top X$, outliers (use Huber/RANSAC), heteroscedastic noise (weighted LS).

**Why does L1 give sparsity?** Diamond-shaped constraint touches loss contours at axes; subgradient at 0 is an interval so weights can sit exactly at zero.

**Difference between probability and likelihood?** Probability: data varies, params fixed. Likelihood: data fixed, params vary; it is not a distribution over θ.

**Why Gauss–Newton over Newton?** Ignores second-derivative-of-residual term; $J^\top J$ is PSD and cheap, great when residuals are small.
