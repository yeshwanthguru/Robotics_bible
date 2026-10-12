---
title: State Estimation & Filters
---

# State Estimation

## Bayes filter
Predict: $bel^-(x_t)=\int p(x_t|x_{t-1},u_t)\,bel(x_{t-1})dx$. Update: $bel(x_t)=\eta\,p(z_t|x_t)\,bel^-(x_t)$. All filters are approximations of this.

| Filter | Assumption | Cost | Use |
|---|---|---|---|
| Histogram / grid | discrete | $O(\text{cells})$ | coarse localization |
| **Kalman (KF)** | linear + Gaussian | $O(n^3)$ | optimal; tracking |
| **EKF** | linearize via Jacobians | $O(n^3)$ | GNSS/IMU, EKF-SLAM, `robot_localization` |
| **UKF** | sigma points, no Jacobians | $O(n^3)$ | strongly non-linear |
| **Particle filter** | sample set, any distribution | $O(N)$ | MCL/AMCL, global localization |
| Information filter | inverse covariance | sparse | SLAM, multi-sensor |
| **ESKF / error-state KF** | filter the error; nominal state integrates | | IMU-based INS, VIO, quaternions |
| **Invariant EKF (InEKF)** | Lie-group symmetry; log-linear error | | legged state estimation, consistent |
| **Factor graph smoothing** (iSAM2, GTSAM) | MAP over trajectory | sparse | VIO/SLAM back-end |
| Moving-horizon estimation | optimization window | | constraints |

### Kalman filter equations
Model: $x_k=Fx_{k-1}+Bu_k+w$, $w\sim\mathcal N(0,Q)$; $z_k=Hx_k+v$, $v\sim\mathcal N(0,R)$.
- Predict: $\hat x^-=F\hat x+Bu$, $P^-=FPF^\top+Q$
- Gain: $K=P^-H^\top(HP^-H^\top+R)^{-1}$
- Update: $\hat x=\hat x^-+K(z-H\hat x^-)$, $P=(I-KH)P^-$ (Joseph form $(I-KH)P^-(I-KH)^\top+KRK^\top$ for numerical PSD)
- Innovation $\nu=z-H\hat x^-$ with covariance $S=HP^-H^\top+R$; **NIS** $\nu^\top S^{-1}\nu\sim\chi^2$ for consistency; **Mahalanobis gating** rejects outliers.
- EKF: replace $F,H$ by Jacobians of $f,h$ at current estimate.

```python
import numpy as np
def kf_step(x, P, z, F, H, Q, R):
    x = F @ x; P = F @ P @ F.T + Q
    S = H @ P @ H.T + R
    K = P @ H.T @ np.linalg.inv(S)
    x = x + K @ (z - H @ x)
    P = (np.eye(len(x)) - K @ H) @ P
    return x, P
```

### Particle filter (SIR)
1. Sample $x_t^{[i]}\sim p(x_t|x_{t-1}^{[i]},u_t)$ 2. weight $w^{[i]}\propto p(z_t|x_t^{[i]})$ 3. normalize 4. resample when $N_{eff}=1/\sum w^2<N/2$ (systematic/low-variance resampling). **Particle deprivation** → add random particles (KLD-sampling adapts N, augmented-MCL).

### Practical issues
Observability, filter consistency (over-confident covariance), non-linear angles (wrap!), delayed measurements (retrodiction/buffers), out-of-sequence measurements, time sync, tuning Q/R (innovation-based adaptive), outliers (robust kernels), sensor bias states, ZUPT for foot-mounted IMU.

## Sensor fusion examples
- **GNSS + IMU + wheel odom + magnetometer** → EKF (ROS `robot_localization`: `ekf_node`, `navsat_transform_node`).
- **VIO:** MSCKF, OKVIS, VINS-Mono, ORB-SLAM3, OpenVINS, Kimera.
- **Legged:** kinematics + IMU + contact → base velocity (Bloesch, InEKF), plus LiDAR for drift.
- **Visual-inertial initialization:** gyro bias, gravity direction, scale.

## Interview Q&A

**KF is optimal when?** Linear-Gaussian; minimum-variance among all estimators, and best linear unbiased otherwise.

**EKF failure modes?** Poor linearization point, inconsistency (observability mismatch in SLAM), divergence w/ wrong noise tuning. Fix: UKF, IEKF, InEKF, FEJ.

**Why error-state for orientation?** Quaternion has 4 numbers on a 3-DOF manifold; error rotation is small → 3-vector with well-behaved covariance.

**EKF vs factor graph?** EKF marginalizes past (linearization frozen); smoothing re-linearizes → more accurate but heavier; iSAM2 makes it incremental.

**How to pick Q and R?** R from sensor datasheet/measured static noise; Q by trial using NIS/NEES and ground truth, or ML (EM/auto-covariance least squares).
