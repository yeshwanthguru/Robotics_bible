---
title: Quantum Software Stack & Code
---

# Quantum Software Stack

| Framework | Owner | Use |
|---|---|---|
| **Qiskit** | IBM | circuits, transpiler, Runtime primitives (Sampler/Estimator), Aer simulator |
| **PennyLane** | Xanadu | differentiable QML, plugs into PyTorch/JAX, many backends |
| **Cirq** | Google | NISQ circuits, noise models |
| **CUDA-Q** | NVIDIA | GPU-accelerated simulation, hybrid quantum-classical, C++/Python |
| **Q#** / Azure Quantum | Microsoft | FT resource estimation |
| **Braket SDK** | AWS | multiple hardware vendors |
| **Ocean** | D-Wave | annealing, BQM |
| **tket / OpenQASM 3** | Quantinuum / community | compilation, IR |

Compilation stages: logical circuit → decomposition to native gates → layout/routing (SWAP insertion for coupling map) → optimization → pulse schedule.

## Bell state in Qiskit
```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
qc = QuantumCircuit(2, 2)
qc.h(0); qc.cx(0, 1); qc.measure([0, 1], [0, 1])
counts = StatevectorSampler().run([qc], shots=1000).result()[0].data.c.get_counts()
print(counts)   # ~{'00': 500, '11': 500}
```

## VQE-style variational circuit in PennyLane
```python
import pennylane as qml
from pennylane import numpy as np

dev = qml.device("default.qubit", wires=2)
H = qml.Hamiltonian([1.0, 0.5], [qml.PauliZ(0) @ qml.PauliZ(1), qml.PauliX(0)])

@qml.qnode(dev)
def cost(theta):
    qml.RY(theta[0], wires=0); qml.RY(theta[1], wires=1)
    qml.CNOT(wires=[0, 1])
    return qml.expval(H)

opt = qml.AdamOptimizer(0.1)
theta = np.array([0.1, 0.2], requires_grad=True)
for _ in range(100):
    theta = opt.step(cost, theta)
print(cost(theta))
```

## Grover (2 qubits, marking |11⟩)
```python
from qiskit import QuantumCircuit
qc = QuantumCircuit(2)
qc.h([0, 1])
qc.cz(0, 1)                       # oracle
qc.h([0, 1]); qc.x([0, 1]); qc.cz(0, 1); qc.x([0, 1]); qc.h([0, 1])  # diffusion
qc.measure_all()                  # measures 11 with prob 1 (N=4, 1 iteration)
```

## Hybrid quantum-classical in robotics
Typical loop: ROS2 node publishes problem (e.g. assignment cost matrix) → quantum service (simulator/QPU via cloud) → returns solution → fallback to classical solver on timeout. Treat QPU as an **accelerator behind an async action server**, never in a hard real-time loop.

## Interview Q&A

**What do Estimator and Sampler primitives return?** Estimator → expectation values of observables; Sampler → bitstring quasi-distributions.

**Why transpile?** Hardware supports only native gates & limited connectivity.

**Why simulate classically only to ~50 qubits?** State vector needs $2^n\cdot16$ bytes (50 qubits ≈ 16 PB); tensor-network methods stretch low-entanglement circuits.
