---
title: 2. Build a VLM
---

# 2. Build a Vision-Language Model (end to end)

:::tip[The 30-second version]
A VLM = **a vision encoder** (turns the picture into vectors) + **a connector** (translates those vectors into the language model's "word space") + **an LLM** (reads the translated picture plus your question and writes the answer).
You almost never train all of it from zero. You **assemble pretrained parts** and train in **two stages**: first teach only the connector to translate (alignment), then teach the whole system to follow instructions.
:::

![vlm token flow](/img/fig/vlm-token-flow.svg)
*The picture becomes ~729 "image tokens" that sit in the same sequence as the text tokens. The LLM then does ordinary next-token prediction, with loss only on the answer.*

## The plan at a glance

| Step | What you do | Output |
|---|---|---|
| 0 | Choose the route (tiny / assemble / fine-tune) | a decision |
| 1 | Choose the three components | model recipe |
| 2 | Build the input format (image tokens, chat template, label masking) | a working forward pass |
| 3 | Build the datasets for each stage | versioned data |
| 4 | Train stage 1 (alignment) | aligned connector |
| 5 | Train stage 2 (instruction tuning) | a useful VLM |
| 6 | Evaluate (benchmarks + your own set) + error analysis | scorecard |
| 7 | Deploy and monitor | an API |

## Step 0. Pick your route

| Route | When | Effort |
|---|---|---|
| **A. Tiny from scratch** (script below) | to understand every part | minutes on CPU |
| **B. Assemble from pretrained parts** (LLaVA recipe) | you need a custom architecture or a research model | days, multi-GPU |
| **C. Fine-tune an existing VLM** (Qwen2-VL, SmolVLM, PaliGemma, InternVL, Idefics) | **you need a working VLM for your domain** | hours, 1 GPU |

**Recommendation:** do A to learn, then do C for real work. Do B only if you need something the existing models lack.

## Part A. The tiny VLM (learn every part)

The script builds a synthetic world (coloured shapes on the left or right), then a miniature VLM and trains it in the **same two stages as LLaVA**.

### What each piece does
1. **Data generator**: renders a 32×32 image with one shape; caption `a red circle .` (stage 1), and questions *"what color is it ?"*, *"what shape is it ?"*, *"where is it ?"* (stage 2).
2. **Vision encoder**: a mini ViT. A conv "patchify" step cuts the image into 16 patches; a small transformer produces 16 vectors.
3. **Connector**: a 2-layer MLP mapping vision vectors into the LLM's embedding size.
4. **Language model**: a small causal transformer over `[16 image tokens] + [question] + <bos> + [answer]`.
5. **Loss masking**: labels are `-100` (ignored) everywhere except the answer tokens.
6. **Stage 1**: train everything on captions (alignment). **Stage 2**: **freeze the vision encoder**, train connector + LM on questions.
7. **Evaluation**: greedy-decode the answer and compare to ground truth.

### The code (complete and runnable)

```python
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
```

*Source file: `examples/02_tiny_vlm.py` in the repository.*

### Expected result (tested)
```
params: 0.47M on cpu
Stage 1: alignment (captions) ... loss 3.49 -> 0.05
Stage 2: instruction tuning (VQA) ... loss -> ~0.01
accuracy: {'color': 1.0, 'shape': 0.95, 'where': 1.0}      # about 75 seconds on a 4-core CPU
```

### Experiments that teach you the real design rules (measured)

I ran these variants on the same tiny VLM (single run each, so small gaps are noise):

| Variant | color | shape | where | What it teaches |
|---|---|---|---|---|
| **Full recipe**: stage 1 (train all) → stage 2 (freeze encoder) | 100 % | 95 % | 100 % | the baseline |
| Stage 1, then **don't freeze** the encoder in stage 2 | 100 % | 96 % | 100 % | on a tiny synthetic task freezing makes little difference; with big pretrained encoders and small data it protects the features |
| **Skip stage 1**, train everything in stage 2 | 100 % | 91 % | 100 % | alignment first helps, a little here and much more with real pretrained parts |
| **Skip stage 1 and freeze** the (untrained!) vision encoder | 100 % | **54 %** | 100 % | **never freeze a vision encoder that hasn't been pretrained**: it keeps random features and can't see shape |

*Takeaway:* "freeze the vision encoder" is correct advice only when the encoder is already good (SigLIP, CLIP). Easy attributes (colour, left/right) were learned even from random features; the harder attribute (shape) shows the difference.

Other things worth trying yourself: remove the loss masking (train on the question too) and watch capacity get wasted; add a shape that never appeared in training and watch accuracy collapse (VLMs do not generalise to concepts they never saw).

## Part B. Assemble a real VLM from pretrained parts (the LLaVA recipe)

### Step 1. Choose the components

| Part | Good choices | Notes |
|---|---|---|
| **Vision encoder** | **SigLIP** (so400m, 384 px), CLIP ViT-L/14-336, DINOv2 (good spatial detail; many robot VLMs combine SigLIP + DINOv2) | encoders trained with image–text alignment give semantics; DINO gives geometry |
| **LLM** | Qwen2.5 (0.5–7B), Llama 3.x, Gemma, SmolLM2 | start small (0.5–1.5B) to iterate fast |
| **Connector** | 2-layer MLP (LLaVA), pixel-shuffle + MLP (fewer tokens), Q-Former / perceiver resampler (fixed token count) | MLP is simplest and works well |
| **Resolution** | single 336–384 px, or **AnyRes tiling** (split a big image into tiles + a thumbnail) | OCR and small objects need resolution |

**Token budget:** a 384 px image with 14 px patches gives 27 × 27 = **729 tokens**; a 336 px CLIP ViT-L/14 gives 24 × 24 = **576**. Pixel-shuffle (merge 2 × 2 neighbours) cuts this by 4×. More tokens = better detail but slower training and inference.

### Step 2. Build the sequence format
1. Write a **chat template**: system / user / assistant turns.
2. Put a special placeholder `<image>` in the user turn.
3. At the embedding step, **replace the placeholder with the connector's output** (the image tokens).
4. Build **labels**: copy the token ids, set everything that is not an assistant answer to `-100`.
5. Build the **attention mask**. For multi-image or video, add one placeholder per image/frame.

Sketch of the forward pass for a hand-built model:
```python
# vision_tower: e.g. SiglipVisionModel;  llm: AutoModelForCausalLM;  proj: nn.Sequential(Linear, GELU, Linear)
def forward(pixel_values, input_ids, labels, image_token_id):
    img_feats = vision_tower(pixel_values).last_hidden_state        # [B, N_patches, d_v]
    img_embeds = proj(img_feats)                                    # [B, N_patches, d_llm]
    txt_embeds = llm.get_input_embeddings()(input_ids)              # [B, T, d_llm]
    mask = input_ids == image_token_id                              # where the placeholder tokens are
    txt_embeds[mask] = img_embeds.reshape(-1, img_embeds.size(-1)).to(txt_embeds.dtype)   # splice image tokens in
    return llm(inputs_embeds=txt_embeds, labels=labels)             # standard LM loss with -100 masking
```
(For this to work, the text must contain exactly `N_patches` placeholder tokens per image. Hugging Face already implements this for `LlavaForConditionalGeneration`; use it when you can, and read its `forward` to see the same idea.)

### Step 3. Build the data

| Stage | Data | Size (LLaVA-1.5) | Goal |
|---|---|---|---|
| **1. Alignment** | image–caption pairs (filtered CC3M / LAION subsets, e.g. the LLaVA 558 K set) | ≈ 0.5 M | connector learns to translate |
| **1.5 (optional)** | high-quality detailed captions, OCR/doc data | 1–10 M | add knowledge |
| **2. Instruction tuning** | visual Q&A, conversations, reasoning, OCR, charts (LLaVA-665 K mix, ShareGPT4V, The Cauldron, Cambrian) | ≈ 0.7 M | follow instructions |
| **Domain** | **your** images + questions | 1 k–50 k | specialise |

**Data format** (one example):
```json
{"image": "images/0001.jpg",
 "conversations": [
   {"from": "human", "value": "<image>\nWhat object is the robot gripper holding?"},
   {"from": "gpt",   "value": "A red mug, grasped by the handle."}]}
```
**Quality rules:** diverse questions (what / where / count / compare / why), include **negative** questions ("Is there a dog?" → "No") to reduce hallucination, include OCR, spatial ("left of", "behind"), and for robotics **grounding** (pointing to or boxing objects) and **embodied reasoning** (can I reach it? what next?). Synthetic questions generated by a strong VLM are common; always sample-check them.

### Step 4. Training stage 1: alignment

| Setting | Value (LLaVA-1.5 style) |
|---|---|
| Trainable | **connector only** |
| Frozen | vision encoder and LLM |
| Learning rate | 1e-3 |
| Batch size | 256 (use gradient accumulation) |
| Epochs | 1 |
| Precision | bf16 |

*Why:* the connector starts random; if you let it push noisy gradients into the LLM, you damage the LLM. Training only the connector first makes the translation sensible.

**Check:** loss falls steadily; generate captions for 20 training images; they should match the content.

### Step 5. Training stage 2: instruction tuning

| Setting | Value |
|---|---|
| Trainable | connector + LLM (full or LoRA); vision encoder frozen (or a very small lr ≈ 2e-6 to adapt it) |
| Learning rate | 2e-5 full fine-tune (1e-4 with LoRA) |
| Batch size | 128 |
| Epochs | 1–3 |
| Max sequence | image tokens + text; ≥ 2048 |

**Check:** loss masked on answers only; accuracy on a small validation Q&A set; qualitative chats.

### Route C. Fine-tune an existing VLM (the fast, practical path)

Most real projects: take **Qwen2-VL / Qwen2.5-VL, SmolVLM, PaliGemma, Idefics3, InternVL**, and fine-tune with LoRA on your data.

```python
# pip install transformers peft trl accelerate datasets pillow
import torch
from datasets import load_dataset
from peft import LoraConfig
from transformers import AutoModelForImageTextToText, AutoProcessor
from trl import SFTTrainer, SFTConfig

name = "HuggingFaceTB/SmolVLM-Instruct"                 # or "Qwen/Qwen2-VL-2B-Instruct", etc.
processor = AutoProcessor.from_pretrained(name)
model = AutoModelForImageTextToText.from_pretrained(name, torch_dtype=torch.bfloat16)

def collate(batch):                                      # builds inputs + masked labels for a batch of examples
    texts = [processor.apply_chat_template(ex["messages"], tokenize=False) for ex in batch]   # messages include {"type":"image"}
    images = [[ex["image"].convert("RGB")] for ex in batch]
    enc = processor(text=texts, images=images, return_tensors="pt", padding=True)
    labels = enc["input_ids"].clone()
    labels[labels == processor.tokenizer.pad_token_id] = -100            # ignore padding
    # TODO for production: also set prompt/image positions to -100 so loss is on the assistant answer only
    enc["labels"] = labels
    return enc

cfg = SFTConfig(output_dir="out-vlm", per_device_train_batch_size=2, gradient_accumulation_steps=16,
                learning_rate=1e-4, num_train_epochs=2, bf16=True, logging_steps=10, gradient_checkpointing=True,
                remove_unused_columns=False, dataset_kwargs={"skip_prepare_dataset": True})
peft_cfg = LoraConfig(r=16, lora_alpha=32, target_modules="all-linear", task_type="CAUSAL_LM")
ds = load_dataset("json", data_files="vlm_train.jsonl")["train"]         # your examples
SFTTrainer(model=model, args=cfg, train_dataset=ds, data_collator=collate, peft_config=peft_cfg).train()
```
*This is a template: the exact chat-template message format, processor arguments, and `SFTTrainer` options differ by model and library version. Follow the model card on Hugging Face and the TRL "VLM fine-tuning" example for the current form. What does **not** change: build the chat text with an image placeholder, tokenise with the processor, mask labels to the answer, LoRA, small LR.*

## Step 6. Evaluate

| What | Tool / benchmark |
|---|---|
| **General VQA** | VQAv2, GQA |
| **Text in images (OCR)** | TextVQA, DocVQA, ChartQA, OCRBench |
| **Hallucination** | **POPE** (object existence) |
| **Broad ability** | MMBench, MME, MMMU, RealWorldQA |
| **Spatial / grounding (robotics!)** | RefCOCO, BLINK, CV-Bench, pointing accuracy |
| **Toolkit** | `lmms-eval` runs most of these for you |
| **Your domain** | a held-out set of 200–1000 real questions with exact-match / rubric scoring |

**Error analysis:** categorise 100 wrong answers: perception error (didn't see), reasoning error, OCR error, language prior (answered from habit, ignoring the image), hallucination. Fix with targeted data.

**Test that it really uses the image:** feed a blank or wrong image; if the answer doesn't change, the model is ignoring vision (a common failure).

## Step 7. Deploy
- **Serve** with vLLM or SGLang (both support many VLMs): `vllm serve <model> --max-model-len 8192`; send images as base64 in the OpenAI-style API.
- **Latency levers:** fewer image tokens (lower resolution or pixel-shuffle), quantisation (AWQ/FP8), prefix caching, batching.
- **On robots (edge):** quantise to 4–8 bit, run via TensorRT-LLM / llama.cpp / MLC, cap image resolution, run at 1–10 Hz.
- **Monitor:** log image hashes, prompts, outputs; sample for review; track hallucination reports.

## Common problems and fixes

| Symptom | Cause | Fix |
|---|---|---|
| Answers ignore the image | weak alignment, language prior | longer stage 1, more image-grounded data, check placeholder splicing |
| Hallucinated objects | no negative examples | add "is there X?" negatives, POPE-style data |
| Great on benchmarks, bad on your images | domain gap | add domain data in stage 2 |
| Forgets general chat ability | too high LR / only domain data | LoRA, lower LR, mix in general instruction data |
| Can't read small text | low resolution | AnyRes tiling, higher-res encoder |
| Training OOM | too many image tokens | smaller images, pixel-shuffle, gradient checkpointing |
| Loss doesn't drop in stage 1 | wrong label mask / placeholder count mismatch | print one batch: ids, labels, number of image tokens |
