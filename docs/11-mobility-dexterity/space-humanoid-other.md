---
title: Space, Soft, Surgical & Other Robots
---

# Specialised Robot Domains

:::tip[The 30-second version]
Different environments change the rules. In **space** there's no gravity, no repair crew and a long communication delay; in **surgery** safety and precision beat everything; **soft robots** deform instead of staying rigid. For each domain, the interview question is usually "*what changes compared with a standard robot?*"
:::

## Space robotics

| Constraint | Consequence |
|---|---|
| **Microgravity** | moving the arm moves the whole satellite (momentum is conserved) |
| **Communication delay** (Moon ≈ 1.3 s one-way, Mars 4–24 min) | high onboard autonomy, goal-level commands, simulation before execution |
| **Radiation, vacuum, temperature extremes** | rad-hard computers, conservative software, fault protection |
| **No repair** | extreme reliability, formal verification, graceful degradation |

- **Free-flying / orbital manipulators:** control uses the **generalised Jacobian** (accounts for base reaction). Capturing a tumbling satellite needs visual servoing and soft-docking impedance. Examples: Canadarm2/Dextre, ETS-VII, OSAM-1, Astrobee.
- **Planetary rovers:** wheel–soil interaction (**terramechanics**, slip), visual odometry, autonomous navigation (Perseverance AutoNav), traversability from stereo, energy-aware planning, sampling arms; helicopters (Ingenuity); legged / tethered concepts.
- **Autonomy architecture:** onboard planners, fault protection, rad-hard CPUs (RAD750), FPGA acceleration, NASA cFS / F′ flight software.
- **Perception:** star trackers, relative navigation to satellites (SPEED+ dataset), terrain-relative navigation.
- **Humanoids and servicing:** Robonaut 2, Valkyrie; in-space servicing, assembly and manufacturing (ISAM).
- **Quantum angle:** cold-atom gyros and clocks for GNSS-denied navigation; quantum links between satellites.

## Soft robotics
Compliant bodies (silicone, hydrogel) driven by air pressure (PneuNets), tendons, shape-memory alloys or dielectric elastomers. Modelling: piecewise-constant curvature, Cosserat rods, FEM (SOFA), differentiable simulation. Good for safe grasping of delicate objects and medical use; hard to sense and control precisely.

## Surgical / medical
Teleoperation (da Vinci), remote centre of motion (RCM), tremor filtering, haptic feedback, image-to-patient registration, flexible continuum robots and catheters, autonomy levels 0–5, regulation (IEC 60601, FDA). Learning on surgical video and imitation is emerging (e.g. autonomous steps demonstrated on ex-vivo tissue).

## Agriculture, underwater, inspection, construction
Row-following + visual servoing for harvesting; AUV SLAM with sonar/DVL; legged inspection robots (ANYmal, Spot) for plants and tunnels; excavators with RL autonomy; drones for infrastructure inspection.

## Human–robot interaction and safety
Intent prediction, shared autonomy, **hand-overs**, speech/gesture interfaces, trust and explainability. Safety: **ISO/TS 15066** power-and-force limiting, speed-and-separation monitoring, social navigation, privacy and ethics of data collection.

## Multi-robot and swarms
Consensus, coverage, formation control, auction-based task allocation (CBBA), communication-limited planning, distributed SLAM (DOOR-SLAM, Swarm-SLAM), multi-agent RL.

## Interview Q&A

**Why is manipulation in space different?**
*Simply:* the base floats, so every arm motion pushes the satellite; contact can send the robot drifting away; there's no gravity to hold objects.

**How do you handle a 20-minute communication delay?**
*Simply:* give goals, not joystick commands; let the robot verify and recover on its own; rehearse in simulation first.

**Why does terramechanics matter for rovers?**
*Simply:* wheels sink and slip in soft soil; ignoring it can leave the rover stuck (Spirit).

**What changes for a surgical robot?**
*Simply:* safety and precision dominate: constrained motion about a fixed pivot, tremor filtering, strong verification and regulation.
