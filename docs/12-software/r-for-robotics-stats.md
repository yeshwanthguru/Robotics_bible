---
title: R for Robotics Data & Statistics
---

# R in Robotics & ML Research

R is rarely on the robot; it shines for **experiment analysis, statistics, and publication-quality plots** — important for PhD-style rigor (comparing controllers/policies, human studies, reliability).

## Core
- Vectors/data frames/tibbles, factors, lists; vectorized ops; `apply` family; `%>%` / `|>` pipes.
- **tidyverse:** `dplyr` (filter/mutate/group_by/summarise/join), `tidyr` (pivot), `ggplot2` (grammar of graphics), `readr`, `purrr`, `lubridate`.
- Others: `data.table` (fast), `lme4`/`nlme` (mixed models), `survival` (time-to-failure), `emmeans`, `caret`/`tidymodels`/`mlr3`, `glmnet`, `randomForest`/`xgboost`, `forecast`, `Matrix`, `reticulate` (call Python), `Rcpp` (C++ speedups), `shiny` dashboards, `rmarkdown`/`quarto`.

## Example: compare policy success rates
```r
library(tidyverse)
df <- read_csv("trials.csv")     # columns: policy, task, success (0/1), time_s
df |> group_by(policy) |>
  summarise(n = n(), rate = mean(success),
            lo = binom.test(sum(success), n)$conf.int[1],
            hi = binom.test(sum(success), n)$conf.int[2])

fit <- glm(success ~ policy + task, data = df, family = binomial)
summary(fit); anova(fit, test = "Chisq")

ggplot(df, aes(policy, time_s, fill = policy)) + geom_boxplot() + facet_wrap(~task) + theme_minimal()
```
Repeated-measures / hierarchical: `lmer(time_s ~ policy + (1|task) + (1|operator), data=df)`.

## Statistical toolbox to know
- Hypothesis testing: t-test, Welch, Mann–Whitney, paired tests, χ², Fisher exact; multiple-comparison correction (Bonferroni, Holm, BH-FDR); effect size (Cohen's d); power analysis (sample size for success-rate difference); bootstrap CIs; Bayesian alternatives (`brms`, `rstanarm`).
- Reliability: Weibull/exponential failure models, Kaplan–Meier, MTBF.
- Time series: ARIMA, state-space (`KFAS`), spectral analysis for vibration/gait.
- Reproducibility: `renv`, seeds, Quarto notebooks.

## R vs Python
R: statistics-first, superior ggplot/mixed-model ecosystem; Python: ML/robotics integration. Use R for analysis of logged trial data exported from ROS bag → CSV/Parquet (`arrow` package).

## Interview Q&A

**p-value meaning?** Probability of data this extreme under H0 — not P(H0 true).

**Why report CIs for success rate with n=20?** Point estimates are noisy; Wilson/exact intervals show uncertainty (e.g. 18/20 → 95% CI ≈ 70–99%).

**Why mixed-effects?** Trials nested within operators/objects violate independence; random effects model that.

**Multiple comparisons problem?** Testing many policies/tasks inflates false-positive rate; correct with Holm/BH.
