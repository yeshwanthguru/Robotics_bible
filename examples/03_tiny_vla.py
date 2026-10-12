"""A complete, tiny Vision-Language-Action policy, end to end, in a 2-D 'reach the coloured dot' world.

Pipeline shown end to end:
  simulator -> scripted expert -> demonstration dataset -> VLA model (vision + language + state -> action chunk)
  -> training (behaviour cloning OR flow matching) -> closed-loop evaluation with receding-horizon execution.

Run:  python examples/03_tiny_vla.py --head bc       (regression head)
      python examples/03_tiny_vla.py --head flow     (flow-matching head, like pi0's action expert)
"""
import argparse, time
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F

IMG, H, STEP = 32, 8, 0.06             # image size, action-chunk length (steps predicted at once), max move per step
INSTR = ["red", "blue"]                # the "language": which dot to go to (embedded as a token)


# ---------- 1. Simulator: two dots (red, blue), an agent point, an instruction ----------
class ReachEnv:
    def __init__(self, seed=0): self.rng = np.random.default_rng(seed)
    def reset(self):
        self.red, self.blue = self.rng.uniform(.1, .9, 2), self.rng.uniform(.1, .9, 2)
        while np.linalg.norm(self.red - self.blue) < .3: self.blue = self.rng.uniform(.1, .9, 2)
        self.pos, self.instr, self.t = self.rng.uniform(.1, .9, 2), int(self.rng.integers(2)), 0
        return self.obs()
    def target(self): return self.blue if self.instr else self.red
    def obs(self):
        img = np.zeros((3, IMG, IMG), np.float32)
        for p, ch in ((self.red, 0), (self.blue, 2)):
            x, y = (p * (IMG - 1)).astype(int); img[ch, max(y - 1, 0):y + 2, max(x - 1, 0):x + 2] = 1.0   # 3x3 coloured dot
        x, y = (self.pos * (IMG - 1)).astype(int); img[:, y, x] = 1.0                                       # agent = white pixel
        return img, self.pos.astype(np.float32).copy(), self.instr
    def step(self, a):
        self.pos = np.clip(self.pos + np.clip(a, -STEP, STEP), 0, 1); self.t += 1
        return self.obs(), np.linalg.norm(self.pos - self.target()) < .05, self.t >= 60


def expert_action(env):                 # a scripted expert: move straight toward the target
    d = env.target() - env.pos; n = np.linalg.norm(d)
    return d if n < STEP else d / n * STEP


# ---------- 2. Collect demonstrations -> (image, state, instruction, action chunk of the next H steps) ----------
def collect(n_episodes, seed=0):
    env = ReachEnv(seed); data = []
    for _ in range(n_episodes):
        img, st, ins = env.reset(); traj = []
        for _ in range(60):
            a = expert_action(env); traj.append((img, st, ins, a))
            (img, st, ins), done, _ = env.step(a)
            if done: break
        acts = np.stack([t[3] for t in traj])
        for i, (im, s, ins, _) in enumerate(traj):
            chunk = acts[i:i + H]
            if len(chunk) < H: chunk = np.concatenate([chunk, np.zeros((H - len(chunk), 2), np.float32)])   # pad with "stay still"
            data.append((im, s, ins, chunk.astype(np.float32)))
    im, s, ins, ch = zip(*data)
    return torch.tensor(np.stack(im)), torch.tensor(np.stack(s)), torch.tensor(ins), torch.tensor(np.stack(ch))


# ---------- 3. The VLA: vision encoder + instruction embedding + state -> context -> action head ----------
class TinyVLA(nn.Module):
    def __init__(self, head="bc", d=128):
        super().__init__()
        self.head_type = head
        self.vision = nn.Sequential(nn.Conv2d(3, 32, 5, 2, 2), nn.GELU(), nn.Conv2d(32, 64, 3, 2, 1), nn.GELU(),
                                    nn.Conv2d(64, 64, 3, 2, 1), nn.GELU(), nn.Flatten(), nn.Linear(64 * 4 * 4, d))   # sees
        self.lang = nn.Embedding(len(INSTR), d)                                                                       # reads
        self.state = nn.Linear(2, d)                                                                                  # proprioception
        self.fuse = nn.Sequential(nn.Linear(3 * d, 2 * d), nn.GELU(), nn.Linear(2 * d, d))                            # the "backbone"
        if head == "bc":
            self.action_head = nn.Sequential(nn.Linear(d, 2 * d), nn.GELU(), nn.Linear(2 * d, H * 2))
        else:                                                    # flow matching: predict a velocity for a noisy action chunk
            self.action_head = nn.Sequential(nn.Linear(d + H * 2 + 1, 2 * d), nn.GELU(), nn.Linear(2 * d, 2 * d), nn.GELU(), nn.Linear(2 * d, H * 2))
    def context(self, img, st, ins): return self.fuse(torch.cat([self.vision(img), self.lang(ins), self.state(st)], -1))
    def loss(self, img, st, ins, chunk):
        c = self.context(img, st, ins)
        if self.head_type == "bc":
            return F.l1_loss(self.action_head(c).view(-1, H, 2), chunk)
        x1 = chunk.flatten(1) / STEP                              # normalise actions to ~[-1, 1]
        x0 = torch.randn_like(x1); t = torch.rand(x1.size(0), 1)
        xt = (1 - t) * x0 + t * x1                                # a point on the straight path noise -> data
        v = self.action_head(torch.cat([c, xt, t], -1))
        return F.mse_loss(v, x1 - x0)                             # regress the velocity of that path
    @torch.no_grad()
    def act(self, img, st, ins, steps=10):
        c = self.context(img, st, ins)
        if self.head_type == "bc": return self.action_head(c).view(-1, H, 2)
        x = torch.randn(c.size(0), H * 2)
        for k in range(steps):                                    # Euler-integrate the learned velocity field from noise to actions
            t = torch.full((c.size(0), 1), k / steps)
            x = x + self.action_head(torch.cat([c, x, t], -1)) / steps
        return (x * STEP).view(-1, H, 2)


# ---------- 4. Closed-loop evaluation: execute the first K actions of each chunk, then re-plan (receding horizon) ----------
@torch.no_grad()
def rollout_success(model, n=100, execute=4, seed=123):
    env = ReachEnv(seed); wins = 0; model.eval()
    for _ in range(n):
        (img, st, ins), done, timeout = env.reset(), False, False
        while not (done or timeout):
            chunk = model.act(torch.tensor(img)[None], torch.tensor(st)[None], torch.tensor([ins]))[0].numpy()
            for a in chunk[:execute]:
                (img, st, ins), done, timeout = env.step(a)
                if done or timeout: break
        wins += done
    model.train()
    return wins / n


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--head", default="bc", choices=["bc", "flow"])
    ap.add_argument("--episodes", type=int, default=1000); ap.add_argument("--epochs", type=int, default=40)
    a = ap.parse_args(); torch.manual_seed(0); t0 = time.time()
    img, st, ins, ch = collect(a.episodes)
    n = len(img); perm = torch.randperm(n); tr, va = perm[: int(.9 * n)], perm[int(.9 * n):]
    print(f"{a.episodes} demos -> {n} training samples; head = {a.head}")
    model = TinyVLA(a.head); opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, a.epochs * (len(tr) // 128 + 1))
    for ep in range(a.epochs):
        idx = tr[torch.randperm(len(tr))]
        for i in range(0, len(idx), 128):
            b = idx[i:i + 128]; loss = model.loss(img[b], st[b], ins[b], ch[b])
            opt.zero_grad(); loss.backward(); opt.step(); sched.step()
        if ep % 5 == 0 or ep == a.epochs - 1:
            with torch.no_grad(): v = model.loss(img[va], st[va], ins[va], ch[va]).item()
            print(f"epoch {ep:3d}  train {loss.item():.4f}  val {v:.4f}")
    print(f"closed-loop success rate over 100 new episodes: {rollout_success(model):.0%}  ({time.time() - t0:.0f}s)")
