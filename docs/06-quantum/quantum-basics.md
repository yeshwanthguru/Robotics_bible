---
title: Quantum Computing Basics
---

# Quantum Computing Fundamentals

## Qubit & state
$|\psi\rangle=\alpha|0\rangle+\beta|1\rangle$, $|\alpha|^2+|\beta|^2=1$. Bloch sphere: $|\psi\rangle=\cos\tfrac\theta2|0\rangle+e^{i\phi}\sin\tfrac\theta2|1\rangle$. $n$ qubits → $2^n$ complex amplitudes (tensor product space). Global phase is unobservable; relative phase matters (interference).

**Measurement (Born rule):** $P(i)=|\langle i|\psi\rangle|^2$; state collapses. Expectation $\langle O\rangle=\langle\psi|O|\psi\rangle$.

**Density matrix** $\rho=\sum p_i|\psi_i\rangle\langle\psi_i|$ for mixed states; pure iff $\mathrm{Tr}\rho^2=1$. Partial trace gives reduced states; decoherence = loss of off-diagonals.

## Gates

| Gate | Matrix / action |
|---|---|
| X (NOT) | $\begin{pmatrix}0&1\\1&0\end{pmatrix}$ bit flip |
| Z | $\mathrm{diag}(1,-1)$ phase flip |
| Y | $iXZ$ |
| H | $\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$: $|0\rangle\to|+\rangle$ |
| S, T | $\mathrm{diag}(1,i)$, $\mathrm{diag}(1,e^{i\pi/4})$ |
| $R_x,R_y,R_z(\theta)$ | $e^{-i\theta\sigma/2}$ rotations |
| CNOT | flips target if control=1; creates entanglement |
| CZ, SWAP, Toffoli (CCNOT), Fredkin | multi-qubit |

Universal set: {H, T, CNOT} (Clifford+T). **Clifford** circuits are classically simulable (Gottesman–Knill); T gates supply the “magic”. All gates are **unitary** ($U^\dagger U=I$) → reversible. **No-cloning theorem**: unknown states cannot be copied.

**Bell state:** $H\otimes I$ then CNOT on $|00\rangle$ → $\frac{|00\rangle+|11\rangle}{\sqrt2}$. Entanglement: not a product state; Schmidt rank>1; entropy of reduced state measures it. Bell/CHSH inequality violation (up to $2\sqrt2$) rules out local hidden variables.

## Core protocols
- **Superdense coding**: 2 classical bits via 1 qubit + shared entanglement.
- **Teleportation**: 1 qubit state ↔ 2 classical bits + Bell pair.
- **QKD (BB84, E91)**: eavesdropping disturbs states.

## Hardware platforms

| Platform | Examples | Strengths | Weakness |
|---|---|---|---|
| Superconducting transmon | IBM, Google, Rigetti | fast gates (~10-100 ns) | cryogenic (10 mK), connectivity, coherence ~100 µs |
| Trapped ion | IonQ, Quantinuum | high fidelity, all-to-all | slow gates |
| Neutral atom | QuEra, Pasqal, Atom Computing | scalable arrays, analog mode | gate speed |
| Photonic | PsiQuantum, Xanadu | room temp networking | probabilistic gates |
| Spin / silicon | Intel, Diraq | CMOS compat | early |
| Topological | Microsoft | intrinsic protection | contested/experimental |
| Annealer | D-Wave | optimization (QUBO) | not universal |

**Noise:** T1 (relaxation), T2 (dephasing), gate/readout error, crosstalk. **NISQ** = Noisy Intermediate-Scale Quantum (50–1000 qubits, no full error correction).

## Error correction
Logical qubit from many physical qubits. Bit-flip repetition code; Shor 9-qubit; **stabilizer codes**, **surface code** (threshold ≈1 %, 2-D nearest-neighbour; Google "below threshold" demonstration), qLDPC codes (lower overhead). Fault-tolerant: threshold theorem, magic state distillation, lattice surgery. Mitigation (NISQ): zero-noise extrapolation, probabilistic error cancellation, readout correction, dynamical decoupling, Pauli twirling.

## Interview Q&A

**Why can’t a quantum computer try all answers in parallel?** Superposition holds all amplitudes but measurement yields one; algorithms must use interference to boost the right answer’s amplitude.

**Superposition vs classical probability?** Amplitudes are complex and can cancel (negative/phase), probabilities can’t.

**What is decoherence?** Interaction with the environment turns pure states into mixed states, destroying interference.

**Why are gates unitary?** Norm preservation → probabilities sum to 1; implies reversibility.

**Difference between NISQ and fault-tolerant?** NISQ: shallow noisy circuits, mitigation. FT: logical qubits with error correction → arbitrarily deep circuits at big overhead (~1000 physical per logical).
