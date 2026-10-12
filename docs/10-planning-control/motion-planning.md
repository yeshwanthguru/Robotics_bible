---
title: Motion & Path Planning
---

# Motion Planning

:::tip[The 30-second version]
**Planning** = finding a safe route from *here* to *there*. For a car-like robot that's a path on a floor plan. For a 7-joint arm it's a path through a 7-dimensional "space of poses". The key trick for arms: instead of checking the whole arm against obstacles, treat the **arm's entire pose as a single point** in **configuration space** and search that.
:::

## Configuration space (C-space)

Each joint angle is one axis. A pose of the whole arm = one point. Obstacles in the real world become "forbidden regions" in C-space. Planning = find a path for the point avoiding those regions. In 2-D this is easy to draw; in 7-D you can't draw it but the idea is the same, which is why **random sampling** works well there.

## The families of planners

| Family | Algorithms | Plain idea | Best for |
|---|---|---|---|
| **Grid / graph search** | Dijkstra, **A\***, D\* Lite, Hybrid A\*, lattice | search a map of cells or states | mobile robots, low dimensions |
| **Sampling-based** | **RRT, RRT-Connect, RRT\***, PRM, BIT\* | randomly sample poses, connect the free ones | **arms** (high dimension) |
| **Trajectory optimisation** | CHOMP, STOMP, TrajOpt, **cuRobo**, iLQR | start with a rough path, optimise smoothness and clearance | smooth, dynamic motion |
| **Potential fields** | attractive + repulsive | goal pulls, obstacles push | simple local avoidance (local minima!) |
| **Reactive / local** | DWA, MPPI, VO/ORCA | choose the best short motion now | dynamic obstacles, Nav2 local planner |
| **Learning-based** | Motion Policy Nets, diffusion planners | neural network proposes paths | speed, narrow passages |

### RRT: grow a tree toward random points

![rrt tree](/img/fig/rrt-tree.svg)
*RRT: pick a random point, extend the nearest tree node toward it, keep it if collision-free. Repeat until the tree reaches the goal.*

```python
def rrt(start, goal, n_iter, step, is_free, sample):
    tree = {start: None}
    for _ in range(n_iter):
        q_rand = goal if random() < 0.05 else sample()      # a little goal bias
        q_near = nearest(tree, q_rand)
        q_new  = steer(q_near, q_rand, step)                # small step toward the sample
        if is_free(q_near, q_new):                          # edge collision check
            tree[q_new] = q_near
            if dist(q_new, goal) < eps: return extract_path(tree, q_new)
```

- **RRT** is fast and finds *a* path, not the best one. **RRT\*** also "rewires" the tree to get progressively shorter paths (asymptotically optimal). **PRM** builds a reusable roadmap for many queries.
- Raw RRT paths are jagged → **shortcut + smooth + time-parameterise** (TOTG, Ruckig, TOPP-RA).
- Completeness words: *complete*, *resolution-complete*, **probabilistically complete** (RRT), *asymptotically optimal* (RRT\*).

## Collision checking
Robots are approximated by spheres/capsules/convex meshes (GJK/EPA, FCL), obstacles by voxels or **signed-distance fields** (nvblox), and checked along edges (continuous collision detection). A **self-collision matrix** (SRDF) skips link pairs that can't collide. GPU planners (cuRobo / cuMotion) check thousands of paths in parallel.

## Planning stacks you must know

### MoveIt 2 (arms)
`planning scene` → planner (OMPL RRTConnect default, Pilz for straight-line/blend moves, CHOMP/STOMP, cuMotion) → time parameterisation → `ros2_control` execution. **MoveIt Servo** gives real-time teleop; Cartesian paths via `computeCartesianPath`; path constraints (keep the cup upright) via constrained sampling.

### Nav2 (mobile robots)
Global planner (NavFn, Smac Hybrid-A\*/Lattice, Theta\*) → local controller (DWB, **MPPI**, Regulated Pure Pursuit) → **costmaps** (static + obstacles + inflation) → a **behavior-tree navigator** with recovery behaviours (spin, back up, clear costmap).

## Multi-robot and coverage
MAPF (conflict-based search), coverage patterns (boustrophedon), auctions for task allocation (CBBA), formation control, Open-RMF for fleets.

## Task and motion planning (TAMP)
A **symbolic planner** decides *which actions* (pick A, move, place), while a **motion planner** checks they're geometrically feasible and returns the continuous details. Tools: PDDLStream, logic-geometric programming, LLM-assisted planners. See [Task planning & PDDL](./task-planning-pddl.md).

## Interview Q&A

**RRT vs PRM?**
*Simply:* PRM draws a reusable road map first (many queries); RRT grows a tree for one query and handles motion constraints.

**Is RRT optimal?**
*Simply:* no. RRT\* is asymptotically optimal.

**Why does A\* need an admissible heuristic?**
*Simply:* if the hint never over-estimates, the first path found is the best.

**Planning vs control?**
*Simply:* planning decides the route; control follows it in real time with feedback.

**How do you handle moving obstacles?**
*Simply:* predict their motion, plan in space-time or replan fast (D\* Lite, MPC with safety margins).

**Why smooth an RRT path?**
*Simply:* random paths are jerky and not dynamically feasible, so shortcut and re-time them.
