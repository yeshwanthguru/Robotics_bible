---
title: 1. Build an AI model
---

# 1. Build an AI Model (end to end)

:::tip[The 30-second version]
Building any AI model is the same seven steps: **define the goal → get and clean data → make a simple baseline → design the model → train it → evaluate honestly → deploy and watch it.** In this chapter you do it twice: first from scratch with a tiny GPT (so nothing is hidden), then the practical way, by **fine-tuning a real pretrained LLM** with LoRA, which is how almost everyone builds real models today.
:::

## Part A. The seven steps (for any model)

### Step 1: Define the problem and the metric
Write one sentence: *"Given X, predict Y, and success means metric Z ≥ target."*

| Decide | Example answer | Why it matters |
|---|---|---|
| **Task type** | text generation / classification / regression / detection | picks the architecture and loss |
| **Input and output** | prompt → answer; image → label | defines the data format |
| **Metric** | accuracy, F1, perplexity, exact match, pass@k, win-rate | what "better" means |
| **Baseline to beat** | majority class, keyword rules, a pretrained model zero-shot | proves you added value |
| **Constraints** | latency, memory, privacy, cost | decides model size and serving |

### Step 2: Get and prepare the data (this is 60 % of the work)
1. **Collect:** public datasets (Hugging Face Hub), your own logs, human labelling, synthetic data from a strong model.
2. **Inspect:** print 50 random samples. Check label noise, duplicates, weird characters, class balance.
3. **Clean:** deduplicate (exact + near-duplicate), remove broken samples, filter toxic/private content, normalise formats.
4. **Split:** train / validation / test. **Split by group** (by document, user, scene, episode), never by random row if samples are related, or you will leak.
5. **Tokenise / preprocess:** turn raw data into model inputs. Save the processed dataset with a **version tag**.
6. **Write a data card:** source, size, licence, known issues.

### Step 3: Build the baseline first
A baseline is the dumbest model that could work (logistic regression, a rule, or a pretrained model used zero-shot). If your deep model can't beat it, something is wrong. It also gives you a number to compare with.

### Step 4: Design the model
Pick the *smallest* model that could work. For text: a small decoder-only transformer. Settings you choose:

| Hyper-parameter | Meaning | Tiny model | 125 M | 1 B |
|---|---|---|---|---|
| `d_model` | width of the vectors | 128 | 768 | 2048 |
| `n_layers` | depth | 4 | 12 | 16–24 |
| `n_heads` | attention heads | 4 | 12 | 16–32 |
| `context length` | tokens it can see | 128 | 1024 | 2048–8192 |
| `vocab size` | distinct tokens | ~100 (chars) | ~50k | 32k–150k |

### Step 5: Train
The loop is always: **sample a batch → forward → loss → backward → clip gradients → optimizer step → update learning rate → log → occasionally evaluate and save a checkpoint.** Defaults that work: AdamW (lr 3e-4 for small models, 1e-4–2e-5 for fine-tuning), warm-up then cosine decay, weight decay 0.1, gradient clipping 1.0, bf16 on modern GPUs.

### Step 6: Evaluate honestly
- Report the metric on the **test set** once, after all tuning.
- Do **error analysis**: read 50 failures and group them. This tells you what to fix (data, prompt, model).
- Check **robustness**: new phrasing, edge cases, out-of-distribution inputs.

### Step 7: Deploy and monitor
Export, quantise if needed, serve behind an API, log inputs and outputs, watch for drift, and keep a path to retrain.

## Part B. Build a tiny GPT from scratch

### What you will learn
Every component of a language model, in about 120 lines: tokenizer, embedding, causal self-attention, transformer block, loss, training loop, evaluation, sampling.

### The plan
1. **Tokenizer (char-level).** Map each character to an integer. (Real models use BPE with 32k–150k tokens, but the idea is the same.)
2. **Batches.** Cut text into windows; the target is the input *shifted by one position*, so the model predicts the next token at every position.
3. **Model.** Token embeddings + position embeddings → *N* blocks of (LayerNorm → causal self-attention → residual) and (LayerNorm → MLP → residual) → LayerNorm → linear head to vocabulary logits.
4. **Loss.** Cross-entropy between predicted and true next token.
5. **Training loop.** AdamW, warm-up + cosine learning-rate schedule, gradient clipping.
6. **Evaluation.** Validation loss on held-out text (perplexity = exp(loss)).
7. **Sampling.** Feed a prompt, repeatedly sample the next token with temperature and top-k.

### The code (complete and runnable)

```python
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
```

*Source file: `examples/01_tiny_gpt.py` in the repository.*

### How to run and what to expect
```bash
pip install torch
python examples/01_tiny_gpt.py                      # trains on its own source code (a pipeline test)
python examples/01_tiny_gpt.py --text mybook.txt --steps 3000
```
- The first line prints the parameter count (**0.82 M**) and the device.
- **Tested result (4-core CPU, 600 steps, about 100 seconds):** validation loss falls from **4.34** (that is ≈ ln 81, i.e. random guessing over 81 characters) to **0.09**. It gets this low only because the default demo text is the script itself repeated 20×, so the model memorises it. That makes it a good *pipeline test*, not a language-modelling result.
- On real book-like English at character level, expect the validation loss to settle roughly around 1.5–2.0 with a model this small, and to improve with more data, a bigger model and longer training.
- If the loss stays near ln(vocab) it isn't learning: check the learning rate and that targets are shifted by one position.
- The sample printed at the end should look like the training text in style (here: Python code). Early in training it is only word-shaped.

### Experiments to build intuition (do these)
| Change | Predict, then observe |
|---|---|
| `lr` ×10 | loss spikes or NaN |
| remove `clip_grad_norm_` | occasional instabilities |
| `n_layers` 4 → 1 | worse loss: less capacity |
| `dropout` 0.1 → 0.5 | slower training, less overfitting |
| train on 1 KB of text | train loss ≈ 0, val loss rises: overfitting |
| `temperature` 0.2 vs 1.5 | repetitive vs chaotic text |

### Scaling this up (the same code, bigger numbers)
| Model | Params | Data | Roughly what it needs |
|---|---|---|---|
| This script | ~0.8 M | 100 KB | a laptop |
| nanoGPT-style | 10–125 M | 0.1–10 B tokens | 1 GPU, hours–days |
| Small LLM | 1–3 B | 1–10 T tokens | 100s of GPUs, weeks |
| Frontier-class | 100 B+ | 10 T+ tokens | thousands of GPUs, months |

Training compute ≈ $6 \times N \times D$ FLOPs (N parameters, D tokens). To change from characters to a real subword tokenizer, train a BPE tokenizer (`tokenizers` or `sentencepiece`) on your corpus and replace `CharTokenizer`.

## Part C. Build a real model by fine-tuning (the practical path)

Training from scratch is for learning and for organisations with huge budgets. For real work you **start from a pretrained model and adapt it.**

### The decision

| Your goal | Technique | Cost |
|---|---|---|
| Better answers using your documents | **RAG** (retrieval) | cheapest, no training |
| New style, format or domain skills | **SFT** with **LoRA** | a few GPU-hours |
| Match human preferences / safety | **DPO** (after SFT) | a few more GPU-hours |
| Reasoning on checkable tasks (math, code) | **RL with verifiable rewards (GRPO)** | more |
| New knowledge or language at scale | continued pretraining | expensive |

### Step C1. Pick a base model
Small open models to start with: Qwen2.5 (0.5B–7B), Llama 3.x (1B–8B), Gemma 2/3, SmolLM2, Mistral 7B. Choose the **smallest model that solves your task zero-shot reasonably**, and use the *Instruct* variant if you want chat behaviour.

### Step C2. Prepare the dataset
Use the **chat format**: each example is a list of messages.
```json
{"messages": [
  {"role": "user", "content": "Explain what an inverse Jacobian is, simply."},
  {"role": "assistant", "content": "It converts a desired hand movement into the joint movements needed..."}
]}
```
Quality beats quantity: 1,000 clean, diverse examples often beat 50,000 noisy ones. Hold out 5–10 % for validation. Train on **assistant tokens only** (mask the prompt).

### Step C3. Fine-tune with LoRA

**LoRA in one line:** freeze the model, learn small low-rank matrices added to the attention/MLP layers, so you train ~0.1–1 % of the parameters.

```python
# pip install transformers datasets peft trl accelerate bitsandbytes
from datasets import load_dataset
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig

ds = load_dataset("json", data_files={"train": "train.jsonl", "validation": "val.jsonl"})

peft_cfg = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, target_modules="all-linear", task_type="CAUSAL_LM")
cfg = SFTConfig(
    output_dir="out-sft",
    per_device_train_batch_size=4, gradient_accumulation_steps=8,     # effective batch 32
    learning_rate=1e-4, lr_scheduler_type="cosine", warmup_ratio=0.03,
    num_train_epochs=2, bf16=True, logging_steps=10,
    eval_strategy="steps", eval_steps=100, save_steps=100,
    gradient_checkpointing=True,                                       # trade compute for memory
)
trainer = SFTTrainer(model="Qwen/Qwen2.5-1.5B-Instruct", args=cfg,
                     train_dataset=ds["train"], eval_dataset=ds["validation"], peft_config=peft_cfg)
trainer.train()
trainer.save_model("out-sft/final")
```
*(Library arguments are renamed between versions: for example `eval_strategy` vs `evaluation_strategy`, `max_length` vs `max_seq_length`. If something errors, read the current TRL docs; the structure stays the same.)*

**Memory options when the GPU is small:** 4-bit **QLoRA** (`load_in_4bit` via bitsandbytes), smaller batch + more accumulation, gradient checkpointing, shorter max length.

| Setting | Typical value | If it goes wrong |
|---|---|---|
| LoRA rank `r` | 8–64 | too low: underfits; too high: slow, overfits |
| LR (LoRA) | 1e-4 – 2e-4 | too high: forgetting / NaN; too low: nothing changes |
| LR (full fine-tune) | 1e-5 – 2e-5 | |
| Epochs | 1–3 | more epochs on small data → memorisation |
| Max length | 1k–4k tokens | truncating loses answers |

### Step C4. (Optional) Preference tuning with DPO
Data: triples `{prompt, chosen, rejected}`.
```python
from trl import DPOTrainer, DPOConfig
cfg = DPOConfig(output_dir="out-dpo", beta=0.1, learning_rate=5e-6, per_device_train_batch_size=2,
                gradient_accumulation_steps=16, num_train_epochs=1, bf16=True)
DPOTrainer(model="out-sft/final", args=cfg, train_dataset=pref_ds).train()
```
`beta` controls how far the model may drift from the SFT model (lower = more drift). Use a small LR.

### Step C5. Evaluate
1. **Your own held-out set** with the metric from Step 1 (exact match, rubric, win-rate versus the base model).
2. **General benchmarks** to detect forgetting: `lm-evaluation-harness` (MMLU, ARC, HellaSwag, GSM8K).
3. **Human or LLM-as-judge review** of 50–100 outputs (beware judge bias toward long answers).
4. **Compare against the base model and a prompting-only baseline.** If prompting + RAG is as good, don't fine-tune.

### Step C6. Merge, quantise, serve
```bash
# merge the LoRA adapter into the base weights, then serve with vLLM
python -c "from peft import AutoPeftModelForCausalLM as M; M.from_pretrained('out-sft/final').merge_and_unload().save_pretrained('merged')"
vllm serve merged --max-model-len 4096          # OpenAI-compatible API
```
Quantise (AWQ / GPTQ / FP8 / GGUF for `llama.cpp`) to cut memory and latency; re-run your evaluation after quantising.

### GPU memory guide (rough)
| Model | Inference (bf16) | LoRA fine-tune | Full fine-tune |
|---|---|---|---|
| 0.5–1.5 B | 2–4 GB | 8–16 GB | 16–32 GB |
| 7–8 B | 16 GB | 24–40 GB (QLoRA ≈ 12–16 GB) | 80 GB × several |
| 70 B | 140 GB | multi-GPU QLoRA | cluster |

## Part D. Pretraining from scratch (overview for when you need it)
1. **Data:** crawl → language ID → quality filter → deduplicate (MinHash) → remove PII → mix domains (web, books, code, math). Track token counts.
2. **Tokenizer:** train BPE on the mix; check fertility (tokens per word) and special tokens.
3. **Architecture:** decoder-only transformer with RMSNorm, RoPE, SwiGLU, grouped-query attention.
4. **Budget:** pick parameters N and tokens D from a compute budget (~20 tokens per parameter is compute-optimal; "over-train" smaller models for cheaper inference).
5. **Infrastructure:** data parallel + sharding (FSDP/ZeRO) + tensor/pipeline parallel; bf16; FlashAttention; checkpoint often; resume automatically.
6. **Monitoring:** loss, grad-norm, throughput (tokens/s/GPU), loss spikes (lower LR, skip bad batches, restart from checkpoint).
7. **After pretraining:** SFT → preference tuning → safety/evals → quantise → serve.

## Pitfalls checklist

| Symptom | Likely cause | Fix |
|---|---|---|
| Loss is NaN | LR too high, fp16 overflow, bad data | lower LR, use bf16, clip gradients, check inputs |
| Loss stuck at ln(vocab) | targets not shifted / labels all masked / LR ~0 | print a batch, check labels |
| Train ↓ but val ↑ | overfitting | more data, regularise, fewer epochs, early stop |
| Great val, bad real use | data leak or distribution shift | re-split by group, test on real traffic |
| Fine-tuned model got "dumber" | too high LR / too many epochs (forgetting) | lower LR, LoRA, mix in general data |
| Repeats itself | sampling settings | add temperature / top-p, repetition penalty |
| OOM | batch/sequence too big | gradient checkpointing, smaller batch, QLoRA |
