# Robotics & AI Bible

Interview reference site (Docusaurus) covering ML, DL, RL, LLM/VLM/VLA, quantum computing, Physical AI, robotics (kinematics, dynamics, control, planning, localization/SLAM, mobility, dexterity), ROS/ROS 2, Python, C++, MATLAB, R, PDDL, and simulation (Isaac Sim, Isaac Lab, Isaac Gym, MuJoCo, Gazebo).

```bash
npm ci
npm start        # dev server at http://localhost:3000/Robotics_bible/
npm run build    # static site in build/
```

Deployed to GitHub Pages by `.github/workflows/deploy.yml` (Settings → Pages → Source: GitHub Actions).
Content lives in `docs/` (numbered folders = sidebar order). Math: KaTeX (`$...$`), diagrams: Mermaid.
