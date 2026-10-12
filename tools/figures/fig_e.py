"""Figures for the 'Build It Yourself' section."""
from lib import *


def build_roadmap():
    fig, ax = canvas(12, 5, (0, 120), (0, 50))
    box(ax, 20, 25, 30, 16, "1. BUILD AN AI MODEL\nlearn the full loop on a\ntiny GPT, then fine-tune\na real LLM", BLUE, bold=True, fs=9.5)
    box(ax, 60, 25, 30, 16, "2. BUILD A VLM\nadd eyes: vision encoder +\nprojector + LLM, in 2 stages", PURPLE, bold=True, fs=9.5)
    box(ax, 100, 25, 30, 16, "3. BUILD A VLA\nadd hands: VLM + action head,\ntrained on robot demos", ORANGE, bold=True, fs=9.5)
    arrow(ax, (35.6, 25), (44.4, 25), color=GRAY, lw=2.5); arrow(ax, (75.6, 25), (84.4, 25), color=GRAY, lw=2.5)
    box(ax, 60, 6, 100, 7, "Shared skills: data pipelines · training loops · evaluation · debugging · deployment", GRAY, fs=10)
    for x in (20, 60, 100): arrow(ax, (x, 9.8), (x, 16.4), color="#9ca3af", style="<|-|>")
    label(ax, 60, 46, "The learning path: each model reuses the previous one", bold=True, fs=12)
    save(fig, "build-roadmap")


def vlm_stages():
    fig, ax = canvas(12, 5.2, (0, 120), (0, 52))
    label(ax, 60, 49, "Two-stage VLM training: what is frozen and what is learning", bold=True, fs=12)
    heads = [("Vision encoder", 28), ("Connector (MLP)", 52), ("Language model", 76)]
    for n, x in heads: label(ax, x, 42, n, bold=True, fs=10)
    rows = [("Stage 1\nAlign", 30, ("frozen", "TRAIN", "frozen"), "captions: teach the connector\nto translate image → LLM tokens"),
            ("Stage 2\nInstruct", 12, ("frozen\n(or tiny lr)", "TRAIN", "TRAIN"), "visual Q&A, chat, OCR, reasoning:\nteach it to follow instructions")]
    for name, y, states, note in rows:
        label(ax, 8, y, name, bold=True, fs=10)
        for (n, x), s in zip(heads, states):
            box(ax, x, y, 20, 10, s, ORANGE if s == "TRAIN" else GRAY, bold=(s == "TRAIN"), fs=9.5)
        label(ax, 118, y, note, fs=8.5, ha="right", color=INK)
    save(fig, "vlm-stages")


def vlm_token_flow():
    fig, ax = canvas(12, 4.6, (0, 120), (0, 46))
    box(ax, 12, 34, 20, 8, "Image\n(384×384)", GRAY); box(ax, 40, 34, 22, 8, "Vision encoder\n(SigLIP / CLIP)", BLUE)
    box(ax, 70, 34, 20, 8, "Connector\n(MLP)", ORANGE); arrow(ax, (22.4, 34), (28.4, 34)); arrow(ax, (51.4, 34), (59.4, 34))
    label(ax, 40, 41, "729 patch vectors", fs=9, color=BLUE); label(ax, 70, 41, "729 'image tokens'", fs=9, color=ORANGE)
    cells = [("<image>", ORANGE)] * 4 + [("USER: what is on the table?", GRAY), ("ASSISTANT:", GRAY), ("a red mug", GREEN)]
    x = 8
    for t, c in cells:
        w = 6.5 if t == "<image>" else (30 if "USER" in t else (16 if "ASSIST" in t else 15)); box(ax, x + w / 2, 11, w - .8, 7, t, c, fs=8.2); x += w + 1
    arrow(ax, (70, 29.5), (30, 17), color=ORANGE, rad=.2)
    label(ax, 60, 2.5, "The LLM sees one long sequence: image tokens + text tokens. Loss is computed ONLY on the answer (green).", fs=9.5, bold=True)
    box(ax, 104, 34, 20, 8, "LLM\n(Qwen / Llama)", PURPLE); arrow(ax, (80.4, 34), (93.6, 34), color=GRAY)
    save(fig, "vlm-token-flow")


def vla_flywheel():
    fig, ax = canvas(10.5, 5, (0, 100), (0, 50))
    pts = [(50, 42, "1. Collect demos\n(teleoperation)", ORANGE), (84, 26, "2. Train policy\n(ACT / SmolVLA / π0)", BLUE), (68, 7, "3. Evaluate\n(sim, then real)", GREEN), (32, 7, "4. Deploy + log\nfailures", PURPLE), (16, 26, "5. Analyse failures\n→ what data is missing?", RED)]
    for x, y, t, c in pts: box(ax, x, y, 26, 10, t, c, fs=9.5, bold=True)
    for (a, b) in zip(pts, pts[1:] + pts[:1]):
        dx, dy = b[0] - a[0], b[1] - a[1]; n = (dx * dx + dy * dy) ** .5
        arrow(ax, (a[0] + dx / n * 14, a[1] + dy / n * 8), (b[0] - dx / n * 14, b[1] - dy / n * 8), color=GRAY, lw=2.2, rad=.15)
    label(ax, 50, 25, "THE DATA\nFLYWHEEL", fs=12, bold=True, color=GRAY)
    save(fig, "vla-flywheel")


def async_chunks():
    fig, ax = plt.subplots(figsize=(10, 3.6))
    for i in range(4):
        ax.barh(1, 5, left=i * 5, color=ORANGE if i % 2 == 0 else "#f6b26b", ec="white"); ax.text(i * 5 + 2.5, 1, f"execute chunk {i + 1}", ha="center", va="center", fontsize=9)
    for i in range(4):
        ax.barh(0, 3.2, left=i * 5 + 1, color=BLUE, ec="white"); ax.text(i * 5 + 2.6, 0, "model infers\nchunk %d" % (i + 2), ha="center", va="center", fontsize=8, color="white")
    ax.set_yticks([0, 1]); ax.set_yticklabels(["GPU (thinking)", "Robot (moving)"]); ax.set_xlabel("time →"); ax.set_xlim(0, 20); ax.set_ylim(-.6, 1.6)
    ax.set_title("Asynchronous inference: the robot keeps moving on the current chunk while the next one is computed")
    save(fig, "async-chunks")


def vla_design():
    fig, ax = canvas(12, 5.8, (0, 120), (0, 58))
    box(ax, 14, 44, 22, 8, "Camera images\n(wrist + front)", GRAY, fs=9); box(ax, 14, 31, 22, 8, "Instruction\ntext", GRAY, fs=9); box(ax, 14, 18, 22, 8, "Joint state\n(proprioception)", GRAY, fs=9)
    box(ax, 50, 44, 22, 8, "Vision encoder\n+ connector", BLUE, fs=9); box(ax, 50, 31, 22, 8, "Tokenizer\n+ embeddings", BLUE, fs=9); box(ax, 50, 18, 22, 8, "State → token", BLUE, fs=9)
    box(ax, 82, 31, 20, 30, "VLM backbone\n(pretrained)\n\nreads image + text\n+ state tokens", PURPLE, bold=True, fs=9.5)
    box(ax, 107, 31, 20, 30, "ACTION EXPERT\nsmall transformer\n+ flow matching\n\nattends to the\nVLM's features", ORANGE, bold=True, fs=9)
    for y in (44, 31, 18): arrow(ax, (25.4, y), (38.6, y)); arrow(ax, (61.4, y), (71.6, 31 + (y - 31) * .6))
    arrow(ax, (92.4, 31), (96.6, 31))
    box(ax, 107, 8, 24, 7, "action chunk (50 steps)", GREEN, fs=9); arrow(ax, (107, 15.6), (107, 11.8), color=GREEN)
    box(ax, 107, 49, 22, 6, "noisy actions + time t", GRAY, fs=8.5); arrow(ax, (107, 46), (107, 46.3), color=GRAY)
    label(ax, 55, 56, "A pi0-style VLA: a VLM understands, a small action expert generates smooth motion", bold=True, fs=11)
    save(fig, "vla-design")


def run():
    for f in (build_roadmap, vlm_stages, vlm_token_flow, vla_flywheel, async_chunks, vla_design): f()


if __name__ == "__main__":
    run()
