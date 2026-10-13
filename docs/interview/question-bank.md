---
title: Interview Q&A Hub
sidebar_position: 0
---

# Interview Q&A: the complete question bank

:::tip[How this section works]
Every question has a **Short answer** (say it in about 20 seconds) and a **Go deeper** line for follow-ups. Each question is its own heading, so you can **search any question or keyword with Ctrl+K**. Use it for interviews, but also as a quick-answer reference whenever you need to refresh a topic.
:::

## Browse by domain

| # | Page | Covers |
|---|---|---|
| 1 | [Math, CS & Machine Learning](./qa-1-math-cs-ml.md) | linear algebra, probability, optimisation, algorithms, concurrency, ML evaluation, classical models |
| 2 | [Deep Learning](./qa-2-deep-learning.md) | training, normalisation, CNN/transformer/GNN, diffusion, flow matching, representation learning |
| 3 | [Reinforcement Learning](./qa-3-reinforcement-learning.md) | MDPs, PPO/SAC, reward design, offline RL, imitation, RLHF |
| 4 | [LLM, VLM & VLA](./qa-4-llm-vlm-vla.md) | pretraining, LoRA, RAG, serving, VLM design, VLA action heads, evaluation |
| 5 | [Quantum Computing](./qa-5-quantum.md) | qubits, gates, Grover/Shor, VQE/QAOA, error correction, quantum robotics |
| 6 | [Kinematics, Dynamics & Control](./qa-6-kinematics-dynamics-control.md) | rotations, Jacobians, dynamics, PID, LQR, MPC, impedance, WBC |
| 7 | [Perception, SLAM & Estimation](./qa-7-perception-slam-estimation.md) | Kalman/particle filters, SLAM, ICP, camera geometry, sensors |
| 8 | [Planning & Navigation](./qa-8-planning-navigation.md) | RRT/PRM/A*, trajectory optimisation, PDDL, behavior trees, Nav2 |
| 9 | [Manipulation, Dexterity & Locomotion](./qa-9-manipulation-locomotion.md) | grasping, tactile, in-hand, legged, humanoid, space and soft robots |
| 10 | [Software: ROS 2, C++, Python…](./qa-10-software-ros2-cpp-python.md) | ROS 2, C++, Python, MATLAB, R, Docker, CI |
| 11 | [Simulation & Sim-to-Real](./qa-11-simulation-isaac-sim2real.md) | Isaac Sim/Lab/Gym, MuJoCo, domain randomisation, deployment |
| — | [System design](./system-design.md) | design a robot or fleet end to end |
| — | [Coding challenges](./coding-challenges.md) | code you should write from memory |
| — | [Behavioral & story bank](./behavioral.md) | your own stories, research questions |

## Rapid-fire self-test (say each answer in under 30 seconds)

**ML / DL:** Bias vs variance? L1 vs L2? Why cross-entropy? Explain backprop. Why residuals? Attention complexity? LayerNorm vs BatchNorm? Overfitting fixes? Class imbalance?

**RL:** Bellman equation? On vs off-policy? PPO clip? SAC entropy? GAE? Sparse rewards? Why domain randomisation? Offline RL's main problem?

**LLM / VLM / VLA:** KV cache? LoRA? RLHF vs DPO? RAG failure modes? How are VLA actions represented? Why action chunking? Dual-system design? How do you evaluate a VLA?

**Quantum:** Qubit vs bit? Why unitary? Grover speed-up? Shor's idea? VQE limits? NISQ vs fault tolerant?

**Robotics core:** Rotation representations? DH vs PoE? Singularity handling? Computed torque? Impedance vs admittance? ZMP vs capture point? EKF vs UKF vs PF? Loop closure? ICP pitfalls? A* vs RRT*? LQR vs MPC?

**Software and simulation:** QoS compatibility? Callback groups? Lifecycle nodes? TF extrapolation? Move semantics? Real-time C++ rules? GIL? Isaac Sim vs Lab vs Gym? Manager vs direct? What is USD? Decimation? Sim2sim?

## Show-off follow-up scenarios

- *"Your policy works in sim but jitters on hardware. Debug."* → latency, PD gain mismatch, observation noise, missing actuator model, action-rate penalty, filters.
- *"The robot drifts after 10 minutes."* → odometry bias, no loop closure, wheel slip, time sync, thermal IMU bias.
- *"You have a week and a budget to collect data for a new task."* → define success metric, ACT baseline with ~50 diverse demos, evaluate with confidence intervals, tag failures, collect targeted data.
- *"Why not just use a bigger model?"* → latency, power, data, safety, and evaluation cost.
