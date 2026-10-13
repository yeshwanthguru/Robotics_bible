---
title: "More Math: Numerics, Graphical Models, Information Theory"
---

# More Math: Numerical Methods, Graphical Models and Information Theory

:::tip[The 30-second version]
Three extra toolkits that keep reappearing: **numerical methods** (how computers actually solve equations, and why they sometimes get them wrong), **graphical models** (drawing which quantities depend on which, so inference becomes systematic), and **information theory** (measuring uncertainty and surprise). SLAM, filters, generative models and RL all rest on them.
:::

## 1. Numerical methods: how computers do maths

### Floating-point numbers
Computers store real numbers with limited precision, so results carry **round-off error**.

| Format | Bits | Typical use |
|---|---|---|
| **fp64 (double)** | 64 | scientific computing, estimation |
| **fp32 (float)** | 32 | graphics, most simulation |
| **fp16 / bf16** | 16 | deep learning (bf16 keeps fp32's range) |
| **int8 / int4** | 8 / 4 | quantised inference |

**Rules of thumb:** never compare floats with `==`; subtracting nearly equal numbers loses precision (catastrophic cancellation); summing many numbers is more accurate with pairwise or Kahan summation; unit quaternions drift off unit length and need renormalising.

### Solving linear systems $Ax=b$
| Method | When |
|---|---|
| **LU decomposition** | general square systems |
| **Cholesky** | symmetric positive-definite (covariance, normal equations): fastest and stable |
| **QR** | least squares, better conditioned than normal equations |
| **SVD** | rank-deficient or ill-conditioned problems (pseudo-inverse) |
| **Conjugate gradient** | huge sparse SPD systems (iterative) |
| **Sparse Cholesky / QR** | SLAM and bundle adjustment normal equations |

> **Never compute an explicit inverse** to solve a system. Use a factorisation: it is faster and more accurate (MATLAB `A\b`, NumPy `np.linalg.solve`).

**Condition number** κ tells how much input error is amplified: expect to lose about log₁₀ κ digits.

### Root finding and optimisation
- **Newton's method:** repeatedly follow the tangent; converges quadratically near the root but needs derivatives and a good start.
- **Gauss–Newton / Levenberg–Marquardt:** Newton for least squares; LM adds damping to blend with gradient descent.
- **Quasi-Newton (BFGS, L-BFGS):** build a Hessian approximation from gradients.
- **Line search and trust region:** make sure each step actually decreases the cost.

### Integrating ODEs (simulation and dynamics)
Robot dynamics and simulators step forward in time with a numerical integrator.

| Method | Order | Notes |
|---|---|---|
| **Explicit Euler** | 1 | simple, can gain energy and blow up |
| **Semi-implicit (symplectic) Euler** | 1 | better energy behaviour; common in games and physics engines |
| **Runge–Kutta 4 (RK4)** | 4 | accurate for smooth systems |
| **Implicit methods (backward Euler)** | 1+ | stable for stiff systems (contacts, stiff springs) |

**Time step trade-off:** small steps are accurate but slow; large steps are fast but unstable. Contact-rich simulation often needs sub-stepping.

### Interpolation and splines
Linear, cubic and B-splines, and quintic polynomials produce smooth trajectories through waypoints; quintic gives continuous acceleration with zero velocity/acceleration at the ends.

### Automatic differentiation
Computes exact derivatives by applying the chain rule to the program itself (forward mode for few inputs, reverse mode for many inputs = backpropagation). Used in PyTorch, JAX, CasADi, differentiable simulators.

## 2. Graphical models: pictures of dependence

A **graphical model** draws variables as nodes and dependencies as edges, so you can compute with large probability distributions piece by piece.

| Model | Graph | Example |
|---|---|---|
| **Bayesian network** | directed acyclic | cause → effect diagnosis |
| **Markov random field** | undirected | image denoising, spatial fields |
| **Hidden Markov model** | chain of hidden states + observations | speech, gesture, gait phases |
| **Kalman filter / state-space model** | continuous HMM | tracking, localisation |
| **Factor graph** | variables + factors (constraints) | SLAM, bundle adjustment (GTSAM) |

**Inference** means computing probabilities of unknowns given observations:
- **Exact:** variable elimination, belief propagation on trees (forward–backward, Viterbi for HMMs).
- **Approximate:** loopy belief propagation, **MCMC** (Metropolis–Hastings, Gibbs), **variational inference** (maximise the ELBO), **particle methods**.

### Conjugate priors (handy shortcuts)
| Likelihood | Conjugate prior | Meaning |
|---|---|---|
| Bernoulli / binomial | Beta | success-rate estimation with a prior |
| Categorical | Dirichlet | probabilities over classes |
| Gaussian (known variance) | Gaussian | Kalman-style update |

> **In words:** with a conjugate prior the posterior has the same shape as the prior, so Bayesian updating is just adding counts or averaging means.

### MCMC in one paragraph
Run a random walk whose long-run visits follow the target distribution. **Metropolis–Hastings:** propose a move, accept with probability min(1, target(new)/target(old)) (for symmetric proposals). Samples are correlated, so check burn-in and effective sample size.

### Variational inference and the ELBO
Replace the hard posterior with a simple distribution q and maximise the **evidence lower bound**, $\mathrm{ELBO}=\mathbb E_q[\log p(x|z)]-D_{KL}(q(z)\,\|\,p(z))$.

> **In words:** "reconstruct the data well, but keep your explanation close to the prior." This is exactly the VAE loss.

## 3. Information theory

| Quantity | Meaning | Where used |
|---|---|---|
| **Entropy** $H=-\sum p\log p$ | average surprise / uncertainty | decision trees, SAC entropy bonus |
| **Cross-entropy** $H(p,q)$ | cost of coding p with a model q | classification and language-model losses |
| **KL divergence** | extra cost from using q instead of p | VAEs, RLHF, PPO trust regions |
| **Mutual information** | how much one variable tells about another | feature selection, representation learning, active sensing |
| **Information gain** | entropy reduction from a measurement | tree splits, next-best-view planning |
| **Perplexity** $=e^{H}$ | effective number of choices | language models |

**Why cross-entropy is the loss:** minimising it is maximum-likelihood training, and its gradient with softmax is simply *prediction minus target*.

## Interview Q&A

**Why not invert a matrix to solve Ax = b?**
*Simply:* factorisations are faster and more accurate. *Deeper:* inversion amplifies round-off, especially for ill-conditioned matrices.

**Explicit versus implicit integrators?**
*Simply:* explicit steps are cheap but can blow up with stiff dynamics; implicit steps are stable but need a solve each step.

**What is MCMC for?**
*Simply:* sampling from distributions you can only evaluate up to a constant. *Deeper:* the chain's stationary distribution equals the target (detailed balance).

**Why is the ELBO a lower bound?**
*Simply:* by Jensen's inequality the log of an average is at least the average of the log, so it bounds the evidence from below.

**Entropy versus cross-entropy versus KL?**
*Simply:* cross-entropy = entropy + KL; minimising it makes the model's distribution match the data's.
