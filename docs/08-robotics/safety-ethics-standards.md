---
title: Safety, Ethics & Standards
---

# Safety, Ethics and Standards

:::tip[The 30-second version]
A robot that works in a demo can still be unsafe in the real world. **Safety engineering** is the discipline of *designing so that failures don't hurt people*: independent safety systems, limits enforced outside the AI, and following standards. **Ethics** covers privacy, bias, accountability and the social effects of deploying AI and robots. Interviewers increasingly ask about both.
:::

## 1. Core safety principles

1. **Hazard analysis first.** List what can go wrong (HAZOP, FMEA, fault-tree analysis), how severe, how likely, and how to detect and mitigate it.
2. **Safety is a layer outside the AI.** Neural networks can be wrong in unpredictable ways; enforce limits (speed, force, workspace, joint limits) in simple, verified code and hardware.
3. **Redundancy and diversity.** Duplicate critical sensors/processors; use different implementations to avoid common-cause failures.
4. **Fail-safe defaults.** On any fault, power loss or lost communication, move to a safe state (brakes on, torque off, stop).
5. **Defence in depth.** E-stop, safety-rated sensors, software limits, physical guarding and procedures work together.
6. **Test the failure modes**, not just success: sensor dropouts, delays, adversarial inputs, human mistakes.

### Typical safety functions
| Function | Meaning |
|---|---|
| **Emergency stop (E-stop)** | immediate stop by a human-operated control |
| **Safe torque off (STO)** | removes motor torque via hardware |
| **Safe limited speed / position** | monitored speed and workspace limits |
| **Speed and separation monitoring** | slow/stop as a person approaches (safety LiDAR zones) |
| **Power and force limiting** | limit contact force/pressure to safe levels |
| **Hand guiding** | operator moves robot by hand at reduced speed |
| **Watchdogs and heartbeats** | detect a frozen controller or lost link |
| **Geofencing** | confine drones/vehicles to allowed areas |

## 2. Standards map

| Standard | Scope |
|---|---|
| **ISO 10218-1/-2** | industrial robots and robot systems (2025 editions replaced the 2011 versions and integrated collaborative-operation requirements formerly in ISO/TS 15066) |
| **ISO/TS 15066** | collaborative robots: body-region force/pressure limits (the 2025 revision of ISO 10218 has absorbed this content, so check whether your project follows the older TS or the new edition) |
| **ISO 13482** | personal care robots (mobile servants, physical assistants) |
| **ISO 13849** | safety-related parts of machine control systems (performance levels) |
| **IEC 61508** | functional safety of electrical/electronic systems (SIL) |
| **ISO 26262** | automotive functional safety (ASIL levels) |
| **ISO 21448 (SOTIF)** | hazards from performance limits of intended functions (perception!) |
| **UL 4600** | safety case for autonomous products |
| **IEC 60601** | medical electrical equipment (surgical robots) |
| **DO-178C / DO-254** | airborne software / hardware |
| **ISO 3691-4** | driverless industrial trucks |
| **ISO/IEC 42001, EU AI Act, NIST AI RMF** | AI management and regulation frameworks |

*Standards evolve; check the current editions and regional rules (EU, US, China, etc.) before design decisions.*

## 3. Safety of learned systems

- **Runtime monitors:** check that outputs are within limits and inputs are in distribution (confidence, OOD detectors).
- **Safety filters:** a control barrier function (CBF) or MPC layer adjusts the AI's command minimally to stay safe.
- **Shadow mode and staged rollout:** evaluate the policy without acting, then expand gradually.
- **Scenario-based testing:** simulation and fuzzing of rare events; replay of logged failures.
- **Formal methods:** verify critical logic, reachability analysis for simple components.
- **Safety case:** a structured argument with evidence that the system is acceptably safe.
- **Logging and black-box recording:** make incidents analysable.

## 4. Ethics and responsible AI

| Topic | Questions to ask |
|---|---|
| **Privacy** | what is recorded (cameras, microphones), where is it stored, who can see it, consent? |
| **Bias and fairness** | does performance differ across people, environments, accents, skin tones? |
| **Transparency and explainability** | can users understand what the robot is doing and why? |
| **Accountability** | who is responsible when something goes wrong? |
| **Human oversight** | can a person intervene, and is the interface effective? |
| **Security** | can the robot or its fleet be hacked? (SROS2, secure boot, updates, network segmentation) |
| **Labour and societal impact** | job displacement, accessibility, equitable benefits |
| **Dual use and misuse** | could the technology be repurposed for harm? |
| **Data governance** | licences, provenance, consent for datasets; model and data cards |
| **Environmental impact** | training energy, hardware lifecycle |

**LLM-specific risks:** hallucination, prompt injection, jailbreaks, data leakage, over-reliance. Mitigations: grounding, validation, least-privilege tool access, human confirmation for consequential actions, red-teaming.

## 5. Security basics for robots
- **Network:** segment robot networks, firewalls, VPN, disable unused ports.
- **ROS 2:** SROS2 (DDS-Security): authentication, encryption, access control.
- **Software supply chain:** pin and verify dependencies, signed updates, SBOMs.
- **Access control:** unique credentials, least privilege, audit logs.
- **Physical:** tamper protection, locked debug ports.

## Interview Q&A

**Why keep safety functions outside the neural network?**
*Simply:* networks can fail in unexpected ways, so hard limits must be simple and verifiable. *Deeper:* independent hardware/software layers (STO, safety PLC) provide guarantees the learned policy cannot.

**What is SOTIF?**
*Simply:* safety of the intended function: hazards that come from limitations of correctly working systems, like perception errors. *Deeper:* ISO 21448 complements ISO 26262.

**How do collaborative robots stay safe near people?**
*Simply:* they limit speed, force and pressure and can stop when a person approaches. *Deeper:* ISO/TS 15066 (now folded into the 2025 edition of ISO 10218-2) gives body-region limits; risk assessment of the whole application is required.

**How would you deploy a learned policy safely?**
*Simply:* shadow mode, a safety filter, limits outside the model, staged rollout. *Deeper:* monitor OOD inputs, log everything, keep a fallback behaviour.

**Name two ethical issues in home robots.**
*Simply:* privacy of camera and microphone data, and over-trust in capabilities. *Deeper:* data minimisation, on-device processing, transparent behaviour and clear limits.
