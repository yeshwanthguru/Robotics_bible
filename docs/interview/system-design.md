---
title: Robotics System Design Interviews
---

# System Design for Robotics / Physical AI

## Framework (use every time)
1. **Requirements:** task, environment, throughput/cycle time, success rate, safety, budget, uptime.
2. **Constraints:** compute (edge vs cloud), latency, power, comms, certification.
3. **Architecture:** sensing → perception → state estimation → planning → control → actuation + safety supervisor + monitoring.
4. **Data & learning loop:** collect → label → train → evaluate (sim + real) → deploy → monitor → retrain.
5. **Failure modes & mitigations.**
6. **Metrics & rollout plan.**

## Example 1 — Warehouse mobile manipulator for bin picking
- Requirements: 600 picks/hr, 99 % success, SKU variety 10k, collaborative safety.
- Hardware: AMR base + 6-DOF arm + suction/ parallel gripper, wrist RGB-D, safety LiDAR, F/T sensor.
- Software: Nav2 + AMCL/LiDAR localization; fiducial docking at shelves; perception (segmentation SAM-based + grasp network); MoveIt 2/cuMotion planning; compliant place; BT orchestrates; fleet via Open-RMF; exception handling → teleop assist.
- Learning: grasp model trained on sim (Isaac Sim Replicator) + real failure data; active learning from failed grasps.
- Safety: speed-and-separation, PL-d rated stops, protective stops on force limits.
- Metrics: picks/hr, grasp success, intervention rate, MTBF.

## Example 2 — Humanoid doing household tasks (VLA + loco)
- Stack: VLM/VLA (System 2, 5–10 Hz) for task reasoning and action chunks; learned whole-body controller (System 1, 50–200 Hz) tracks upper-body & locomotion commands; classical safety layer (joint limits, torque, fall detection).
- Data: teleop (VR + MoCap retargeting), sim generation (Isaac Lab Mimic + Cosmos), human egocentric video.
- Training: pretrain VLM → co-train robot data → fine-tune per task → RL fine-tune; evaluate in sim arena then real with N ≥ 50 trials.
- Deployment: Jetson Thor, TensorRT, async chunk inference.
- Risks: latency, OOD objects, long-horizon drift, hardware overheating.

## Example 3 — Autonomous inspection quadruped
Localization: LiDAR-inertial odometry + map prior; terrain mapping; footstep/locomotion RL policy; mission planner; autonomy BT; arm for valves (optional); data capture, thermal camera; comms dropouts → autonomous fallback & return-to-base.

## Example 4 — LLM-driven task planner for ROS 2 robot
NL → structured plan (JSON/PDDL) → validator (VAL/simulator) → BT executor → skill servers (Nav2, MoveIt) → feedback to LLM. Guardrails: action allowlist, parameter bounds, human confirmation for risky actions, timeouts, recovery.

## Example 5 — Sim-to-real RL pipeline for a legged robot
Robot URDF → USD; actuator identification; Isaac Lab task; DR; PPO training; sim2sim in MuJoCo; deploy on hardware; logging; iterate with real data; CI regression of policy on benchmark terrains.

## Example 6 — Perception data engine
Collect fleet data → trigger-based sampling (uncertainty, disagreement) → auto-label (foundation models) → human review → train → shadow-mode eval → staged rollout; metrics drift monitoring.

## Reliability / safety talking points
Independent safety controller (ISO 13849), watchdog, redundancy, fault detection (innovation tests), degraded modes, formal specs for critical logic, simulation fuzzing, scenario-based testing, black-box recorders.
