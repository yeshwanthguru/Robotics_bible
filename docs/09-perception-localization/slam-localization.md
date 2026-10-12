---
title: SLAM & Localization
---

# Localization, Mapping, SLAM

## Problem statements
- **Localization:** know the map, estimate pose. *Tracking* (known start), *global* (kidnapped robot), *re-localization*.
- **Mapping:** known poses, build map (occupancy grid with log-odds $l=\log\frac{p}{1-p}$ additive update).
- **SLAM:** jointly estimate trajectory and map. $p(x_{1:t},m|z_{1:t},u_{1:t})$.

## Map representations
Occupancy grid (2D/3D), OctoMap, TSDF/ESDF (voxblox, **nvblox** on GPU), landmark maps, point-cloud map, surfels, mesh, topological graph, semantic/scene graph (Kimera, Hydra, ConceptGraphs), **NeRF / 3D Gaussian Splatting** SLAM (SplaTAM, MonoGS), HD maps.

## Scan matching & registration
- **ICP:** iterate nearest-neighbour correspondences + SVD (Kabsch) alignment; point-to-point vs **point-to-plane**; needs a good initial guess. Variants GICP, NDT (Gaussian cells; Autoware), KISS-ICP.
- **Global registration:** FPFH features + RANSAC, TEASER++, Fast Global Registration.
- **Correlative scan matching** (Cartographer branch-and-bound).

## Classic SLAM families
| Approach | Examples | Idea |
|---|---|---|
| EKF-SLAM | MonoSLAM | state = pose + landmarks, $O(n^2)$ |
| Particle filter | **FastSLAM**, **GMapping** | Rao–Blackwellization: sample paths, EKF per landmark |
| Graph-based | **Cartographer, slam_toolbox, g2o, GTSAM, Ceres** | nodes=poses, edges=constraints; solve nonlinear LS with Gauss–Newton/LM; sparse Cholesky |
| Direct LiDAR-inertial | **LIO-SAM, FAST-LIO2, LOAM, LeGO-LOAM, KISS-ICP, Point-LIO** | tightly coupled IMU + LiDAR, iterated EKF/factor graph |
| Visual feature-based | **ORB-SLAM3**, PTAM | tracking / local mapping / loop-closing threads, bundle adjustment |
| Direct/semi-direct visual | LSD-SLAM, DSO, SVO | photometric error |
| Visual-inertial | VINS-Fusion, OpenVINS, Basalt, MSCKF | IMU preintegration (Forster) |
| Learning-based | DROID-SLAM, DPVO, MASt3R-SLAM, CUT3R, DUSt3R/VGGT | feed-forward geometry, dense optical-flow BA |

### Graph SLAM formulation
$X^*=\arg\min\sum\|e_{ij}(x_i,x_j)\|^2_{\Omega_{ij}}$. Information matrix is sparse; marginalization causes fill-in; keyframes & sliding windows limit cost. **Loop closure**: place recognition (DBoW2/BoW, NetVLAD, Scan Context, MixVPR, AnyLoc) → geometric verification → add edge → global optimization. False loop closures are catastrophic → robust back-end (switchable constraints, PCM, max-mixtures, GNC).

### Bundle adjustment
$\min\sum\rho(\|z_{ij}-\pi(K,T_i,X_j)\|^2)$; Schur complement eliminates points; reprojection error; solve with LM (Ceres/g2o).

## Visual geometry essentials
- Pinhole: $\lambda\tilde u=K[R|t]\tilde X$. Epipolar constraint $x'^\top Fx=0$; essential matrix $E=[t]_\times R$ (calibrated), 5-pt algorithm (+RANSAC); 8-pt for F; homography for planar/pure rotation.
- PnP (EPnP, P3P), triangulation (DLT), scale ambiguity for monocular (resolved by IMU/stereo/depth).
- Feature types: SIFT, SURF, ORB (FAST+BRIEF), SuperPoint+LightGlue/SuperGlue, LoFTR; optical flow (KLT, RAFT).

## Monte Carlo Localization (AMCL)
Particle filter over $(x,y,\theta)$ on known grid map; motion model (odometry model with noise), sensor model (likelihood field / beam); resample; adaptive N (KLD). Issues: symmetric environments, kidnapped robot, dynamic obstacles. ROS: `nav2_amcl`. Alternatives: LiDAR NDT localization, visual re-loc (hloc), AprilTag/QR fiducials, UWB anchors, GNSS-RTK + lane maps, magnetic/WiFi fingerprinting.

## Evaluation
ATE (absolute trajectory error after SE(3)/Sim(3) alignment), RPE (relative), drift %, loop-closure precision/recall, map accuracy, tools: `evo`, KITTI, EuRoC, TUM-RGBD, Hilti, NCLT, Newer College.

## Failure modes
Perceptual aliasing, dynamic objects, textureless/ glare, feature-poor corridors (LiDAR degeneracy – detect via Hessian eigenvalues), motion blur, IMU saturation, time offsets, lost tracking, wheel slip, long-term map change.

## Interview Q&A

**Why loop closure?** Odometry drifts unboundedly; loop closure adds a constraint that corrects whole trajectory.

**Why graph-based over EKF SLAM?** Sparse, re-linearizable, scales to large maps; EKF is dense and inconsistent due to early linearization.

**What is IMU preintegration?** Integrate IMU between keyframes in a body frame relative to the starting state, so the factor needn't be recomputed when the linearization point changes.

**ICP convergence issues?** Local minima, bad init, partial overlap, degenerate geometry; use point-to-plane, robust kernels, multi-resolution, global init.

**Monocular scale?** Unobservable; fix with IMU, depth, known object size, or learned metric depth.

**Difference between odometry and SLAM?** Odometry = local, drifting; SLAM = adds global consistency (loop closure + map).
