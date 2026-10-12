"""A complete, tiny GPT you can train on a laptop: tokenizer -> model -> training loop -> eval -> sampling.

Run:  python examples/01_tiny_gpt.py --text path/to/any_text_file.txt --steps 2000
(If --text is omitted it trains on this script's own source code, just to prove the pipeline works.)
"""
import argparse, math, time
import torch, torch.nn as nn, torch.nn.functional as F


# ---------- 1. Data: character-level tokenizer + train/val split ----------
class CharTokenizer:
    def __init__(self, text):
        self.chars = sorted(set(text))
        self.stoi = {c: i for i, c in enumerate(self.chars)}
    def encode(self, s): return [self.stoi[c] for c in s if c in self.stoi]
    def decode(self, ids): return "".join(self.chars[i] for i in ids)
    @property
    def vocab_size(self): return len(self.chars)


def get_batch(data, block_size, batch_size, device):
    ix = torch.randint(len(data) - block_size - 1, (batch_size,))
    x = torch.stack([data[i:i + block_size] for i in ix])
    y = torch.stack([data[i + 1:i + block_size + 1] for i in ix])      # target = input shifted by one token
    return x.to(device), y.to(device)


# ---------- 2. Model: decoder-only transformer ----------
class CausalSelfAttention(nn.Module):
    def __init__(self, d, n_heads, dropout):
        super().__init__()
        assert d % n_heads == 0
        self.n_heads, self.qkv, self.proj = n_heads, nn.Linear(d, 3 * d, bias=False), nn.Linear(d, d, bias=False)
        self.drop = nn.Dropout(dropout)
    def forward(self, x):
        B, T, C = x.shape
        q, k, v = self.qkv(x).split(C, dim=2)
        q, k, v = (t.view(B, T, self.n_heads, C // self.n_heads).transpose(1, 2) for t in (q, k, v))
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)    # softmax(QK^T/sqrt(d))V with a causal mask
        return self.drop(self.proj(y.transpose(1, 2).reshape(B, T, C)))


class Block(nn.Module):
    def __init__(self, d, n_heads, dropout):
        super().__init__()
        self.ln1, self.attn = nn.LayerNorm(d), CausalSelfAttention(d, n_heads, dropout)
        self.ln2 = nn.LayerNorm(d)
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d), nn.Dropout(dropout))
    def forward(self, x):
        x = x + self.attn(self.ln1(x))          # residual connection around attention
        return x + self.mlp(self.ln2(x))        # residual connection around the feed-forward net


class TinyGPT(nn.Module):
    def __init__(self, vocab, block_size=128, d=128, n_layers=4, n_heads=4, dropout=0.1):
        super().__init__()
        self.block_size = block_size
        self.tok, self.pos = nn.Embedding(vocab, d), nn.Embedding(block_size, d)
        self.blocks = nn.ModuleList(Block(d, n_heads, dropout) for _ in range(n_layers))
        self.ln_f, self.head = nn.LayerNorm(d), nn.Linear(d, vocab, bias=False)
        self.head.weight = self.tok.weight      # weight tying: input and output embeddings share parameters
        self.apply(self._init)
    @staticmethod
    def _init(m):
        if isinstance(m, (nn.Linear, nn.Embedding)): nn.init.normal_(m.weight, mean=0.0, std=0.02)
    def forward(self, idx, targets=None):
        B, T = idx.shape
        x = self.tok(idx) + self.pos(torch.arange(T, device=idx.device))
        for b in self.blocks: x = b(x)
        logits = self.head(self.ln_f(x))
        loss = None if targets is None else F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1))
        return logits, loss
    @torch.no_grad()
    def generate(self, idx, n_new, temperature=1.0, top_k=None):
        for _ in range(n_new):
            logits, _ = self(idx[:, -self.block_size:])
            logits = logits[:, -1] / temperature
            if top_k:
                v, _ = torch.topk(logits, top_k); logits[logits < v[:, [-1]]] = -float("inf")
            idx = torch.cat([idx, torch.multinomial(F.softmax(logits, -1), 1)], dim=1)
        return idx


# ---------- 3. Training loop: AdamW + warmup/cosine schedule + grad clipping + periodic eval ----------
def lr_at(step, total, base=3e-3, warmup=100, min_lr=3e-4):
    if step < warmup: return base * (step + 1) / warmup
    p = (step - warmup) / max(1, total - warmup)
    return min_lr + 0.5 * (base - min_lr) * (1 + math.cos(math.pi * p))


@torch.no_grad()
def evaluate(model, data, block_size, device, iters=20):
    model.eval()
    losses = [model(*get_batch(data, block_size, 32, device))[1].item() for _ in range(iters)]
    model.train()
    return sum(losses) / len(losses)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", default=None); ap.add_argument("--steps", type=int, default=1500)
    ap.add_argument("--block", type=int, default=128); ap.add_argument("--batch", type=int, default=32)
    a = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(0)
    text = open(a.text, encoding="utf-8").read() if a.text else open(__file__, encoding="utf-8").read() * 20
    tok = CharTokenizer(text)
    data = torch.tensor(tok.encode(text))
    n = int(0.9 * len(data)); train, val = data[:n], data[n:]
    model = TinyGPT(tok.vocab_size, a.block).to(device)
    print(f"params: {sum(p.numel() for p in model.parameters()) / 1e6:.2f}M  device: {device}  chars: {len(data)}  vocab: {tok.vocab_size}")
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3, betas=(0.9, 0.95), weight_decay=0.1)
    t0 = time.time()
    for step in range(a.steps):
        for g in opt.param_groups: g["lr"] = lr_at(step, a.steps)
        x, y = get_batch(train, a.block, a.batch, device)
        _, loss = model(x, y)
        opt.zero_grad(set_to_none=True); loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step()
        if step % 250 == 0 or step == a.steps - 1:
            print(f"step {step:5d}  train {loss.item():.3f}  val {evaluate(model, val, a.block, device):.3f}  ({time.time() - t0:.0f}s)")
    prompt = torch.tensor([tok.encode(text[:16])], device=device)
    print("--- sample ---"); print(tok.decode(model.generate(prompt, 200, temperature=0.8, top_k=20)[0].tolist()))


if __name__ == "__main__":
    main()
