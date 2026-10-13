---
title: "Q&A 8: Planning & Navigation"
---

# Interview Q&A: Planning, Task Planning and Navigation

:::tip[How to use]
Chapters: [Motion planning](../10-planning-control/motion-planning.md) · [Task planning & PDDL](../10-planning-control/task-planning-pddl.md) · [Mobile navigation](../11-mobility-dexterity/mobile-navigation.md).
:::

## Motion planning

### Q: What is configuration space?
**Short answer:** The space of all joint configurations; obstacles become forbidden regions. **Go deeper:** Planning is finding a path for a point in C-space; high dimension motivates sampling.

### Q: RRT versus PRM?
**Short answer:** PRM builds a reusable roadmap; RRT grows a tree for a single query. **Go deeper:** RRT handles kinodynamic constraints; PRM suits repeated queries in static scenes.

### Q: Is RRT optimal?
**Short answer:** No; RRT* is asymptotically optimal. **Go deeper:** RRT* rewires neighbours within a shrinking radius ∝ (log n / n)^{1/d}.

### Q: What does probabilistically complete mean?
**Short answer:** If a solution exists, the probability of finding it tends to 1 as time grows. **Go deeper:** Contrasts with resolution-complete (grid planners).

### Q: Why smooth RRT paths?
**Short answer:** They are jagged and not dynamically feasible. **Go deeper:** Shortcut, fit splines, then time-parameterise (TOPP-RA, Ruckig).

### Q: Sampling-based versus optimisation-based planning?
**Short answer:** Sampling is global but jagged; optimisation is smooth but local and needs initialisation. **Go deeper:** Often combine: RRT initial path, then CHOMP/TrajOpt.

### Q: How does collision checking work?
**Short answer:** Approximate robot and obstacles with simple shapes and test overlap. **Go deeper:** GJK/EPA for convex shapes, BVH, signed-distance fields; continuous collision checking for edges.

### Q: What is a potential field planner's weakness?
**Short answer:** Local minima. **Go deeper:** Navigation functions or combining with global search avoid them.

### Q: Which planners does MoveIt use?
**Short answer:** OMPL (RRTConnect by default), Pilz (industrial moves), CHOMP, STOMP and others like cuMotion. **Go deeper:** Followed by time parameterisation and `ros2_control` execution.

### Q: How do you plan with constraints such as keeping a cup upright?
**Short answer:** Constrained sampling with projection, or trajectory optimisation with the constraint as a cost/constraint. **Go deeper:** MoveIt path constraints, Pilz, or optimisation-based planners.

### Q: What is time-optimal path parameterisation?
**Short answer:** Choosing the fastest speed along a fixed path under velocity/acceleration limits. **Go deeper:** TOPP-RA solves it efficiently.

### Q: How do you handle moving obstacles?
**Short answer:** Predict their motion and replan quickly or plan in space-time. **Go deeper:** D* Lite, velocity obstacles, MPC with chance constraints.

### Q: What is multi-agent path finding?
**Short answer:** Collision-free paths for many agents. **Go deeper:** Conflict-based search and priority planning; used in warehouses.

## Search

### Q: Why does A* need an admissible heuristic?
**Short answer:** So the first path found is optimal. **Go deeper:** Consistency additionally prevents re-expansions.

### Q: How would you choose a heuristic for a grid with diagonal moves?
**Short answer:** Octile distance. **Go deeper:** Manhattan overestimates with diagonals; Euclidean is admissible but weaker.

### Q: Hybrid A*?
**Short answer:** A* over continuous vehicle states respecting turning limits. **Go deeper:** Used for parking and car-like robots (Smac Hybrid-A* in Nav2).

### Q: D* Lite?
**Short answer:** Incremental replanning when the map changes. **Go deeper:** Reuses previous search effort.

## Task planning and behaviours

### Q: What is PDDL?
**Short answer:** A language describing planning domains (actions with preconditions and effects) and problems. **Go deeper:** Domain file plus problem file; extensions for numbers, time, derived predicates.

### Q: How do symbolic planners search efficiently?
**Short answer:** Heuristics from delete relaxation. **Go deeper:** FF, h_add, landmarks, LAMA in Fast Downward.

### Q: What are common PDDL modelling mistakes?
**Short answer:** Forgetting to delete old facts, symmetry blow-up, missing preconditions. **Go deeper:** Grounding explosion from too many objects.

### Q: Behavior tree versus finite-state machine?
**Short answer:** Behavior trees are modular and avoid transition explosion; FSMs are simple but grow messy. **Go deeper:** BTs re-evaluate conditions every tick and compose via sequence/fallback/parallel.

### Q: What do Sequence and Fallback nodes do?
**Short answer:** Sequence runs children in order until one fails; Fallback tries children until one succeeds. **Go deeper:** Both return RUNNING if a child is running.

### Q: How do you recover from failed actions?
**Short answer:** Monitor effects, update the world state, replan, use BT fallbacks. **Go deeper:** Escalate to a human when recovery is exhausted.

### Q: What is task and motion planning?
**Short answer:** Combine symbolic task planning with geometric feasibility checking. **Go deeper:** PDDLStream and logic-geometric programming interface the two.

### Q: How can an LLM be used with a planner?
**Short answer:** Translate language to PDDL, then let a planner and validator produce a verified plan. **Go deeper:** LLM+P; always validate preconditions before execution.

## Navigation (Nav2 and mobile robots)

### Q: Explain the Nav2 architecture.
**Short answer:** Behavior-tree navigator calling a planner server, a controller server, costmaps and recovery behaviours. **Go deeper:** Lifecycle nodes, plugins for planners/controllers, AMCL or SLAM for localisation.

### Q: Global versus local planner?
**Short answer:** Global plans the whole route on the known map; local reacts to nearby obstacles at high rate. **Go deeper:** NavFn/Smac global; DWB/MPPI/RPP local.

### Q: What is a costmap and why inflate it?
**Short answer:** A grid of costs; inflation pads obstacles so the robot can be treated as a point. **Go deeper:** Layers: static, obstacle, inflation, voxel, keep-out.

### Q: Frames in a mobile stack?
**Short answer:** map → odom → base_link → sensors. **Go deeper:** odom is smooth but drifts; map→odom jumps when localisation corrects (REP-105).

### Q: DWA versus MPPI versus pure pursuit?
**Short answer:** DWA samples velocities, MPPI samples whole trajectories with a cost, pure pursuit tracks a look-ahead point. **Go deeper:** MPPI handles complex costs and runs well on GPUs.

### Q: What recovery behaviours exist?
**Short answer:** Clear costmap, spin, back up, wait. **Go deeper:** Escalate to teleop if still stuck.

### Q: Sources of odometry error?
**Short answer:** Wheel slip, wrong wheel size or track width, encoder resolution. **Go deeper:** Fuse with IMU and visual/LiDAR odometry.

### Q: How do you do mobile manipulation?
**Short answer:** Navigate to a base pose from which the arm can reach, then manipulate, correcting base error with vision. **Go deeper:** Whole-body planning treats base and arm jointly.

### Q: How do quadrotors track trajectories?
**Short answer:** Differential flatness lets you plan smooth position/yaw paths; cascaded controllers track them. **Go deeper:** Minimum-snap polynomials; position → attitude → rate → motor mixing (PX4).

### Q: What is social navigation?
**Short answer:** Moving among people with predictable, comfortable behaviour. **Go deeper:** Pedestrian prediction, social-force models, interaction-aware RL/MPC.

### Q: How do you test navigation before deployment?
**Short answer:** Simulation scenarios, bag replay, then staged real tests with safety limits. **Go deeper:** Include dynamic obstacles and localisation failures.

### Q: How does a fleet of robots avoid conflicts?
**Short answer:** Central traffic management (Open-RMF) or decentralised negotiation. **Go deeper:** Lanes, reservations, deadlock detection.
