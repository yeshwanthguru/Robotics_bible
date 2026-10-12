# 🤖 Robotics & AI Bible

> One reference to read before every interview: **ML → DL → RL → LLM/VLM/VLA → Quantum → Physical AI → Robotics → Software → Simulation.**

**📖 Read it online: https://yeshwanthguru.github.io/Robotics_bible/**

Every chapter follows the same pattern: *intuition → equations/code you can write on a whiteboard → interview Q&A*.

## What's inside

| # | Section | Topics |
|---|---|---|
| 0 | **Start Here** | reading plans (1 hour / 1 day / 1 week), role-based paths, 5-step answer framework |
| 1 | **Math & CS** | linear algebra, probability, optimization, data structures, algorithms, real-time systems |
| 2 | **Machine Learning** | bias–variance, metrics, classical algorithms, EM, tuning |
| 3 | **Deep Learning** | training recipes, CNN/RNN/Transformer/GNN, diffusion, flow matching, self-supervised |
| 4 | **Reinforcement Learning** | MDPs, PPO/SAC/TD3, model-based, offline RL, RLHF/DPO/GRPO |
| 5 | **LLM · VLM · VLA** | pretraining, post-training, serving, RAG, agents; π0, OpenVLA, GR00T, world models |
| 6 | **Quantum Computing** | qubits/gates, Grover/Shor, VQE/QAOA, QML, Qiskit & PennyLane, quantum robotics |
| 7 | **Physical AI** | stack overview, imitation learning, teleoperation, robot learning |
| 8 | **Robotics Core** | kinematics, dynamics, contact, sensors & actuators |
| 9 | **Perception & Localization** | Kalman/particle filters, SLAM, ICP, visual geometry, 3D perception |
| 10 | **Planning & Control** | PID → LQR → MPC, impedance, motion planning, PDDL, behavior trees |
| 11 | **Mobility & Dexterity** | wheeled/aerial navigation, legged & humanoid locomotion, grasping, in-hand manipulation, space robots |
| 12 | **Languages & Frameworks** | ROS 1, **ROS 2**, C++, Python, MATLAB/Simulink, R, Docker/CI/Jetson |
| 13 | **Simulation** | **Isaac Sim, Isaac Lab, Isaac Gym**, MuJoCo/MJX, Gazebo, Genesis, ManiSkill, sim-to-real |
| 14 | **Interview Prep** | 80-question rapid-fire bank, system design, coding drills, behavioral story bank |
| 15 | **Cheat Sheets** | formulas, ROS 2 / Isaac / Docker commands, glossary |

## Run locally

```bash
npm ci
npm start          # http://localhost:3000/Robotics_bible/
npm run build      # static site in ./build
```

Requires Node 18+.

## Project layout

```
docs/                numbered folders = sidebar order (each has _category_.json)
src/pages/index.js   redirects the home page to /docs/
docusaurus.config.js site config (KaTeX math, Mermaid diagrams, local search)
.github/workflows/   GitHub Pages deployment
```

Writing conventions: math with `$…$` / `$$…$$` (KaTeX), diagrams with fenced ` ```mermaid ` blocks, `.md` files parsed as plain CommonMark (no MDX), so curly braces in prose are safe.

## Deployment

Pushes to `main` build and deploy via GitHub Actions. One-time setup: **Settings → Pages → Source: GitHub Actions**.

## Contributing to your future self

Add a `## My experience` section at the bottom of any page with your own projects and numbers. Fill in the behavioral story bank. Interviewers remember stories, not definitions.

> Content is written for interview preparation. Verify version-specific details (Isaac Sim/Lab APIs, ROS 2 distros, model releases) against official docs before relying on them.
