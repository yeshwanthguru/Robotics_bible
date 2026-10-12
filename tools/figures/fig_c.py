"""Robotics core, perception, control, planning, mobility, dexterity figures."""
from lib import *


def two_link_arm():
    l1, l2 = 1.0, .8
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.4))
    ax = axs[0]
    th = np.linspace(0, 2 * np.pi, 200)
    ax.add_patch(plt.Circle((0, 0), l1 + l2, fc="#e3edfc", ec=BLUE, lw=1.5)); ax.add_patch(plt.Circle((0, 0), abs(l1 - l2), fc="white", ec=BLUE, lw=1.5, ls="--"))
    q1, q2 = .9, .8
    p1 = np.array([l1 * np.cos(q1), l1 * np.sin(q1)]); p2 = p1 + l2 * np.array([np.cos(q1 + q2), np.sin(q1 + q2)])
    ax.plot([0, p1[0], p2[0]], [0, p1[1], p2[1]], "o-", color=INK, lw=5, ms=11)
    ax.plot(*p2, "*", color=ORANGE, ms=18); ax.text(p2[0] + .08, p2[1] + .1, "hand (end-effector)", color=ORANGE, fontweight="bold")
    ax.text(0, -.12, "base", ha="center", va="top", fontsize=9); ax.text(0, -2.45, "light blue = everywhere the hand can reach (workspace)", ha="center", fontsize=9, color=BLUE)
    ax.set_xlim(-2.1, 2.1); ax.set_ylim(-2.7, 2.1); ax.set_aspect("equal"); ax.axis("off"); ax.set_title("Forward kinematics: joint angles → hand position")
    ax = axs[1]
    target = np.array([1.1, .9]); d = np.linalg.norm(target); c2 = (d * d - l1 * l1 - l2 * l2) / (2 * l1 * l2)
    for sgn, col, nm in ((1, GREEN, "elbow down"), (-1, PURPLE, "elbow up")):
        q2_ = sgn * np.arccos(c2); q1_ = np.arctan2(target[1], target[0]) - np.arctan2(l2 * np.sin(q2_), l1 + l2 * np.cos(q2_))
        e = np.array([l1 * np.cos(q1_), l1 * np.sin(q1_)])
        ax.plot([0, e[0], target[0]], [0, e[1], target[1]], "o-", color=col, lw=5, ms=9, label=nm, alpha=.85)
    ax.plot(*target, "*", color=ORANGE, ms=20); ax.legend(frameon=False, loc="lower right")
    ax.set_xlim(-.6, 2), ax.set_ylim(-.6, 2); ax.set_aspect("equal"); ax.axis("off"); ax.set_title("Inverse kinematics: hand position → joint angles\n(often TWO valid answers)")
    save(fig, "two-link-arm")


def frames_chain():
    fig, ax = canvas(10, 3.6, (0, 100), (0, 36))
    for x, t, c in ((10, "World", GRAY), (32, "Robot base", BLUE), (54, "Arm links\n(joints)", TEAL), (76, "Hand / tool", ORANGE), (92, "Object", GREEN)):
        box(ax, x, 18, 15 if x < 90 else 12, 10, t, c, bold=True)
    for a, b in ((17.8, 24.2), (39.8, 46.2), (61.8, 68.2), (83.8, 85.2)): arrow(ax, (a, 18), (b, 18), color=GRAY)
    label(ax, 50, 31, "Every part has its own coordinate frame; a pose is 'rotation + translation' between two frames", bold=True, fs=10.5)
    label(ax, 50, 5, "To find where the object is in the world, multiply the transforms along the chain  (ROS stores this as the TF tree)", fs=10, color=GRAY)
    save(fig, "frames-chain")


def kalman_fusion():
    x = np.linspace(-1, 9, 400)
    g = lambda m, s: np.exp(-(x - m) ** 2 / (2 * s * s)) / (s * np.sqrt(2 * np.pi))
    fig, ax = plt.subplots(figsize=(8, 3.8))
    p = g(3, 1.4); z = g(5.5, 1.0); m1, s1, m2, s2 = 3, 1.4, 5.5, 1.0
    w = s1 ** 2 / (s1 ** 2 + s2 ** 2); mf = m1 + w * (m2 - m1); sf = np.sqrt(1 / (1 / s1 ** 2 + 1 / s2 ** 2)); f = g(mf, sf)
    ax.fill_between(x, p, color=BLUE, alpha=.25); ax.plot(x, p, color=BLUE, lw=2.2, label="Prediction (from motion model)")
    ax.fill_between(x, z, color=ORANGE, alpha=.25); ax.plot(x, z, color=ORANGE, lw=2.2, label="Measurement (from sensor)")
    ax.fill_between(x, f, color=GREEN, alpha=.35); ax.plot(x, f, color=GREEN, lw=3, label="Fused estimate: narrower = more certain")
    ax.set_yticks([]); ax.set_xlabel("position (m)"); ax.legend(frameon=False, loc="upper left", fontsize=9); ax.set_xlim(-1, 11); ax.set_ylim(0, f.max() * 1.5); ax.set_title("Kalman filter: blend two uncertain guesses; trust the more certain one more")
    save(fig, "kalman-fusion")


def particle_filter():
    rng = np.random.default_rng(4)
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.4))
    truth = np.array([6.5, 3.2])
    P0 = rng.uniform(0, 10, (150, 2)); axs[0].scatter(*P0.T, s=8, color=GRAY, alpha=.7); axs[0].set_title("1. Start: spread guesses\neverywhere")
    d = np.linalg.norm(P0 - truth, axis=1); w = np.exp(-d ** 2 / 4); w /= w.sum()
    sc = axs[1].scatter(*P0.T, s=8 + 700 * w, c=w, cmap="Oranges"); axs[1].set_title("2. Score each guess\n(big = fits the sensor)")
    idx = rng.choice(150, 150, p=w); P2 = P0[idx] + rng.normal(0, .25, (150, 2))
    axs[2].scatter(*P2.T, s=8, color=GREEN); axs[2].set_title("3. Keep the good ones →\ncloud shrinks onto robot")
    for a in axs: a.plot(*truth, "r*", ms=15); a.set_xlim(0, 10); a.set_ylim(0, 10); a.set_xticks([]); a.set_yticks([]); a.set_aspect("equal")
    fig.suptitle("Particle filter: many guesses, keep the ones that match reality (red star = true pose)", fontweight="bold", y=1.12, fontsize=11)
    save(fig, "particle-filter")


def pose_graph():
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    t = np.linspace(0, 2 * np.pi * .98, 24)
    true = np.c_[3 * np.cos(t), 3 * np.sin(t)]
    rng = np.random.default_rng(1); drift = np.cumsum(rng.normal(0, .12, (24, 2)), 0) + np.c_[np.linspace(0, .9, 24), np.linspace(0, .6, 24)]
    est = true + drift
    for ax, pts, ti in ((axs[0], est, "Odometry only: small errors add up → drift,\nthe loop doesn't close"), (axs[1], true + rng.normal(0, .06, (24, 2)), "With loop closure: 'I've been here before!'\n→ whole path snaps back into shape")):
        ax.plot(pts[:, 0], pts[:, 1], "o-", color=BLUE, ms=5, lw=1.6)
        ax.plot(pts[0, 0], pts[0, 1], "s", color=GREEN, ms=10); ax.plot(pts[-1, 0], pts[-1, 1], "s", color=RED, ms=10)
        ax.set_title(ti); ax.set_aspect("equal"); ax.axis("off")
    axs[0].annotate("", est[-1], est[0], arrowprops=dict(arrowstyle="<->", color=RED, ls="--", lw=2)); axs[0].text(0, -.5, "gap = drift", color=RED, ha="center")
    axs[1].plot([true[0, 0], true[-1, 0]], [true[0, 1], true[-1, 1]], color=ORANGE, lw=3); axs[1].text(0, 0, "loop-closure\nconstraint", color=ORANGE, ha="center", fontweight="bold")
    fig.suptitle("SLAM = build the map and locate yourself at the same time (green = start, red = now)", fontweight="bold", y=1.12)
    save(fig, "slam-loop-closure")


def pinhole():
    fig, ax = canvas(10, 4, (0, 100), (0, 40))
    ax.plot([8, 8], [8, 32], color=INK, lw=4); label(ax, 8, 35, "Real object", fs=9.5)
    ax.add_patch(Circle((50, 20), .9, color=INK)); label(ax, 50, 25, "camera centre\n(pinhole)", fs=9.5)
    ax.plot([92, 92], [14, 26], color=BLUE, lw=5); label(ax, 92, 29, "Image sensor\n(upside-down)", fs=9.5, color=BLUE)
    for y0, y1 in ((8, 26), (32, 14)): ax.plot([8, 92], [y0, y1], color=ORANGE, lw=1.5, ls="--")
    arrow(ax, (8, 4), (50, 4), color=GRAY, style="<|-|>"); label(ax, 29, 1.6, "distance Z", fs=9.5)
    arrow(ax, (50, 4), (92, 4), color=GRAY, style="<|-|>"); label(ax, 71, 1.6, "focal length f", fs=9.5)
    label(ax, 50, 38, "Similar triangles: pixel position = f × (X / Z) — far things look small", bold=True, fs=11)
    save(fig, "pinhole-camera")


def occupancy_costmap():
    n = 16
    g = np.zeros((n, n)); g[3:6, 4:12] = 1; g[9:13, 9:11] = 1; g[8, 2:5] = 1
    from scipy_free import dist_transform
    d = dist_transform(g)
    infl = np.where(g == 1, 1.0, np.clip(1 - d / 3.5, 0, 1) * .85)
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.4))
    axs[0].imshow(np.where(g == 1, 0, 1), cmap="gray", vmin=0, vmax=1); axs[0].set_title("Occupancy grid\n(black = obstacle, white = free)")
    axs[1].imshow(infl, cmap="YlOrRd", vmin=0, vmax=1); axs[1].set_title("Costmap: obstacles inflated by robot size\n(red = keep out, yellow = be careful)")
    axs[1].plot(1.5, 14, "go", ms=10); axs[1].plot(14, 1.5, "b*", ms=14)
    for a in axs: a.set_xticks([]); a.set_yticks([])
    save(fig, "occupancy-costmap")


def pid_response():
    t = np.linspace(0, 10, 1500); dt = t[1] - t[0]

    def sim(kp, ki, kd):
        x = v = 0.0; i = 0.0; out = []
        for _ in t:
            e = 1 - x; i += e * dt; u = kp * e + ki * i - kd * v
            v += (u - 1.5 * v - 0.6) * dt; x += v * dt; out.append(x)   # constant 'gravity' pulls it down
        return np.array(out)
    fig, axs = plt.subplots(1, 4, figsize=(13, 3.1), sharey=True)
    for ax, (kp, ki, kd, t_) in zip(axs, ((2, 0, 0, "P only: stops short\n(steady error)"), (30, 0, 0, "Big P: fast but\noscillates"), (30, 0, 8, "P + D: smooth,\nstill a little short"), (30, 40, 8, "P + I + D:\nreaches the target"))):
        ax.plot(t, sim(kp, ki, kd), color=BLUE, lw=2.4); ax.axhline(1, color=GREEN, ls="--"); ax.set_title(t_, fontsize=9.5); ax.set_ylim(0, 1.7); ax.set_xticks([]); ax.set_yticks([])
    axs[0].set_ylabel("position")
    fig.suptitle("PID control: P = push toward target · D = brake to avoid overshoot · I = remove leftover error (green = target)", fontweight="bold", y=1.12, fontsize=11)
    save(fig, "pid-response")


def mpc_horizon():
    fig, ax = plt.subplots(figsize=(8.4, 3.8))
    t = np.arange(0, 12)
    ref = np.sin(t / 2.5) * 1.5
    ax.plot(t, ref, color=GRAY, ls="--", lw=2, label="desired path")
    ax.plot(t[:4], ref[:4] + .15, "o-", color=BLUE, lw=2.6, label="what the robot already did")
    ax.plot(t[3:8], ref[3:8] + np.array([.15, .25, .1, .05, 0]), "o--", color=ORANGE, lw=2.4, label="plan for next N steps (predicted)")
    ax.axvspan(3, 7, color="#fdeedd", alpha=.6); ax.text(5, 1.95, "prediction horizon", ha="center", color=ORANGE, fontweight="bold")
    ax.annotate("execute ONLY this first step,\nthen re-plan with fresh sensors", (3.3, ref[3] + .2), (.3, -1.9), arrowprops=dict(arrowstyle="->", color=GREEN), color=GREEN)
    ax.set_xlabel("time"); ax.set_yticks([]); ax.legend(frameon=False, loc="lower right", fontsize=9); ax.set_ylim(-2.3, 2.3); ax.set_title("Model Predictive Control: plan ahead, act once, repeat")
    save(fig, "mpc-horizon")


def rrt_tree():
    rng = np.random.default_rng(7)
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.4))
    obst = [(3.5, 0, 1.2, 6.2), (6.5, 3.8, 1.2, 6.2)]
    def free(p, q):
        for (x, y, w, h) in obst:
            for t in np.linspace(0, 1, 15):
                r = p + (q - p) * t
                if x <= r[0] <= x + w and y <= r[1] <= y + h: return False
        return True
    start, goal = np.array([1., 1.5]), np.array([9., 8.5])
    for ax, n, ti in ((axs[0], 60, "Early: tree explores"), (axs[1], 700, "Later: tree has found a path (red)")):
        nodes = [start]; par = [-1]
        for _ in range(n):
            q = goal if rng.random() < .06 else rng.uniform(0, 10, 2)
            i = int(np.argmin([np.linalg.norm(q - a) for a in nodes])); d = q - nodes[i]; nq = nodes[i] + d / max(np.linalg.norm(d), 1e-9) * min(.7, np.linalg.norm(d))
            if free(nodes[i], nq):
                nodes.append(nq); par.append(i)
        for k in range(1, len(nodes)): ax.plot(*zip(nodes[k], nodes[par[k]]), color="#8fb0e8", lw=1)
        for (x, y, w, h) in obst: ax.add_patch(Rectangle((x, y), w, h, fc="#374151"))
        ax.plot(*start, "go", ms=11); ax.plot(*goal, "*", color=ORANGE, ms=17)
        dists = [np.linalg.norm(a - goal) for a in nodes]; k = int(np.argmin(dists))
        if dists[k] < .8 and n > 100:
            path = []
            while k != -1: path.append(nodes[k]); k = par[k]
            P = np.array(path); ax.plot(P[:, 0], P[:, 1], color=RED, lw=3)
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([]); ax.set_title(ti)
    fig.suptitle("RRT: grow a random tree from the start until it reaches the goal  (green = start, star = goal)", fontweight="bold", y=1.03)
    save(fig, "rrt-tree")


def diff_drive():
    fig, ax = canvas(9, 4.4, (0, 100), (0, 44))
    ax.add_patch(Rectangle((14, 12), 36, 20, fc=LIGHT[BLUE], ec=BLUE, lw=2)); label(ax, 32, 22, "robot body", fs=10.5)
    ax.add_patch(Rectangle((22, 6), 14, 6, fc=INK)); ax.add_patch(Rectangle((22, 32), 14, 6, fc=INK))
    label(ax, 44, 9, "right wheel", ha="left", fs=9.5); label(ax, 44, 35, "left wheel", ha="left", fs=9.5)
    arrow(ax, (50, 22), (78, 22), color=GREEN, lw=3.2); label(ax, 64, 25.5, "forward speed  v", color=GREEN, bold=True)
    ax.annotate("", (86, 34), (86, 10), arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=2.5, connectionstyle="arc3,rad=-.5"))
    label(ax, 92, 22, "turn\nrate ω", color=ORANGE, bold=True, fs=10)
    label(ax, 50, 41, "Two wheels, two motors: the whole motion comes from their speed difference", bold=True, fs=11)
    label(ax, 50, 1.5, "v = average of the wheel speeds  ·  ω = (difference of wheel speeds) ÷ (distance between wheels)  ·  it cannot slide sideways", fs=9, color=GRAY)
    save(fig, "diff-drive")


def lipm_walking():
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.8), gridspec_kw={"width_ratios": [1.1, 1]})
    ax = axs[0]
    ax.plot([-2.6, 2.6], [0, 0], color=INK, lw=3)
    ax.plot([-.7, .6], [0, 2.0], color=BLUE, lw=5); ax.add_patch(Circle((.6, 2.0), .22, color=ORANGE)); ax.text(.2, 2.5, "centre of mass", color=ORANGE, ha="right")
    ax.add_patch(Rectangle((-1.2, -.08), 1.0, .16, fc=GREEN)); ax.text(-.7, -.5, "support foot", ha="center", color=GREEN)
    ax.annotate("", (1.4, 2.0), (.85, 2.0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.5)); ax.text(1.5, 1.45, "falling\nforward", color=RED)
    ax.set_xlim(-2.6, 3.2); ax.set_ylim(-1, 3); ax.axis("off"); ax.set_aspect("equal"); ax.set_title("Walking = controlled falling:\nan inverted pendulum")
    ax = axs[1]
    t = np.linspace(0, 4, 400); L, R = (np.sin(2 * np.pi * t / 1.0) > 0), (np.sin(2 * np.pi * t / 1.0) <= 0)
    for y, m, nm in ((1, L, "left foot"), (0, R, "right foot")):
        ax.fill_between(t, y, y + .6, where=m, color=GREEN if y else BLUE, step="mid"); ax.text(-.1, y + .3, nm, ha="right", va="center")
    ax.set_xlim(0, 4); ax.set_ylim(-.3, 2); ax.set_yticks([]); ax.set_xlabel("time"); ax.set_title("Gait chart: filled = foot on ground"); ax.spines["left"].set_visible(False)
    save(fig, "walking-pendulum-gait")


def friction_cone_grasp():
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    ax = axs[0]
    ax.add_patch(Rectangle((-3, -.3), 6, .3, fc="#374151")); ax.add_patch(Polygon([[0, 0], [-1.6, 2.2], [1.6, 2.2]], fc="#fde7d0", alpha=.8, ec=ORANGE))
    ax.annotate("", (0, 2.4), (0, 0), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.5)); ax.text(.1, 2.5, "push straight in (normal)", color=GREEN)
    ax.annotate("", (1.2, 1.7), (0, 0), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.5)); ax.text(1.3, 1.4, "OK: inside\nthe cone → grips", color=BLUE)
    ax.annotate("", (2.8, .9), (0, 0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.5)); ax.text(2.0, .35, "too sideways → slips!", color=RED)
    ax.set_xlim(-3, 4.5); ax.set_ylim(-.5, 3.2); ax.axis("off"); ax.set_aspect("equal"); ax.set_title("Friction cone: a finger only grips if its push\nstays inside the cone")
    ax = axs[1]
    ax.add_patch(Circle((0, 0), 1.1, fc="#e3edfc", ec=BLUE, lw=2))
    ax.annotate("", (-1.0, 0), (-2.2, 0), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=3)); ax.annotate("", (1.0, 0), (2.2, 0), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=3))
    ax.add_patch(Rectangle((-2.6, -.5), .4, 1, fc=INK)); ax.add_patch(Rectangle((2.2, -.5), .4, 1, fc=INK))
    ax.annotate("", (0, -1.6), (0, -.2), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.5)); ax.text(.2, -1.7, "gravity", color=RED)
    ax.text(0, 1.7, "two opposite fingertips squeeze;\nfriction holds the object up\n= 'force closure'", ha="center", color=INK)
    ax.set_xlim(-3, 3); ax.set_ylim(-2.2, 2.6); ax.axis("off"); ax.set_aspect("equal"); ax.set_title("Antipodal (pinch) grasp")
    save(fig, "grasp-friction")


def control_hierarchy():
    fig, ax = canvas(10, 5, (0, 100), (0, 52))
    rows = [("Vision-language model", "1–10 Hz", PURPLE), ("Task / motion planner", "1–10 Hz", BLUE), ("Policy / MPC / whole-body control", "20–500 Hz", TEAL),
            ("Joint torque / impedance loop", "1 kHz", ORANGE), ("Motor current (FOC) loop", "10–40 kHz", GREEN)]
    for i, (t, hz, c) in enumerate(rows):
        w = 96 - i * 10
        box(ax, 42, 44 - i * 9.5, w * .62, 7, t, c, fs=10); label(ax, 42 + w * .31 + 4, 44 - i * 9.5, hz, ha="left", fs=10.5, bold=True, color=c)
    arrow(ax, (92, 46), (92, 6), color="#9ca3af", text="", style="-|>")
    label(ax, 94.5, 26, "faster, lower-level", rotation=90, fs=9.5, color=GRAY)
    label(ax, 40, 50, "A robot is many control loops nested, each running at its own speed", bold=True, fs=11)
    save(fig, "control-hierarchy")


def ros2_graph():
    fig, ax = canvas(11, 4.6, (0, 100), (0, 46))
    box(ax, 12, 36, 18, 8, "camera_node", GREEN); box(ax, 42, 36, 18, 8, "detector_node", BLUE); box(ax, 72, 36, 18, 8, "planner_node", BLUE); box(ax, 90, 36, 14, 8, "arm_driver", ORANGE)
    arrow(ax, (21.2, 36), (32.8, 36), text="/image", color=GREEN, dy=1.5)
    arrow(ax, (51.2, 36), (62.8, 36), text="/objects", color=BLUE, dy=1.5)
    arrow(ax, (81.2, 36), (82.8, 36), color=ORANGE)
    box(ax, 72, 14, 20, 8, "perception_srv", PURPLE); arrow(ax, (72, 19.2), (72, 31.8), color=PURPLE, style="<|-|>"); label(ax, 80, 25.5, "service:\nask → reply", fs=9, color=PURPLE)
    box(ax, 90, 14, 14, 8, "pick_server", RED); arrow(ax, (90, 19.2), (90, 31.8), color=RED, style="<|-|>"); label(ax, 96, 25.5, "action:\ngoal +\nfeedback", fs=8, color=RED, ha="left")
    label(ax, 25, 18, "Topic = a radio channel: anyone can talk/listen, no reply\nService = a phone call: ask a question, get one answer\nAction = ordering a pizza: confirm, progress updates, delivery", fs=9.5, ha="center", color=INK, linespacing=1.6)
    label(ax, 50, 44, "ROS 2: small programs (nodes) talking over named channels", bold=True, fs=12)
    save(fig, "ros2-graph")


def sensors_overview():
    fig, ax = canvas(11, 4.2, (0, 100), (0, 42))
    items = [("Camera", "sees colour/shape\ncheap, rich;\nno direct depth", BLUE), ("LiDAR", "laser distance map\naccurate geometry;\ncostly", GREEN), ("IMU", "tilt + rotation + shake\nfast but drifts", ORANGE),
             ("Encoders", "joint / wheel angle\nprecise, local", PURPLE), ("Force/torque", "feels push & pull\nkey for contact", RED), ("Tactile", "fingertip touch\nslip, shape", TEAL)]
    for i, (n, d, c) in enumerate(items):
        x = 9 + i * 16.5
        box(ax, x, 28, 14.5, 7, n, c, bold=True, fs=10.5); label(ax, x, 13, d, fs=8.7, color=INK, linespacing=1.4)
    label(ax, 50, 40, "Robot senses: fuse several imperfect sensors for one reliable picture", bold=True, fs=11.5)
    save(fig, "sensors-overview")


def run():
    for f in (two_link_arm, frames_chain, kalman_fusion, particle_filter, pose_graph, pinhole, occupancy_costmap, pid_response, mpc_horizon, rrt_tree,
              diff_drive, lipm_walking, friction_cone_grasp, control_hierarchy, ros2_graph, sensors_overview):
        f()


if __name__ == "__main__":
    run()
