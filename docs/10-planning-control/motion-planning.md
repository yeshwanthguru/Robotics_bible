---
title: Motion & Path Planning
---

# Motion Planning

## Configuration space
C-space $\mathcal C$ = all joint configs; obstacles map to $\mathcal C_{obs}$; plan in $\mathcal C_{free}$. Planning is PSPACE-hard in general; completeness types: complete, resolution-complete, probabilistically complete, asymptotically optimal.

## Families

| Family | Algorithms | Notes |
|---|---|---|
| Graph search | Dijkstra, **A\***, D\* / D\* Lite (replanning), Theta\*, JPS, ARA\*, Hybrid A\* (car kinematics), lattice planners (state lattice) | low-D grids, mobile robots |
| Potential fields | attractive + repulsive | local minima; navigation functions |
| **Sampling-based** | **PRM** (multi-query), **RRT**, **RRT-Connect** (bidirectional), **RRT\*** (asymptotically optimal, rewiring), **PRM\***, BIT\*, FMT\*, Informed RRT\*, KPIECE, EST, SST (kinodynamic) | high-D manipulators; paths jagged → shortcut/smooth |
| **Trajectory optimization** | CHOMP, STOMP, TrajOpt (sequential convex), GPMP2, **CuRobo** (GPU), iLQR/DDP, direct collocation, MPC | smooth, dynamics-aware; local minima, needs init |
| Search + optimization hybrids | Graphs of Convex Sets (GCS), Drake | global with convex pieces |
| Learning-based | Motion Policy Networks, diffusion planners, neural SDF, VAE-based sampling | |
| Reactive | DWA (dynamic window), VO/ORCA/RVO (multi-agent), CBF-based, MPPI | local planners in Nav2 |

### RRT
```python
def rrt(start, goal, n_iter, step, free, sample):
    tree = {start: None}
    for _ in range(n_iter):
        q_rand = goal if random() < 0.05 else sample()
        q_near = nearest(tree, q_rand)
        q_new = steer(q_near, q_rand, step)
        if free(q_near, q_new):               # edge collision check
            tree[q_new] = q_near
            if dist(q_new, goal) < eps: return extract_path(tree, q_new)
```
RRT* adds: choose best parent within radius $r\sim(\log n/n)^{1/d}$, then rewire neighbours through q_new if cheaper.

## Collision checking
Primitive shapes (sphere/capsule/box), convex meshes (GJK/EPA, FCL, HPP-FCL), BVH (AABB, OBB), signed-distance fields, voxel/ESDF (nvblox), spheres decomposition for GPU (CuRobo). Continuous collision detection for swept volumes. Self-collision matrix (SRDF disable_collisions).

## Manipulation planning stack (MoveIt 2)
`planning scene` → OMPL planners (RRTConnect default) / Pilz (LIN/PTP/CIRC industrial) / CHOMP / STOMP → time parameterization (TOTG, Ruckig, TOPP-RA) → `ros2_control` execution. Cartesian paths with `computeCartesianPath`. Servo (MoveIt Servo) for real-time teleop. Constraints: orientation constraint, joint limits, path constraints (keep cup upright → constrained sampling / projection).

## Mobile robot navigation (Nav2)
Global planner (NavFn Dijkstra/A\*, Smac Hybrid-A\*/Lattice/2D, Theta\*) → local controller (DWB, **MPPI**, Regulated Pure Pursuit, TEB, RPP) → costmap layers (static, obstacle, inflation, voxel, keepout filters) → behavior tree navigator (`NavigateToPose`, recoveries: spin, back-up, clear costmap, wait). Localization: AMCL or LiDAR-localization; SLAM: slam_toolbox.

## Multi-robot & coverage
MAPF (CBS, priority planning), coverage path planning (boustrophedon, spanning tree), traffic management, auctions (CBBA), formation control, swarm (consensus).

## Task and motion planning (TAMP)
Symbolic task planner (PDDL, HTN) chooses actions; geometric motion planner verifies feasibility; interface via sampled continuous parameters. Systems: PDDLStream, TAMP with LLM (LLM+P, SayCan), Logic-Geometric Programming (LGP), Task-and-motion via behavior trees. See [Task Planning & PDDL](./task-planning-pddl.md).

## Interview Q&A

**RRT vs PRM?** PRM builds reusable roadmap (multi-query); RRT grows tree for single-query, handles kinodynamic constraints.

**Is RRT optimal?** No (path cost converges to a suboptimal constant); RRT\* is asymptotically optimal.

**Why does A\* need admissible h?** To guarantee optimality; consistency prevents re-expansions.

**Planning vs control?** Planning produces a feasible reference path/trajectory; control tracks it in real time with feedback.

**How handle dynamic obstacles?** Predict their motion (constant velocity / learned), plan in space-time, replan frequently (D\* Lite), use velocity obstacles/MPC with chance constraints.

**Why smoothing after RRT?** Random tree paths are jagged and non-dynamically-feasible; shortcutting + spline/time-optimal parameterization.
