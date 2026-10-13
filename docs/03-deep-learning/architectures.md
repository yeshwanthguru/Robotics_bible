---
title: Architectures (CNN, RNN, Transformer, GNN, Generative)
---

# Deep Learning Architectures

:::tip[The 30-second version]
An **architecture** is the *shape of the wiring* inside a network, chosen to match the data.
**CNN** = for images (look at small patches, reuse the same detector everywhere).
**RNN / state-space** = for sequences (carry a memory forward).
**Transformer** = for everything now (let every piece of the input look at every other piece).
**GNN** = for graphs. **Diffusion / VAE / GAN** = for *generating* new data.
:::

## 🎮 Try it yourself

<div class="simbox"><div class="simhead"><span>Interactive: Softmax and attention</span><a href="/Robotics_bible/sim/attention.html" target="_blank">open full screen ↗</a></div><iframe src="/Robotics_bible/sim/attention.html" height="560" loading="lazy" title="Softmax and attention"></iframe></div>


## CNN: how machines see

A convolution slides a tiny filter across the image and asks at each spot "is my pattern here?" Early filters find edges, later ones find textures, then parts, then whole objects.

![convolution](/img/fig/convolution.svg)
*An edge-detector filter lights up exactly where the dark side meets the bright side.*

- **Why it works:** local patterns + the same filter reused everywhere = few parameters and built-in translation awareness.
- **Landmarks:** AlexNet → VGG → **ResNet** (skip connections) → MobileNet (cheap, for robots) → EfficientNet → ConvNeXt.
- **Detection:** two-stage (Faster R-CNN) vs one-stage (**YOLO**, SSD) vs **DETR** (transformer). **Segmentation:** U-Net, Mask R-CNN, **SAM/SAM 2** (segment anything with a prompt).

## RNN, LSTM, and state-space models

An RNN reads a sequence one step at a time, carrying a *memory vector*. Plain RNNs forget over long ranges (vanishing gradients). **LSTM/GRU** add gates that decide what to keep, forget and output. Modern **state-space models (Mamba, S4)** do similar jobs but in linear time, a strong alternative for long sequences.

## The Transformer: the architecture behind LLMs, VLMs and VLAs

![transformer](/img/fig/transformer-block.svg)
*One block: attention gathers information from other tokens, the feed-forward network processes it. Stack dozens of blocks.*

**The key idea, attention:** every token asks a question (*query*), every token advertises what it holds (*key*) and offers content (*value*). Each token blends the values of the tokens whose keys match its query best.

![attention heatmap](/img/fig/attention-heatmap.svg)
*Each row shows who a word "listens to". "red" and "cup" attend strongly to each other; "picked" links to "robot".*

$$ \mathrm{Attention}(Q,K,V)=\mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V $$

> **In words:** compare every query with every key (the dot product = similarity), turn the scores into percentages (softmax), and take that weighted mix of the values. The $\sqrt{d_k}$ just keeps the scores from getting so large that softmax becomes all-or-nothing.

| Piece | Plain meaning |
|---|---|
| **Multi-head** | several attention "views" in parallel, each looking for different relationships |
| **Positional encoding (RoPE)** | tells the model the *order* of tokens, since attention alone ignores it |
| **Feed-forward (MLP)** | per-token thinking step; most of the parameters live here |
| **Residual + LayerNorm** | keep training stable |
| **Causal mask** | in LLMs, a token may not peek at the future |

**Cost:** attention compares all pairs → $O(n^2)$ in sequence length. Fixes: **FlashAttention** (same maths, smarter memory use), sliding window, linear attention, **GQA/MQA** (share keys/values to shrink the KV cache).

**Families:** *encoder-only* (BERT: understand), *decoder-only* (GPT/LLaMA: generate), *encoder–decoder* (T5, Whisper: translate). **ViT** = a transformer on image patches.

## Graph neural networks
Nodes pass messages along edges and update themselves from their neighbours. Used for scene graphs, multi-robot teams, molecules, and learned physics.

## Generative models: making new data

| Family | One-line idea | Good for |
|---|---|---|
| **Autoencoder / VAE** | compress to a small code and reconstruct | latent spaces, world models |
| **GAN** | a forger and a detective improve each other | sharp images (unstable training) |
| **Autoregressive** | predict the next piece, again and again | LLMs, code |
| **Diffusion** | learn to remove noise step by step | images, video, **robot actions (Diffusion Policy)** |
| **Flow matching** | learn a smooth path from noise to data | faster sampling; **used in π0** |

![diffusion](/img/fig/diffusion-process.svg)
*Diffusion: gradually destroy a clean trajectory with noise (left → right) and train a network to reverse each tiny step.*

**Why diffusion suits robots:** a demonstrator might go *left or right* around an obstacle. An averaging model would drive straight into it. A diffusion policy keeps both options and *samples* one coherent action sequence.

## Self-supervised and representation learning
SimCLR/MoCo (contrastive: pull views of the same thing together), DINO (self-distillation), **MAE** (hide patches and reconstruct), **CLIP** (match images to captions), **JEPA** (predict in latent space). For robots: R3M, VC-1, DINOv2 provide strong ready-made visual features.

## Interview Q&A

**Why can Transformers train in parallel but RNNs can't?**
*Simply:* an RNN must finish step *t* before starting *t+1*; attention looks at all tokens at once with matrix multiplies.

**What does the KV cache store, and why?**
*Simply:* the past keys and values, so generating each new token doesn't re-read the whole history. *Deeper:* memory grows with layers × tokens × KV heads × head size.

**Why scale by $\sqrt{d_k}$?**
*Simply:* without it big vectors give huge scores and softmax saturates, killing gradients.

**DDPM vs DDIM?**
*Simply:* DDIM is a deterministic sampler that skips steps, 10–50 steps instead of ~1000.

**Why is CLIP important for robotics?**
*Simply:* it puts pictures and words in the same space, so a robot can find "the red mug" without being trained on that exact object.

**CNN vs ViT?**
*Simply:* CNNs have built-in local-pattern assumptions (great with less data); ViTs are more flexible but need more data or pretraining.
