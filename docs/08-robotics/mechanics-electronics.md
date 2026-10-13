---
title: Mechanics & Electronics for Robots
---

# Mechanics and Electronics for Robots

:::tip[The 30-second version]
Every robot is a **machine** (frame, joints, gears, motors) powered by **electronics** (batteries, power converters, motor drivers, microcontrollers, sensors, buses). AI engineers often skip this layer, but hardware limits decide what the software can do: torque, speed, heat, battery life, noise and failure modes. This page gives you the vocabulary and the sizing rules.
:::

## 1. Mechanical building blocks

| Part | What it does | Notes |
|---|---|---|
| **Links / frames** | rigid structure | aluminium, carbon fibre, steel, 3-D printed plastics (PLA, PETG, ABS, nylon); stiffness-to-weight matters |
| **Joints** | allow relative motion | revolute, prismatic, spherical; need bearings |
| **Bearings** | support rotation with low friction | ball, roller, crossed-roller (high stiffness) |
| **Gearboxes** | trade speed for torque | planetary, harmonic (zero backlash), cycloidal (robust), spur/worm |
| **Belts and cables** | transmit motion remotely | tendon drives for hands; backlash-free, stretch and friction issues |
| **Springs / dampers** | store energy, absorb shocks | series elastic actuators |
| **Fasteners and adhesives** | hold it together | thread-locker, tolerances, stress concentrations |
| **Linear motion** | rails, ball screws, belts | gantries and prismatic axes |

**Design concepts:** degrees of freedom, workspace, payload and reach, **stiffness** (deflection under load limits accuracy), **backlash** (play in gears), **repeatability versus accuracy**, mass distribution (keep heavy parts near the base), thermal expansion, vibration and resonance.

## 2. Actuators and sizing

### Electric motors
| Type | Traits |
|---|---|
| **Brushed DC** | simple, cheap, brushes wear |
| **BLDC / PMSM** | efficient, long-lived, needs electronic commutation (FOC); the robotics standard |
| **Stepper** | open-loop positioning, can lose steps; printers, light-duty axes |
| **Servo (integrated)** | motor + driver + encoder in a package; hobby to industrial |

**Key relationships**
- Torque ≈ $K_t \cdot I$ (motor torque constant times current).
- Back-EMF ≈ $K_e \cdot \omega$; voltage limits top speed.
- Heat ≈ $I^2R$: continuous torque is set by cooling, peak torque by current limits.
- With a gearbox of ratio $N$: output torque ≈ $N\tau_m\eta$ (η = efficiency), output speed = $\omega_m/N$, **reflected inertia = $N^2J_m$**.

### Quick sizing recipe (a robot joint)
1. List the worst-case **load torque** (payload × reach + link weights) and **speed**.
2. Add **acceleration torque** $J\alpha$ and a safety factor (1.5–2×).
3. Choose gear ratio so required output torque/speed fit the motor's torque–speed curve.
4. Check **continuous** (thermal) and **peak** torque, voltage, and gearbox rating.
5. Check **backdrivability, backlash, stiffness, noise, cost**.

### Other actuation
Hydraulic (highest power density, leaks, noise), pneumatic (compliant, hard to control), shape-memory alloys and artificial muscles (small, slow), voice-coil/linear motors (fast precise strokes).

## 3. Power electronics and batteries

| Item | Notes |
|---|---|
| **Battery chemistry** | Li-ion (high energy density), LiPo (high current, hobby/drones), LiFePO₄ (safer, long life), lead-acid (heavy) |
| **Capacity and C-rate** | Wh = V × Ah; C-rate is current relative to capacity |
| **BMS** | protects cells (over/under-voltage, over-current, temperature), balances cells |
| **DC–DC converters** | buck (step down), boost (step up), isolated converters for sensitive electronics |
| **Motor drivers** | H-bridge / three-phase inverter + FOC control; current sensing |
| **Regeneration** | motors act as generators when braking; manage bus voltage with braking resistors or capacitors |
| **Protection** | fuses, reverse-polarity protection, precharge, E-stop contactors, STO |

**Energy budgeting:** battery energy ÷ average power = runtime. Peak power (jumping, lifting) sets current and voltage sag; add margin.

## 4. Embedded electronics

- **Microcontrollers (MCUs):** STM32, ESP32, Teensy, RP2040: real-time loops for motor control and sensor reading.
- **Compute:** edge GPUs (Jetson), x86 PCs with a real-time kernel for control and planning.
- **Sensors interfaces:** I²C, SPI, UART, analog (ADC), PWM/encoders, camera interfaces (MIPI, USB, GigE).
- **Buses:** CAN/CAN-FD (robust, daisy-chain), EtherCAT (deterministic, fast), RS-485, Ethernet/TSN.
- **PCB basics:** ground planes, decoupling capacitors, separating power and signal grounds, shielded twisted pairs, ESD protection.
- **EMI:** motor drivers are noisy; use ferrites, shielding, twisted pairs and careful grounding.

## 5. Practical build and test tips
1. Prototype with 3-D printed parts, then machine critical parts.
2. Run **bench tests**: torque vs current, backlash, thermal rise, friction.
3. Add **current and temperature limits** in firmware.
4. Document wiring and connectors; use strain relief; label everything.
5. Test failure modes: power loss (do joints fall?), comms loss (watchdog), over-temperature.

## Interview Q&A

**Why does a high gear ratio hurt force control?**
*Simply:* friction and reflected inertia (N²) make the joint hard to back-drive. *Deeper:* the robot can't feel or comply with contact.

**How do you size a motor and gearbox for a joint?**
*Simply:* compute required torque and speed, add safety factor, match to the motor's torque–speed curve. *Deeper:* check continuous versus peak torque and thermal limits.

**Harmonic drive versus planetary versus cycloidal?**
*Simply:* harmonic is compact and zero-backlash, planetary is robust and efficient, cycloidal tolerates shocks. *Deeper:* choose by backlash, stiffness, efficiency, backdrivability and cost.

**What does FOC do?**
*Simply:* it controls motor torque precisely by regulating current components. *Deeper:* needs rotor position (encoder) and fast current loops (10–40 kHz).

**Why use EtherCAT?**
*Simply:* deterministic, synchronised communication for many axes. *Deeper:* distributed clocks give microsecond-level synchronisation.

**What happens to a robot arm when power is cut?**
*Simply:* it may fall unless brakes engage. *Deeper:* use power-off brakes and safe torque off; design for fail-safe states.
