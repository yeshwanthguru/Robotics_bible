"""RL, LLM/VLA, quantum, Physical AI figures."""
from lib import *
from mpl_toolkits.mplot3d import Axes3D  # noqa


def agent_env_loop():
    fig, ax = canvas(9, 4.2, (0, 100), (0, 46))
    box(ax, 20, 23, 30, 16, "AGENT (the learner)\n\npolicy: state → action", BLUE, bold=True, fs=10)
    box(ax, 80, 23, 30, 16, "ENVIRONMENT\n(the world / robot\n+ simulator)", ORANGE, bold=True, fs=10)
    arrow(ax, (36, 29), (64, 29), color=BLUE, text="action a  (e.g. joint targets)", rad=-.0)
    arrow(ax, (64, 17), (36, 17), color=GREEN, text="new state s' + reward r", dy=-4.6)
    label(ax, 50, 41, "Repeat thousands of times. Goal: pick actions that maximise total future reward.", fs=10.5, bold=True)
    label(ax, 50, 5, "Like training a dog: it tries things, you hand out treats (rewards), it learns what works.", fs=10, color=GRAY)
    save(fig, "rl-loop")


def ppo_clip():
    r = np.linspace(.4, 1.6, 300); eps = .2
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.6), sharey=False)
    for ax, A, t in zip(axs, (1, -1), ("Action was GOOD (advantage > 0)", "Action was BAD (advantage < 0)")):
        un = r * A; cl = np.minimum(r * A, np.clip(r, 1 - eps, 1 + eps) * A)
        ax.plot(r, un, "--", color=GRAY, label="plain objective"); ax.plot(r, cl, color=BLUE if A > 0 else RED, lw=3, label="PPO clipped")
        ax.axvspan(1 - eps, 1 + eps, color="#e8f0fe", alpha=.6); ax.axvline(1, color="#9ca3af", lw=.8)
        ax.set_xlabel("new policy ÷ old policy (probability ratio)"); ax.set_title(t); ax.legend(frameon=False, fontsize=9)
        ax.set_yticks([])
    fig.suptitle("PPO: 'improve, but never change your behaviour too much in one step' (shaded = safe zone)", fontweight="bold", y=1.03)
    save(fig, "ppo-clip")


def gridworld_q():
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.4))
    n = 5
    goal = (4, 4); pit = (2, 2); wall = {(1, 3), (3, 1)}
    V = np.zeros((n, n)); gam = .9
    for _ in range(60):
        for i in range(n):
            for j in range(n):
                if (i, j) in wall or (i, j) in (goal, pit): continue
                best = -9
                for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    a, b = i + d[0], j + d[1]
                    if not (0 <= a < n and 0 <= b < n) or (a, b) in wall: a, b = i, j
                    r = 10 if (a, b) == goal else (-10 if (a, b) == pit else -.1)
                    best = max(best, r + gam * (0 if (a, b) in (goal, pit) else V[a, b]))
                V[i, j] = best
    ax = axs[0]
    for i in range(n):
        for j in range(n):
            c = "#374151" if (i, j) in wall else GREEN if (i, j) == goal else RED if (i, j) == pit else "white"
            ax.add_patch(Rectangle((j, n - 1 - i), 1, 1, fc=c, ec="#9ca3af"))
    ax.text(goal[1] + .5, n - 1 - goal[0] + .5, "GOAL\n+10", ha="center", va="center", color="white", fontweight="bold")
    ax.text(pit[1] + .5, n - 1 - pit[0] + .5, "PIT\n−10", ha="center", va="center", color="white", fontweight="bold")
    ax.add_patch(Circle((.5, n - .5), .3, fc=ORANGE)); ax.text(.5, n - .5, "🤖" if False else "R", ha="center", va="center", fontweight="bold", color="white")
    ax.set_xlim(0, n); ax.set_ylim(0, n); ax.set_aspect("equal"); ax.axis("off"); ax.set_title("The world: reach the goal, avoid the pit")
    ax = axs[1]
    for i in range(n):
        for j in range(n):
            if (i, j) in wall: ax.add_patch(Rectangle((j, n - 1 - i), 1, 1, fc="#374151")); continue
            if (i, j) in (goal, pit): ax.add_patch(Rectangle((j, n - 1 - i), 1, 1, fc=GREEN if (i, j) == goal else RED)); continue
            ax.add_patch(Rectangle((j, n - 1 - i), 1, 1, fc=plt.cm.Blues(.15 + .8 * V[i, j] / 10), ec="#9ca3af"))
            best, bd = -99, None
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a, b = i + d[0], j + d[1]
                if not (0 <= a < n and 0 <= b < n) or (a, b) in wall: continue
                v = 10 if (a, b) == goal else (-10 if (a, b) == pit else V[a, b])
                if v > best: best, bd = v, d
            ax.annotate("", (j + .5 + .3 * bd[1], n - 1 - i + .5 - .3 * bd[0]), (j + .5 - .3 * bd[1], n - 1 - i + .5 + .3 * bd[0]), arrowprops=dict(arrowstyle="-|>", color=INK, lw=2))
    ax.set_xlim(0, n); ax.set_ylim(0, n); ax.set_aspect("equal"); ax.axis("off"); ax.set_title("What it learned: darker = more valuable cell,\narrows = best move")
    save(fig, "gridworld-values")


def kv_cache():
    fig, ax = canvas(10, 4.6, (0, 100), (0, 46))
    label(ax, 25, 42, "WITHOUT cache: re-read everything every step", color=RED, bold=True, fs=10.5)
    label(ax, 75, 42, "WITH KV cache: remember past keys/values", color=GREEN, bold=True, fs=10.5)
    toks = ["The", "robot", "picks", "up", "→ ?"]
    for k in range(3):
        for i, t in enumerate(toks[:3 + k]):
            box(ax, 6 + i * 9, 30 - k * 9, 8, 5, t, RED if i < 2 + k else ORANGE, fs=8)
    label(ax, 25, 5, "work grows with the square of the length", color=RED, fs=9.5)
    for k in range(3):
        for i, t in enumerate(toks[:3 + k]):
            new = i == 2 + k
            box(ax, 56 + i * 9, 30 - k * 9, 8, 5, t, ORANGE if new else GREEN, fs=8)
    label(ax, 75, 5, "only the NEW token is computed; old ones are stored", color=GREEN, fs=9.5)
    label(ax, 50, 17, "", fs=1)
    ax.plot([50, 50], [3, 40], color="#d1d5db", lw=1)
    save(fig, "kv-cache")


def scaling_law():
    N = np.logspace(6, 12, 100)
    fig, ax = plt.subplots(figsize=(7.2, 4))
    for D, c, n in ((1e9, RED, "1B tokens"), (1e11, ORANGE, "100B tokens"), (2e13, GREEN, "20T tokens")):
        L = 1.7 + 400 / N ** .34 + 410 / D ** .28
        ax.plot(N, L, color=c, lw=2.4, label=f"trained on {n}")
    ax.set_xscale("log"); ax.set_xlabel("model size (parameters)"); ax.set_ylabel("loss (lower = smarter)")
    ax.legend(frameon=False); ax.set_title("Scaling laws: bigger model + more data = smoothly lower loss")
    save(fig, "scaling-law")


def rag_flow():
    fig, ax = canvas(12, 4.2, (0, 120), (0, 42))
    box(ax, 12, 30, 18, 8, "Question", GRAY)
    box(ax, 40, 30, 20, 8, "Embed\n(text → numbers)", BLUE)
    box(ax, 70, 30, 22, 8, "Vector search\nin your documents", ORANGE)
    box(ax, 100, 30, 22, 8, "Top-k relevant\npassages", GREEN)
    box(ax, 70, 10, 26, 9, "Your documents\n(chunked + embedded in advance)", GRAY, dashed=True, fs=9.5)
    box(ax, 100, 10, 22, 9, "LLM reads question\n+ passages", PURPLE, bold=True, fs=9.5)
    box(ax, 12, 10, 18, 8, "Answer\nwith citations", GREEN)
    for a_, b_ in (((21.4, 30), (29.6, 30)), ((50.6, 30), (58.4, 30)), ((81.4, 30), (88.6, 30))): arrow(ax, a_, b_)
    arrow(ax, (70, 15.2), (70, 25.6), color="#9ca3af", ls="--")
    arrow(ax, (100, 25.6), (100, 15.2), color=GREEN)
    ax.plot([100, 100, 12], [5.4, 1.2, 1.2], color=PURPLE, lw=1.8); arrow(ax, (12, 1.2), (12, 5.4), color=PURPLE)
    label(ax, 56, 3.2, "LLM writes the answer from the passages", fs=9.5, color=PURPLE)
    label(ax, 60, 39.5, "RAG = give the LLM an open book instead of asking it to memorise everything", bold=True, fs=11)
    save(fig, "rag-flow")


def vla_arch():
    fig, ax = canvas(12, 5, (0, 120), (0, 52))
    box(ax, 12, 40, 20, 8, "Camera images", GRAY); box(ax, 12, 26, 20, 9, "Instruction:\n'put the cup in the sink'", GRAY, fs=9); box(ax, 12, 12, 20, 8, "Robot joint state", GRAY)
    box(ax, 42, 40, 20, 8, "Vision encoder\n(sees)", BLUE); box(ax, 42, 26, 20, 8, "Text tokenizer\n(reads)", BLUE); box(ax, 42, 12, 20, 8, "State projector", BLUE)
    box(ax, 72, 26, 24, 34, "Big language–\nvision model\n(VLM)\n\n'understands the\nscene and goal'", PURPLE, bold=True, fs=10)
    box(ax, 102, 26, 22, 16, "Action head\n(diffusion /\nflow / tokens)", ORANGE, bold=True, fs=10)
    for y in (40, 26, 12):
        arrow(ax, (22.4, y), (31.6, y)); arrow(ax, (52.4, y), (59.5, 26 + (y - 26) * .6))
    arrow(ax, (84.4, 26), (90.6, 26))
    box(ax, 102, 6, 26, 7, "→ controller → motors", GREEN, fs=9.5); arrow(ax, (102, 17.6), (102, 9.8), color=GREEN)
    label(ax, 60, 49.5, "Vision-Language-Action model: sees + reads + acts", bold=True, fs=12)
    save(fig, "vla-architecture")


def dual_system():
    fig, ax = canvas(10, 4.2, (0, 100), (0, 42))
    box(ax, 25, 26, 32, 13, "SYSTEM 2 — slow thinker\n(VLM, ~5–10 times / second)\n'what is the plan? what do I see?'", PURPLE, fs=10, bold=False)
    box(ax, 75, 26, 32, 13, "SYSTEM 1 — fast doer\n(action policy, ~50–200 Hz)\n'move the fingers now, smoothly'", ORANGE, fs=10)
    arrow(ax, (41.5, 26), (58.5, 26), text="goal / plan", dy=1.2)
    box(ax, 73, 8, 36, 8, "Motors, 1000 Hz low-level control", GREEN)
    arrow(ax, (73, 19), (73, 12.2), color=GREEN)
    label(ax, 27, 8, "Like you: deciding to make tea (slow)\nvs your hand pouring it (fast, automatic)", fs=9.5, color=GRAY)
    label(ax, 50, 39, "Why VLAs are split into a slow brain and a fast body", bold=True, fs=12)
    save(fig, "dual-system")


def bloch_sphere():
    fig = plt.figure(figsize=(9, 4.4))
    ax = fig.add_subplot(121, projection="3d")
    u, v = np.mgrid[0:2 * np.pi:40j, 0:np.pi:20j]
    ax.plot_wireframe(np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), np.cos(v), color="#c7d2e6", lw=.5, alpha=.8)
    for vec, c, lab in (((0, 0, 1.45), BLUE, "|0⟩"), ((0, 0, -1.45), RED, "|1⟩"), ((1.45, 0, 0), GRAY, "|+⟩"), ((-1.45, 0, 0), GRAY, "|−⟩")):
        ax.plot([0, vec[0]], [0, vec[1]], [0, vec[2]], color=c, lw=1.2); ax.text(*(np.array(vec) * 1.08), lab, ha="center", fontsize=11, color=c)
    th, ph = 1.0, .9
    s = np.array([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)])
    ax.quiver(0, 0, 0, *s, color=ORANGE, lw=3, arrow_length_ratio=.15)
    ax.set_axis_off(); ax.set_box_aspect((1, 1, 1), zoom=1.35); ax.view_init(20, 35); ax.set_title("A qubit = a point on a sphere\n(orange arrow = its state)")
    ax2 = fig.add_subplot(122); ax2.axis("off")
    ax2.text(0, .95, "Classical bit", fontweight="bold", fontsize=12, va="top"); ax2.text(0, .82, "a light switch: ON or OFF", va="top")
    ax2.text(0, .62, "Qubit", fontweight="bold", fontsize=12, va="top", color=ORANGE)
    ax2.text(0, .5, "a dimmer + a compass:\n• north pole = 0, south pole = 1\n• anywhere else = a blend of both\n• measuring forces a yes/no answer\n  (the odds depend on how close\n  the arrow is to each pole)", va="top", linespacing=1.5)
    save(fig, "bloch-sphere")


def superposition_bars():
    fig, axs = plt.subplots(1, 3, figsize=(10.5, 3.4))
    for ax, (t, p, c) in zip(axs, (("Definitely 0", [1, 0], BLUE), ("50/50 superposition\n(after a Hadamard gate)", [.5, .5], PURPLE), ("Mostly 1", [.15, .85], RED))):
        ax.bar(["0", "1"], p, color=c, width=.55); ax.set_ylim(0, 1.05); ax.set_title(t); ax.set_ylabel("chance when measured")
    fig.suptitle("A qubit's state sets the odds of each answer when you measure it", fontweight="bold", y=1.13)
    save(fig, "superposition-bars")


def circuit_bell():
    fig, ax = canvas(9, 3.4, (0, 100), (0, 34))
    for y, n in ((24, "q0  |0⟩"), (10, "q1  |0⟩")):
        ax.plot([14, 90], [y, y], color=INK, lw=1.4); label(ax, 6, y, n, ha="center", fs=10)
    box(ax, 30, 24, 8, 8, "H", BLUE, bold=True, fs=13)
    ax.plot([52, 52], [10, 24], color=INK, lw=1.6); ax.add_patch(Circle((52, 24), 1.3, color=INK))
    ax.add_patch(Circle((52, 10), 3.2, fc="white", ec=INK, lw=1.6)); ax.plot([52, 52], [6.8, 13.2], color=INK, lw=1.6); ax.plot([48.8, 55.2], [10, 10], color=INK, lw=1.6)
    for y in (24, 10): box(ax, 76, y, 8, 8, "📏" if False else "M", ORANGE, bold=True, fs=12)
    label(ax, 30, 31, "Hadamard:\nmake 50/50", fs=9, color=BLUE); label(ax, 52, 31, "CNOT: q1 flips\nif q0 is 1", fs=9, color=INK); label(ax, 76, 31, "measure", fs=9, color=ORANGE)
    label(ax, 50, 1.5, "Result: only '00' or '11', each 50% — the two qubits are entangled (always agree)", fs=10, bold=True, color=GREEN)
    save(fig, "bell-circuit")


def grover_bars():
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.2))
    N = 8; amp = np.ones(N) / np.sqrt(N); w = 5
    stages = [("1. Start: all answers\nequally likely", amp.copy())]
    a = amp.copy(); a[w] *= -1; stages.append(("2. Oracle: secretly flip\nthe sign of the right answer", a.copy()))
    m = a.mean(); a = 2 * m - a; stages.append(("3. Diffusion: flip around\nthe average → right answer grows", a.copy()))
    for ax, (t, y) in zip(axs, stages):
        ax.bar(range(N), y, color=[ORANGE if i == w else BLUE for i in range(N)]); ax.axhline(0, color=INK, lw=.8)
        ax.set_ylim(-.7, .95); ax.set_title(t, fontsize=10); ax.set_xticks(range(N)); ax.set_yticks([])
    fig.suptitle("Grover search: amplify the right answer (bars = amplitude, orange = target)", fontweight="bold", y=1.18)
    save(fig, "grover-amplitude")


def vqe_loop():
    fig, ax = canvas(10, 4.2, (0, 100), (0, 42))
    box(ax, 18, 22, 24, 12, "Quantum computer\nruns circuit U(θ)\nand measures energy", PURPLE, bold=True)
    box(ax, 62, 22, 24, 12, "Classical computer\nnudges θ to lower\nthe energy", BLUE, bold=True)
    arrow(ax, (30.6, 26), (49.4, 26), text="energy E(θ)", color=PURPLE, rad=-.25, dy=2.6)
    arrow(ax, (49.4, 18), (30.6, 18), text="new angles θ", color=BLUE, rad=-.25, dy=-5.5)
    box(ax, 90, 22, 15, 10, "Lowest energy\n≈ answer", GREEN)
    arrow(ax, (74.6, 22), (82, 22), color=GREEN)
    label(ax, 50, 38, "VQE / QAOA: a tuning loop between a small quantum chip and a normal computer", bold=True, fs=11.5)
    label(ax, 50, 5, "Like tuning a guitar: the chip plays the note, the laptop decides which peg to turn.", color=GRAY, fs=10)
    save(fig, "vqe-loop")


def physical_ai_stack():
    fig, ax = canvas(10, 6, (0, 100), (0, 62))
    layers = [("Foundation models: VLM / VLA / world models  —  'understand and decide'", PURPLE),
              ("Task & motion planning  —  'what steps, which path?'", BLUE),
              ("Skills: imitation + RL policies  —  'how to grasp, walk, pour'", TEAL),
              ("Whole-body / MPC / impedance control  —  'smooth, safe motor commands'", ORANGE),
              ("Perception & state estimation  —  'where am I, what is where?'", GREEN),
              ("Hardware: sensors, motors, compute, battery", GRAY)]
    for i, (t, c) in enumerate(layers):
        box(ax, 44, 54 - i * 9.4, 82, 7, t, c, fs=10.2, bold=(i == 0))
    for i in range(5): arrow(ax, (44, 50.4 - i * 9.4), (44, 47 - i * 9.4 + 1.2), color="#9ca3af", style="<|-|>")
    box(ax, 95, 29, 7, 50, "", GRAY, dashed=True); ax.text(95, 29, "Simulation + synthetic data feed every layer", rotation=90, ha="center", va="center", fontsize=9.5, color=GRAY)
    save(fig, "physical-ai-stack")


def three_computers():
    fig, ax = canvas(11, 3.8, (0, 100), (0, 36))
    box(ax, 17, 18, 26, 18, "1. TRAIN\nbig GPU clusters\nlearn the 'brain'", PURPLE, bold=True)
    box(ax, 50, 18, 26, 18, "2. SIMULATE\nvirtual worlds (Isaac Sim/Lab,\nCosmos): safe practice + data", BLUE, bold=True, fs=9.5)
    box(ax, 83, 18, 26, 18, "3. RUN\nonboard robot computer\n(Jetson): real-time", GREEN, bold=True)
    arrow(ax, (30.6, 18), (36.4, 18)); arrow(ax, (63.6, 18), (69.4, 18)); label(ax, 50, 4, "↺ real-world data and failures flow back into training", fs=10, color=GRAY)
    label(ax, 50, 33, "NVIDIA's 'three computers' view of Physical AI", bold=True, fs=12)
    save(fig, "three-computers")


def run():
    for f in (agent_env_loop, ppo_clip, gridworld_q, kv_cache, scaling_law, rag_flow, vla_arch, dual_system, bloch_sphere, superposition_bars,
              circuit_bell, grover_bars, vqe_loop, physical_ai_stack, three_computers):
        f()


if __name__ == "__main__":
    run()
