---
title: "Q&A 1: Math, CS & Machine Learning"
---

# Interview Q&A: Math, CS & Machine Learning

:::tip[How to use]
Each question has a **Short answer** you can say in 20 seconds, then **Go deeper** for follow-ups. Press Ctrl+K to search any question. Chapter links: [Math](../01-foundations/linear-algebra-probability.md) · [CS](../01-foundations/cs-dsa-complexity.md) · [ML](../02-machine-learning/ml-fundamentals.md).
:::

## Linear algebra and probability

### Q: What is the rank of a matrix and why does it matter in robotics?
**Short answer:** Rank is the number of independent directions the matrix can act in. **Go deeper:** If a robot's Jacobian loses rank the arm is at a singularity: some hand motions become impossible and the inverse needs infinite joint speed.

### Q: What does SVD give you?
**Short answer:** It writes any matrix as rotate, stretch, rotate: A = UΣVᵀ. **Go deeper:** Singular values give stretch factors; SVD yields the pseudo-inverse, the best low-rank approximation (Eckart–Young), PCA, rigid alignment in ICP (Kabsch) and the manipulability ellipsoid of a Jacobian.

### Q: Why is a covariance matrix symmetric positive semi-definite?
**Short answer:** Variance can never be negative in any direction. **Go deeper:** For any vector v, vᵀΣv = Var(vᵀx) ≥ 0, and Σ = E[(x−μ)(x−μ)ᵀ] is symmetric by construction.

### Q: Explain eigenvalues and eigenvectors in one sentence.
**Short answer:** Eigenvectors are directions a matrix only stretches, and eigenvalues are the stretch factors. **Go deeper:** They determine stability (eigenvalues of a dynamics matrix) and principal directions (PCA).

### Q: What is the condition number and what does a big one mean?
**Short answer:** The ratio of largest to smallest singular value; large means nearly singular. **Go deeper:** Tiny noise gets amplified by about that factor, so solutions are unreliable; regularise (ridge, damped least squares).

### Q: Probability versus likelihood?
**Short answer:** Probability fixes the model and asks about data; likelihood fixes the data and asks which model fits. **Go deeper:** Likelihood is a function of parameters and is not a probability distribution over them.

### Q: Explain Bayes' rule and where it appears in robotics.
**Short answer:** New belief ∝ what the sensor says × what I believed before. **Go deeper:** Every Bayes filter (Kalman, particle, histogram) is this rule applied recursively.

### Q: MLE versus MAP?
**Short answer:** MLE picks the parameters that make the data most likely; MAP also multiplies by a prior. **Go deeper:** A Gaussian prior on weights equals L2 regularisation, a Laplace prior equals L1.

### Q: Why are Gaussians so popular in robotics?
**Short answer:** They are closed under linear maps, marginalisation and conditioning, so estimates stay exactly Gaussian. **Go deeper:** That closure is why the Kalman filter is optimal for linear-Gaussian systems; non-linear cases need EKF/UKF/particles.

### Q: What is KL divergence?
**Short answer:** A (non-symmetric) measure of how different two distributions are. **Go deeper:** KL(p‖q) ≥ 0, zero only if equal. Cross-entropy = entropy + KL, which is why minimising cross-entropy fits a distribution.

### Q: What does the central limit theorem say?
**Short answer:** Averages of many independent samples are approximately Gaussian. **Go deeper:** It justifies Gaussian noise assumptions and confidence intervals for means.

### Q: How does Monte-Carlo estimation scale?
**Short answer:** Error shrinks like 1/√N regardless of dimension. **Go deeper:** That dimension-independence is why sampling methods (particle filters, MCTS, MPPI) work in high dimensions where grids fail.

### Q: What is a p-value?
**Short answer:** The chance of data at least this extreme if the null hypothesis were true. **Go deeper:** It is not the probability the hypothesis is true; correct for multiple comparisons (Holm, Benjamini–Hochberg).

### Q: How do you compute a confidence interval for a robot success rate?
**Short answer:** Use a Wilson or exact binomial interval, not the naive one. **Go deeper:** 18/20 successes gives roughly 70 % to 97 %; small trial counts give wide intervals, so run ≥ 30–50 trials.

## Optimisation

### Q: Gradient descent: what does the learning rate do?
**Short answer:** It sets the step size downhill. **Go deeper:** Too small is slow; too large overshoots or diverges; schedules (warm-up, cosine) and adaptive optimisers help.

### Q: Why Adam over plain SGD?
**Short answer:** It gives each parameter its own step size, so it copes with ill-conditioned problems with little tuning. **Go deeper:** SGD with momentum can generalise slightly better in some vision tasks but needs careful tuning.

### Q: What is a convex problem and why do we like them?
**Short answer:** A single bowl-shaped problem: every local minimum is global. **Go deeper:** LP, QP, SOCP and SDP are solved reliably; MPC and whole-body control rely on QPs.

### Q: What is Gauss–Newton and why is it used in SLAM?
**Short answer:** It solves "sum of squared errors" problems by repeated linear least squares. **Go deeper:** It uses JᵀJ as the curvature, so it only needs first derivatives; Levenberg–Marquardt adds damping for robustness.

### Q: What are the KKT conditions?
**Short answer:** Necessary conditions for optimality with constraints: stationarity, feasibility, and complementary slackness. **Go deeper:** They underpin SQP and interior-point methods used in trajectory optimisation.

### Q: Why does L1 give sparsity but L2 doesn't?
**Short answer:** The L1 ball has pointy corners on the axes where optima tend to land. **Go deeper:** L1's subgradient at zero is an interval, so weights can sit exactly at zero; L2 only shrinks smoothly.

## CS and algorithms

### Q: A* versus Dijkstra?
**Short answer:** A* is Dijkstra with a distance-to-goal hint. **Go deeper:** Dijkstra is A* with heuristic 0; with an admissible, consistent heuristic A* is optimal and expands each node at most once.

### Q: What makes a heuristic admissible and consistent?
**Short answer:** Admissible never overestimates; consistent obeys the triangle inequality. **Go deeper:** Consistency implies admissibility and guarantees no re-expansions.

### Q: BFS versus DFS?
**Short answer:** BFS explores level by level and finds shortest paths on unweighted graphs; DFS goes deep first and uses less memory. **Go deeper:** DFS underlies topological sort and cycle detection.

### Q: What is dynamic programming?
**Short answer:** Solve overlapping sub-problems once and cache the answers. **Go deeper:** Value iteration, Viterbi decoding, edit distance and knapsack are examples; it needs optimal substructure.

### Q: Complexity of a KD-tree nearest-neighbour search?
**Short answer:** Roughly O(log n) on average in low dimensions. **Go deeper:** It degrades toward O(n) in high dimensions, so use approximate methods (HNSW) for embeddings.

### Q: Mutex versus semaphore?
**Short answer:** A mutex is a lock owned by one thread; a semaphore is a counter limiting concurrent access. **Go deeper:** Only the thread that locked a mutex may unlock it.

### Q: What are the four conditions for deadlock?
**Short answer:** Mutual exclusion, hold-and-wait, no preemption, circular wait. **Go deeper:** Break any one (e.g. lock ordering) to prevent deadlock.

### Q: What is priority inversion?
**Short answer:** A low-priority task holds a lock needed by a high-priority one, which is then blocked by medium tasks. **Go deeper:** Solve with priority inheritance (the Mars Pathfinder fix).

### Q: Why avoid `malloc` in a real-time loop?
**Short answer:** Its run time is unpredictable. **Go deeper:** It may take locks or request memory from the OS; pre-allocate and reuse memory.

### Q: TCP versus UDP?
**Short answer:** TCP is reliable and ordered; UDP is faster with no guarantees. **Go deeper:** Sensor streams and DDS use UDP-style transports with their own reliability options.

## Machine learning

### Q: Explain bias and variance.
**Short answer:** Bias is being too rigid to fit the pattern; variance is being so flexible you memorise noise. **Go deeper:** Error = bias² + variance + noise. Fix high bias with a richer model; fix high variance with more data, regularisation or bagging.

### Q: How do you detect overfitting?
**Short answer:** Training error keeps falling while validation error rises. **Go deeper:** Use learning curves, cross-validation and early stopping; check for data leakage if validation looks too good.

### Q: What is data leakage and how do you avoid it?
**Short answer:** Information from the test set or the future sneaks into training. **Go deeper:** Fit scalers only on training data, split by group (episode, user, scene), never shuffle time series randomly, and de-duplicate across splits.

### Q: Precision versus recall: which for a pedestrian detector?
**Short answer:** Recall, because a miss is a collision. **Go deeper:** Then reduce false alarms with temporal filtering and sensor fusion; choose the threshold from the PR curve.

### Q: What is the ROC curve and AUC?
**Short answer:** True-positive rate versus false-positive rate over thresholds; AUC is the area under it. **Go deeper:** For rare positives prefer the precision–recall curve.

### Q: How do you handle class imbalance?
**Short answer:** Reweight the loss, resample, or use focal loss; evaluate with PR-AUC or F1. **Go deeper:** SMOTE creates synthetic minority samples; threshold tuning often helps most.

### Q: Bagging versus boosting?
**Short answer:** Bagging averages independent models to cut variance; boosting trains models in sequence to cut bias. **Go deeper:** Random forest is bagging; XGBoost/LightGBM are boosting.

### Q: Why do gradient-boosted trees often beat neural nets on tabular data?
**Short answer:** Tables have mixed, irregular features and modest size where trees shine. **Go deeper:** Trees handle missing values, scale differences and sharp interactions without tuning.

### Q: Explain k-means and its weaknesses.
**Short answer:** Alternate assigning points to the nearest centre and moving centres to the mean. **Go deeper:** It needs k, assumes round clusters, depends on initialisation (use k-means++) and is sensitive to outliers.

### Q: What does PCA do?
**Short answer:** Projects data onto the directions with the most variance. **Go deeper:** Compute via SVD of the centred data; it is linear, so use UMAP/autoencoders for non-linear structure.

### Q: Explain the EM algorithm.
**Short answer:** Guess hidden assignments (E-step), refit parameters to them (M-step), repeat. **Go deeper:** It monotonically increases the likelihood but may reach a local optimum; GMM is the classic use.

### Q: What is calibration?
**Short answer:** Predicted probabilities match real frequencies. **Go deeper:** Measure with reliability diagrams/ECE; fix with temperature scaling or isotonic regression.

### Q: How do you cross-validate time-series data?
**Short answer:** Train on the past, test on the future (forward chaining). **Go deeper:** Random folds leak the future and give optimistic results.

### Q: Why standardise features?
**Short answer:** So large-scale features don't dominate. **Go deeper:** Distance- and gradient-based methods (k-NN, SVM, neural nets) are scale-sensitive; trees are not.

### Q: How would you tune hyper-parameters efficiently?
**Short answer:** Random search or Bayesian optimisation (Optuna) with early stopping of poor runs. **Go deeper:** Always tune on validation, keep the test set untouched, and log every run.

### Q: What is an SVM and the kernel trick?
**Short answer:** SVM finds the widest-margin boundary; the kernel trick computes similarities in a high-dimensional space without building it. **Go deeper:** Training is O(n²–n³), so it suits small to medium data.

### Q: What is a Gaussian process and when would you use one?
**Short answer:** A distribution over functions that gives predictions with uncertainty. **Go deeper:** Great for small data and Bayesian optimisation; O(n³) cost limits scale.

### Q: What is anomaly detection and how would you do it for robot sensors?
**Short answer:** Flag data unlike normal operation. **Go deeper:** Use residuals from a model/filter (innovation tests), isolation forests, autoencoder reconstruction error, or density estimates; set thresholds from normal-operation data.
