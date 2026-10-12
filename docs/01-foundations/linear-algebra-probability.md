---
title: Linear Algebra, Probability, Optimization
---

# Math Foundations (without the fear)

:::tip[The 30-second version]
Robotics math boils down to three ideas.
**Linear algebra** = how to move and stretch things in space (a robot arm, a camera view).
**Probability** = how to reason when sensors are noisy and you are never 100 % sure.
**Optimization** = how to find the best answer by repeatedly nudging a guess downhill.
Almost every algorithm in this book is one of these three wearing a costume.
:::

## 1. Linear algebra: moving things around

### Vectors and matrices
A **vector** is a list of numbers, such as a position `(x, y, z)` or all 7 joint angles of an arm. A **matrix** is a grid of numbers that acts like a *machine*: feed in a vector, get a transformed vector out.

![matrix transform](/img/fig/matrix-transform.svg)
*A matrix rotates, stretches or squashes the whole space. Red and green arrows show where the x and y directions end up.*

This is exactly what a rotation matrix does to a robot's frame, and what a camera does to the world.

### The ideas you must know

| Idea | Plain English | Where it appears in robotics |
|---|---|---|
| **Rank** | how many independent directions the matrix can really act in | Jacobian loses rank → robot arm is stuck at a *singularity* |
| **Eigenvectors / eigenvalues** | directions that the matrix only stretches, never turns | PCA, stability of control systems |
| **SVD** | any matrix = rotate → stretch → rotate | pseudo-inverse, ICP point-cloud alignment, PCA |
| **Positive definite** | "always positive energy", like a bowl shape | covariance matrices, inertia matrix |
| **Condition number** | how close a matrix is to being useless (singular) | near-singular arm configurations explode joint speeds |
| **Least squares** | best compromise when no exact answer exists | calibration, SLAM, regression |

### Least squares: the workhorse
When you have more equations than unknowns (noisy measurements), no solution is perfect. Least squares picks the one with the smallest total squared error.

$$ x^{*} = (A^\top A)^{-1} A^\top b $$

> **In words:** "find the answer that fits all the measurements as well as possible on average." This is how a robot fits a plane to a point cloud, or finds its pose from many noisy landmark sightings.

## 2. Probability: thinking with uncertainty

Sensors lie a little. A GPS says "you are here ± 3 m". Probability gives us a language for "how sure am I?"

### Bayes' rule: updating beliefs
$$ p(\text{state}\mid\text{data}) \;\propto\; p(\text{data}\mid\text{state})\; p(\text{state}) $$

> **In words:** *new belief = what the sensor says × what I believed before* (then renormalise).

![bayes update](/img/fig/bayes-update.svg)
*Blue = old belief, orange = new measurement, green = updated belief. It lands in between, closer to the more certain source.*

**Every filter in this book (Kalman, particle, SLAM) is this one picture repeated.**

### The Gaussian (bell curve)
A Gaussian is described by a **mean** (best guess) and a **covariance** (how spread out and how correlated the uncertainty is).

![gaussian covariance](/img/fig/gaussian-covariance.svg)
*The ellipse is the "cloud of doubt". A tilted ellipse means two quantities are correlated.*

Why robotics loves Gaussians: if you push a Gaussian through a *linear* function, you get another Gaussian, and you can compute it exactly. That is the whole reason the Kalman filter works.

$$ y = Ax + b \;\Rightarrow\; y \sim \mathcal N\big(A\mu + b,\; A\Sigma A^\top\big) $$

> **In words:** "the average moves like the data; the uncertainty cloud gets stretched the same way."

### More probability you will be asked
- **MLE vs MAP.** MLE: "which parameters make my data most likely?" MAP: same, but also use a prior belief. A Gaussian prior on weights equals **L2 regularisation**; a Laplace prior equals **L1**.
- **KL divergence.** A measure of how different two distributions are (not symmetric). Cross-entropy loss is KL plus a constant.
- **Monte-Carlo.** Estimate an average by random sampling; the error shrinks like $1/\sqrt{N}$. Particle filters are Monte-Carlo.
- **Entropy.** How surprised you are on average; used in RL (SAC) and information gain.

## 3. Optimization: finding the best answer

Training a network, solving inverse kinematics, aligning two scans: all are "find the inputs that minimise a cost".

### Gradient descent: walking downhill in fog
You can only feel the slope under your feet. So you step downhill, repeat.

$$ x \leftarrow x - \eta\,\nabla f(x) $$

> **In words:** "move a little bit opposite to the slope; η (the learning rate) is the step size."

![gradient descent](/img/fig/gradient-descent.svg)
*Left: tiny steps crawl. Middle: good steps. Right: huge steps overshoot and zig-zag.*

### The optimizer family tree

| Method | Plain idea | Used for |
|---|---|---|
| **SGD + momentum** | roll downhill like a ball with inertia | most deep learning |
| **Adam / AdamW** | each parameter gets its own step size | transformers, default choice |
| **Newton / BFGS** | use curvature to jump straight to the bottom | small smooth problems |
| **Gauss–Newton / Levenberg–Marquardt** | for "sum of squared errors": treat as repeated least squares | **SLAM, bundle adjustment, IK** |
| **LP / QP** | optimise with straight-line rules (constraints) | **MPC, whole-body control** |
| **CMA-ES / Bayesian opt.** | black-box: no gradients available | tuning domain randomization |

**Convex vs non-convex:** a convex problem is a single smooth bowl (one bottom, easy). Neural networks are bumpy landscapes with many dips; SGD noise helps escape bad ones.

**Constraints (KKT / Lagrange):** "minimise cost *while* staying inside limits". This is how a robot minimises effort while respecting joint limits and friction cones.

## Interview Q&A

**Why is a covariance matrix always positive semi-definite?**
*Simply:* variance can't be negative, in any direction. *Deeper:* for any direction $v$, $v^\top\Sigma v=\mathrm{Var}(v^\top x)\ge 0$.

**When does least squares fail?**
*Simply:* when a few measurements are wildly wrong (outliers) or the problem has too little information. *Deeper:* use RANSAC / Huber loss for outliers, regularise rank-deficient problems.

**Why does L1 regularisation give sparse solutions?**
*Simply:* its constraint region has pointy corners on the axes, so the best solution tends to land exactly on a corner (a weight = 0).

**Probability vs likelihood?**
*Simply:* probability: fix the model, ask about data. Likelihood: fix the data, ask which model fits.

**Why Gauss–Newton instead of Newton for SLAM?**
*Simply:* the cost is a sum of squares, so you can approximate the curvature cheaply from first derivatives only. It is faster and always well-behaved.

**What does a large condition number tell you?**
*Simply:* the problem is nearly broken; tiny noise gets hugely amplified. In robotics: the arm is near a singularity.
