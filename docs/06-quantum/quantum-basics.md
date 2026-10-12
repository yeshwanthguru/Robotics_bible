---
title: Quantum Computing Basics
---

# Quantum Computing Fundamentals

:::tip[The 30-second version]
A normal bit is a light switch: **0 or 1**. A **qubit** is more like a dimmer plus a compass: it can sit in a *blend* of 0 and 1, and the blend has a direction (a "phase") that lets possibilities **interfere**, adding up or cancelling out, like waves.
A quantum algorithm is a clever choreography that makes the *wrong* answers cancel and the *right* answer reinforce, so that when you finally measure, you probably see the right one.
It does **not** try every answer at once and pick the best. That's the most common myth.
:::

## The qubit

![bloch sphere](/img/fig/bloch-sphere.svg)
*A qubit's state is a point on a sphere. The poles are 0 and 1; every other point is a blend.*

$$ |\psi\rangle=\alpha|0\rangle+\beta|1\rangle,\qquad |\alpha|^2+|\beta|^2=1 $$

> **In words:** the qubit holds two numbers (amplitudes). Their squares are the chances of seeing 0 or 1 when measured.

![superposition](/img/fig/superposition-bars.svg)
*Measurement gives a plain 0 or 1; the state decides the odds. Measuring also destroys the blend.*

- **n qubits** hold $2^n$ amplitudes at once, which is why classical simulation explodes (50 qubits ≈ petabytes).
- **Phase** matters: two paths to the same outcome can *cancel* (destructive interference). This is the engine of quantum speed-ups.
- **Density matrix** $\rho$ describes noisy / mixed states; **decoherence** (the environment leaking in) turns a clean blend into plain randomness.

## Gates: the instructions

A **gate** is a reversible rotation of the qubit's state (mathematically a *unitary* matrix, which keeps total probability at 1).

| Gate | What it does | Everyday picture |
|---|---|---|
| **X** | flips 0 ↔ 1 | NOT |
| **H** (Hadamard) | 0 → 50/50 blend | "make it undecided" |
| **Z / S / T** | change the phase only | rotate the compass |
| **Rx, Ry, Rz(θ)** | rotate by any angle | the knobs in variational circuits |
| **CNOT** | flip the target if the control is 1 | links two qubits (creates entanglement) |

![bell circuit](/img/fig/bell-circuit.svg)
*Hadamard then CNOT creates a Bell pair: two qubits whose results always agree, even though each alone is random.*

**Entanglement:** the joint state can't be described qubit by qubit. Measure one, and you instantly know the other's result (without sending a signal faster than light). **No-cloning theorem:** an unknown quantum state cannot be copied. **Universal gate set:** {H, T, CNOT}. **Clifford** circuits (without T) can be simulated classically; T gates supply the real power.

## Protocols worth knowing
- **Teleportation:** send a qubit's state using one entangled pair plus 2 classical bits.
- **Superdense coding:** 2 classical bits using 1 qubit and shared entanglement.
- **QKD (BB84):** any eavesdropper disturbs the qubits and is detected.

## Hardware

| Platform | Examples | Plus | Minus |
|---|---|---|---|
| **Superconducting** | IBM, Google | very fast gates | needs ~10 mK fridge, short coherence |
| **Trapped ions** | IonQ, Quantinuum | highest fidelity, all-to-all links | slow |
| **Neutral atoms** | QuEra, Pasqal | many qubits, flexible layout | slower gates |
| **Photonic** | PsiQuantum, Xanadu | room-temperature networking | probabilistic gates |
| **Spin (silicon)** | Intel | works with chip factories | early |
| **Annealers** | D-Wave | optimisation problems | not general-purpose |

**Noise:** T1 (energy loss), T2 (phase loss), gate errors, readout errors, crosstalk. **NISQ** = "noisy intermediate-scale quantum": ~50–1000 noisy qubits, no full error correction.

## Error correction
Spread one *logical* qubit across many physical qubits and check parities without looking at the data (**stabiliser codes**, **surface code**, qLDPC). If physical error < threshold (~1 %), adding qubits makes the logical qubit *better*. Cost: hundreds to thousands of physical qubits per logical one. For NISQ machines we use **error mitigation** instead: zero-noise extrapolation, readout correction, dynamical decoupling.

## Interview Q&A

**Why can't a quantum computer just try all answers in parallel?**
*Simply:* it holds all the amplitudes but a measurement returns only one outcome. Algorithms must use interference to make the right answer likely.

**Superposition vs ordinary uncertainty?**
*Simply:* ordinary probabilities can only add; amplitudes have phase and can cancel.

**Why are gates unitary?**
*Simply:* total probability must stay 1, which forces reversibility.

**What's decoherence?**
*Simply:* the environment "measures" the qubit by accident and the delicate blend turns into ordinary randomness.

**NISQ vs fault-tolerant?**
*Simply:* NISQ = short noisy circuits with tricks; fault-tolerant = error-corrected logical qubits that allow long computations, at huge qubit overhead.
