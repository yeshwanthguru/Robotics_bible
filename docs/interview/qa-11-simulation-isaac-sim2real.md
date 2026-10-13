---
title: "Q&A 11: Simulation, Isaac Sim/Lab/Gym & Sim-to-Real"
---

# Interview Q&A: Simulation, Isaac Sim, Isaac Lab, Isaac Gym and Sim-to-Real

:::tip[How to use]
Chapters: [Landscape](../13-simulation/simulation-landscape.md) · [Isaac Sim](../13-simulation/isaac-sim.md) · [Isaac Lab](../13-simulation/isaac-lab.md) · [Isaac Gym](../13-simulation/isaac-gym.md) · [Other simulators](../13-simulation/other-simulators.md) · [Sim-to-real](../13-simulation/sim2real.md).
:::

## Concepts

### Q: Why simulate?
**Short answer:** Safe, fast, parallel, resettable, and gives perfect labels. **Go deeper:** Also privileged information, domain randomisation, CI testing and synthetic data; the price is the reality gap.

### Q: Why can GPU simulators run thousands of environments?
**Short answer:** State lives in GPU tensors and physics, observations and rewards are batched without CPU–GPU copies. **Go deeper:** Environments are cloned into one scene and reset independently with masks.

### Q: MuJoCo versus PhysX versus Bullet contact?
**Short answer:** MuJoCo uses soft convex contact (smooth, great for control research); PhysX uses iterative rigid-body solvers (robust, GPU-scalable); Bullet is general-purpose. **Go deeper:** Solver iterations and timestep matter for stability.

### Q: What is OpenUSD and why is it used?
**Short answer:** A layered, composable scene format. **Go deeper:** Supports references, variants and physics schemas; enables collaboration and digital twins.

### Q: What does decimation mean in Isaac Lab?
**Short answer:** Physics steps per policy step. **Go deeper:** dt 0.005 s with decimation 4 gives 50 Hz control.

## Isaac Sim

### Q: What is Isaac Sim?
**Short answer:** NVIDIA's robotics simulator on Omniverse with PhysX, RTX sensors, USD scenes, ROS 2 bridge and Replicator. **Go deeper:** Runs headless, in containers or standalone Python.

### Q: Why does Isaac Sim need an RTX GPU?
**Short answer:** RT cores accelerate ray-traced rendering and RTX sensors. **Go deeper:** GPUs without RT cores (some datacentre parts) can't render but may run physics headless.

### Q: How do you bring in a custom robot?
**Short answer:** Import URDF/MJCF to USD, check articulation, set drives from real actuator data, tune inertia and collisions, add sensors. **Go deeper:** Validate against real logs.

### Q: How does the ROS 2 bridge work?
**Short answer:** OmniGraph nodes publish and subscribe topics (clock, TF, joint states, images, LiDAR). **Go deeper:** Match distro, use sim time, check frames and QoS.

### Q: What is Replicator used for?
**Short answer:** Domain randomisation and synthetic data generation. **Go deeper:** Randomise poses, lights, textures, cameras; write RGB, depth, segmentation, boxes.

### Q: Common causes of a robot exploding or flying in sim?
**Short answer:** Bad inertia or mass, missing articulation root, wrong units, stiff drives, too-large timestep. **Go deeper:** Check collision overlaps and joint limits.

### Q: How do you speed up Isaac Sim?
**Short answer:** Headless, fewer or smaller cameras, tiled rendering, simplified collision meshes, GPU pipeline. **Go deeper:** Use tensor APIs instead of per-prim loops.

## Isaac Lab and Isaac Gym

### Q: Isaac Sim versus Isaac Lab?
**Short answer:** Sim is the simulator; Lab is the robot-learning framework built on it. **Go deeper:** Lab provides environments, managers, assets, RL/IL scripts.

### Q: Isaac Gym versus Isaac Lab?
**Short answer:** Isaac Gym is the older standalone GPU RL tool (now deprecated); Isaac Lab replaced it. **Go deeper:** Lab adds USD, RTX sensors, modular managers, tiled cameras, teleoperation and imitation tools.

### Q: Manager-based versus direct workflow?
**Short answer:** Manager-based is declarative and modular; direct gives full control and performance. **Go deeper:** Managers: observation, action, reward, termination, event, command, curriculum.

### Q: Walk through training a locomotion policy in Isaac Lab.
**Short answer:** Robot config and actuators → terrain and curriculum → commands → observations → rewards → randomisation events → terminations → PPO with ~4096 envs → play, export, sim-to-sim, deploy. **Go deeper:** Use asymmetric critic and actuator models.

### Q: What are actuator models in Isaac Lab?
**Short answer:** Models mapping commands to torques: implicit PD, ideal PD, DC motor, learned networks. **Go deeper:** They set gains, saturation and delay; actuator nets reduce sim-to-real gap.

### Q: What RL libraries work with Isaac Lab?
**Short answer:** rsl_rl, skrl, rl_games, Stable-Baselines3. **Go deeper:** rsl_rl is the common choice for locomotion.

### Q: What is Isaac Lab Mimic?
**Short answer:** A tool that generates many demonstrations from a few human ones. **Go deeper:** Annotate subtasks and transform object-relative motion.

### Q: How do you scale Isaac Lab training?
**Short answer:** More environments per GPU, multi-GPU/multi-node via distributed training. **Go deeper:** Tune PhysX GPU buffer sizes if you see overflow warnings.

### Q: Common Isaac Lab pitfalls?
**Short answer:** Wrong action scaling, mismatched joint ordering, observation normalisation not exported, unmarked time-outs, privileged information leaking into the actor. **Go deeper:** Also quaternion order differences when porting from Isaac Gym.

### Q: How do you port an Isaac Gym task to Isaac Lab?
**Short answer:** Convert assets to USD, move PD gains to actuator configs, port logic to a direct env or manager terms. **Go deeper:** Check up-axis, quaternion order, joint ordering and solver parameters; re-tune rewards.

### Q: What is tiled rendering?
**Short answer:** Rendering all environments' cameras in one batched call. **Go deeper:** Enables vision-based RL at scale.

## Sim-to-real

### Q: Sources of the reality gap?
**Short answer:** Dynamics, actuation, sensing, appearance, latency and unmodelled effects. **Go deeper:** Actuator models and delays are often the largest.

### Q: What is domain randomisation and when does it hurt?
**Short answer:** Randomising simulator parameters so reality looks like another sample. **Go deeper:** Too wide a range makes policies timid; use ADR or system-ID to narrow it.

### Q: System identification versus domain randomisation?
**Short answer:** System ID measures real parameters; randomisation covers uncertainty. **Go deeper:** Best results use both.

### Q: What is an actuator network?
**Short answer:** A neural net trained from real data that predicts motor torque. **Go deeper:** Used for ANYmal to capture motor dynamics.

### Q: Why validate sim-to-sim?
**Short answer:** To catch overfitting to one engine's contact quirks before hardware. **Go deeper:** E.g. train in Isaac Lab, test in MuJoCo.

### Q: How would you deploy a trained policy?
**Short answer:** Export (TorchScript/ONNX), match observation order and scaling, run at policy frequency with PD at higher rate, add safety limits. **Go deeper:** Start with low gains/speeds and a gantry or harness.

### Q: How do you decide what to randomise?
**Short answer:** Sensitivity analysis plus what varies on hardware. **Go deeper:** Friction, mass, delay and motor gains usually matter most.

### Q: What is real-to-sim-to-real?
**Short answer:** Reconstruct the real scene into simulation, train or evaluate there, deploy back. **Go deeper:** NeRF/Gaussian splats or scans give assets; reduces visual and geometric gaps.

### Q: How do you measure sim-to-real success?
**Short answer:** Task success, tracking error and energy on hardware compared with simulation logs. **Go deeper:** Compare torque, velocity and contact-timing distributions.

### Q: Which simulator would you choose for X?
**Short answer:** Massively parallel RL: Isaac Lab/MJX/Genesis. Photoreal sensors and digital twins: Isaac Sim. ROS integration tests: Gazebo. Model-based control research: MuJoCo/Drake. **Go deeper:** Justify with speed, fidelity, ecosystem and licensing.
