---
title: Interactive Simulators
---

# Interactive Simulators

:::tip[Learn by playing]
Each simulator runs **in your browser** (no install). Drag, click and move the sliders, and watch the concept behave. Every one is also embedded in its chapter under **🎮 Try it yourself**.
:::

| Simulator | What to try | Chapter | Full screen |
|---|---|---|---|
| PID controller | raise Kp until it rings, add Kd to damp, add Ki to remove offset | [Control](../10-planning-control/control.md) | [open](pathname:///Robotics_bible/sim/pid.html) |
| Balancing pole (cart-pole) | switch the controller off, weaken the gains | [Control](../10-planning-control/control.md) | [open](pathname:///Robotics_bible/sim/cartpole.html) |
| Gradient descent | large learning rate, momentum | [DL fundamentals](../03-deep-learning/dl-fundamentals.md) | [open](pathname:///Robotics_bible/sim/gradient-descent.html) |
| Neural-network playground | spiral dataset, few vs many hidden units | [DL fundamentals](../03-deep-learning/dl-fundamentals.md) | [open](pathname:///Robotics_bible/sim/mlp-playground.html) |
| Softmax and attention | temperature from sharp to flat | [Architectures](../03-deep-learning/architectures.md) | [open](pathname:///Robotics_bible/sim/attention.html) |
| Over/underfitting | polynomial degree 1 to 12 | [ML fundamentals](../02-machine-learning/ml-fundamentals.md) | [open](pathname:///Robotics_bible/sim/bias-variance.html) |
| k-means | wrong k, bad initial centres | [More ML](../02-machine-learning/ml-more-topics.md) | [open](pathname:///Robotics_bible/sim/kmeans.html) |
| Q-learning grid world | exploration ε, walls, the cliff | [RL foundations](../04-reinforcement-learning/rl-foundations.md) | [open](pathname:///Robotics_bible/sim/qlearning.html) |
| Bloch sphere | H, then Z, then H | [Quantum basics](../06-quantum/quantum-basics.md) | [open](pathname:///Robotics_bible/sim/bloch.html) |
| 2-link arm IK | reach limits, elbow flip, singularity | [Kinematics](../08-robotics/kinematics.md) | [open](pathname:///Robotics_bible/sim/ik-2link.html) |
| Kalman filter | change Q and R | [State estimation](../09-perception-localization/state-estimation.md) | [open](pathname:///Robotics_bible/sim/kalman.html) |
| Particle filter localization | kidnap the robot | [SLAM and localization](../09-perception-localization/slam-localization.md) | [open](pathname:///Robotics_bible/sim/particle-filter.html) |
| Pinhole camera | focal length, camera pose | [3-D vision](../09-perception-localization/computer-vision-3d.md) | [open](pathname:///Robotics_bible/sim/camera.html) |
| A\* / Dijkstra / RRT | draw walls, compare explored area | [Motion planning](../10-planning-control/motion-planning.md) | [open](pathname:///Robotics_bible/sim/path-planning.html) |
| Differential-drive odometry | wheel-size error makes the path drift | [Mobile navigation](../11-mobility-dexterity/mobile-navigation.md) | [open](pathname:///Robotics_bible/sim/diff-drive.html) |
| Pure pursuit | look-ahead distance | [Mobile navigation](../11-mobility-dexterity/mobile-navigation.md) | [open](pathname:///Robotics_bible/sim/pure-pursuit.html) |

## What these are, and are not

These are **teaching models**: simplified physics and algorithms written in plain JavaScript (`tools/sims/src/*.js`, built by `python3 tools/sims/build.py`). They show how a concept *behaves*. For real robot simulation (contact, sensors, GPU physics) use [Isaac Sim / Lab, MuJoCo or Gazebo](../13-simulation/simulation-landscape.md).

## Adding a new simulator

1. Create `tools/sims/src/my-sim.js` starting with `//TITLE:` and `//NOTE:` lines. Use the helpers in `static/sim/common.js` (`setup`, `slider`, `btn`, `drag`, `loop`).
2. Run `python3 tools/sims/build.py` to write `static/sim/my-sim.html`.
3. Embed it in a chapter with the same `<div class="simbox">…<iframe>` snippet used in the existing chapters.
