---
title: More ML Topics (Time Series, Anomalies, Uncertainty, Recommenders)
---

# More ML Topics

:::tip[The 30-second version]
Beyond classification and regression, real projects need: **forecasting** (what happens next in a time series), **anomaly detection** (what looks wrong), **uncertainty** (how sure is the model), **recommenders** (what to suggest), **explainability** (why did it decide that), and **optimising expensive experiments**. These are the supporting skills that make a model trustworthy in the field.
:::

## 1. Time series

A **time series** is data ordered in time (joint torques, battery voltage, IMU). Key ideas:

| Idea | Plain meaning |
|---|---|
| **Trend / seasonality / noise** | slow drift, repeating patterns, random wiggles |
| **Stationarity** | statistics don't change over time (many classical models need it; use differencing) |
| **Autocorrelation** | a signal's similarity with a delayed copy of itself |
| **Lag features** | previous values used as inputs |
| **Forward-chaining validation** | train on the past, test on the future (never shuffle) |

| Model | Idea | When |
|---|---|---|
| **Moving average / exponential smoothing** | weighted recent average | quick baselines |
| **ARIMA / SARIMA** | autoregression + differencing + moving average (+ seasonal) | univariate forecasting |
| **State-space / Kalman models** | latent state with dynamics | tracking, sensor data |
| **Gradient-boosted trees with lag features** | tabular treatment of time series | strong practical baseline |
| **RNN / LSTM / TCN / Transformers (PatchTST, TFT)** | neural sequence models | many series, long history |
| **Fourier / wavelet analysis** | frequency content | vibration, gait, fault diagnosis |

**Common mistakes:** random train/test splits, leakage through features computed with future data, ignoring changes in sampling rate, evaluating only one-step-ahead accuracy.

## 2. Anomaly and fault detection

**Goal:** flag data unlike normal operation, usually with few or no labelled faults.

| Approach | Idea |
|---|---|
| **Statistical thresholds** | z-scores, control charts |
| **Residual-based** | compare measurements with a model/filter prediction (innovation tests, Mahalanobis gating) |
| **Isolation forest** | anomalies are isolated by fewer random splits |
| **One-class SVM / density estimation** | model "normal" and score deviations |
| **Autoencoders** | high reconstruction error means unusual |
| **Predictive maintenance models** | forecast remaining useful life (survival analysis) |

**Practice:** set thresholds from normal-operation data, balance false alarms versus misses, and add a human or safe-fallback path.

## 3. Uncertainty and out-of-distribution detection

A model that says "I'm not sure" is safer than one that is confidently wrong.

| Method | How it estimates uncertainty |
|---|---|
| **Ensembles** | disagreement between several independently trained models |
| **MC dropout** | keep dropout on at test time and sample |
| **Bayesian neural nets / Laplace approximations** | distribution over weights |
| **Gaussian processes** | built-in predictive variance |
| **Conformal prediction** | wraps any model to give sets with guaranteed coverage |
| **Calibration (temperature scaling)** | makes probabilities match frequencies |
| **OOD detectors** | max-softmax, energy scores, feature-space distance |

**Two kinds:** *aleatoric* (noise in the data; irreducible) and *epistemic* (lack of knowledge; shrinks with more data).

## 4. Explainability

| Tool | Gives you |
|---|---|
| **Feature importance / permutation importance** | which inputs matter overall |
| **SHAP / LIME** | per-prediction attribution |
| **Saliency / Grad-CAM** | which image regions drove a CNN's decision |
| **Attention maps** | where a transformer looked (use with caution) |
| **Partial dependence plots** | how the output changes with one feature |

## 5. Recommenders and ranking

- **Collaborative filtering:** recommend what similar users liked.
- **Matrix factorisation:** learn low-rank user and item vectors whose dot product predicts a rating.
- **Two-tower models:** one network embeds users, another items; retrieve by nearest neighbour.
- **Learning to rank:** optimise ordered lists (pairwise/listwise losses, NDCG).
- **Cold start:** new users/items lack history; use content features or exploration (bandits).

## 6. Bayesian optimisation and bandits

When each evaluation is expensive (a real robot trial, a long training run):
- **Bayesian optimisation:** fit a probabilistic surrogate (Gaussian process), pick the next point by an acquisition function (expected improvement, UCB). Used to tune controller gains and hyper-parameters.
- **Multi-armed bandits:** balance exploring options and exploiting the best (UCB, Thompson sampling); A/B tests as a special case.

## 7. Data-centric practice

- **Label noise:** audit labels; use confident learning to find errors.
- **Active learning:** label the most uncertain samples first.
- **Weak supervision / synthetic data:** programmatic labels, simulation.
- **Dataset shift:** covariate shift, label shift, concept drift; monitor and retrain.
- **Fairness and privacy:** evaluate across groups; consider differential privacy and federated learning where needed.

## Interview Q&A

**Why can't you shuffle a time series for validation?**
*Simply:* the model would peek at the future. *Deeper:* use forward-chaining splits and leak-free features.

**How would you detect a failing motor from current and temperature signals?**
*Simply:* model normal behaviour and flag residuals. *Deeper:* combine a physics/filter residual with an isolation forest or autoencoder; tune thresholds on normal data; validate with fault injection.

**Aleatoric versus epistemic uncertainty?**
*Simply:* noise in the world versus ignorance of the model. *Deeper:* only epistemic uncertainty shrinks with more data.

**Why is conformal prediction attractive?**
*Simply:* it gives guaranteed coverage with any model. *Deeper:* needs exchangeable calibration data.

**How would you tune a robot controller with only 20 trials?**
*Simply:* Bayesian optimisation. *Deeper:* a GP surrogate with expected improvement and safety constraints.
