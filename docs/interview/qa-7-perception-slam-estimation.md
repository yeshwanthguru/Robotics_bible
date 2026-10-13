---
title: "Q&A 7: Perception, SLAM & State Estimation"
---

# Interview Q&A: Perception, SLAM and State Estimation

:::tip[How to use]
Chapters: [State estimation](../09-perception-localization/state-estimation.md) · [SLAM & localization](../09-perception-localization/slam-localization.md) · [Robot perception](../09-perception-localization/computer-vision-3d.md) · [Sensors](../08-robotics/sensors-actuators.md).
:::

## State estimation and filters

### Q: Explain the Kalman filter in plain words.
**Short answer:** Predict with the motion model, then correct with the sensor, trusting whichever is more certain. **Go deeper:** Gain K = P⁻Hᵀ(HP⁻Hᵀ+R)⁻¹ blends prediction and measurement; covariance shrinks after each update.

### Q: When is the Kalman filter optimal?
**Short answer:** For linear systems with Gaussian noise. **Go deeper:** It is the minimum-variance estimator; for non-Gaussian noise it is still the best linear unbiased estimator.

### Q: EKF versus UKF versus particle filter?
**Short answer:** EKF linearises with Jacobians, UKF propagates sigma points, particle filters use weighted samples. **Go deeper:** Particle filters handle multimodal, non-Gaussian beliefs (global localisation) at higher cost.

### Q: Why does an EKF diverge?
**Short answer:** Poor linearisation points, wrong noise tuning or inconsistent covariance. **Go deeper:** Use UKF, iterated EKF, InEKF or better tuning; check NIS/NEES.

### Q: What is the innovation and what is it used for?
**Short answer:** The difference between measurement and prediction. **Go deeper:** Its normalised squared value (NIS) tests consistency and gates outliers via Mahalanobis distance.

### Q: How do you choose Q and R?
**Short answer:** R from sensor noise measurements; Q by tuning against ground truth. **Go deeper:** Use innovation statistics, adaptive estimation or auto-covariance least squares.

### Q: Why use an error-state filter for orientation?
**Short answer:** The error is small so a 3-vector describes it well. **Go deeper:** A quaternion has 4 numbers for 3 degrees of freedom; the nominal state integrates separately.

### Q: Explain a particle filter's steps.
**Short answer:** Move each particle, weight by how well it explains the measurement, resample. **Go deeper:** Resample when effective sample size drops; inject random particles to avoid deprivation; KLD sampling adapts the count.

### Q: What is observability?
**Short answer:** Whether measurements can determine the state. **Go deeper:** A monocular camera alone can't observe scale; IMU or stereo fixes it.

### Q: EKF versus factor graph?
**Short answer:** EKF squeezes history into one estimate; a factor graph keeps constraints and re-linearises. **Go deeper:** Smoothing is more accurate; iSAM2 makes it incremental.

### Q: How do you fuse GNSS, IMU and wheel odometry?
**Short answer:** An EKF with IMU for prediction and GNSS/odometry as updates. **Go deeper:** `robot_localization` (ekf_node, navsat_transform_node) does this in ROS.

### Q: Why does an IMU drift?
**Short answer:** Biases and noise accumulate on integration. **Go deeper:** Double integration of accelerometer bias gives position error growing as t²; fuse with vision/LiDAR/GNSS and estimate biases.

### Q: How do you handle delayed or out-of-order measurements?
**Short answer:** Buffer states and re-apply the measurement at the right time. **Go deeper:** Retrodiction or fixed-lag smoothing.

## SLAM and localisation

### Q: What is SLAM?
**Short answer:** Building a map while tracking your pose in it. **Go deeper:** It estimates p(trajectory, map | measurements); the main enemy is drift.

### Q: Why do we need loop closure?
**Short answer:** It removes accumulated drift by recognising revisited places. **Go deeper:** Place recognition then geometric verification adds a constraint; false loop closures are catastrophic so use robust back-ends.

### Q: Graph-based SLAM versus EKF-SLAM?
**Short answer:** Graph SLAM is sparse and re-linearisable; EKF-SLAM is dense, O(n²) and becomes inconsistent. **Go deeper:** Pose graphs minimise Σ‖e_ij‖² with Gauss–Newton/LM.

### Q: What is bundle adjustment?
**Short answer:** Jointly refining camera poses and 3-D points by minimising reprojection error. **Go deeper:** The Schur complement eliminates points; solved with LM (Ceres/g2o).

### Q: Explain ICP and its failure cases.
**Short answer:** Match nearest points, compute the best rigid transform (SVD), repeat. **Go deeper:** Needs a good initial guess; fails with little overlap or degenerate geometry; use point-to-plane, robust kernels, global initialisation.

### Q: What is IMU preintegration?
**Short answer:** Summarise IMU data between keyframes into one relative-motion factor. **Go deeper:** Avoids re-integration when the linearisation point changes.

### Q: Visual SLAM: feature-based versus direct?
**Short answer:** Feature-based tracks keypoints and minimises reprojection error; direct minimises pixel intensity error. **Go deeper:** Direct methods use more of the image but are sensitive to lighting.

### Q: How does AMCL work?
**Short answer:** A particle filter on a known 2-D map: odometry moves particles, LiDAR scans weight them. **Go deeper:** Fails with symmetric environments and kidnapping; mitigated by adaptive particle counts and recovery.

### Q: What is the kidnapped robot problem?
**Short answer:** Being moved without knowing and needing global re-localisation. **Go deeper:** Particle filters with random injection or place recognition handle it.

### Q: Monocular scale ambiguity?
**Short answer:** One camera can't tell size and distance apart. **Go deeper:** Fix with IMU, stereo, depth, known object size, or learned metric depth.

### Q: How do you evaluate SLAM?
**Short answer:** ATE and RPE against ground truth, plus loop-closure precision/recall. **Go deeper:** Align trajectories (SE(3) or Sim(3)); tools like `evo`; datasets KITTI, EuRoC, TUM, Hilti.

### Q: Typical SLAM failure modes?
**Short answer:** Dynamic objects, textureless scenes, perceptual aliasing, feature-poor corridors, motion blur. **Go deeper:** LiDAR degeneracy in long corridors; IMU saturation; time offsets.

### Q: What map types do robots use?
**Short answer:** Occupancy grids, TSDF/ESDF, landmark, point-cloud, semantic and scene-graph maps. **Go deeper:** Occupancy uses log-odds updates; nvblox builds ESDFs on GPU.

### Q: Odometry versus SLAM?
**Short answer:** Odometry is local and drifts; SLAM adds a map and loop closure for global consistency.

## Vision and sensing

### Q: Describe the pinhole camera model.
**Short answer:** u = fₓX/Z + cₓ, v = f_yY/Z + c_y. **Go deeper:** Add lens distortion; intrinsics from calibration; extrinsics place the camera in the robot frame.

### Q: Stereo depth formula?
**Short answer:** Z = f·B/d (focal length, baseline, disparity). **Go deeper:** Depth error grows with Z²; textureless regions fail.

### Q: What is the essential matrix?
**Short answer:** It encodes relative rotation and translation between two calibrated views. **Go deeper:** E = [t]ₓR; recover pose via the 5-point algorithm with RANSAC.

### Q: What is RANSAC?
**Short answer:** Fit a model to random minimal subsets and keep the one most data agree with. **Go deeper:** Robust to outliers; iterations needed grow with outlier ratio.

### Q: IoU and mAP?
**Short answer:** IoU is overlap divided by union; mAP is average precision over classes and IoU thresholds. **Go deeper:** COCO mAP averages over IoU 0.5–0.95.

### Q: What does non-maximum suppression do?
**Short answer:** Removes duplicate detections of the same object. **Go deeper:** DETR avoids NMS via bipartite matching.

### Q: Why is SAM useful for robots?
**Short answer:** Promptable zero-shot masks give grasp targets and auto-labelling. **Go deeper:** SAM 2 extends to video tracking.

### Q: How do you get a 6-D pose from an RGB-D image?
**Short answer:** Segment the object, match to its model (e.g. FoundationPose), refine with ICP. **Go deeper:** Category-level methods handle unseen instances.

### Q: LiDAR versus camera versus radar?
**Short answer:** LiDAR gives accurate geometry, cameras give semantics, radar works in bad weather and measures velocity. **Go deeper:** Fusion (BEVFusion) combines their strengths.

### Q: Rolling versus global shutter?
**Short answer:** Rolling shutter reads rows at different times and distorts fast motion. **Go deeper:** Global shutter is preferred for visual-inertial odometry.

### Q: How do you calibrate a camera and an IMU together?
**Short answer:** Use a tool like Kalibr with a target and excitation motion. **Go deeper:** Estimate extrinsics and time offset.

### Q: Why is time synchronisation critical?
**Short answer:** Fusing data from different times creates errors proportional to speed × offset. **Go deeper:** Use hardware triggers or PTP; estimate residual offsets.

### Q: How do you make perception robust to lighting changes?
**Short answer:** Augmentation, domain randomisation, auto-exposure control, multi-modal sensing. **Go deeper:** Test across conditions and monitor confidence.

### Q: How do you detect that perception is failing?
**Short answer:** Monitor confidence, innovation statistics and out-of-distribution scores. **Go deeper:** Fall back to a safe behaviour when uncertainty is high.
