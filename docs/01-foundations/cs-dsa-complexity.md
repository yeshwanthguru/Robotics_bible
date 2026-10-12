---
title: CS, Data Structures, Algorithms
---

# CS Fundamentals for Robotics Interviews

:::tip[The 30-second version]
Interviewers use data-structure and algorithm questions to check one thing: **can you write correct, efficient code under pressure?** For robotics, the favourites are *graph search* (path planning), *nearest-neighbour lookups* (point clouds), *queues and threads* (sensor pipelines), and *real-time rules* (never block the control loop).
:::

## Big-O: how the work grows

![Big O](/img/fig/big-o.svg)
*If you double the input, an n² algorithm does 4× the work; a 2ⁿ algorithm becomes hopeless.*

**In words:** Big-O describes *how the running time grows* with the input size, ignoring constant factors. When someone asks "what's the complexity?", answer with the growth curve and what the input size *n* is (points in a cloud? cells in a grid?).

## Data structures cheat sheet

| Structure | Everyday picture | Fast at | Robotics use |
|---|---|---|---|
| **Array / vector** | numbered lockers in a row | jump to item *i* | sensor buffers, trajectories |
| **Hash map** | a dictionary | look up by key, O(1) average | caching, TF frame lookup |
| **Heap / priority queue** | "most urgent first" line | get the smallest item | the open list in **A\*** and Dijkstra |
| **Balanced tree (`std::map`)** | sorted phone book | ordered lookups | event timelines |
| **KD-tree** | repeatedly cut space in half | nearest neighbour in 3-D | **ICP, point-cloud matching** |
| **Octree / voxel hash** | 3-D grid that only stores filled boxes | 3-D occupancy | OctoMap, nvblox |
| **Union-find** | "which group is this in?" | merge and query groups | clustering, loop closures |

## The algorithms robotics interviews love

### Path search on a grid
![A* vs Dijkstra](/img/fig/astar-vs-dijkstra.svg)
*Dijkstra spreads out like a puddle. A\* uses a "distance to goal" hint (the heuristic) so it mostly explores toward the goal.*

- **BFS**: shortest path when every step costs the same.
- **Dijkstra**: shortest path when steps have different costs.
- **A\***: Dijkstra plus a hint. Optimal if the hint never *over*-estimates (admissible).
- **Dynamic programming**: solve small pieces once and reuse (value iteration, Viterbi).
- **Others to know:** DFS, topological sort, minimum spanning tree, union-find, binary search, two pointers, sliding window, quickselect (median), RANSAC (robust line/plane fitting).

### A\* in 20 lines (write this from memory)

```python
import heapq

def astar(grid, start, goal):
    h = lambda a: abs(a[0] - goal[0]) + abs(a[1] - goal[1])      # Manhattan hint
    pq, cost, prev = [(h(start), 0, start)], {start: 0}, {}
    while pq:
        _, c, u = heapq.heappop(pq)
        if u == goal:                                            # rebuild the path
            path = [u]
            while u in prev: u = prev[u]; path.append(u)
            return path[::-1]
        if c > cost[u]: continue                                 # stale queue entry
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            v = (u[0] + dx, u[1] + dy)
            if 0 <= v[0] < len(grid) and 0 <= v[1] < len(grid[0]) and grid[v[0]][v[1]] == 0:
                if c + 1 < cost.get(v, 1e18):
                    cost[v], prev[v] = c + 1, u
                    heapq.heappush(pq, (c + 1 + h(v), c + 1, v))
    return None
```

**How to explain it out loud:** "I keep a priority queue ordered by *cost so far + estimated cost to go*. I always expand the most promising cell. When I pop the goal I rebuild the path from parent pointers."

## Systems knowledge (the part people forget to study)

| Topic | Plain English | Why robotics cares |
|---|---|---|
| **Thread vs process** | threads share memory, processes don't | a ROS 2 node = process; callbacks = threads |
| **Mutex** | a bathroom key: one holder at a time | protect shared sensor data |
| **Deadlock** | two people each holding what the other needs | needs all four: exclusion, hold-and-wait, no preemption, circular wait |
| **Priority inversion** | a low-priority task blocks a high-priority one | classic real-time bug (Mars Pathfinder!) |
| **Real-time** | meeting a deadline *every* time, not just on average | control loops at 1 kHz |
| **Cache / memory layout** | arrays beat linked lists because of CPU caches | fast point-cloud processing |
| **Zero-copy** | pass a pointer, don't copy the image | ROS 2 intra-process, NITROS |
| **TCP vs UDP** | reliable-but-slower vs fast-but-lossy | video/LiDAR streaming vs commands |

## Interview Q&A

**A\* vs Dijkstra?**
*Simply:* A\* is Dijkstra with a compass. *Deeper:* Dijkstra is A\* with heuristic = 0. With a consistent heuristic each node is expanded at most once.

**Why not allocate memory inside a real-time control loop?**
*Simply:* you can't predict how long it will take. *Deeper:* `malloc` may take a lock or ask the OS for pages → unbounded latency; pre-allocate and reuse.

**Mutex vs semaphore?**
*Simply:* a mutex is a key held by one thread; a semaphore is a counter of available slots. *Deeper:* a mutex has an owner (only the locker may unlock).

**What is a hash collision and how is it handled?**
*Simply:* two keys land in the same bucket. *Deeper:* chaining (a list per bucket) or open addressing (probe the next slot); average O(1), worst-case O(n).

**Complexity of nearest-neighbour search in a KD-tree?**
*Simply:* fast on average (log n), but gets worse in very high dimensions. That is why we use it for 3-D points, not 1000-D embeddings.
