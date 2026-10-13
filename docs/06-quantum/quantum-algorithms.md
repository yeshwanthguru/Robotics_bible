---
title: Quantum Algorithms & Variational Methods
---

# Quantum Algorithms

:::tip[The 30-second version]
Only a few problems are known to run much faster on a quantum computer. The famous ones:
**Shor** (factor huge numbers → breaks today's RSA encryption), **Grover** (search in √N steps instead of N), and **simulating quantum physics** (chemistry, materials, probably the first real "killer app").
Today's noisy chips mostly run **hybrid** algorithms (VQE, QAOA) where a small quantum circuit is tuned by a normal computer.
:::

## What is actually faster?

| Algorithm | Problem | Speed-up | Reality check |
|---|---|---|---|
| **Shor** | factoring, discrete log | super-polynomial | needs ~1M noisy qubits; motivates post-quantum cryptography |
| **Grover** | unstructured search | quadratic ($\sqrt N$) | proven optimal; modest but broad |
| **Hamiltonian simulation** | simulate molecules / materials | exponential | most promising real application |
| **HHL** | linear equations | exponential *with big caveats* | data loading and readout kill much of it |
| **QPE** | find eigenvalues | foundation | inside Shor and chemistry |
| **VQE / QAOA** | chemistry / optimisation | heuristic | NISQ-friendly, no proven advantage yet |
| **Boson sampling / RCS** | random sampling | exponential | proves hardware power, no practical use |

**Complexity:** BQP = problems quantum computers solve efficiently. It contains P and is believed *not* to contain NP-complete problems, so quantum is **not** a magic NP-solver.

## Grover: amplify the right answer

![grover](/img/fig/grover-amplitude.svg)
*Start with every answer equally likely. The oracle secretly flips the sign of the right one. Reflecting about the average then makes that one tall. Repeat about $\tfrac{\pi}{4}\sqrt N$ times.*

**In words:** each round is a tiny rotation toward the right answer. Rotate too many times and you overshoot, so the number of rounds matters.

## Shor: factoring by finding a rhythm
Pick a number *a*; the sequence $a^x \bmod N$ repeats with some period *r*. A quantum Fourier transform finds that period fast; then a bit of arithmetic ($\gcd(a^{r/2}\pm1,N)$) gives the factors. *(Gidney, 2025, a resource estimate not a demonstration: under a million noisy qubits and under a week of run time for RSA-2048.)*

## Variational algorithms: the hybrid loop

![VQE loop](/img/fig/vqe-loop.svg)
*The quantum chip evaluates a cost for a set of angles θ; a classical optimiser proposes better angles. Repeat.*

- **VQE** finds the lowest energy of a molecule. By the *variational principle*, any trial state's energy is ≥ the true ground state, so lowering it can only help.
 $E(\theta)=\langle\psi(\theta)|H|\psi(\theta)\rangle \ge E_0$
- **QAOA** solves combinatorial problems (e.g. Max-Cut): alternate a "problem" step and a "mixing" step with tunable angles.
- **Gradients on hardware:** the *parameter-shift rule* $\partial_\theta f=\tfrac12[f(\theta+\tfrac\pi2)-f(\theta-\tfrac\pi2)]$ is exact, unlike finite differences.
- **Pain points:** **barren plateaus** (the landscape goes flat as qubits grow, so gradients vanish), noise, shot noise (finite measurements), many Pauli terms to measure, local minima.
- **QUBO / Ising:** many optimisation problems can be rewritten as "minimise $x^\top Q x$ over bits", the format annealers and QAOA take.

## Quantum machine learning (QML)
- **Quantum kernels:** map data into quantum states and use their overlap as a similarity for a normal SVM.
- **Variational classifiers / QNNs, QCNNs, quantum GANs, reservoir computing.**
- **Honest assessment (say this in interviews):** no proven practical advantage for *classical* data yet. Loading data is expensive, readout is limited, and several "quantum speed-ups" were later matched by classical algorithms ("dequantisation"). More promising for *quantum* data (chemistry, physics sensors).

## Quantum + robotics (connect this to your research)

| Area | Idea | Maturity |
|---|---|---|
| **Optimisation** | route planning, task allocation, multi-robot scheduling as QUBO | experimental on annealers/QAOA |
| **Quantum RL** | variational circuits as small policies/value functions | research |
| **Sensing** | cold-atom gyroscopes/accelerometers, quantum magnetometers → GPS-denied navigation | real hardware, early |
| **Communication / security** | QKD for fleet links, post-quantum crypto | deployed in places |
| **Control** | RL and optimal control for calibrating quantum devices | active |
| **Space** | quantum clocks and links on satellites | pilots |

**Practical architecture:** put the quantum solver behind an *asynchronous service* (like a ROS 2 action server) with a classical fallback. Never put it inside a hard real-time loop.

## Interview Q&A

**Why is Grover optimal?**
*Simply:* nobody can search an unstructured list faster than ~√N queries, even with a quantum computer (BBBV theorem).

**What is a barren plateau?**
*Simply:* the cost surface becomes so flat that the optimiser can't tell which way is downhill. Avoid with shallow, structured circuits and local costs.

**Why parameter-shift instead of finite differences?**
*Simply:* it is exact and works with noisy measurements at a safe step size.

**Is VQE guaranteed to find the ground state?**
*Simply:* no. It gives an upper bound, limited by the ansatz, optimiser and noise.

**Where could quantum realistically help robotics first?**
*Simply:* quantum **sensing** and secure communication first; optimisation speed-ups are still unproven.
