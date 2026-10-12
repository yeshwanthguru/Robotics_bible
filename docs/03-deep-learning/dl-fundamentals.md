---
title: DL Fundamentals & Training
---

# Deep Learning Fundamentals

## Neural network basics

- Neuron: $a=\phi(w^\top x+b)$. Universal approximation: one wide hidden layer can approximate any continuous function on a compact set.
- **Backprop** = chain rule on a computation graph (reverse-mode autodiff). Cost ≈ 2–3× forward.
- Layer $\ell$: $\delta^{\ell}=(W^{\ell+1\top}\delta^{\ell+1})\odot\phi'(z^\ell)$; $\partial L/\partial W^\ell=\delta^\ell a^{\ell-1\top}$.

### Activations
| Name | Formula | Note |
|---|---|---|
| Sigmoid | $1/(1+e^{-x})$ | saturates, vanishing grads |
| Tanh | | zero-centered |
| ReLU | $\max(0,x)$ | dead neurons |
| Leaky/PReLU/ELU | | fix dead ReLU |
| GELU | $x\Phi(x)$ | transformers |
| SiLU/Swish | $x\sigma(x)$ | modern CNNs, LLMs |
| SwiGLU | $\mathrm{SiLU}(xW)\odot xV$ | LLaMA-style FFN |
| Softmax | $e^{z_i}/\sum e^{z_j}$ | stabilize by subtracting max |

### Initialization
Xavier (tanh): $\mathrm{Var}=2/(n_{in}+n_{out})$; He (ReLU): $2/n_{in}$. Goal: keep activation/gradient variance constant across depth.

### Losses
MSE, L1/Huber, cross-entropy, focal, hinge, contrastive/InfoNCE $-\log\frac{e^{s^+/\tau}}{\sum e^{s/\tau}}$, triplet, KL, CTC, Dice, diffusion ε-prediction MSE.

### Optimizers
| Optimizer | Update |
|---|---|
| SGD+momentum | $v\leftarrow\beta v+g;\ \theta\leftarrow\theta-\eta v$ |
| RMSProp | divide by running RMS of g |
| Adam | $m,v$ moving averages with bias-correction; $\theta\leftarrow\theta-\eta\hat m/(\sqrt{\hat v}+\epsilon)$ |
| AdamW | decoupled weight decay — default for transformers |
| Lion, Adafactor, Muon, Shampoo | memory/curvature-efficient variants |

LR schedules: warmup + cosine decay; one-cycle; linear decay. Batch size ↑ ⇒ lr ↑ (linear scaling rule), use warmup.

### Regularization & normalization
Weight decay, dropout ($p$ drop, scale at train), data augmentation, label smoothing, mixup/cutmix, early stopping, stochastic depth.
- **BatchNorm:** normalize over batch; train/eval mismatch, bad for small batch / RL.
- **LayerNorm / RMSNorm:** per-sample; transformers. Pre-LN more stable than Post-LN.
- **GroupNorm:** small-batch vision, diffusion policy.

### Training stability checklist
1. Overfit a single batch first. 2. Check data/labels/augmentations visually. 3. Loss at init ≈ $\log C$. 4. Gradient clipping (norm 1.0). 5. Mixed precision (bf16 > fp16; no loss scaling needed). 6. Monitor grad-norm, update/weight ratio ~1e-3. 7. NaNs: lr too high, log(0), fp16 overflow, bad data.

## Vanishing/exploding gradients
Fixes: ReLU-family, residual connections, normalization, careful init, gradient clipping, gating (LSTM).

## Distributed / efficient training
DDP (data parallel, all-reduce grads), FSDP/ZeRO (shard params/grads/optimizer), tensor parallel (split matmuls), pipeline parallel (split layers), sequence/context parallel, gradient checkpointing (trade compute for memory), mixed precision, gradient accumulation, `torch.compile`, FlashAttention.

## Interview Q&A

**Why residual connections work?** Identity path gives gradient highway: $y=x+F(x)\Rightarrow \partial y/\partial x=I+\partial F/\partial x$; also loss landscape smoother.

**BatchNorm vs LayerNorm?** BN statistics across batch (needs big batch, differs train/test); LN across features per token (batch independent).

**Why Adam over SGD?** Per-parameter adaptive lr handles sparse/ill-conditioned problems; SGD+momentum can generalize slightly better in vision with tuning.

**Dropout at inference?** Off; weights scaled (inverted dropout scales at train time).

**What is label smoothing?** Replace one-hot with $(1-\epsilon)$ on true class, $\epsilon/(K-1)$ others; reduces over-confidence.

**Explain mixed precision.** Forward/backward in fp16/bf16, master weights in fp32; bf16 keeps fp32's exponent range.
