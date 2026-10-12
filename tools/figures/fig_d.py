"""Simulation, learning pipelines, behaviour trees, and foundation visuals."""
from lib import *


def big_o():
    n = np.linspace(1, 10, 200)
    fig, ax = plt.subplots(figsize=(7.4, 4))
    for f, nm, c in ((np.log2(n), "log n  (binary search)", GREEN), (n, "n  (scan a list)", BLUE), (n * np.log2(n), "n log n  (good sorting)", TEAL), (n ** 2, "n²  (compare all pairs)", ORANGE), (2 ** n / 8, "2ⁿ  (try every subset)", RED)):
        ax.plot(n, f, color=c, lw=2.5, label=nm)
    ax.set_ylim(0, 60); ax.set_xlabel("input size  n"); ax.set_ylabel("work"); ax.legend(frameon=False, fontsize=9.5); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("Big-O: how the work grows as the input grows")
    save(fig, "big-o")


def bayes_update():
    x = np.linspace(-4, 8, 400); g = lambda m, s: np.exp(-(x - m) ** 2 / (2 * s * s))
    fig, ax = plt.subplots(figsize=(8, 3.6))
    pr, li = g(0, 1.8), g(3.5, 1.2); po = pr * li; po /= po.max()
    ax.fill_between(x, pr, color=BLUE, alpha=.25); ax.plot(x, pr, color=BLUE, lw=2.3, label="Prior: what I believed before")
    ax.fill_between(x, li, color=ORANGE, alpha=.25); ax.plot(x, li, color=ORANGE, lw=2.3, label="Likelihood: what the new data says")
    ax.fill_between(x, po, color=GREEN, alpha=.3); ax.plot(x, po, color=GREEN, lw=3, label="Posterior: updated belief (prior × likelihood)")
    ax.set_yticks([]); ax.set_ylim(0, 1.7); ax.legend(frameon=False, loc="upper right", fontsize=9); ax.set_xlabel("quantity we're estimating"); ax.set_title("Bayes' rule: update beliefs when new evidence arrives")
    save(fig, "bayes-update")


def isaac_family():
    fig, ax = canvas(11.5, 5.6, (0, 100), (0, 56))
    box(ax, 50, 50, 78, 6, "NVIDIA Omniverse (Kit) + OpenUSD + PhysX + RTX  =  the engine and file format", GRAY, fs=9.5)
    box(ax, 25, 34, 44, 12, "ISAAC SIM\nthe simulator app: physics, camera and\nLiDAR sensors, ROS 2 bridge, synthetic data", BLUE, bold=False, fs=9.2)
    box(ax, 75, 34, 44, 12, "ISAAC LAB\nrobot-learning toolkit on top of Sim:\nthousands of parallel envs, RL + imitation", GREEN, fs=9.2)
    box(ax, 25, 15, 44, 12, "ISAAC ROS\nGPU-accelerated ROS 2 perception on the\nreal robot (cuVSLAM, nvblox, FoundationPose)", ORANGE, fs=9.2)
    box(ax, 75, 15, 44, 12, "ISAAC GR00T + COSMOS\nhumanoid foundation model and world\nmodels (data generation, evaluation)", PURPLE, fs=9.2)
    arrow(ax, (40, 46.6), (28, 40.4), color=GRAY); arrow(ax, (60, 46.6), (72, 40.4), color=GRAY)
    arrow(ax, (47.4, 34), (52.6, 34), color=GRAY, style="<|-|>"); arrow(ax, (75, 27.6), (75, 21.4), color=GRAY, style="<|-|>"); arrow(ax, (25, 27.6), (25, 21.4), color=GRAY, style="<|-|>")
    label(ax, 50, 3.5, "Old 'Isaac Gym' (standalone GPU RL tool) is deprecated: Isaac Lab replaced it", color=RED, bold=True, fs=10)
    save(fig, "isaac-family")


def parallel_envs():
    fig, ax = canvas(10, 4.4, (0, 100), (0, 44))
    for r in range(3):
        for c in range(8):
            x, y = 8 + c * 8.5, 36 - r * 8.2
            ax.add_patch(Rectangle((x - 3.6, y - 3.4), 7.2, 6.8, fc="#f3f4f6", ec="#9ca3af"))
            ax.plot([x, x + (c % 3 - 1) * 1.2], [y - 1.5, y + 1.5], color=BLUE, lw=2.2); ax.add_patch(Circle((x + (c % 3 - 1) * 1.2, y + 2), .9, color=ORANGE))
    label(ax, 85, 28, "…× 4096", fs=14, bold=True, color=RED)
    box(ax, 27, 5, 46, 6.5, "ONE GPU simulates thousands of robots", BLUE, bold=True, fs=10)
    box(ax, 77, 5, 40, 6.5, "all experience pooled → 1 policy", GREEN, bold=True, fs=10)
    arrow(ax, (50.5, 5), (56, 5), color=GRAY)
    label(ax, 50, 41.5, "Why simulation can teach a robot to walk in minutes: massive parallel practice", bold=True, fs=11.5)
    save(fig, "parallel-envs")


def domain_randomization():
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.6))
    x = np.linspace(0, 2, 300)
    ax = axs[0]
    ax.axvline(.7, color=RED, lw=2.5, label="simulator guess (one value)")
    ax.fill_between(x, 0, 1, where=(x > .3) & (x < 1.3), color=GREEN, alpha=.35, label="randomised range")
    ax.axvline(1.05, color=ORANGE, lw=3, ls="--", label="real robot's true value (unknown)")
    ax.set_yticks([]); ax.set_xlabel("floor friction"); ax.legend(frameon=False, fontsize=9, loc="upper left"); ax.set_ylim(0, 1.6); ax.set_title("Domain randomization:\ntrain on many worlds so reality is 'just another one'")
    ax = axs[1]; ax.axis("off")
    items = ["friction · mass · centre of mass", "motor strength · PD gains", "sensor noise · camera lighting", "delay / latency · pushes", "terrain roughness"]
    ax.text(0, .95, "What gets randomised", fontweight="bold", va="top", fontsize=12)
    for i, t in enumerate(items): ax.text(.02, .8 - i * .13, "🎲 " if False else "•  " + t, va="top")
    ax.text(0, -.08, "Too narrow → policy fails on real robot.\nToo wide → policy becomes timid.", color=GRAY, va="bottom")
    save(fig, "domain-randomization")


def sim2real_gap():
    fig, ax = plt.subplots(figsize=(8, 3.8))
    t = np.linspace(0, 10, 200)
    real = np.sin(t) * 1.0
    sim = real + .02 * t * np.sin(1.5 * t) * 0; sim = np.sin(t * 1.0 + .0)
    ax.plot(t, sim, color=BLUE, lw=2.4, label="Behaviour in simulation")
    ax.plot(t, np.sin(t - .35) * .75 + .15 * np.sin(5 * t), color=RED, lw=2.4, label="Behaviour on the real robot (naive)")
    ax.plot(t, np.sin(t - .08) * .95 + .02 * np.sin(5 * t), color=GREEN, lw=2.4, ls="--", label="After randomization + system ID")
    ax.fill_between(t, sim, np.sin(t - .35) * .75 + .15 * np.sin(5 * t), color=RED, alpha=.12)
    ax.text(5.2, -1.3, "the 'reality gap'", color=RED, fontweight="bold")
    ax.set_yticks([]); ax.set_xlabel("time"); ax.legend(frameon=False, fontsize=9, loc="upper right"); ax.set_ylim(-1.5, 1.9); ax.set_title("Sim-to-real gap: the same policy behaves a bit differently on hardware")
    save(fig, "sim2real-gap")


def teacher_student():
    fig, ax = canvas(11, 4.4, (0, 100), (0, 44))
    box(ax, 20, 28, 34, 14, "TEACHER (trained in sim by RL)\nsees the secrets: exact terrain,\nfriction, true velocity", PURPLE, bold=True, fs=9.5)
    box(ax, 80, 28, 34, 14, "STUDENT (what you deploy)\nsees only what real sensors give:\njoint angles, IMU, camera", GREEN, bold=True, fs=9.5)
    arrow(ax, (37.4, 28), (62.6, 28), color=ORANGE, lw=2.6, text="student copies the\nteacher's actions", dy=1.8)
    box(ax, 78, 8, 34, 8, "Runs on the real robot", GRAY, fs=10); arrow(ax, (78, 20.8), (78, 12.2), color=GREEN)
    label(ax, 22, 8, "Like learning to drive with an\ninstructor who sees everything", fs=9.5, color=GRAY)
    label(ax, 50, 41, "Teacher–student: learn easily with privileged info, deploy with realistic info", bold=True, fs=11)
    save(fig, "teacher-student")


def bc_compounding():
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
    t = np.linspace(0, 1, 100); expert = np.sin(np.pi * t)
    for ax, ti, drift in ((axs[0], "Behaviour cloning: small errors snowball", True), (axs[1], "DAgger: expert corrects the learner's own mistakes", False)):
        ax.plot(t, expert, color=GREEN, lw=3, label="expert (demos)")
        if drift: ax.plot(t, expert + 1.3 * t ** 2 * np.sin(8 * t) * .5 + .8 * t ** 2, color=RED, lw=2.4, label="learner drifts into\nstates it never saw")
        else: ax.plot(t, expert + .08 * np.sin(14 * t), color=BLUE, lw=2.4, label="learner stays close")
        ax.set_xticks([]); ax.set_yticks([]); ax.set_title(ti, fontsize=10.5); ax.legend(frameon=False, fontsize=9, loc="lower center"); ax.set_ylim(-.3, 2.2)
    save(fig, "bc-compounding")


def behavior_tree():
    fig, ax = canvas(10, 5, (0, 100), (0, 52))
    box(ax, 50, 46, 24, 6, "→ Sequence (do all, in order)", BLUE, fs=9.5, bold=True)
    box(ax, 18, 32, 20, 6, "Go to shelf", GREEN, fs=9.5); box(ax, 50, 32, 22, 6, "? Fallback (try until one works)", ORANGE, fs=9, bold=True); box(ax, 84, 32, 20, 6, "Go to table", GREEN, fs=9.5)
    box(ax, 36, 18, 18, 6, "Grasp", GREEN, fs=9.5); box(ax, 64, 18, 22, 6, "Retry ×3: re-grasp\nfrom new view", GREEN, fs=8.5)
    box(ax, 84, 8, 20, 6, "Place cup", GREEN, fs=9.5)
    for a, b in (((50, 43), (18, 35)), ((50, 43), (50, 35)), ((50, 43), (84, 35)), ((50, 29), (36, 21)), ((50, 29), (64, 21))): arrow(ax, a, b, color=GRAY)
    arrow(ax, (84, 29), (84, 11), color=GRAY, ls="--")
    label(ax, 14, 8, "Green = actions the robot performs\nTick the tree ~10×/s: each node says\nSUCCESS / FAILURE / RUNNING", ha="left", fs=9, color=GRAY)
    save(fig, "behavior-tree")


def imitation_pipeline():
    fig, ax = canvas(11, 3.8, (0, 100), (0, 38))
    steps = [("1. Demonstrate", "human teleoperates\n(VR, leader arm)", ORANGE), ("2. Record", "camera + joint states\n+ actions", BLUE), ("3. Train", "policy learns\nobservation → action", PURPLE), ("4. Deploy", "robot repeats the\nskill on its own", GREEN), ("5. Fix failures", "add demos where it\nfailed; retrain", RED)]
    for i, (h, d, c) in enumerate(steps):
        x = 10 + i * 20; box(ax, x, 18, 17, 14, h + "\n" + d, c, fs=9)
        if i: arrow(ax, (x - 11.5, 18), (x - 8.8, 18), color=GRAY)
    arrow(ax, (90, 10.6), (10, 10.6), color="#9ca3af", rad=.0, ls="--")
    label(ax, 50, 6.8, "repeat until reliable", color=GRAY, fs=9.5); label(ax, 50, 33, "Teaching a robot by showing it (imitation learning)", bold=True, fs=11.5)
    save(fig, "imitation-pipeline")


def llm_training_pipeline():
    fig, ax = canvas(12, 3.8, (0, 120), (0, 38))
    steps = [("Pretraining", "read the internet:\npredict the next word", BLUE), ("Fine-tuning (SFT)", "learn to follow\ninstructions", TEAL), ("Preference tuning\n(RLHF / DPO)", "learn what humans\nprefer", ORANGE), ("Reasoning RL", "practice on problems\nwith checkable answers", PURPLE), ("Serve", "quantize, batch,\nKV-cache", GREEN)]
    for i, (h, d, c) in enumerate(steps):
        x = 12 + i * 24; box(ax, x, 17, 21, 16, h + "\n\n" + d, c, fs=8.8)
        if i: arrow(ax, (x - 12.6, 17), (x - 10.8, 17), color=GRAY)
    label(ax, 60, 33, "How a raw text predictor becomes a helpful assistant", bold=True, fs=11.5)
    save(fig, "llm-training-pipeline")


def simulator_map():
    fig, ax = plt.subplots(figsize=(8.2, 5))
    pts = [("Isaac Sim", 5.5, 9.3, BLUE), ("Isaac Lab", 8.7, 8.2, GREEN), ("Isaac Gym\n(deprecated)", 8.9, 3.5, GRAY), ("MuJoCo / MJX /\nMuJoCo Warp", 6.6, 6.6, PURPLE), ("Genesis", 8.3, 5.2, TEAL),
           ("ManiSkill3", 7.8, 7.0, ORANGE), ("Gazebo", 2.0, 5.5, RED), ("PyBullet", 3.4, 3.4, YELLOW), ("Drake", 2.0, 7.2, "#8b5cf6")]
    for n, x, y, c in pts: ax.scatter(x, y, s=260, color=c, edgecolor="white", zorder=3); ax.text(x + .22, y + .1, n, fontsize=9.5, va="center")
    ax.set_xlim(0, 11); ax.set_ylim(2, 10.5); ax.set_xlabel("raw speed for training (parallel environments) →"); ax.set_ylabel("sensor realism & ecosystem (rendering, ROS, assets) →")
    ax.set_xticks([]); ax.set_yticks([]); ax.set_title("Rough mental map of simulators (opinionated, not a benchmark)")
    ax.text(.3, 10.1, "slow but realistic", color=GRAY, fontsize=9); ax.text(10.7, 2.3, "fast but plain", color=GRAY, fontsize=9, ha="right")
    save(fig, "simulator-map")


def policy_io():
    fig, ax = canvas(11, 4.4, (0, 100), (0, 44))
    box(ax, 18, 22, 30, 28, "What the policy SEES\n\n• body tilt (gravity direction)\n• joint angles & speeds\n• last action\n• command: 'walk 0.8 m/s'\n• (teacher) terrain heights", BLUE, fs=9.5)
    box(ax, 50, 22, 18, 14, "Neural net\n(MLP / LSTM)\n~50 Hz", PURPLE, bold=True)
    box(ax, 80, 30, 30, 12, "Output: target joint angles", ORANGE, fs=10)
    box(ax, 80, 12, 30, 12, "PD controller → motor torque\n(200–1000 Hz)", GREEN, fs=9.5)
    arrow(ax, (33.4, 22), (40.6, 22)); arrow(ax, (59.4, 24), (65, 29)); arrow(ax, (80, 23.8), (80, 18.4), color=GRAY)
    label(ax, 50, 41, "A locomotion policy is a small network: sensors in → joint targets out", bold=True, fs=11.5)
    label(ax, 50, 3, "Training reward = track the commanded speed − energy − jerk − falls", fs=9.5, color=GRAY)
    save(fig, "policy-io")


def reward_shaping():
    fig, ax = canvas(10, 3.8, (0, 100), (0, 38))
    items = [("+  track commanded velocity", GREEN), ("+  feet leave the ground rhythmically", GREEN), ("−  wasted energy / torque", RED), ("−  jerky actions", RED), ("−  falling over (episode ends)", RED)]
    for i, (t, c) in enumerate(items): box(ax, 30, 31 - i * 6.2, 50, 4.6, t, c, fs=10)
    arrow(ax, (57, 18), (68, 18), color=GRAY, lw=2.5)
    box(ax, 83, 18, 26, 14, "Sum of weighted terms\n= the reward the robot\ntries to maximise", BLUE, bold=True, fs=9.5)
    label(ax, 50, 36.5, "Reward design: you describe 'good behaviour' as a score", bold=True, fs=11.5)
    save(fig, "reward-terms")


def run():
    for f in (big_o, bayes_update, isaac_family, parallel_envs, domain_randomization, sim2real_gap, teacher_student, bc_compounding,
              behavior_tree, imitation_pipeline, llm_training_pipeline, simulator_map, policy_io, reward_shaping):
        f()


if __name__ == "__main__":
    run()
