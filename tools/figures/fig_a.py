"""Foundations, ML and DL figures."""
from lib import *
from matplotlib.patches import Ellipse


def matrix_transform():
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.8))
    A = {"Original grid": np.eye(2),
         "Rotate 30°": np.array([[np.cos(.52), -np.sin(.52)], [np.sin(.52), np.cos(.52)]]),
         "Stretch x2, squash y": np.array([[2, .8], [0, .6]])}
    for ax, (t, M) in zip(axs, A.items()):
        for k in np.linspace(-2, 2, 9):
            for P, Q in (((k, -2), (k, 2)), ((-2, k), (2, k))):
                a, b = M @ np.array(P), M @ np.array(Q)
                ax.plot([a[0], b[0]], [a[1], b[1]], color="#c7d2e6", lw=.9)
        e1, e2 = M @ [1, 0], M @ [0, 1]
        ax.annotate("", e1, (0, 0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.4))
        ax.annotate("", e2, (0, 0), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.4))
        sq = np.array([[0, 0], [1, 0], [1, 1], [0, 1]]) @ M.T
        ax.add_patch(Polygon(sq, fc=ORANGE, alpha=.35, ec=ORANGE))
        ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.set_aspect("equal"); ax.set_title(t)
        ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("A matrix is a machine that moves every point in space", fontweight="bold", y=1.03)
    save(fig, "matrix-transform")


def gaussian_cov():
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.6))
    rng = np.random.default_rng(1)
    covs = [([[1, 0], [0, 1]], "No correlation"), ([[1, .8], [.8, 1]], "Positive correlation"),
            ([[1.8, -.3], [-.3, .35]], "Different spreads")]
    for ax, (C, t) in zip(axs, covs):
        X = rng.multivariate_normal([0, 0], C, 300)
        ax.scatter(X[:, 0], X[:, 1], s=7, color=BLUE, alpha=.5)
        w, v = np.linalg.eigh(np.array(C))
        ang = np.degrees(np.arctan2(v[1, 1], v[0, 1]))
        for k, a in ((1, .5), (2, .25)):
            ax.add_patch(Ellipse((0, 0), 2 * k * np.sqrt(w[1]), 2 * k * np.sqrt(w[0]), angle=ang,
                                 fc="none", ec=ORANGE, lw=2, alpha=1 if k == 1 else .6))
        ax.set_xlim(-4.5, 4.5); ax.set_ylim(-4.5, 4.5); ax.set_aspect("equal"); ax.set_title(t)
        ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("Covariance = the shape of the uncertainty cloud (ellipses = 1σ, 2σ)", fontweight="bold", y=1.03)
    save(fig, "gaussian-covariance")


def gradient_descent():
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.7))
    X, Y = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-3, 3, 200))
    f = lambda x, y: .5 * (x ** 2 + 6 * y ** 2)
    g = lambda p: np.array([p[0], 6 * p[1]])
    for ax, lr, t in zip(axs, (.02, .15, .36), ("Learning rate too small", "Just right", "Too large: bounces / diverges")):
        ax.contour(X, Y, f(X, Y), levels=14, colors="#b8c4dc", linewidths=.9)
        p = np.array([-2.6, 2.0]); path = [p.copy()]
        for _ in range(25):
            p = p - lr * g(p); path.append(p.copy())
            if np.abs(p).max() > 5: break
        P = np.array(path)
        ax.plot(P[:, 0], P[:, 1], "o-", color=RED, ms=3, lw=1.4)
        ax.plot(0, 0, "*", color=GREEN, ms=15)
        ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_title(t); ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("Gradient descent = walking downhill; the learning rate is your step size", fontweight="bold", y=1.03)
    save(fig, "gradient-descent")


def astar_grid():
    n = 15
    obst = set([(7, y) for y in range(2, 13)] + [(x, 7) for x in range(3, 8)] + [(10, y) for y in range(0, 9)])
    import heapq
    s, g = (2, 3), (13, 11)

    def run(use_h):
        h = (lambda a: abs(a[0] - g[0]) + abs(a[1] - g[1])) if use_h else (lambda a: 0)
        pq = [(h(s), 0, s)]; cost = {s: 0}; prev = {}; seen = []
        while pq:
            _, c, u = heapq.heappop(pq)
            if c > cost[u]: continue
            seen.append(u)
            if u == g: break
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                v = (u[0] + d[0], u[1] + d[1])
                if 0 <= v[0] < n and 0 <= v[1] < n and v not in obst and c + 1 < cost.get(v, 1e9):
                    cost[v] = c + 1; prev[v] = u; heapq.heappush(pq, (c + 1 + h(v), c + 1, v))
        path = [g]
        while path[-1] in prev: path.append(prev[path[-1]])
        return seen, path
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.6))
    for ax, use_h, t in zip(axs, (False, True), ("Dijkstra: explores in all directions", "A*: the heuristic aims at the goal")):
        seen, path = run(use_h)
        for (x, y) in obst: ax.add_patch(Rectangle((x, y), 1, 1, fc="#374151"))
        for (x, y) in seen: ax.add_patch(Rectangle((x, y), 1, 1, fc="#cfe0fb"))
        P = np.array(path) + .5
        ax.plot(P[:, 0], P[:, 1], color=RED, lw=3)
        ax.add_patch(Rectangle(s, 1, 1, fc=GREEN)); ax.add_patch(Rectangle(g, 1, 1, fc=ORANGE))
        ax.set_xlim(0, n); ax.set_ylim(0, n); ax.set_aspect("equal"); ax.set_title(f"{t}\n{len(seen)} cells visited")
        ax.set_xticks([]); ax.set_yticks([]); ax.axis("on")
    fig.suptitle("Blue = cells the planner looked at · red = final path · green = start · orange = goal", y=0.02, fontsize=10)
    save(fig, "astar-vs-dijkstra")


def bias_variance():
    rng = np.random.default_rng(3)
    x = np.sort(rng.uniform(0, 1, 14)); y = np.sin(2 * np.pi * x) + rng.normal(0, .25, x.size)
    xs = np.linspace(0, 1, 200)
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.5))
    for ax, deg, t, c in zip(axs, (1, 3, 12), ("Underfit (too simple)", "Good fit", "Overfit (memorises noise)"), (RED, GREEN, RED)):
        co = np.polyfit(x, y, deg)
        ax.plot(xs, np.sin(2 * np.pi * xs), "--", color=GRAY, label="truth")
        ax.plot(xs, np.clip(np.polyval(co, xs), -2, 2), color=c, lw=2.4, label="model")
        ax.scatter(x, y, color=BLUE, zorder=5, s=28)
        ax.set_ylim(-2, 2); ax.set_title(t); ax.set_xticks([]); ax.set_yticks([])
    axs[0].legend(loc="lower left", frameon=False)
    fig.suptitle("Same data, three models: the bias–variance trade-off", fontweight="bold", y=1.03)
    save(fig, "bias-variance")


def train_val_curve():
    ep = np.arange(1, 60)
    tr = 1.0 * np.exp(-ep / 12) + .05
    va = .85 * np.exp(-ep / 10) + .22 + .0075 * np.maximum(ep - 20, 0) ** 1.2
    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.plot(ep, tr, color=BLUE, lw=2.4, label="training loss")
    ax.plot(ep, va, color=ORANGE, lw=2.4, label="validation loss")
    k = va.argmin(); ax.axvline(ep[k], color=GREEN, ls="--"); ax.text(ep[k] + 1, .95, "stop here\n(early stopping)", color=GREEN, fontsize=10)
    ax.annotate("overfitting zone: train ↓ but val ↑", (52, va[52]), (27, .5), arrowprops=dict(arrowstyle="->", color=RED), color=RED)
    ax.set_xlabel("training time (epochs)"); ax.set_ylabel("loss"); ax.legend(frameon=False)
    ax.set_title("Watch the validation curve, not the training one")
    save(fig, "train-val-curves")


def decision_boundaries():
    rng = np.random.default_rng(0)
    n = 90
    X = np.vstack([rng.normal([-1, -.6], .8, (n, 2)), rng.normal([1, .8], .8, (n, 2))]); y = np.r_[np.zeros(n), np.ones(n)]
    gx, gy = np.meshgrid(np.linspace(-3.5, 3.5, 250), np.linspace(-3, 3.2, 250)); G = np.c_[gx.ravel(), gy.ravel()]

    def lin(G):
        m0, m1 = X[y == 0].mean(0), X[y == 1].mean(0); w = m1 - m0; b = -w @ (m0 + m1) / 2; return (G @ w + b > 0)

    def knn(G, k=1):
        d = ((G[:, None, :] - X[None]) ** 2).sum(-1); idx = d.argsort(1)[:, :k]; return y[idx].mean(1) > .5

    def tree(G):  # crude axis-aligned stump-ish ensemble
        return ((G[:, 0] > -.2) & (G[:, 1] > -1.1)) | ((G[:, 0] > 1.2))
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.6))
    for ax, f, t in zip(axs, (lin, lambda G: knn(G, 1), tree), ("Linear model: one straight cut", "1-nearest-neighbour: wiggly", "Decision tree: axis-aligned boxes")):
        Z = f(G).reshape(gx.shape)
        ax.contourf(gx, gy, Z, levels=[-.5, .5, 1.5], colors=["#fde7d0", "#d5e5fb"])
        ax.scatter(X[:, 0], X[:, 1], c=np.where(y == 1, BLUE, ORANGE), s=14, ec="white", lw=.4)
        ax.set_title(t); ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("Different algorithms draw different borders between classes", fontweight="bold", y=1.03)
    save(fig, "decision-boundaries")


def kmeans_pca():
    rng = np.random.default_rng(5)
    C = np.array([[-2, -1], [2, 1.5], [-.5, 2.5]])
    X = np.vstack([rng.normal(c, .6, (60, 2)) for c in C])
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.6))
    axs[0].scatter(X[:, 0], X[:, 1], s=12, color=GRAY); axs[0].set_title("Unlabelled data")
    cent = X[[0, 70, 150]].copy()
    for _ in range(10):
        lab = ((X[:, None] - cent[None]) ** 2).sum(-1).argmin(1)
        cent = np.array([X[lab == k].mean(0) for k in range(3)])
    cols = [BLUE, ORANGE, GREEN]
    for k in range(3): axs[1].scatter(*X[lab == k].T, s=12, color=cols[k])
    axs[1].scatter(*cent.T, marker="X", s=140, color="black"); axs[1].set_title("k-means: 3 groups\n(X = group centre)")
    Z = rng.normal(0, 1, (200, 3)) * [3, 1.2, .25]; R = np.linalg.qr(rng.normal(size=(3, 3)))[0]; Z = Z @ R
    Zc = Z - Z.mean(0); U, S, Vt = np.linalg.svd(Zc, full_matrices=False); P = Zc @ Vt[:2].T
    axs[2].scatter(P[:, 0], P[:, 1], s=12, color=PURPLE); axs[2].set_title(f"PCA: 3-D squashed to 2-D\n(keeps {100 * (S[:2] ** 2).sum() / (S ** 2).sum():.0f}% of the variation)")
    for a in axs: a.set_xticks([]); a.set_yticks([])
    save(fig, "kmeans-pca")


def roc_confusion():
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    t = np.linspace(0, 1, 100)
    for k, c, lab in ((1, GRAY, "random guess"), (4, ORANGE, "OK model"), (12, GREEN, "great model")):
        axs[0].plot(t, t ** (1 / k) if k > 1 else t, color=c, lw=2.4, label=lab, ls="--" if k == 1 else "-")
    axs[0].set_xlabel("False positive rate (false alarms)"); axs[0].set_ylabel("True positive rate (catches)")
    axs[0].legend(frameon=False, loc="lower right"); axs[0].set_title("ROC curve: higher-left is better")
    ax = axs[1]; ax.axis("off")
    cells = [("True Positive\n(caught it)", GREEN, 0, 1), ("False Positive\n(false alarm)", ORANGE, 1, 1),
             ("False Negative\n(missed it!)", RED, 0, 0), ("True Negative\n(correctly ignored)", GREEN, 1, 0)]
    for tx, c, i, j in cells:
        ax.add_patch(Rectangle((i * 1.1, j * 1.1), 1, 1, fc=LIGHT[c], ec=c, lw=2)); ax.text(i * 1.1 + .5, j * 1.1 + .5, tx, ha="center", va="center", fontsize=8.5)
    ax.text(.5, 2.35, "Actually YES", ha="center", fontweight="bold"); ax.text(1.6, 2.35, "Actually NO", ha="center", fontweight="bold")
    ax.text(-.2, 1.6, "Predicted\nYES", ha="right", va="center", fontweight="bold"); ax.text(-.2, .5, "Predicted\nNO", ha="right", va="center", fontweight="bold")
    ax.set_xlim(-1.2, 2.4); ax.set_ylim(-.2, 2.6); ax.set_title("Confusion matrix")
    save(fig, "roc-confusion")


def activations():
    x = np.linspace(-4, 4, 400)
    sig = 1 / (1 + np.exp(-x)); relu = np.maximum(0, x); gelu = x * .5 * (1 + np.tanh(.79788 * (x + .044715 * x ** 3))); silu = x * sig
    fig, axs = plt.subplots(1, 4, figsize=(12, 3))
    for ax, (n, y, c, note) in zip(axs, (("Sigmoid", sig, BLUE, "squashes to 0–1\n(old school)"), ("ReLU", relu, ORANGE, "off below 0, linear above\n(fast, default)"),
                                         ("GELU", gelu, GREEN, "smooth ReLU\n(transformers)"), ("SiLU / Swish", silu, PURPLE, "smooth, used in\nmodern LLMs"))):
        ax.plot(x, y, color=c, lw=2.6); ax.axhline(0, color="#d1d5db", lw=.8); ax.axvline(0, color="#d1d5db", lw=.8)
        ax.set_title(n); ax.set_xlabel(note, fontsize=9); ax.set_ylim(-1, 4); ax.set_xticks([]); ax.set_yticks([])
    save(fig, "activations")


def backprop_graph():
    fig, ax = canvas(11, 4.2, (0, 100), (0, 40))
    nodes = [(8, 20, "input\nx", GRAY), (28, 20, "layer 1\nz = Wx+b", BLUE), (48, 20, "ReLU", ORANGE), (68, 20, "layer 2\nŷ", BLUE), (90, 20, "loss L\n(ŷ − y)²", RED)]
    for x, y, t, c in nodes: box(ax, x, y, 14, 9, t, c)
    for a, b in zip(nodes[:-1], nodes[1:]): arrow(ax, (a[0] + 7.3, 24), (b[0] - 7.3, 24), color=BLUE, text=None)
    for a, b in zip(nodes[:-1], nodes[1:]): arrow(ax, (b[0] - 7.3, 16), (a[0] + 7.3, 16), color=RED, rad=0)
    label(ax, 50, 35, "FORWARD pass → compute the prediction and the error", color=BLUE, bold=True)
    label(ax, 50, 5, "← BACKWARD pass: send 'how much did you contribute to the error?' back, layer by layer (chain rule)", color=RED, bold=True, fs=10)
    save(fig, "backprop-flow")


def attention_heatmap():
    words = ["The", "robot", "picked", "up", "the", "red", "cup"]
    rng = np.random.default_rng(2)
    A = rng.random((7, 7)) * .25
    for i, j, v in ((6, 5, .9), (5, 6, .5), (2, 1, .8), (1, 2, .5), (6, 4, .5), (3, 2, .7), (6, 1, .35), (2, 6, .45)): A[i, j] += v
    A = A / A.sum(1, keepdims=True)
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    im = ax.imshow(A, cmap="Blues"); ax.set_xticks(range(7)); ax.set_xticklabels(words, rotation=40, ha="right"); ax.set_yticks(range(7)); ax.set_yticklabels(words)
    ax.set_xlabel("word being looked AT"); ax.set_ylabel("word doing the looking"); ax.spines[:].set_visible(False)
    ax.set_title("Attention: every word decides how much to\nlisten to every other word (dark = strong)")
    save(fig, "attention-heatmap")


def conv_filter():
    fig, axs = plt.subplots(1, 3, figsize=(10, 3.4))
    img = np.zeros((10, 10)); img[:, 5:] = 1
    k = np.array([[-1, 0, 1]] * 3)
    out = np.zeros((8, 8))
    for i in range(8):
        for j in range(8): out[i, j] = (img[i:i + 3, j:j + 3] * k).sum()
    axs[0].imshow(img, cmap="gray"); axs[0].set_title("Input image\n(dark | bright edge)")
    axs[1].imshow(k, cmap="RdBu_r"); axs[1].set_title("3×3 filter\n(edge detector)")
    for (i, j), v in np.ndenumerate(k): axs[1].text(j, i, int(v), ha="center", va="center", fontweight="bold")
    axs[2].imshow(out, cmap="viridis"); axs[2].set_title("Output feature map\n(lights up on the edge)")
    for a in axs: a.set_xticks([]); a.set_yticks([])
    fig.suptitle("A convolution slides a small filter over the image and asks 'is my pattern here?'", fontweight="bold", y=1.04)
    save(fig, "convolution")


def diffusion_process():
    rng = np.random.default_rng(1)
    t = np.linspace(0, 1, 80); clean = np.sin(2 * np.pi * t) * .8
    fig, axs = plt.subplots(1, 5, figsize=(13, 2.7))
    for ax, s in zip(axs, (0, .15, .4, .75, 1.0)):
        y = np.sqrt(1 - s) * clean + np.sqrt(s) * rng.normal(0, .6, t.size)
        ax.plot(t, y, color=BLUE if s < 1 else RED, lw=1.6); ax.set_ylim(-2, 2); ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(["clean\n(e.g. a robot trajectory)", "a bit noisy", "noisier", "very noisy", "pure noise"][[0, .15, .4, .75, 1.0].index(s)], fontsize=9.5)
    fig.text(.5, -.1, "Training: learn to UNDO one small bit of noise.   Generating: start from noise, undo step by step → a clean trajectory ←", ha="center", color=GREEN, fontweight="bold", fontsize=11)
    fig.text(.5, 1.1, "Diffusion models: destroy data with noise, then learn to reverse it", ha="center", fontweight="bold", fontsize=13)
    save(fig, "diffusion-process")


def transformer_block():
    fig, ax = canvas(7, 7.2, (0, 60), (0, 78))
    box(ax, 30, 6, 30, 7, "Token embeddings + position info\n(words → vectors)", GRAY)
    box(ax, 30, 24, 30, 9, "Self-attention\n'which other tokens matter to me?'", BLUE)
    box(ax, 30, 42, 30, 9, "Feed-forward network\n'think about what I gathered'", ORANGE)
    box(ax, 30, 60, 30, 7, "Repeat this block N times (12–100+)", PURPLE)
    box(ax, 30, 73, 30, 6, "Output: next-word probabilities", GREEN)
    for y0, y1 in ((9.6, 19.4), (28.6, 37.4), (46.6, 56.4), (63.6, 70)): arrow(ax, (30, y0), (30, y1), color=GRAY)
    for y in (24, 42): arrow(ax, (47, y - 1), (47, y + 4.5), color=GREEN, rad=-.0); label(ax, 54, y + 2, "+ skip\nconnection", fs=8.5, color=GREEN)
    save(fig, "transformer-block")


def lr_curves():
    ep = np.arange(0, 60)
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.plot(ep, 2 * np.exp(-ep / 40) + .3, color=BLUE, lw=2.3, label="lr too small: crawls")
    ax.plot(ep, 2 * np.exp(-ep / 9) + .3, color=GREEN, lw=2.6, label="lr good: steady drop")
    rng = np.random.default_rng(0); ax.plot(ep, 1.5 + .5 * rng.standard_normal(60).cumsum() * .15 + np.sin(ep / 2) * .5, color=RED, lw=2.3, label="lr too big: unstable")
    ax.set_xlabel("steps"); ax.set_ylabel("loss"); ax.set_ylim(0, 3); ax.legend(frameon=False); ax.set_title("What a healthy loss curve looks like")
    save(fig, "lr-curves")


def run():
    for f in (matrix_transform, gaussian_cov, gradient_descent, astar_grid, bias_variance, train_val_curve, decision_boundaries,
              kmeans_pca, roc_confusion, activations, backprop_graph, attention_heatmap, conv_filter, diffusion_process, transformer_block, lr_curves):
        f()


if __name__ == "__main__":
    run()
