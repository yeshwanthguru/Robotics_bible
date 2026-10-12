---
title: Simulation Landscape & Comparison
---

# Simulation for Robotics

## Why simulate
Safety, speed (1000× parallel), cost, privileged information (ground-truth state/terrain), reset/repeatability, synthetic data with perfect labels, CI testing, digital twins. Why not: reality gap (contact, friction, actuation, sensor noise, latency), modelling effort.

## What a simulator is made of
1. **Physics engine** – integrator, collision detection (broadphase/narrowphase), constraint/contact solver, articulation (maximal vs reduced coordinates).
2. **Scene description** – URDF, SDF, MJCF, **USD**.
3. **Renderer** – rasterization or ray/path tracing for camera sensors.
4. **Sensor models** – camera, depth, LiDAR (ray-cast), IMU, contact/force, encoders, noise.
5. **Middleware bridge** – ROS/ROS 2, Python API, gym API.
6. **Tooling** – domain randomization, data generation, recording, replay.

## Simulator comparison
| Simulator | Physics | GPU parallel | Rendering | Strengths | Weaknesses |
|---|---|---|---|---|---|
| **Isaac Sim** | PhysX 5 (GPU) (+ Newton in newer releases) | yes | RTX ray/path-traced | photoreal sensors, USD, digital twins, ROS 2, Replicator | heavy (RTX GPU, big VRAM), learning curve |
| **Isaac Lab** | PhysX on Isaac Sim | yes (thousands of envs) | RTX tiled cameras | official RL/IL framework, modular, many robots | tied to Isaac Sim |
| **Isaac Gym (Preview 4)** | PhysX GPU | yes | basic | pioneered GPU RL (legged_gym) | **deprecated**, Linux only, no more updates |
| **MuJoCo** (+ **MJX**, **MuJoCo Warp**, **MuJoCo Playground**) | soft convex contact, generalized coords | MJX/Warp on GPU/TPU | OpenGL | accuracy, speed, differentiable (MJX), research standard | fewer sensors/assets natively |
| **Gazebo (gz sim)** | DART/Bullet/TPE | no | OGRE2 | ROS native, mature | slow for RL |
| **PyBullet** | Bullet | CPU | OpenGL | easy, free | aging |
| **Genesis** | multiple (rigid, MPM, SPH, FEM) | yes, very fast | Rasterizer/ray-tracer | generative, differentiable, unified | young |
| **ManiSkill3 / SAPIEN** | PhysX | yes | GPU rasterizer | manipulation benchmarks, fast vision RL | |
| **Drake** | exact-ish contact, convex | CPU | meshcat | model-based control, systems framework | RL scale |
| **Brax** | generalized, JAX | TPU/GPU | minimal | blazing RL | simplified contact |
| **Webots / CoppeliaSim / RoboDK** | ODE/Bullet/Vortex | no | | education, industrial | |
| **CARLA / AirSim / LGSVL** | Unreal/Unity | | photoreal | driving, drones | |
| **Newton** | open-source GPU physics (NVIDIA + Google DeepMind + Disney; Linux Foundation) on NVIDIA Warp | yes | | differentiable, MuJoCo-Warp solver | new |

Selection heuristic: **massively parallel RL** → Isaac Lab / MJX / Genesis / ManiSkill3; **photoreal perception data & digital twin** → Isaac Sim; **fast ROS prototyping** → Gazebo; **model-based control research** → MuJoCo/Drake; **differentiable physics** → MJX/Warp/Genesis/Brax.

## Physics concerns to mention
- Time step & substeps (dt=0.005 sim step, decimation 4 → policy 50 Hz), solver iterations, penetration/ contact offset, restitution, friction combine modes, joint armature/damping, drive stiffness/damping (PD gains), maximum depenetration velocity, articulation self-collisions, mesh convex decomposition (V-HACD/CoACD), collision proxies vs visual meshes.
- **Determinism**: GPU simulation not bitwise reproducible; seed all RNGs.

## Interview Q&A

**Why can GPU simulators run thousands of environments?** State stored as GPU tensors; physics and observation/reward computation batched without CPU-GPU transfers.

**Why did Isaac Gym get replaced?** Isaac Lab sits on Isaac Sim/Omniverse: USD assets, RTX sensors, modular managers, active development, ROS 2 and sim-data tools; Gym was standalone and unmaintained.

**MuJoCo vs PhysX contact?** MuJoCo: soft, convex-optimization contact – smooth, good for gradients and control research; PhysX: rigid-body with PGS/TGS solvers – robust for large scenes and GPU scale.
