---
title: Coding Challenges You Should Be Able to Write
---

# Coding Challenges (write from memory)

## 1. Rotation matrix ↔ quaternion
```python
import numpy as np
def quat_to_R(q):                       # q = [w, x, y, z], unit
    w, x, y, z = q
    return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w),   2*(x*z+y*w)],
                     [2*(x*y+z*w),   1-2*(x*x+z*z), 2*(y*z-x*w)],
                     [2*(x*z-y*w),   2*(y*z+x*w),   1-2*(x*x+y*y)]])
```

## 2. Differential-drive odometry
```python
def odom_step(x, y, th, v, w, dt):
    return x + v*np.cos(th)*dt, y + v*np.sin(th)*dt, th + w*dt
```

## 3. PID with anti-windup
```python
class PID:
    def __init__(s, kp, ki, kd, umin, umax): s.kp,s.ki,s.kd,s.umin,s.umax=kp,ki,kd,umin,umax; s.i=0; s.prev=None
    def __call__(s, e, dt, meas_rate=None):
        d = (e - s.prev)/dt if s.prev is not None else 0.0; s.prev = e
        u_un = s.kp*e + s.ki*s.i + s.kd*d
        u = min(max(u_un, s.umin), s.umax)
        if u == u_un or (u_un - u) * e < 0: s.i += e*dt      # conditional integration
        return u
```

## 4. Particle filter resampling (systematic)
```python
def systematic_resample(w):
    N = len(w); pos = (np.arange(N) + np.random.rand())/N
    c = np.cumsum(w); idx = np.searchsorted(c, pos); return idx
```

## 5. Kabsch / ICP step (rigid alignment)
```python
def kabsch(P, Q):                          # find R,t: Q ≈ R P + t
    cp, cq = P.mean(0), Q.mean(0)
    H = (P-cp).T @ (Q-cq); U,S,Vt = np.linalg.svd(H)
    R = Vt.T @ np.diag([1,1,np.linalg.det(Vt.T@U.T)]) @ U.T
    return R, cq - R@cp
```

## 6. Softmax attention from scratch
```python
def attention(Q, K, V, mask=None):
    s = Q @ K.swapaxes(-1,-2) / np.sqrt(Q.shape[-1])
    if mask is not None: s = np.where(mask, s, -1e9)
    s = np.exp(s - s.max(-1, keepdims=True)); s /= s.sum(-1, keepdims=True)
    return s @ V
```

## 7. PPO clipped loss (PyTorch)
```python
def ppo_loss(logp, logp_old, adv, clip=0.2):
    r = (logp - logp_old).exp()
    return -torch.min(r*adv, r.clamp(1-clip, 1+clip)*adv).mean()
```

## 8. GAE
```python
def gae(r, v, done, gamma=0.99, lam=0.95):
    adv = np.zeros_like(r); last = 0
    for t in reversed(range(len(r))):
        nv = v[t+1] if t+1 < len(v) else 0
        delta = r[t] + gamma*nv*(1-done[t]) - v[t]
        last = delta + gamma*lam*(1-done[t])*last; adv[t] = last
    return adv
```

## 9. Occupancy grid log-odds update
```python
l[cell] += np.log(p_hit/(1-p_hit)) if occupied else np.log(p_miss/(1-p_miss))
```

## 10. Bresenham ray casting, DFS/BFS, Dijkstra, A*, union-find, LRU cache, binary search, two-sum — drill these from [CS Fundamentals](../01-foundations/cs-dsa-complexity.md).

## 11. Minimal ROS 2 subscriber → publisher bridge (see ROS 2 page); thread-safe queue & SPSC ring buffer (see C++ page).

## 12. Diffusion forward noising & DDPM training step
```python
def diffusion_loss(model, x0, alphas_bar):
    t = torch.randint(0, len(alphas_bar), (x0.size(0),))
    eps = torch.randn_like(x0); ab = alphas_bar[t].view(-1, *[1]*(x0.dim()-1))
    xt = ab.sqrt()*x0 + (1-ab).sqrt()*eps
    return F.mse_loss(model(xt, t), eps)
```
