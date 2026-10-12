---
title: Rapid-Fire Question Bank
---

# Rapid-Fire Question Bank

Answer each in **≤ 30 seconds**. Cover the answer and test yourself.

## ML / DL
1. Bias–variance trade-off? → error = bias² + variance + noise; capacity moves along the curve.
2. L1 vs L2? → L1 sparse (Laplace prior), L2 shrinks (Gaussian prior).
3. Why cross-entropy for classification? → MLE under categorical model; convex for logistic, strong gradients when wrong.
4. Explain backprop. → reverse-mode autodiff of chain rule through computation graph.
5. Why residual connections? → gradient highway, easier optimization.
6. Attention complexity and fixes? → O(n²); FlashAttention (IO), sparse/linear/SSM.
7. LayerNorm vs BatchNorm? → per-sample feature vs batch statistics.
8. How does dropout regularize? → ensemble of subnetworks, prevents co-adaptation.
9. Overfitting remedies? → data, augmentation, regularization, early stopping, simpler model.
10. How do you handle class imbalance? → reweight, focal loss, resample, PR-AUC.

## RL
11. Bellman equation? 12. On vs off-policy? 13. PPO clip purpose? 14. SAC entropy term? 15. Why GAE? 16. Exploration–exploitation? 17. Sparse reward handling (shaping, HER, curriculum, demos)? 18. Why sim RL needs domain randomization? 19. Reward hacking example? 20. Offline RL's main problem (OOD actions/extrapolation error)?

## LLM / VLM / VLA
21. How does KV cache work? 22. LoRA mechanics? 23. RLHF vs DPO? 24. RAG failure modes? 25. How do VLAs represent actions? 26. π0 vs OpenVLA? 27. Why action chunking? 28. How do you evaluate a VLA? 29. Hallucination mitigation? 30. Dual-system architecture rationale?

## Quantum
31. Qubit vs bit? 32. Why unitary gates? 33. Grover speed-up and optimality? 34. Shor's key idea (period finding)? 35. VQE steps and limits (barren plateaus)? 36. NISQ vs fault tolerant? 37. QUBO → Ising? 38. Where could quantum help robotics (optimization, sensing)? 39. Quantum kernel idea? 40. Entanglement measure?

## Robotics core
41. Rotation representations pros/cons? 42. DH vs PoE? 43. Jacobian singularity handling? 44. Computed torque control? 45. Impedance vs admittance? 46. ZMP vs capture point? 47. EKF vs UKF vs PF? 48. Graph SLAM and loop closure? 49. ICP steps and pitfalls? 50. A* vs RRT* vs trajectory optimization? 51. MPC vs LQR? 52. Differential drive kinematics? 53. Nav2 architecture? 54. MoveIt planning pipeline? 55. Force vs form closure? 56. Why tactile sensing? 57. In-hand manipulation via RL pitfalls? 58. Whole-body control QP structure? 59. How do quadrotors achieve trajectory tracking (flatness, cascaded)? 60. Sensor fusion for GPS-denied navigation?

## Software
61. ROS 2 QoS compatibility rules? 62. Callback groups & executors? 63. Lifecycle nodes? 64. TF extrapolation error causes? 65. ros2_control architecture? 66. C++ move semantics / RAII / smart pointers? 67. Real-time constraints in C++? 68. Python GIL? 69. MATLAB vs Python for control? 70. PDDL action modelling & BT vs FSM?

## Simulation
71. Isaac Sim vs Isaac Lab vs Isaac Gym? 72. Manager-based vs direct workflow? 73. What is USD? 74. Replicator use? 75. Decimation, dt, policy frequency? 76. DR parameters for locomotion? 77. Sim2sim validation? 78. Actuator net? 79. Tiled camera rendering? 80. Common PhysX failure causes?

## Show-off follow-ups
- “What would you do with a week of data collection budget for a new manipulation task?”
- “Your policy works in sim but jitters on hardware. Debug.” → latency, PD gain mismatch, observation noise, action-rate penalty, filters, actuator model.
- “Robot drifts after 10 min.” → odometry bias, loop closure absent, wheel slip, time sync, thermal IMU bias.
- “Why not just use a bigger model?” → latency, power, data, safety.
