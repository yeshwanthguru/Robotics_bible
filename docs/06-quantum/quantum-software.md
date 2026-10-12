---
title: Quantum Software Stack & Code
---

# Quantum Software Stack

:::tip[The 30-second version]
You program a quantum computer by writing a **circuit**: a list of gates on qubits, then "measure". The software stack takes your circuit, translates it to the chip's native gates, fits it onto the chip's wiring, and runs it many times ("shots") to estimate probabilities. **Qiskit** (IBM) and **PennyLane** (Xanadu) are the two names to know.
:::

## What each framework is for

| Framework | Owner | Pick it for |
|---|---|---|
| **Qiskit** | IBM | circuits, transpiler, real IBM hardware, Runtime primitives |
| **PennyLane** | Xanadu | differentiable quantum ML; plugs into PyTorch/JAX |
| **Cirq** | Google | noise-aware NISQ circuits |
| **CUDA-Q** | NVIDIA | GPU-accelerated simulation, hybrid quantum–classical |
| **Q#** / Azure Quantum | Microsoft | fault-tolerant resource estimation |
| **Amazon Braket** | AWS | many hardware vendors in one SDK |
| **Ocean** | D-Wave | annealing / QUBO |
| **OpenQASM 3 / tket** | community / Quantinuum | circuit IR and compilation |

**Compilation pipeline:** logical circuit → decompose into native gates → **layout and routing** (insert SWAPs because qubits only talk to neighbours) → optimise → pulse schedule.

**Primitives (Qiskit):** *Sampler* returns bit-string counts; *Estimator* returns expectation values of observables (what VQE needs).

## Example 1: a Bell pair (the "hello world")

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(2, 2)
qc.h(0)              # put qubit 0 in a 50/50 blend
qc.cx(0, 1)          # entangle: qubit 1 follows qubit 0
qc.measure([0, 1], [0, 1])

counts = StatevectorSampler().run([qc], shots=1000).result()[0].data.c.get_counts()
print(counts)        # about {'00': 500, '11': 500}   (never '01' or '10')
```

## Example 2: a tiny VQE in PennyLane

```python
import pennylane as qml
from pennylane import numpy as np

dev = qml.device("default.qubit", wires=2)
H = qml.Hamiltonian([1.0, 0.5], [qml.PauliZ(0) @ qml.PauliZ(1), qml.PauliX(0)])   # the "energy" to minimise

@qml.qnode(dev)
def energy(theta):
    qml.RY(theta[0], wires=0)
    qml.RY(theta[1], wires=1)
    qml.CNOT(wires=[0, 1])
    return qml.expval(H)

opt = qml.AdamOptimizer(0.1)
theta = np.array([0.1, 0.2], requires_grad=True)
for _ in range(100):
    theta = opt.step(energy, theta)       # classical optimiser tunes the quantum circuit
print(energy(theta))
```

## Example 3: Grover on 2 qubits (finds |11⟩ in one round)

```python
from qiskit import QuantumCircuit
qc = QuantumCircuit(2)
qc.h([0, 1])                                        # all answers equally likely
qc.cz(0, 1)                                         # oracle: mark |11>
qc.h([0, 1]); qc.x([0, 1]); qc.cz(0, 1); qc.x([0, 1]); qc.h([0, 1])   # diffusion: amplify
qc.measure_all()                                    # now measures 11 with ~100% probability
```

## Using a quantum solver from a robot stack
1. A ROS 2 node publishes the optimisation problem (e.g. a cost matrix).
2. A **quantum service node** submits it to a simulator or cloud QPU (queue times can be minutes).
3. The result returns through an **action server**, with a **classical solver as fallback**.
4. Quantum never sits inside a real-time control loop.

## Interview Q&A

**What do Sampler and Estimator return?**
*Simply:* Sampler gives bit-string frequencies; Estimator gives the average value of an observable.

**Why transpile?**
*Simply:* real chips only support a few native gates and limited connectivity.

**Why can classical computers simulate only ~50 qubits exactly?**
*Simply:* the state needs $2^n$ numbers: 50 qubits is petabytes. Tensor-network methods stretch this for lightly entangled circuits.

**What is a "shot"?**
*Simply:* one run of the circuit; you repeat it thousands of times to estimate probabilities.
