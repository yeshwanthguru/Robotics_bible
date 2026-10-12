---
title: Python for Robotics & ML
---

# Python for Robotics & ML

## Language internals
- **GIL:** one thread executes bytecode at a time → threads help I/O-bound only; CPU-bound → `multiprocessing`, NumPy/C extensions (release GIL), `concurrent.futures`, Numba, Cython. Python 3.13 free-threaded build (experimental, PEP 703).
- **Memory:** reference counting + cyclic GC; `__slots__`; generators for lazy evaluation; mutable default arg trap; shallow vs deep copy.
- **Data model:** dunder methods, descriptors, decorators, context managers, iterators/generators, `dataclasses`, `typing` (Protocol, TypedDict, Generic), `abc`, metaclasses (rare).
- **Async:** `asyncio` event loop, `await`, tasks; rclpy uses executors not asyncio by default (futures can be awaited).
- **Packaging:** venv/uv/conda, `pyproject.toml`, wheels, `pip install -e`, pinned requirements, Docker.
- **Performance:** vectorize (avoid Python loops), `np.einsum`, broadcasting, `numba.njit`, `jax.jit`, `torch.compile`, profile with `cProfile`, `line_profiler`, `py-spy`.

## The scientific stack
| Library | Use |
|---|---|
| NumPy | arrays, linear algebra, broadcasting |
| SciPy | optimize, integrate (`solve_ivp`), `spatial.transform.Rotation`, sparse, signal, KD-tree |
| Pandas / Polars | tabular logs |
| Matplotlib / Plotly | plots |
| OpenCV (`cv2`) | vision |
| Open3D | point clouds |
| scikit-learn | classic ML |
| PyTorch / JAX / TF | deep learning |
| Gymnasium / Stable-Baselines3 / RLlib / skrl / rsl_rl | RL |
| CasADi / cvxpy / OSQP / Drake pydrake | optimization/control |
| Pinocchio / RoboticsToolbox (Peter Corke) / ikpy / pytransform3d | kinematics/dynamics |
| MuJoCo / PyBullet / Isaac Lab / Genesis / SAPIEN / ManiSkill | simulation |
| rclpy, MoveIt Py, py_trees | ROS 2 |
| HuggingFace Transformers / LeRobot / PEFT / vLLM | LLM/VLA, robot learning |
| Qiskit / PennyLane / Cirq | quantum |
| `unified-planning` / PDDLPy / `up-fast-downward` | planning |

## PyTorch essentials
```python
import torch, torch.nn as nn
class MLP(nn.Module):
    def __init__(s, i, h, o):
        super().__init__(); s.net = nn.Sequential(nn.Linear(i,h), nn.GELU(), nn.Linear(h,h), nn.GELU(), nn.Linear(h,o))
    def forward(s, x): return s.net(x)

model = MLP(10, 128, 2).cuda()
opt = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=1e-2)
for x, y in loader:
    x, y = x.cuda(non_blocking=True), y.cuda()
    with torch.autocast('cuda', dtype=torch.bfloat16):
        loss = nn.functional.mse_loss(model(x), y)
    opt.zero_grad(set_to_none=True); loss.backward()
    nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step()
```
Know: autograd (`requires_grad`, `.detach()`, `torch.no_grad`), `DataLoader` (num_workers, pin_memory), `state_dict`, `torch.compile`, DDP launch via `torchrun`, `torch.profiler`, ONNX export, TorchScript, TensorRT.

## Robotics Python snippets

### Rotation with SciPy
```python
from scipy.spatial.transform import Rotation as R
r = R.from_euler('xyz', [10, 20, 30], degrees=True)
q = r.as_quat()            # (x, y, z, w) — scipy order!  ROS also x,y,z,w; Eigen constructor takes w first
R_mat = r.as_matrix(); v = r.apply([1, 0, 0])
```

### Simple 2-link FK/IK
```python
import numpy as np
def fk(q, l1=1.0, l2=1.0):
    return np.array([l1*np.cos(q[0]) + l2*np.cos(q[0]+q[1]),
                     l1*np.sin(q[0]) + l2*np.sin(q[0]+q[1])])
def jac(q, l1=1.0, l2=1.0):
    s1, c1, s12, c12 = np.sin(q[0]), np.cos(q[0]), np.sin(q[0]+q[1]), np.cos(q[0]+q[1])
    return np.array([[-l1*s1-l2*s12, -l2*s12], [l1*c1+l2*c12, l2*c12]])
def ik(target, q0, lam=1e-2, iters=100):
    q = q0.copy()
    for _ in range(iters):
        e = target - fk(q)
        if np.linalg.norm(e) < 1e-4: break
        J = jac(q); q += J.T @ np.linalg.solve(J @ J.T + lam**2*np.eye(2), e)  # damped least squares
    return q
```

### Gymnasium env skeleton
```python
import gymnasium as gym, numpy as np
class Reach(gym.Env):
    def __init__(s): 
        s.observation_space = gym.spaces.Box(-np.inf, np.inf, (4,), np.float32)
        s.action_space = gym.spaces.Box(-1, 1, (2,), np.float32)
    def reset(s, seed=None, options=None):
        super().reset(seed=seed); s.pos = np.zeros(2); s.goal = s.np_random.uniform(-1,1,2)
        return s._obs(), {}
    def step(s, a):
        s.pos += 0.1*np.clip(a,-1,1); d = np.linalg.norm(s.pos-s.goal)
        return s._obs(), -d, d<0.05, False, {}
    def _obs(s): return np.concatenate([s.pos, s.goal]).astype(np.float32)
```

### PPO via Stable-Baselines3
```python
from stable_baselines3 import PPO
PPO("MlpPolicy", Reach(), verbose=1, n_steps=2048, batch_size=64).learn(200_000)
```

## Testing & quality
`pytest` (fixtures, parametrize), `hypothesis` property tests, mocks, `ruff`/`black`/`mypy`, pre-commit, CI (GitHub Actions), reproducibility (seeds, deterministic algos, version pins), experiment tracking (W&B, MLflow, TensorBoard), configuration (Hydra/OmegaConf).

## Interview Q&A

**GIL consequences for ROS 2 nodes?** Callbacks in one executor thread; multi-threaded executor gives concurrency only for I/O or C-extension calls; heavy compute → separate process/C++ node.

**List vs tuple vs set vs dict?** Mutable ordered / immutable ordered / unique unordered hash / key-value hash (insertion-ordered ≥3.7).

**`is` vs `==`?** Identity vs equality.

**Generators?** Lazy iterators via `yield`; O(1) memory for streaming sensor data.

**Why vectorize?** Python loop overhead ≈ 50–100 ns/iter vs C-level inner loops with SIMD.

**Decorator example?** `@functools.wraps`-based timing/ retry decorators.

**Deep copy pitfalls with numpy/torch tensors?** Use `.copy()` / `.clone()`; views share memory.
