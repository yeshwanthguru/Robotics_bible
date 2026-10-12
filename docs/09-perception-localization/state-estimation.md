---
title: State Estimation & Filters
---

# State Estimation

:::tip[The 30-second version]
Your robot never *knows* where it is. It has a **guess** from motion (wheel odometry, IMU) and **measurements** from sensors (GPS, camera). Each is noisy. A **filter** combines them: predict with the motion model, then correct with the sensor, trusting whichever is more certain. The Kalman filter is the textbook version of this, and it's inside almost every robot.
:::

## The predict–correct cycle

Every filter does the same two steps, forever:

1. **Predict:** "I was here, I moved this much, so I'm probably *there*, but less sure than before."
2. **Update:** "A sensor says I'm *here*. Blend it with my prediction, weighted by who is more certain."

![kalman fusion](/img/fig/kalman-fusion.svg)
*Blue = the prediction, orange = the measurement. The green result sits between them, closer to the narrower (more certain) one, and it is narrower than both. Fusing information always shrinks uncertainty.*

## The Kalman filter

Assumes linear motion and Gaussian noise. With state $x$ and covariance $P$:

**Predict:** $\hat x^- = F\hat x + Bu,\qquad P^- = FPF^\top + Q$
**Update:** $K=P^-H^\top(HP^-H^\top+R)^{-1},\quad \hat x=\hat x^-+K(z-H\hat x^-),\quad P=(I-KH)P^-$

> **In words:**
> - $Q$ = how much I distrust my motion model; $R$ = how much I distrust the sensor.
> - $K$ (the Kalman gain) is a "trust dial" between 0 and 1: if the sensor is precise ($R$ small), $K$ is large and I follow the measurement; if it's noisy, $K$ is small and I stick with my prediction.
> - $z-H\hat x^-$ is the **innovation**: "how surprised am I by this measurement?" Large surprises are gated out as outliers (Mahalanobis test).

```python
import numpy as np
def kf_step(x, P, z, F, H, Q, R):
    x = F @ x;           P = F @ P @ F.T + Q                      # predict
    S = H @ P @ H.T + R; K = P @ H.T @ np.linalg.inv(S)           # trust dial
    x = x + K @ (z - H @ x)                                       # correct with the surprise
    P = (np.eye(len(x)) - K @ H) @ P
    return x, P
```

## When the world is not linear / Gaussian

| Filter | Plain idea | When |
|---|---|---|
| **EKF** | linearise the model at the current guess | GNSS + IMU, `robot_localization`, EKF-SLAM |
| **UKF** | pass a few "sigma points" through the true non-linear model | strong non-linearity |
| **Particle filter** | track thousands of weighted guesses | multi-modal beliefs, global localisation (AMCL) |
| **Error-state KF (ESKF)** | filter the *small error*, not the full state | IMU/INS, quaternions |
| **Invariant EKF** | uses the symmetry of rotations/poses | legged-robot state estimation |
| **Factor-graph smoothing (iSAM2)** | solve for the whole trajectory by optimisation | VIO / SLAM back-ends |

### Particle filter in pictures

![particle filter](/img/fig/particle-filter.svg)
*Scatter guesses everywhere, score each by how well it matches the sensor, keep the good ones: the cloud collapses onto the true pose.*

1. **Move** each particle with the motion model plus noise. 2. **Weight** by how well it explains the sensor reading. 3. **Resample** (keep high-weight particles, drop low ones). Watch for *particle deprivation* (all guesses wrong): inject some random particles.

## Practical issues that separate juniors from seniors
- **Observability:** can the measurements actually determine the state? (A camera alone can't see scale.)
- **Consistency:** is the filter's claimed uncertainty honest? Test with NIS/NEES. Over-confident covariances cause divergence.
- **Angle wrapping:** subtract angles modulo 2π!
- **Delayed / out-of-order measurements:** buffer and re-apply.
- **Time sync and outliers:** gate with Mahalanobis distance, use robust loss functions.
- **Tuning Q and R:** R from sensor datasheets or static data; Q by testing against ground truth.

## Typical sensor-fusion setups
- **GNSS + IMU + wheel odometry + magnetometer** → EKF (ROS: `robot_localization`).
- **Visual-inertial odometry (VIO):** MSCKF, VINS-Mono, OpenVINS, ORB-SLAM3.
- **Legged:** leg kinematics + IMU + foot contact → base velocity, plus LiDAR to cancel drift.

## Interview Q&A

**When is the Kalman filter optimal?**
*Simply:* linear system with Gaussian noise; then it gives the minimum-variance estimate.

**Why does the EKF sometimes diverge?**
*Simply:* it linearises around a wrong guess, and its covariance can become over-confident. *Fixes:* UKF, iterated EKF, InEKF, better tuning.

**EKF vs factor graph?**
*Simply:* an EKF squeezes history into one estimate and moves on; a factor graph keeps the history and can re-solve it, more accurate but heavier (iSAM2 makes it incremental).

**Why error-state filters for orientation?**
*Simply:* the *error* in rotation is tiny, so a 3-vector describes it cleanly (a quaternion has 4 numbers for 3 degrees of freedom).

**How do you choose Q and R?**
*Simply:* R from sensor noise measurements; Q by tuning until the innovation statistics look right.
