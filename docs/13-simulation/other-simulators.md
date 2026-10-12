---
title: MuJoCo, Gazebo, PyBullet, Genesis, ManiSkill, Drake
---

# Other Simulators You Should Know

## MuJoCo ecosystem
- **MuJoCo** (Multi-Joint dynamics with Contact; now open-source under DeepMind): generalized coordinates, soft convex contact model (solver-based, smoothing via `solref/solimp`), MJCF XML, tendons, actuators, sensors (touch, force, IMU, rangefinder), fast and numerically stable; `mujoco` Python bindings, `mujoco.viewer`.
- **MJX**: JAX re-implementation → GPU/TPU, `jax.vmap` batch thousands of envs, differentiable. **MuJoCo Warp (MJWarp)**: NVIDIA Warp backend, GPU-accelerated, (co-developed with DeepMind; used by Newton). **MuJoCo Playground**: RL environments (locomotion, manipulation, dexterous) with MJX; sim-to-real recipes for Go1, Berkeley Humanoid, Booster T1, Panda, LEAP hand. **dm_control** / **Menagerie** (curated robot models: UR5e, Panda, Spot, Go2, H1, G1, Allegro, Shadow hand).
- Tools: `gymnasium` MuJoCo envs (Ant, Humanoid, HalfCheetah), `robosuite` (manipulation benchmark), `robopianist`, `LocoMuJoCo`, MuJoCo MPC (MJPC).

```python
import mujoco, mujoco.viewer
m = mujoco.MjModel.from_xml_path("scene.xml"); d = mujoco.MjData(m)
with mujoco.viewer.launch_passive(m, d) as v:
    while v.is_running():
        d.ctrl[:] = policy(d.qpos, d.qvel)
        mujoco.mj_step(m, d); v.sync()
```

## Gazebo (Ignition/gz sim)
Entity-component architecture, plugins (physics: DART default, Bullet, TPE; rendering OGRE2; sensors), SDF worlds, `ros_gz_bridge`/`ros_gz_sim`, `gz_ros2_control`; classic Gazebo (Gazebo 11) is EOL. Strengths: ROS 2 integration, community models (Gazebo Fuel), headless CI; weaknesses: no massive parallelism, contact fidelity moderate. Typical use: Nav2 / MoveIt integration testing, TurtleBot3, PX4 SITL.

## PyBullet
Bullet physics via Python; URDF/SDF/MJCF; `p.loadURDF`, `p.stepSimulation`, inverse kinematics built-in; easy but limited fidelity and no GPU scale. Used in older RL papers (`pybullet_envs`, `panda-gym`, `gym-pybullet-drones`).

## Genesis
Universal physics platform (Python) with rigid, MPM, SPH, FEM, PBD; GPU-accelerated (Taichi, now also supporting more backends); claims very high simulation throughput; photorealistic ray-tracing renderer; differentiable; generative data pipeline. Good for soft/ fluid/ deformable contact tasks and RL. Newer ecosystem – check maturity per use-case.

## ManiSkill3 / SAPIEN
GPU-parallelized manipulation simulator (PhysX GPU) with fast GPU rasterized cameras, hundreds of tasks (pick cube, peg insertion, humanoid, mobile manipulation, dexterous), benchmark for imitation/RL, includes demonstration datasets and motion-planning solutions; supports sim-to-real pipelines (SO-100 / LeRobot arms, Panda, xArm).

## Drake
MIT/TRI: multibody dynamics, hydroelastic contact, optimization-based planning/control (MathematicalProgram, GCS, trajectory optimization), systems framework (diagram/block-based), Meshcat. Best for model-based control and verification (Lyapunov/SOS).

## Brax / MJX style (JAX physics)
Whole training loop JIT-compiled on accelerator (PPO/SAC, evolutionary strategies). Millions of steps/s; simplified contact; ideal for algorithm research.

## Webots / CoppeliaSim / RoboDK / Unity ML-Agents / Unreal (CARLA, AirSim)
Education, industrial offline programming, game-engine photorealism for driving/drone simulation.

## Choosing & validating (sim2sim)
Train in a fast engine (Isaac Lab/MJX) → validate in a second engine (MuJoCo/Gazebo) to catch overfitting to one engine's contact quirks → deploy. Compare trajectories, contact timing, torque profiles.

## Interview Q&A

**MuJoCo vs Bullet vs PhysX?** MuJoCo: accuracy/smoothness for control; Bullet: general, easy; PhysX: scalable GPU & rendering ecosystem via Isaac.

**What is MJX good for?** Massively parallel differentiable sim in JAX; policy gradients through physics; RL at TPU/GPU scale.

**Why still use Gazebo?** ROS-native integration tests, sensor plugins, CI without GPU, PX4 SITL.
