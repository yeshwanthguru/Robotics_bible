---
title: Architectures (CNN, RNN, Transformer, GNN, Generative)
---

# Deep Learning Architectures

## CNN
- Convolution: local, weight-shared, translation-equivariant. Output size $\lfloor (n+2p-k)/s\rfloor+1$. Receptive field grows with depth/dilation. Params $=k^2 C_{in}C_{out}$.
- Milestones: LeNet → AlexNet → VGG → Inception → **ResNet** (skip) → DenseNet → MobileNet (depthwise-separable) → EfficientNet (compound scaling) → ConvNeXt.
- Detection: two-stage (Faster R-CNN, RPN + ROI-pool) vs one-stage (YOLO, SSD, RetinaNet focal loss, DETR set prediction w/ Hungarian matching). Segmentation: FCN, U-Net, DeepLab (atrous), Mask R-CNN, **SAM / SAM2**.
- 1×1 conv = channel mixing; depthwise separable reduces compute ≈ $1/C_{out}+1/k^2$.

## RNN / LSTM / GRU / SSM
- RNN: $h_t=\phi(W_hh_{t-1}+W_xx_t)$; BPTT; vanishing gradient.
- LSTM gates: forget, input, output; cell state = additive path. GRU: update+reset gates.
- Modern: **State space models** (S4, Mamba – selective SSM, linear-time) and RWKV challenge attention for long sequences.

## Transformer (must know cold)

$$\mathrm{Attn}(Q,K,V)=\mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

- Why $\sqrt{d_k}$: dot-product variance grows with $d_k$ → saturating softmax.
- Multi-head: h parallel subspaces; concat + $W_O$.
- Block: `x + MHA(LN(x))` then `x + FFN(LN(x))`; FFN expands 4× (or 8/3× w/ SwiGLU).
- **Positional info:** sinusoidal, learned, **RoPE** (rotation of q/k; relative; extrapolation via NTK/YaRN scaling), ALiBi.
- **Complexity:** $O(n^2 d)$ time, $O(n^2)$ memory → FlashAttention (IO-aware, exact), sliding window, sparse, linear attention, MQA/GQA (shrink KV cache).
- Encoder-only (BERT, masked LM), decoder-only (GPT, causal mask), encoder–decoder (T5, Whisper).
- **ViT:** split image to patches (16×16), linear embed, [CLS], transformer. Needs lots of data or self-supervision (DINO/MAE).

## Graph neural networks
Message passing: $h_v^{k+1}=\phi(h_v^k,\ \bigoplus_{u\in N(v)}\psi(h_u^k,e_{uv}))$. GCN, GraphSAGE, GAT, GIN (WL-expressive). Robotics: scene graphs, multi-agent, molecule/contact graphs, learned physics simulators.

## Generative models
| Family | Idea | Pros / Cons |
|---|---|---|
| Autoencoder / VAE | encoder q(z\|x), decoder p(x\|z); ELBO $=E_q[\log p(x|z)]-D_{KL}(q\|p)$; reparam trick $z=\mu+\sigma\epsilon$ | stable, blurry |
| GAN | min-max G vs D | sharp, unstable/mode collapse; WGAN, spectral norm |
| Normalizing flow | invertible maps, exact likelihood | restricted architectures |
| Autoregressive | $p(x)=\prod p(x_t|x_{<t})$ | LLMs; slow sampling |
| **Diffusion / score** | forward noising $x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon$; learn ε-prediction; reverse sampling DDPM/DDIM | high quality; many steps |
| **Flow matching / rectified flow** | regress velocity field along straight paths | fewer steps (π0 uses it) |
| Consistency models | one-step distillation | fast |

Diffusion in robotics: **Diffusion Policy** (action chunk denoising, conditioned on observations; handles multimodal demos), Diffuser/Decision Diffuser (trajectory planning), π0 (flow-matching action expert).

## Self-supervised / representation learning
SimCLR/MoCo (contrastive), BYOL/DINO (self-distillation), MAE (masked patches), CLIP (image-text contrastive), JEPA (predict in latent space), VC-1/R3M/Voltron/DINOv2 for robot visual representations.

## Interview Q&A

**Why can't RNNs parallelize but Transformers can?** RNN step t depends on t-1; attention computes all pairs with matmuls.

**What does the KV cache store?** Past keys/values per layer so decoding step is $O(n)$ rather than recomputing $O(n^2)$; memory $=2\cdot L\cdot n\cdot h_{kv}d_h\cdot$bytes.

**Why GQA?** Share K/V across query-head groups → smaller KV cache, near-MHA quality.

**ELBO derivation sketch:** $\log p(x)\ge E_q[\log p(x|z)]-KL(q(z|x)\|p(z))$ via Jensen.

**DDPM vs DDIM?** DDIM is deterministic (non-Markovian) sampler → skip steps (10–50 vs 1000).

**Why CLIP matters for robotics?** Shared image–text embedding enables language-conditioned perception, open-vocabulary detection, zero-shot goals.
