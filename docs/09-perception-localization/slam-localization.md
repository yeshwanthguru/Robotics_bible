---
title: SLAM & Localization
---

# Localization, Mapping, SLAM

:::tip[The 30-second version]
**Localization:** "I have a map, where am I?" **Mapping:** "I know where I am, what does the world look like?" **SLAM:** *both at once*, like exploring a dark building with a torch and drawing the floor-plan while keeping track of where you stand.
The main enemy is **drift**: tiny errors in each step add up. The cure is **loop closure**: recognising "I've been here before" and snapping the path back into shape.
:::

## 🎮 Try it yourself

<div class="simbox"><div class="simhead"><span>Interactive: Particle-filter localization</span><a href="/Robotics_bible/sim/particle-filter.html" target="_blank">open full screen ↗</a></div><iframe src="/Robotics_bible/sim/particle-filter.html" height="560" loading="lazy" title="Particle-filter localization"></iframe></div>


## The big picture

![slam loop closure](/img/fig/slam-loop-closure.svg)
*Left: odometry alone drifts, so the loop doesn't close. Right: once the robot recognises the starting place, one extra constraint corrects the whole trajectory.*

| Task | Known | Unknown |
|---|---|---|
| **Localization** (tracking, global, re-localisation) | map | pose |
| **Mapping** | poses | map |
| **SLAM** | nothing | both |
| **Odometry** | previous pose | next pose (drifts, no global fix) |

## Maps: how robots remember the world

![occupancy and costmap](/img/fig/occupancy-costmap.svg)
*Left: an occupancy grid (every cell: free / occupied / unknown). Right: a navigation costmap inflates obstacles by the robot's size so the planner can treat the robot as a point.*

| Map | What it stores | Used by |
|---|---|---|
| **Occupancy grid** (2-D/3-D, OctoMap) | probability each cell is occupied | Nav2, planners |
| **TSDF / ESDF** (voxblox, **nvblox**) | distance to nearest surface | manipulation, drones, GPU planning |
| **Landmark map** | positions of recognisable features | feature SLAM |
| **Point-cloud map** | raw 3-D points | LiDAR localisation |
| **Semantic / scene graph** | objects and relations ("mug on table") | task planning with LLMs |
| **NeRF / 3D Gaussian splatting** | photoreal appearance | newer dense SLAM |

Occupancy update uses **log-odds**: each hit adds a constant, each miss subtracts one, so updating is just addition.

## Aligning scans: ICP

**ICP** (Iterative Closest Point) lines up two point clouds: match each point to its nearest neighbour, compute the best rigid motion (via SVD), apply, repeat.
Pitfalls: needs a decent starting guess, gets stuck in local minima, fails in featureless corridors. Better variants: point-to-plane, GICP, **NDT**, KISS-ICP. For a global guess use feature matching (FPFH + RANSAC, TEASER++).

## SLAM families

| Approach | Examples | Idea |
|---|---|---|
| **Filter-based** | EKF-SLAM, FastSLAM, GMapping | track a belief over robot + landmarks |
| **Graph-based** | slam_toolbox, Cartographer, g2o, GTSAM | nodes = poses, edges = constraints; solve one big least-squares problem |
| **LiDAR-inertial** | LIO-SAM, FAST-LIO2, KISS-ICP | tightly fuse LiDAR + IMU |
| **Visual feature SLAM** | ORB-SLAM3 | track image features; tracking / mapping / loop-closure threads |
| **Direct visual** | DSO, LSD-SLAM | minimise pixel brightness error |
| **Visual-inertial** | VINS-Fusion, OpenVINS, Basalt | camera + IMU (gives metric scale) |
| **Learning-based** | DROID-SLAM, MASt3R-SLAM | neural dense matching |

### Graph SLAM in one sentence
Each odometry step and each loop closure is a **spring** between two poses; SLAM finds the arrangement of poses that stretches the springs least.

$$ X^{*}=\arg\min_X \sum_{ij}\big\|e_{ij}(x_i,x_j)\big\|^2_{\Omega_{ij}} $$

> **In words:** "find the trajectory whose predicted relative motions best match everything we measured, weighting each constraint by how much we trust it." Solved with Gauss–Newton / Levenberg–Marquardt on a sparse matrix.

**Loop closure** = place recognition (bag-of-words, NetVLAD, Scan Context) + geometric verification. A *false* loop closure ruins the map, so back-ends use robust methods (switchable constraints, GNC).

**Bundle adjustment:** jointly refine camera poses and 3-D points by minimising reprojection error.

## Visual geometry essentials

![pinhole](/img/fig/pinhole-camera.svg)
*The pinhole camera: far things look small because of similar triangles.*

- **Projection:** a 3-D point $(X,Y,Z)$ lands at pixel $u=f_xX/Z+c_x$, $v=f_yY/Z+c_y$.
- **Epipolar geometry:** a point in one image lies on a *line* in the other; the essential matrix ($E=[t]_\times R$) encodes the relative pose of two views.
- **PnP:** known 3-D points + their pixels → camera pose. **Triangulation:** two views → 3-D point.
- **Monocular scale ambiguity:** one camera can't tell a big far thing from a small near one; fix with an IMU, stereo, depth or known object size.
- **Features:** ORB, SIFT, SuperPoint + LightGlue, optical flow (KLT, RAFT).

## Monte-Carlo Localization (AMCL)
Particle filter over $(x,y,\theta)$ on a known map: move particles with odometry, weight by how well the LiDAR scan fits the map, resample. Weak spots: symmetric corridors, the "kidnapped robot", moving people. Alternatives: NDT localisation, visual re-localisation, AprilTags, UWB, RTK-GNSS.

## How SLAM is evaluated
**ATE** (absolute trajectory error after alignment), **RPE** (relative error), drift %, loop-closure precision/recall. Tools: `evo`. Datasets: KITTI, EuRoC, TUM-RGBD, Hilti, Newer College.

## Failure modes to mention
Perceptual aliasing (two places look the same), moving objects, textureless or glaring scenes, feature-poor corridors (LiDAR degeneracy), motion blur, IMU saturation, time offsets, wheel slip, long-term map changes.

## Interview Q&A

**Why do we need loop closure?**
*Simply:* odometry drifts without bound; recognising a previously visited place gives a constraint that corrects the whole path.

**Why graph-based SLAM instead of EKF-SLAM?**
*Simply:* graphs are sparse, re-linearisable and scale to big maps; EKF-SLAM is dense, becomes inconsistent and costs $O(n^2)$.

**What is IMU preintegration?**
*Simply:* summarise many IMU readings between two keyframes into one relative-motion factor, so the optimiser doesn't redo the integration at each step.

**Why can ICP fail?**
*Simply:* bad initial guess, little overlap, or degenerate geometry (a long flat wall). Use point-to-plane, robust loss, multi-resolution, or a global initialiser.

**Odometry vs SLAM?**
*Simply:* odometry is local and drifts; SLAM adds a map and loop closure for global consistency.
