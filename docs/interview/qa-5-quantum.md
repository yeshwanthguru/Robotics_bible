---
title: "Q&A 5: Quantum Computing"
---

# Interview Q&A: Quantum Computing

:::tip[How to use]
Chapters: [Basics](../06-quantum/quantum-basics.md) · [Algorithms](../06-quantum/quantum-algorithms.md) · [Software](../06-quantum/quantum-software.md).
:::

## Basics

### Q: What is a qubit?
**Short answer:** A two-level quantum system in a blend of 0 and 1. **Go deeper:** State α|0⟩ + β|1⟩ with |α|² + |β|² = 1; measuring gives 0 or 1 with those probabilities.

### Q: Superposition versus classical probability?
**Short answer:** Amplitudes have phase and can cancel; probabilities only add. **Go deeper:** Interference is the resource algorithms exploit.

### Q: What is entanglement?
**Short answer:** Qubits whose joint state cannot be described separately. **Go deeper:** Bell pairs; correlations violate Bell/CHSH inequalities, ruling out local hidden variables, but cannot send signals.

### Q: Why are quantum gates unitary?
**Short answer:** They must preserve total probability, which forces reversibility. **Go deeper:** UU† = I; measurement is the only non-unitary step.

### Q: What does the Hadamard gate do?
**Short answer:** Turns |0⟩ into an equal blend of 0 and 1. **Go deeper:** Maps Z-basis to X-basis; creating uniform superpositions is its main job.

### Q: What does CNOT do?
**Short answer:** Flips the target if the control is 1. **Go deeper:** With H it creates Bell states; CNOT plus single-qubit gates is universal.

### Q: What is the no-cloning theorem?
**Short answer:** An unknown quantum state cannot be copied. **Go deeper:** It protects quantum key distribution and complicates error correction.

### Q: What is measurement doing to the state?
**Short answer:** It returns a classical result and collapses the state. **Go deeper:** Born rule: probability = |amplitude|².

### Q: What is decoherence?
**Short answer:** The environment disturbs the qubit and destroys the delicate blend. **Go deeper:** Characterised by T1 (energy relaxation) and T2 (dephasing).

### Q: NISQ versus fault-tolerant?
**Short answer:** NISQ: short noisy circuits with mitigation. Fault-tolerant: error-corrected logical qubits for long computations. **Go deeper:** Fault tolerance needs hundreds to thousands of physical qubits per logical one.

### Q: How does error correction work?
**Short answer:** Spread one logical qubit across many physical ones and measure parities without learning the data. **Go deeper:** Surface code threshold about 1 %; below threshold more qubits give lower logical error.

### Q: What are the main hardware platforms?
**Short answer:** Superconducting, trapped ion, neutral atom, photonic, silicon spin, and annealers. **Go deeper:** Trade-offs: speed versus fidelity versus connectivity versus scalability.

### Q: Can a quantum computer try all answers at once?
**Short answer:** No. **Go deeper:** It holds all amplitudes but measurement returns one; algorithms use interference to make the right answer likely.

## Algorithms

### Q: Explain Grover's algorithm.
**Short answer:** Search N items in about √N steps by repeatedly flipping the target's sign and reflecting about the average. **Go deeper:** Rotates the state toward the solution by 2θ per iteration; optimal ≈ (π/4)√(N/M) iterations; too many overshoot.

### Q: Why is Grover optimal?
**Short answer:** No quantum algorithm can search an unstructured list faster. **Go deeper:** The BBBV theorem proves Ω(√N) queries.

### Q: Explain Shor's algorithm in one minute.
**Short answer:** Factoring reduces to finding the period of aˣ mod N; a quantum Fourier transform finds that period efficiently. **Go deeper:** Then gcd(a^{r/2} ± 1, N) gives factors; threatens RSA, motivating post-quantum cryptography.

### Q: What is quantum phase estimation?
**Short answer:** Estimating the eigenvalue (phase) of a unitary. **Go deeper:** It uses controlled powers of the unitary plus an inverse QFT and underlies Shor, HHL and chemistry.

### Q: What is the quantum Fourier transform?
**Short answer:** The quantum version of the discrete Fourier transform using O(n²) gates. **Go deeper:** Exponentially fewer gates than classical FFT on n qubits, but outputs amplitudes, not readable values.

### Q: What is BQP?
**Short answer:** Problems a quantum computer solves in polynomial time with bounded error. **Go deeper:** Contains P, is inside PSPACE, and is believed not to contain NP-complete problems.

### Q: What is HHL and what are its caveats?
**Short answer:** A quantum algorithm for linear systems with potential exponential speed-up. **Go deeper:** Needs sparse well-conditioned matrices, fast state preparation and only returns observables, not the full solution.

### Q: What is the best-known real application of quantum computers?
**Short answer:** Simulating quantum systems (chemistry, materials). **Go deeper:** Hamiltonian simulation; optimisation and ML speed-ups remain unproven.

### Q: What is VQE?
**Short answer:** A hybrid algorithm that tunes circuit parameters to minimise a molecule's energy. **Go deeper:** Uses the variational principle E(θ) ≥ E₀; limited by ansatz, noise and optimiser.

### Q: What is QAOA?
**Short answer:** A hybrid algorithm for combinatorial optimisation that alternates problem and mixer layers. **Go deeper:** Depth p improves approximation; Max-Cut maps to an Ising Hamiltonian.

### Q: What is a barren plateau?
**Short answer:** The cost landscape becomes flat so gradients vanish. **Go deeper:** Variance shrinks exponentially with qubits for random deep circuits; use local costs, shallow structured ansätze and good initialisation.

### Q: Why the parameter-shift rule?
**Short answer:** It gives exact gradients from circuit evaluations. **Go deeper:** ∂f = ½[f(θ+π/2) − f(θ−π/2)] works on hardware where finite differences are noisy.

### Q: What is a QUBO and how does it relate to Ising?
**Short answer:** Binary optimisation of xᵀQx; equivalent to an Ising model by x = (1−z)/2. **Go deeper:** Annealers and QAOA take this form.

### Q: What is quantum advantage versus supremacy?
**Short answer:** Advantage: useful speed-up; supremacy: beating classical on any task. **Go deeper:** Random-circuit sampling demonstrations lack practical use; claims need strong classical baselines.

### Q: What is dequantisation?
**Short answer:** Showing a claimed quantum speed-up can be matched classically. **Go deeper:** Tang's result for recommendation systems removed an apparent exponential advantage.

### Q: How do quantum kernels work?
**Short answer:** Map data to quantum states and use their overlap as a similarity in an SVM. **Go deeper:** Advantage requires structured data that classical kernels can't compute efficiently.

## Practical and robotics-related

### Q: Which frameworks have you used?
**Short answer:** Qiskit (IBM), PennyLane (differentiable QML), Cirq (Google), CUDA-Q (GPU). **Go deeper:** Mention transpilation, primitives (Sampler/Estimator) and simulators.

### Q: What is transpilation?
**Short answer:** Rewriting a circuit into the device's native gates and layout. **Go deeper:** Includes SWAP routing for limited connectivity and optimisation.

### Q: Why can classical machines simulate only about 50 qubits exactly?
**Short answer:** State size doubles with each qubit. **Go deeper:** 50 qubits need petabytes; tensor networks extend this for low-entanglement circuits.

### Q: Where could quantum help robotics?
**Short answer:** Sensing (cold-atom gyroscopes, magnetometers) and secure communication first; optimisation and planning speed-ups are speculative. **Go deeper:** Task allocation as QUBO on annealers, quantum RL, QML for sensor data are research directions.

### Q: How would you integrate a quantum solver in a robot stack?
**Short answer:** As an asynchronous service with a classical fallback. **Go deeper:** Behind a ROS 2 action server; never in a hard real-time loop.

### Q: What is post-quantum cryptography?
**Short answer:** Classical encryption designed to resist quantum attacks. **Go deeper:** Lattice-based schemes (Kyber, Dilithium) standardised by NIST.

### Q: What is quantum key distribution?
**Short answer:** Sharing keys whose security comes from quantum mechanics: eavesdropping disturbs the qubits. **Go deeper:** BB84, E91; limited by distance and rate.

### Q: Explain error mitigation.
**Short answer:** Post-processing tricks that reduce noise without full error correction. **Go deeper:** Zero-noise extrapolation, probabilistic error cancellation, readout correction, dynamical decoupling.
