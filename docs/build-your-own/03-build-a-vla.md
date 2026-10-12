---
title: 3. Build a VLA
---

# 3. Build a Vision-Language-Action Model (end to end)

:::tip[The 30-second version]
A VLA takes **camera images + a text instruction + the robot's joint readings** and outputs **the next few robot actions**. You build one in five moves: **(1) pick a task and a robot, (2) collect demonstrations, (3) choose or build the policy, (4) train it, (5) test it on the robot and feed the failures back into more data.** The data loop matters more than the model.
:::

![vla flywheel](/img/fig/vla-flywheel.svg)
*Building a VLA is a loop, not a line. Each lap (collect → train → evaluate → deploy → analyse failures) improves the policy.*

## The plan at a glance

| Step | What you do | Output |
|---|---|---|
| 0 | Choose task, success metric, route (sim / low-cost real arm / bigger robot) | project spec |
| 1 | Set up the robot, cameras, teleoperation, safety | a working teleop rig |
| 2 | Collect and validate demonstrations | a versioned dataset |
| 3 | Choose the policy (ACT → SmolVLA / π0 …) or design your own | a model recipe |
| 4 | Train and monitor | checkpoints |
| 5 | Evaluate in simulation and on the robot, with statistics | a results table |
| 6 | Deploy with async inference and a safety layer | a running system |
| 7 | Failure analysis → targeted data → retrain | each lap better than the last |

## Step 0. Define the project

| Decide | Good first choice | Why |
|---|---|---|
| **Task** | "pick the red cube and put it in the bowl" (one object, one place) | simple, measurable |
| **Success metric** | cube inside bowl within 30 s, judged by a fixed rule | removes arguments |
| **Variation** | start with 3–5 object positions, then widen | generalisation comes later |
| **Language** | 2–4 instructions that actually change behaviour ("red cube" vs "blue cube") | proves the VLA part works |
| **Route** | A: simulation only · B: low-cost real arm · C: industrial arm / humanoid | see below |

**Routes**
- **A. Simulation (free, safe, repeatable):** LIBERO, ManiSkill3, RoboCasa, or **Isaac Lab** for custom scenes and humanoids. Best for learning the pipeline and for large-scale data generation.
- **B. Low-cost real arm:** LeRobot-compatible arms such as **SO-100 / SO-101** (a leader arm you move by hand + a follower arm that copies it) with two USB cameras. A few hundred dollars. The most popular way to learn VLAs on real hardware.
- **C. Bigger robots:** Franka, UR, xArm, ALOHA bimanual, Unitree/Figure-class humanoids. Same recipe, more safety and calibration work.

## Part A. The tiny VLA (understand every part first)

Before touching hardware, run a complete VLA pipeline in a 2-D simulator. A white dot (the "robot") must go to the red or blue dot, whichever the *instruction* says.

### What each piece does
1. **Simulator (`ReachEnv`)**: renders a 32×32 image (red dot, blue dot, white agent pixel), keeps the agent's position (proprioception), and the instruction (0 = red, 1 = blue).
2. **Scripted expert**: moves straight toward the target. This replaces the human teleoperator.
3. **Demonstration collection**: for every step records `(image, state, instruction, next H actions)`. The **action chunk** is the next `H = 8` actions, the same idea as ACT and π0.
4. **VLA model**: a small CNN *sees*, an embedding *reads* the instruction, a linear layer encodes the state; the three are fused into a context vector; an **action head** outputs the chunk.
5. **Two action heads** you can compare:
   - `bc`: plain regression (L1 loss) of the chunk.
   - `flow`: **flow matching**: learn a velocity field that turns noise into the action chunk; at inference integrate 10 Euler steps. This is the approach in π0's action expert.
6. **Closed-loop evaluation**: run the policy in the simulator, execute the first 4 actions of each chunk, then predict again (**receding horizon**).

### The code (complete and runnable)

```python
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
```

*Source file: `examples/03_tiny_vla.py` in the repository.*

### Results (tested on a 4-core CPU)

| Demonstrations | BC head success | Flow-matching head success |
|---|---|---|
| 300 | 31 % | 31 % |
| 1,000 | 98 % | 100 % |
| 3,000 | 100 % | 100 % |

*(40 epochs, 100 fresh test episodes, one run each. Small differences, such as 98 % vs 100 %, are within noise; a different seed can move the 300-demo row by ±10 points.)*

**Lesson 1: data quantity matters enormously.** With too few demos the policy can't learn *where the dots are* from pixels. Real robots need the same discipline: a policy that fails is usually short of the right data, not short of model size.

### More experiments you can run (measured, 1,000 demos, BC head, 100 test episodes)

| Experiment | Success | What it teaches |
|---|---|---|
| **Chunk length H = 1** (predict one action at a time) | 83 % | no chunking → more compounding error and jitter |
| **H = 8, execute 1 action then re-plan** | 95 % | re-planning every step works but re-queries the model constantly |
| **H = 8, execute 4 then re-plan** (default) | 98 % | a good balance: smooth and responsive |
| **H = 8, execute all 8** (open loop for 8 steps) | 97 % | fewer model calls; slightly less reactive |
| **Wrong instruction given at test time** | **3–4 %** | the policy genuinely uses the language: it drives to the *other* dot |

**Lesson 2: action chunking helps.** Predicting several steps at once beat single-step prediction by about 15 points here, and executing only part of each chunk before re-planning (receding horizon) gives the best trade-off between smoothness and reactivity.

**Lesson 3: always run the "wrong instruction" test.** If success stayed high when you swap the instruction, the model would be ignoring the language (a very common VLA failure). Here it collapses to chance, which proves the language pathway works.

*Single run each, so differences of a few points are within noise. Repeat with several seeds before drawing conclusions about small effects.*


## Part B. Build on a real robot (route B, with LeRobot)

### Step 1. Hardware and setup checklist
| Item | Recommendation | Notes |
|---|---|---|
| **Arms** | leader + follower pair (SO-101 or similar) | the leader is what you move by hand |
| **Cameras** | 1 fixed front/top camera + 1 wrist camera, 640×480 @ 30 fps | wrist view is the biggest single boost for grasping |
| **Compute** | PC with an NVIDIA GPU (≥ 12–24 GB) | training and inference |
| **Workspace** | fixed table, fixed lighting, marked object positions | repeatability |
| **Safety** | emergency stop / power switch within reach, torque limits | humans first |
| **Calibration** | motor calibration (so leader and follower agree), camera focus fixed | redo after any mechanical change |

Install: `pip install lerobot` (or install from source for the newest features), then follow the robot-specific assembly and calibration guide in the LeRobot docs. **Test teleoperation first**: the follower should mirror the leader smoothly before you record anything.

```bash
# Command names and flags change between LeRobot versions: use `<command> --help` and the docs as the source of truth.
lerobot-teleoperate --robot.type=so101_follower --robot.port=/dev/ttyACM0 \
                    --teleop.type=so101_leader  --teleop.port=/dev/ttyACM1
```

### Step 2. Collect demonstrations (the most important step)

```bash
lerobot-record \
  --robot.type=so101_follower --robot.port=/dev/ttyACM0 \
  --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30},
                     wrist: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30} }" \
  --teleop.type=so101_leader --teleop.port=/dev/ttyACM1 \
  --dataset.repo_id=$HF_USER/pick_red_cube \
  --dataset.single_task="Pick the red cube and put it in the bowl" \
  --dataset.num_episodes=50 --display_data=true
```
Each episode stores, at every time step: camera frames, **`observation.state`** (joint positions), **`action`** (leader joint positions, i.e. the commanded targets), timestamp, and the **task text**. LeRobot saves this in its `LeRobotDataset` format (Parquet + MP4) and can push it to the Hugging Face Hub.

**How many demos?**
| Policy | Rough starting point |
|---|---|
| ACT / Diffusion Policy, one simple task | **~50 good demos** |
| SmolVLA, one task, fine-tuned from a pretrained base | **~50 demos per task** |
| π0 / π0.5 fine-tune for a new task | **tens to a few hundred**, more for harder tasks |
| Generalising to new objects / places | hundreds to thousands, with **diverse** positions, objects, lighting |

**Collection protocol (follow this):**
1. **Same strategy every time** (approach direction, grasp point, speed); inconsistency is the #1 cause of bad policies.
2. **Vary the start**: move the object over a grid of positions and orientations; vary distractors slightly.
3. **Smooth, confident motion**; no long pauses; end with the arm in a standard pose.
4. **Include some recoveries** (a regrasp after a slip) once the basic task works, but don't mix in sloppy demos.
5. **Language:** one clear sentence per task; use several phrasings if you want language robustness.
6. **Quality control:** replay episodes (`lerobot-replay` or the dataset visualiser), delete bad ones, check camera sync and dropped frames.
7. **Hold out** scenes/object positions for evaluation (don't train on every position you will test).
8. **Write it down:** date, lighting, objects, calibration version.

### Step 3. Choose the policy

| Policy | Size | Language | Best for | Notes |
|---|---|---|---|---|
| **ACT** (Action Chunking Transformer) | ~tens of M | no | first real baseline, ≈ 50 demos | fast to train and run; temporal ensembling for smoothness |
| **Diffusion Policy** | ~100 M | no | multimodal behaviour, precise tasks | denoises an action sequence; more inference steps |
| **SmolVLA** | ≈ 450 M | **yes** | low-cost arms, language-conditioned tasks | designed for consumer GPUs and asynchronous inference |
| **π0 / π0.5** (openpi, also in LeRobot) | ≈ 3 B | **yes** | best generalisation; harder tasks | flow-matching action expert on a PaliGemma VLM |
| **OpenVLA** | 7 B | yes | research; tokenised actions | LoRA fine-tuning; slower inference |
| **GR00T N-series** | ~2–3 B | yes | humanoids, Isaac ecosystem | dual-system design |

**Recommended path:** (1) **ACT first**: it proves your hardware, data and control loop work, with a quick training run. (2) Then **SmolVLA or π0** for language and generalisation. (3) Compare them in a table with the same evaluation protocol.

### Step 4. Train

```bash
# Baseline: ACT (≈ 100k steps is the usual order of magnitude; watch the loss curves)
lerobot-train --dataset.repo_id=$HF_USER/pick_red_cube \
              --policy.type=act --output_dir=outputs/train/act_pick \
              --job_name=act_pick --policy.device=cuda --wandb.enable=true

# Language-conditioned: fine-tune SmolVLA from the pretrained base on your demos
lerobot-train --policy.path=lerobot/smolvla_base \
              --dataset.repo_id=$HF_USER/pick_red_cube \
              --batch_size=64 --steps=20000 --output_dir=outputs/train/smolvla_pick \
              --policy.device=cuda --wandb.enable=true
```
*(Typical defaults at the time of writing: ACT chunk size ≈ 100 steps, lr ≈ 1e-5; Diffusion Policy horizon ≈ 16, lr ≈ 1e-4; SmolVLA fine-tuning ≈ 20k steps at batch 64 on one GPU. Always check the current defaults with `--help`.)*

**What to watch while training**
| Signal | Healthy | Problem |
|---|---|---|
| Training loss | steadily down | flat from the start → bug (normalisation, indexing, LR) |
| Validation loss on held-out episodes | follows training down | diverges → overfitting; get more diverse demos |
| Evaluation rollouts | success increases with checkpoints | loss is low but robot fails → data/deployment mismatch |
| GPU utilisation | high | low → data-loading bottleneck (decode video, more workers) |

**Pick the checkpoint by closed-loop success**, not lowest loss. Evaluate several checkpoints with the same protocol.

### Step 5. Evaluate (simulation first, then real)
- **Simulation sanity check:** LIBERO (10 tasks per suite: Spatial, Object, Goal, Long) lets you compare your pipeline with published numbers. With Isaac Lab you can build your own scenes and evaluate **many** episodes cheaply.
- **Real-world protocol:** fixed start positions (mark them on the table), **≥ 30–50 trials per condition**, randomise the order when comparing policies, record video, report success with a **Wilson confidence interval** (see chapter 4).
- **Generalisation splits:** new object positions, new objects, new lighting, new phrasing of the instruction, distractor objects.
- **Failure taxonomy:** missed grasp, wrong object, collision, stuck/loop, drop, timeout. Count each.
- **Ablations:** wrist camera on/off, chunk length, number of demos (10 / 25 / 50 / 100), with/without language.

### Step 6. Deploy on the robot

![async chunks](/img/fig/async-chunks.svg)
*The policy predicts a chunk of future actions. The robot executes the current chunk while the GPU already computes the next one, so motion stays smooth despite slow inference.*

```python
# The structure of a safe control loop (pseudocode)
queue, last_cmd = deque(), robot.read_joints()
while running:
    obs = robot.get_observation()                          # images + joint state, timestamped
    if len(queue) < REFILL_THRESHOLD and not request_in_flight:
        request_in_flight = policy.predict_async(obs, instruction)     # runs on the GPU in another thread
    if request_in_flight and request_in_flight.done():
        queue.extend(blend(queue, request_in_flight.result()))         # smooth the join between chunks
    if queue:
        cmd = queue.popleft()
        cmd = clip_to_joint_limits(cmd)                                # SAFETY LAYER (outside the model)
        cmd = limit_velocity(last_cmd, cmd, MAX_STEP)
        if not inside_workspace(cmd) or watchdog_tripped(): robot.hold(); continue
        robot.send_action(cmd); last_cmd = cmd
    sleep_until_next_tick(30)                              # fixed control rate (e.g. 30 Hz)
```

**Deployment checklist**
- [ ] **Same preprocessing as training**: image size, colour order, normalisation, action scaling, joint order.
- [ ] Control frequency equals the dataset fps.
- [ ] Camera latency measured; frames timestamped.
- [ ] Joint-limit, velocity and workspace limits enforced **outside** the neural network.
- [ ] Emergency stop reachable; first runs at low speed with a person watching.
- [ ] Log every run (video + actions + policy outputs) for failure analysis.

### Step 7. Improve: the data flywheel
1. Watch the failure videos; tag causes.
2. Collect **targeted** demos for the top failure (e.g. cube near the bowl edge).
3. Optionally add **human-in-the-loop corrections** (HG-DAgger): when the policy is about to fail, take over with the leader arm; those segments are the most valuable data.
4. Retrain from the pretrained base on old + new data. Re-run the *same* evaluation.
5. Later: RL fine-tuning, a bigger backbone, more embodiments, simulation data (below).

## Part C. Design your own VLA from scratch (the π0-style recipe)

![vla design](/img/fig/vla-design.svg)
*A π0-style VLA: a pretrained VLM understands the scene and instruction; a small "action expert" generates smooth action chunks with flow matching, attending to the VLM's features.*

**Step C1. Backbone.** Start from a pretrained VLM (PaliGemma 3B, SmolVLM, Qwen-VL, Eagle). Build it with the previous chapter if you must; usually you just load one.

**Step C2. Observation encoding.** Resize each camera image (224–384 px) and pass it through the vision encoder (≈ 256 tokens per image at 224 px with patch 14); tokenise the instruction; project the robot state (joint positions) into **one state token**. Concatenate: `[image tokens | text tokens | state token]`.

**Step C3. Action representation.**
- **Normalise** states and actions with dataset statistics (mean/std, or the 1st–99th percentiles mapped to [−1, 1]). Save the stats; use the same at deployment.
- Predict **action chunks** of H steps (≈ 1 second of motion: H = 50 at 50 Hz, or 100 at 30 Hz for ACT).
- Prefer **joint position targets** for hobby arms; **end-effector delta poses + gripper** for transfer across arms; relative-to-current-state targets often train better than absolute.

**Step C4. Action head.** Options:
| Head | How | Pros / cons |
|---|---|---|
| **Regression** (L1/L2) | MLP or transformer outputs the chunk | simplest; averages multi-modal demos |
| **Tokenised** (bins, or **FAST** = DCT + BPE compression) | LLM predicts action tokens autoregressively | reuses LLM head; slower, less smooth |
| **Diffusion / flow-matching action expert** (π0) | a separate small transformer takes noisy actions + time and predicts a velocity; attends to the VLM's key/values | smooth, multi-modal; extra denoising steps |

**Flow-matching training step** (this is exactly what `03_tiny_vla.py` does):
$$ x_t=(1-t)\,\epsilon+t\,a,\qquad \mathcal L=\big\|v_\theta(x_t,t,\text{obs})-(a-\epsilon)\big\|^2 $$
> **In words:** take a real action chunk $a$, blend it with noise $\epsilon$ by an amount $t$, and train the network to predict the direction that moves noise toward the real actions. At run time start from noise and take ~10 small steps along the predicted direction.

**Step C5. Attention layout.** Image/text/state tokens attend to each other (bidirectionally within the prefix). Action tokens attend to the whole prefix, but the prefix never attends to action tokens, so the VLM's features stay clean and can be cached.

**Step C6. Training recipe (starting points).**
| Item | Typical choice |
|---|---|
| Init | pretrained VLM weights; random action expert |
| Optimizer | AdamW, cosine schedule with warm-up |
| LR | VLM 1e-5 or LoRA; action expert 1e-4 |
| Batch | 32–256 (use accumulation) |
| Steps | 20k–100k for fine-tuning; far more for pre-training |
| Augmentation | small random crops/shifts (≈ 95 % crop), colour jitter; **no flips** (they break left/right semantics) |
| EMA | keep an exponential moving average of weights for evaluation |
| Co-training | mix in web VQA so the language skills are not forgotten |
| Precision | bf16 |

**Step C7. Inference.** Cache the VLM prefix once per observation, run ~10 flow steps for the action expert, return a chunk, execute the first *k* steps asynchronously.

**Step C8. Pre-train vs fine-tune.** Pre-training a generalist needs **large multi-robot datasets** (Open X-Embodiment, DROID, AgiBot World, LeRobot community datasets) and many GPUs. For your own robot, **fine-tune** a pretrained generalist (SmolVLA, π0, GR00T) on your demos; that is both cheaper and better.

## Part D. Simulation and synthetic data (scale without hardware)

| Tool | Use |
|---|---|
| **LIBERO / ManiSkill3 / RoboCasa** | standard benchmarks and ready datasets; compare with papers |
| **Isaac Lab** | custom scenes, many parallel environments, teleoperation devices, recorders |
| **Isaac Lab Mimic / MimicGen** | record ~10 human demos, **annotate subtasks**, auto-generate hundreds–thousands of new demos by transforming the object-relative motion |
| **Cosmos (world foundation models)** | augment rendered videos with photoreal variations; generate more data |
| **GR00T workflow** | collect → augment (Mimic + Cosmos) → post-train the VLA → evaluate in Isaac Lab → deploy on Jetson |

**Sim-to-real tips for policies trained with simulated data:** match camera intrinsics and placement, randomise textures/lighting, add image noise, co-train with real demos (even 10–20 % real data helps), and always evaluate on the real robot.

## Part E. Troubleshooting a VLA

| Symptom | Likely cause | Fix |
|---|---|---|
| Robot shakes or jitters | action noise, chunk joins, high control gain | larger chunk + blending/temporal ensembling, lower PD gains, smooth actions |
| Moves in a wrong direction | joint-order or sign mismatch, wrong normalisation stats, wrong action space | replay a recorded episode through the same deployment code path |
| Works only at training positions | too few / non-diverse demos | add demos over a wider grid; augmentation |
| Ignores the instruction | language rarely changes the demonstrated behaviour | include tasks where the instruction decides the outcome; more phrasings |
| Gets stuck, repeats | no recovery data; ambiguous state | add recovery demos; add history; longer chunks |
| Grasp timing wrong | gripper action is hard to regress | weight gripper loss, add wrist camera, binarise gripper |
| Loss low, robot bad | train/deploy mismatch, latency | compare observations, check fps, measure latency |
| Policy ok in the morning, bad later | lighting/camera shift | augmentation, fixed exposure, recalibrate |
| Slow control loop | inference too slow | async inference, smaller model, quantise, lower image resolution |
| Sim-trained policy fails on hardware | visual / dynamics gap | domain randomisation, real co-training, calibrate cameras |

## What "done" looks like

You can show: a dataset with versioned episodes; a baseline (ACT) and a VLA, trained with logged configs; a results table with confidence intervals across at least three generalisation splits; failure videos with a tagged taxonomy; a deployment loop with a safety layer; and the *next* planned data collection driven by the failures.
