---
title: Isaac Gym (Legacy but Still Asked)
---

# Isaac Gym

**Isaac Gym Preview (1–4)** — NVIDIA's standalone high-performance GPU physics simulator for RL (2021). It kept simulation *and* observation/reward computation on the GPU, exposing state as PyTorch tensors, which is why training locomotion in minutes became possible ("Learning to Walk in Minutes Using Massively Parallel Deep RL", Rudin et al.). It is **deprecated** in favour of **Isaac Lab**, but a lot of papers, `legged_gym`, `IsaacGymEnvs`, `rsl_rl`, `DexPBT`, `DeXtreme`, `ExtremeParkour`, Unitree/Humanoid codebases still use it.

## Core API (gymapi)
```python
from isaacgym import gymapi, gymtorch, gymutil
import torch

gym = gymapi.acquire_gym()
sim_params = gymapi.SimParams()
sim_params.up_axis = gymapi.UP_AXIS_Z
sim_params.dt = 1/60.; sim_params.substeps = 2
sim_params.physx.use_gpu = True; sim_params.use_gpu_pipeline = True
sim = gym.create_sim(0, 0, gymapi.SIM_PHYSX, sim_params)

asset = gym.load_asset(sim, "assets", "urdf/anymal.urdf", gymapi.AssetOptions())
for i in range(num_envs):
    env = gym.create_env(sim, lower, upper, envs_per_row)
    actor = gym.create_actor(env, asset, pose, "robot", i, 1)

gym.prepare_sim(sim)
root_states = gymtorch.wrap_tensor(gym.acquire_actor_root_state_tensor(sim))   # [N, 13]
dof_states  = gymtorch.wrap_tensor(gym.acquire_dof_state_tensor(sim))          # [N*dofs, 2]
gym.set_dof_position_target_tensor(sim, gymtorch.unwrap_tensor(targets))
gym.simulate(sim); gym.fetch_results(sim, True)
gym.refresh_actor_root_state_tensor(sim); gym.refresh_dof_state_tensor(sim)
```
Key points: **tensor API** (acquire → wrap → refresh after each step), `use_gpu_pipeline=True`, env/actor handles, DOF properties (`DOF_MODE_POS/VEL/EFFORT`, stiffness, damping), force sensors, rigid-body contact tensor, viewer (disable for headless), camera sensors (basic rasterization, `gym.get_camera_image_gpu_tensor`).

## Frameworks on top
| Repo | Purpose |
|---|---|
| **IsaacGymEnvs** | official tasks: Ant, Humanoid, ShadowHand, AllegroHand, Anymal, Franka cabinet, Factory (assembly) with rl_games PPO |
| **legged_gym** (ETH Zürich RSL) | quadruped locomotion, terrain curriculum, PPO via `rsl_rl` |
| **rsl_rl** | compact PPO |
| **DexPBT, DeXtreme** | population-based training / dexterous hand sim2real |
| **walk-these-ways, Extreme Parkour, ANYmal parkour** | agile locomotion |
| **humanoid-gym, HumanoidVerse, ASAP, H2O, ExBody** | humanoid RL |

## Typical task skeleton (IsaacGymEnvs)
`VecTask` subclass: `create_sim()`, `_create_envs()`, `pre_physics_step(actions)` (apply targets), `post_physics_step()` → `compute_observations()`, `compute_reward()` (torch.jit scripted), `reset_idx(env_ids)`. Config YAML: `numEnvs`, `episodeLength`, `controlFrequencyInv`, reward scales, randomization ranges.

## Domain randomization in Gym
`randomization_params` with distribution/ range / schedule: gravity, dof properties, rigid body mass/friction, actor scale, observation/action noise, delay. `gym.set_actor_rigid_shape_properties` for friction/restitution, push by setting root velocity.

## Migrating to Isaac Lab
- Task logic ports to `DirectRLEnv` almost one-to-one; or reformulate as Manager-based terms.
- URDF → USD (importer) with same actuator parameters; PD stiffness/damping move to `ActuatorCfg`.
- Different default conventions: quaternion order (Gym: xyzw; Isaac Lab: wxyz), up-axis, joint ordering (breadth-first in Lab vs depth-first in Gym for some assets), solver parameters; re-tune rewards and verify with sim2sim.
- Config style: YAML → Python `@configclass`.

## Interview Q&A

**Why was Isaac Gym so fast?** No CPU-GPU copies: physics, state tensors, rewards, observations, and resets live on GPU; thousands of envs per step.

**Limitations?** Standalone preview w/o support, basic rendering and sensors, Linux-only, URDF/MJCF only, Python 3.6–3.8 era dependencies, no active maintenance.

**What is `legged_gym` reward structure?** Linear/angular velocity tracking, base height & orientation, torques, joint acc/vel limits, action rate, feet air time, collisions, termination.

**Quaternion convention bug example?** Gym xyzw vs Isaac Lab wxyz → wrong orientation observation after porting.
