---
title: Space, Soft, Surgical & Other Robots
---

# Specialised Robot Domains

## Space robotics
- **Environments:** microgravity, vacuum, thermal extremes, radiation, comms delay (Moon ≈ 1.3 s one-way; Mars 4–24 min) → high autonomy, supervised autonomy, shared control.
- **Free-flying / orbital manipulators:** base is not fixed; momentum conservation → **Generalized Jacobian** $J^*=J_m-J_bH_b^{-1}H_{bm}$, base disturbance, reaction-null-space, capture of tumbling targets (detumbling, visual servoing, impedance for soft-docking). Examples: Canadarm2/Dextre, ETS-VII, Orbital Express, OSAM-1, ClearSpace, Astrobee (ISS free-flyer).
- **Planetary rovers:** wheel–soil interaction (terramechanics, Bekker/Wong), slip estimation, visual odometry (MER, Perseverance's AutoNav), traversability from stereo, energy-aware planning, sample caching arms, helicopter (Ingenuity), legged/ tethered (DuAxel, LEMUR), lava tubes (Cave-R).
- **Autonomy architecture:** sense-plan-act, onboard planners (CASPER), fault protection, radiation-hardened compute (RAD750), FPGA acceleration, formal verification (NASA cFS, F′ flight framework).
- **Humanoids in space:** Robonaut 2, Valkyrie (NASA), Fedor.
- **In-space servicing & assembly (ISAM):** truss assembly, refueling, cable routing.
- **Perception:** star trackers, relative navigation (LiDAR, monocular pose estimation of known satellites – SPEED+ dataset), terrain relative navigation (Mars 2020 LVS).
- **Quantum link:** quantum sensors (cold-atom gyroscopes, clocks) for GNSS-denied navigation; quantum comms (Micius satellite).

## Soft robotics
Compliant materials (silicone, hydrogel), pneumatic (PneuNets), tendon, SMA, dielectric elastomers. Modelling: Piecewise Constant Curvature, Cosserat rod, FEM (SOFA), differentiable sim. Control: model-based reduced-order + learning. Applications: grasping, medical, bio-inspired.

## Surgical / medical
Teleoperation (da Vinci), RCM (remote center of motion), haptic feedback, tremor filtering, registration (CT↔patient), flexible continuum/ catheters, autonomy levels (0–5), regulatory (IEC 60601, FDA). Learning: surgical video foundation models, imitation (SRT-H autonomous gallbladder surgery in ex-vivo).

## Agricultural, underwater, inspection, construction
Row following + visual servoing for harvesting; AUV SLAM with sonar/DVL; pipe/ tank crawlers; legged inspection (ANYmal, Spot); excavators (RL autonomy); drone-based inspection; legged + arm door opening.

## Human–robot interaction (HRI) & safety
Intent prediction, shared autonomy, handover (grasp-release timing), speech/gesture interfaces, trust, explainability, ISO/TS 15066 power & force limiting, speed-and-separation monitoring, social navigation, privacy & ethics (data collection, bias), failure transparency.

## Multi-robot / swarm
Consensus, coverage, formation control, task allocation (auction/ CBBA), communication-constrained planning, distributed SLAM (DOOR-SLAM, Swarm-SLAM), MARL.

## Interview Q&A

**Why is manipulation in space different?** Floating base couples arm motion to base attitude/position; contact can push the robot away; no gravity for stabilizing objects.

**How to handle 20-minute comms delay?** Command at goal level, onboard autonomy with verification, simulation-based pre-validation, "science autonomy" for opportunistic decisions.

**Terramechanics why?** Wheel sinkage & slip depend on soil; ignoring leads to stuck rovers (Spirit).
