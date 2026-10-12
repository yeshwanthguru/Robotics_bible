"""A complete, tiny Vision-Language Model (LLaVA-style) trained from scratch on a synthetic 'shapes' world.

Pipeline shown end to end:
  data generation -> vision encoder (ViT-lite) -> projector -> language model (decoder)
  -> Stage 1: alignment on captions -> Stage 2: instruction tuning on questions -> evaluation.

Run:  python examples/02_tiny_vlm.py            (CPU is fine, a few minutes)
"""
import random, time
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F

COLORS = ["red", "green", "blue", "yellow"]
SHAPES = ["circle", "square", "triangle"]
RGB = {"red": (1, 0, 0), "green": (0, .8, 0), "blue": (0, 0, 1), "yellow": (1, 1, 0)}
SIDE = ["left", "right"]
VOCAB = ["<pad>", "<bos>", "<eos>", "<img>", "what", "color", "shape", "is", "it", "where", "a", "the", "?", "."] + COLORS + SHAPES + SIDE
STOI = {w: i for i, w in enumerate(VOCAB)}
IMG = 32


# ---------- 1. Synthetic data: an image with one shape + captions + questions ----------
def render(color, shape, side):
    img = np.zeros((IMG, IMG, 3), np.float32)
    cx = random.randint(5, 10) if side == "left" else random.randint(21, 26)
    cy = random.randint(8, 24); r = random.randint(4, 6)
    yy, xx = np.mgrid[:IMG, :IMG]
    if shape == "circle": m = (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r
    elif shape == "square": m = (abs(xx - cx) <= r) & (abs(yy - cy) <= r)
    else: m = (yy >= cy - r) & (yy <= cy + r) & (abs(xx - cx) <= (yy - (cy - r)) / 2)
    img[m] = RGB[color]
    return img


def make_sample(kind):
    c, s, side = random.choice(COLORS), random.choice(SHAPES), random.choice(SIDE)
    img = render(c, s, side)
    if kind == "caption":   q, a = "what is it ?", f"a {c} {s} ."                       # stage-1 target
    else:
        q, a = random.choice([("what color is it ?", c), ("what shape is it ?", s), ("where is it ?", side)])  # stage-2
    return img, q.split(), a.split(), (c, s, side)


def batch(kind, n, device="cpu"):
    imgs, ids, labels = [], [], []
    for _ in range(n):
        img, q, a, _ = make_sample(kind)
        seq = [STOI["<img>"]] + [STOI[w] for w in q] + [STOI["<bos>"]] + [STOI[w] for w in a] + [STOI["<eos>"]]
        lab = [-100] * (len(q) + 2) + [STOI[w] for w in a] + [STOI["<eos>"]]          # loss ONLY on the answer tokens
        imgs.append(img); ids.append(seq); labels.append(lab)
    L = max(map(len, ids))
    pad = lambda s, v: s + [v] * (L - len(s))
    ids = torch.tensor([pad(s, 0) for s in ids]); labels = torch.tensor([pad(s, -100) for s in labels])
    return torch.tensor(np.stack(imgs)).permute(0, 3, 1, 2).to(device), ids.to(device), labels.to(device)


# ---------- 2. Model: vision encoder -> projector -> language model ----------
class VisionEncoder(nn.Module):                  # a miniature ViT: patchify -> transformer
    def __init__(self, d=64, patch=8, layers=2):
        super().__init__()
        self.patch = nn.Conv2d(3, d, patch, patch)                       # 32x32 image -> 4x4 = 16 patch tokens
        self.pos = nn.Parameter(torch.zeros(1, (IMG // patch) ** 2, d))
        self.enc = nn.TransformerEncoder(nn.TransformerEncoderLayer(d, 4, 4 * d, 0.0, batch_first=True, norm_first=True), layers, enable_nested_tensor=False)
    def forward(self, x): return self.enc(self.patch(x).flatten(2).transpose(1, 2) + self.pos)


class TinyVLM(nn.Module):
    def __init__(self, d_v=64, d=96, layers=3):
        super().__init__()
        self.vision = VisionEncoder(d_v)
        self.projector = nn.Sequential(nn.Linear(d_v, d), nn.GELU(), nn.Linear(d, d))   # the "connector"
        self.tok, self.pos = nn.Embedding(len(VOCAB), d), nn.Embedding(64, d)
        self.lm = nn.TransformerEncoder(nn.TransformerEncoderLayer(d, 4, 4 * d, 0.0, batch_first=True, norm_first=True), layers, enable_nested_tensor=False)
        self.head = nn.Linear(d, len(VOCAB))
    def forward(self, img, ids):
        v = self.projector(self.vision(img))                              # [B, 16, d] image tokens in the LM's "language"
        t = self.tok(ids)                                                 # [B, T, d]; position 0 is the <img> placeholder
        x = torch.cat([v, t[:, 1:]], dim=1)                               # replace <img> by the 16 image tokens
        x = x + self.pos(torch.arange(x.size(1), device=x.device))
        mask = torch.triu(torch.ones(x.size(1), x.size(1), device=x.device, dtype=torch.bool), 1)
        logits = self.head(self.lm(x, mask=mask))
        return logits[:, v.size(1) - 1:]                                  # keep text positions aligned with ids


def loss_fn(model, img, ids, labels):
    logits = model(img, ids)
    return F.cross_entropy(logits[:, :-1].reshape(-1, logits.size(-1)), labels[:, 1:].reshape(-1), ignore_index=-100)


# ---------- 3. Training stages ----------
def train(model, kind, steps, params, lr, bs=64):
    opt = torch.optim.AdamW(params, lr=lr, weight_decay=0.01)
    for s in range(steps):
        loss = loss_fn(model, *batch(kind, bs))
        opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step()
        if s % 200 == 0 or s == steps - 1: print(f"  [{kind}] step {s:4d} loss {loss.item():.3f}")


# ---------- 4. Evaluation: greedy decoding + exact-match accuracy ----------
@torch.no_grad()
def answer(model, img, question):
    ids = [STOI["<img>"]] + [STOI[w] for w in question.split()] + [STOI["<bos>"]]
    out = []
    for _ in range(6):
        logits = model(img, torch.tensor([ids + out], device=device))
        nxt = logits[0, -1].argmax().item()
        if nxt == STOI["<eos>"]: break
        out.append(nxt)
    return " ".join(VOCAB[i] for i in out)


def evaluate(model, n=300):
    model.eval(); ok = {"color": 0, "shape": 0, "where": 0}; tot = dict.fromkeys(ok, 0)
    for _ in range(n):
        img, _, _, (c, s, side) = make_sample("vqa")
        x = torch.tensor(img).permute(2, 0, 1)[None].to(device)
        for key, q, gold in (("color", "what color is it ?", c), ("shape", "what shape is it ?", s), ("where", "where is it ?", side)):
            ok[key] += answer(model, x, q) == gold; tot[key] += 1
    model.train()
    return {k: round(ok[k] / tot[k], 3) for k in ok}


if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    random.seed(0); torch.manual_seed(0)
    model = TinyVLM().to(device)
    print(f"params: {sum(p.numel() for p in model.parameters()) / 1e6:.2f}M on {device}")
    t0 = time.time()
    print("Stage 1: alignment (captions) - train vision encoder + projector + LM"); train(model, "caption", 600, model.parameters(), 2e-3)
    print("Stage 2: instruction tuning (VQA) - freeze the vision encoder, train projector + LM")
    for p in model.vision.parameters(): p.requires_grad = False
    train(model, "vqa", 1200, [p for p in model.parameters() if p.requires_grad], 1e-3)
    print("accuracy:", evaluate(model), f"({time.time() - t0:.0f}s)")
