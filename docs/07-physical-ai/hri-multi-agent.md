---
title: Human–Robot Interaction & Multi-Robot Systems
---

# Human–Robot Interaction (HRI) and Multi-Robot Systems

:::tip[The 30-second version]
Robots rarely work alone. **HRI** is about robots working *with and around people*: understanding what a person wants, sharing control, passing objects, moving politely, and being trusted. **Multi-robot systems** are about many robots cooperating: dividing tasks, avoiding each other, and sharing a map. Both are mostly about **communication, prediction and safety** rather than new mathematics.
:::

## 1. Human–robot interaction

### Interaction modes

| Mode | Plain meaning | Examples |
|---|---|---|
| **Teleoperation** | a human drives the robot remotely | surgery, bomb disposal, data collection for imitation learning |
| **Shared autonomy** | human gives intent, robot handles details | assistive wheelchair arm, grasp assist |
| **Supervised autonomy** | robot works alone, human approves or intervenes | warehouse fleets, space missions |
| **Collaboration** | human and robot work on the same task | cobot assembly, hand-overs |
| **Social interaction** | robot communicates socially | reception, education, elder care |

### Communication channels
Speech and language (LLM/VLM interfaces), gestures and pointing, gaze, touch, screens and lights (intent displays), sounds, haptics. Good designs make the robot's **intent legible**: a robot that slows down and signals before turning is easier to trust.

### Key technical topics

| Topic | What it involves |
|---|---|
| **Intent and goal prediction** | infer what a person will do (trajectory prediction, goal inference with Bayesian filters or learned models) |
| **Hand-overs** | timing, grasp release detection, force/pose planning so the human can take the object comfortably |
| **Legible and predictable motion** | choose motions that reveal the goal early, not just the shortest path |
| **Social navigation** | keep personal space, pass on the correct side, interpret crowd flow (social-force models, learned/ interaction-aware planners) |
| **Shared control / arbitration** | blend human and robot commands; give the human final authority |
| **Teaching by demonstration and feedback** | kinesthetic teaching, corrections, preference learning, language feedback |
| **Trust and transparency** | explain decisions and failures; calibrate user trust to actual reliability |
| **Safety around people** | speed-and-separation, power-and-force limiting, safe stops (see [Safety](../08-robotics/safety-ethics-standards.md)) |

### Evaluating HRI
Objective: task time, error rate, number of interventions, comfort distance violations. Subjective: questionnaires (NASA-TLX workload, SUS usability, trust scales). **Use proper statistics** (mixed-effects models, correction for multiple comparisons) and report participant numbers. Ethical review applies to human studies.

## 2. Multi-robot systems

### Why use many robots
Parallelism (cover more area), robustness (no single point of failure), specialisation (heterogeneous teams), cost (many simple robots).

### Core problems

| Problem | Typical approaches |
|---|---|
| **Task allocation** | auctions and market-based methods (CBBA), optimal assignment (Hungarian), MILP |
| **Multi-agent path finding (MAPF)** | priority planning, conflict-based search (CBS), traffic rules/lanes |
| **Formation and consensus control** | graph-Laplacian consensus, leader–follower, virtual structures |
| **Coverage and exploration** | Voronoi partitioning, frontier-based exploration, boustrophedon patterns |
| **Distributed SLAM** | share maps and loop closures (DOOR-SLAM, Swarm-SLAM), robust to outliers |
| **Communication-aware planning** | keep connectivity, handle delays and dropouts |
| **Fleet management** | Open-RMF, VDA5050, central traffic manager, elevators/doors integration |
| **Swarm robotics** | simple local rules produce collective behaviour (flocking, aggregation) |

### Architectures
| Architecture | Idea | Trade-off |
|---|---|---|
| **Centralised** | one planner for everyone | optimal, single point of failure, scales poorly |
| **Decentralised** | each robot decides from local info | robust, may be suboptimal |
| **Hierarchical / hybrid** | central goals, local execution | common in practice |

### Multi-agent learning
**MARL** trains several policies at once. Difficulty: from each agent's view the world is non-stationary. Common remedy: **centralised training, decentralised execution** (MAPPO, QMIX, MADDPG). Also emergent communication and population-based training.

## Interview Q&A

**What is shared autonomy?**
*Simply:* human and robot jointly control one robot. *Deeper:* infer the user's goal and blend commands, always letting the human override.

**How would you design a robust hand-over?**
*Simply:* detect the human's hand, approach legibly, release only when pull is sensed. *Deeper:* force thresholds, vision/tactile cues, safe speeds.

**Centralised versus decentralised multi-robot control?**
*Simply:* central is optimal but fragile; decentral is robust but may be worse. *Deeper:* hybrids are common.

**How do you assign tasks to many robots?**
*Simply:* auctions or optimal assignment. *Deeper:* CBBA for decentralised consensus; MILP for small problems.

**Why is MARL hard?**
*Simply:* other agents keep changing, so the environment is non-stationary. *Deeper:* CTDE is the standard fix.
