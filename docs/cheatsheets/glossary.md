---
title: Glossary (A–Z)
---

# Glossary: plain-English definitions

:::tip[How to use this page]
Skim it the night before. Each term has a one-line meaning you could say out loud in an interview.
:::

| Term | Plain English |
|---|---|
| **ACT** | Action Chunking Transformer: predicts a whole short sequence of actions at once from demos |
| **ADE / FDE** | average / final displacement error: how far predicted trajectories are from real ones |
| **AMCL** | Adaptive Monte-Carlo Localization: particle-filter localisation on a known map (Nav2) |
| **AMR** | autonomous mobile robot, e.g. a warehouse cart that drives itself |
| **BA** | bundle adjustment: jointly refine camera poses and 3-D points by minimising reprojection error |
| **BC** | behavior cloning: supervised learning from expert demonstrations |
| **BT** | behavior tree: a hierarchical way to organise robot behaviours |
| **CBF** | control barrier function: a safety constraint that keeps the system inside a safe set |
| **CoM / CoP** | centre of mass / centre of pressure |
| **CQL** | conservative Q-learning: offline RL that avoids over-trusting unseen actions |
| **DDS** | Data Distribution Service: the messaging middleware under ROS 2 |
| **DH parameters** | four numbers per joint that describe a robot arm's geometry |
| **DoF** | degrees of freedom: independent ways something can move |
| **DR** | domain randomization: vary the simulator so the policy generalises |
| **EKF / UKF** | extended / unscented Kalman filter: Kalman filters for non-linear systems |
| **ESDF / TSDF** | (Euclidean) signed distance field: a map storing distance to the nearest surface |
| **FK / IK** | forward / inverse kinematics: joints → hand pose / hand pose → joints |
| **FOC** | field-oriented control: smart current control for efficient motors |
| **GAE** | generalised advantage estimation: a smoother estimate of how good an action was |
| **GCS** | graph of convex sets: a planning method combining search with convex optimisation |
| **GRPO** | group relative policy optimization: RL for LLMs that compares a group of answers |
| **HIL** | hardware-in-the-loop, or human-in-the-loop |
| **ICP** | iterative closest point: aligns two point clouds |
| **IMU** | inertial measurement unit: gyro + accelerometer |
| **InEKF** | invariant EKF: a Kalman filter that respects rotation/pose symmetry |
| **LIPM** | linear inverted pendulum model: simple model of walking |
| **LIO / VIO** | LiDAR- / visual-inertial odometry |
| **LoRA** | low-rank adaptation: fine-tune a big model by training a small add-on |
| **MoE** | mixture of experts: many sub-networks, a router uses a few per token |
| **MPC / MPPI** | model predictive control / path-integral variant: plan ahead, act, replan |
| **NISQ** | noisy intermediate-scale quantum: today's imperfect quantum chips |
| **NITROS** | NVIDIA's zero-copy transport for ROS 2 |
| **OMPL** | Open Motion Planning Library (RRT, PRM and friends) |
| **PDDL** | Planning Domain Definition Language: the standard language for task planning |
| **PEFT** | parameter-efficient fine-tuning |
| **PoE** | product of exponentials: a clean way to write forward kinematics |
| **PPO / SAC / TD3** | popular RL algorithms (on-policy clipped, entropy off-policy, twin-critic off-policy) |
| **QAOA / VQE** | hybrid quantum algorithms for optimisation / chemistry |
| **QoS** | quality of service: delivery rules for ROS 2 messages |
| **QUBO** | quadratic unconstrained binary optimisation: a format for annealers |
| **RAG** | retrieval-augmented generation: LLM answers using retrieved documents |
| **REP** | ROS enhancement proposal: official conventions (e.g. REP-103 units, REP-105 frames) |
| **RMW** | ROS middleware layer: swap DDS vendors without changing code |
| **RNEA** | recursive Newton–Euler algorithm: fast inverse dynamics |
| **SEA** | series elastic actuator: motor + spring for force control |
| **SLAM** | simultaneous localization and mapping |
| **TAMP** | task and motion planning |
| **TF** | transform tree: the live family tree of coordinate frames in ROS |
| **URDF / SDF / MJCF / USD** | robot / scene description formats (ROS / Gazebo / MuJoCo / Isaac) |
| **VLA / VLM** | vision-language(-action) model |
| **WBC** | whole-body control |
| **ZMP** | zero-moment point: the ground point where tipping torque is zero |
