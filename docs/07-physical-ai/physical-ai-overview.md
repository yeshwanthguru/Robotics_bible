---
title: Physical AI Overview
---

# Physical AI

:::tip[The 30-second version]
**Physical AI** = AI that doesn't just *talk* but *acts in the real world*: robots, self-driving cars, drones, factory machines. Chat AI learned from the internet's text; Physical AI has a harder job because there is **no internet of robot actions**, the world is messy, and mistakes break things. So it leans on **simulation** to practise safely and on **foundation models** to understand and plan.
:::

## The three-computer picture

![three computers](/img/fig/three-computers.svg)
*Train the brain on big GPUs, practise it in simulation, run it on the robot's own computer.*

1. **Train**: GPU clusters train foundation models and policies.
2. **Simulate**: virtual worlds (Isaac Sim / Isaac Lab, Cosmos) provide safe practice, synthetic data and testing.
3. **Run**: an onboard computer (e.g. Jetson) executes the policy in real time.

## The stack, layer by layer

![physical ai stack](/img/fig/physical-ai-stack.svg)
*Each layer relies on the one below it; simulation and data feed all of them.*

| Layer | Question it answers | Typical tools |
|---|---|---|
| **Foundation models** | what is going on, what should I do? | VLM, VLA, world models |
| **Task & motion planning** | what steps, which collision-free path? | PDDL, behavior trees, MoveIt |
| **Skills** | how do I grasp / walk / pour? | imitation learning, RL policies |
| **Whole-body control** | how do I move the motors smoothly and safely? | MPC, impedance, WBC |
| **Perception & estimation** | where am I, what's where? | SLAM, filters, detection |
| **Hardware** | sensors, motors, compute, battery | Jetson, EtherCAT, BLDC |

## Why it is hard

| Challenge | Plain explanation |
|---|---|
| **Data scarcity** | no web-scale dataset of robot actions → teleoperation, simulation, human video, shared datasets |
| **Sim-to-real gap** | simulators approximate friction, contact and motors imperfectly |
| **Real-time + safety** | decisions at 100–1000 Hz; failures hurt hardware and people |
| **Contact-rich physics** | touching, sliding, sticking is hard to model and simulate |
| **Long horizons** | a household task is dozens of steps; errors compound |
| **Evaluation** | real tests are slow and noisy; you need many trials for honest numbers |

*Moravec's paradox:* things that feel easy to humans (picking up a sock) are hard for machines, and things that feel hard (chess) are easy.

## Ways to build a behaviour

| Paradigm | Idea | Strength | Weakness |
|---|---|---|---|
| **Classical** (model + planning + control) | engineer it | guarantees, explainable | brittle perception, effort per task |
| **RL in simulation** | trial and error at scale | agile, robust locomotion | reward design, sim gap |
| **Imitation / VLA** | learn from demonstrations | many tasks, language | needs demos, covariate shift |
| **Hybrid** | VLM planner + learned skills + classical safety | what works today | integration complexity |

**Industry pattern today:** end-to-end VLAs for manipulation, RL for locomotion, classical control and safety layers underneath.

## The embodiments
Arms and grippers, dexterous hands, mobile manipulators, quadrupeds (Spot, Go2, ANYmal), humanoids (Atlas, Optimus, Figure, Digit, Unitree G1/H1), drones, autonomous vehicles, underwater and space robots, soft and surgical robots.

## Interview Q&A

**Physical AI vs embodied AI?**
*Simply:* mostly the same idea; "Physical AI" stresses real deployment and simulation-driven data.

**Why simulate first?**
*Simply:* safe, fast, parallel, resettable, and gives perfect labels.

**Is end-to-end learning enough for manipulation?**
*Simply:* it works for many tasks, but keep reactive safety layers for force limits and guarantees.

**What do you think is the biggest bottleneck?**
*Good answer:* data (diverse, high-quality robot experience) and reliable evaluation. Models are improving faster than our ability to collect data and measure real success.
