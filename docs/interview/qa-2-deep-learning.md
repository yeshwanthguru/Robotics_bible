---
title: "Q&A 2: Deep Learning"
---

# Interview Q&A: Deep Learning

:::tip[How to use]
Say the **Short answer** first, then add depth only if asked. Chapters: [DL fundamentals](../03-deep-learning/dl-fundamentals.md) · [Architectures](../03-deep-learning/architectures.md).
:::

## Training basics

### Q: Explain backpropagation.
**Short answer:** It computes how much each weight contributed to the error by applying the chain rule backwards through the network. **Go deeper:** Reverse-mode autodiff reuses forward activations; cost is about 2–3× a forward pass.

### Q: Why do we need non-linear activations?
**Short answer:** Without them, stacked linear layers collapse into a single linear map. **Go deeper:** Non-linearities (ReLU, GELU) let networks approximate complex functions (universal approximation).

### Q: ReLU versus sigmoid versus GELU?
**Short answer:** ReLU is fast and avoids saturation; sigmoid saturates and causes vanishing gradients; GELU/SiLU are smooth ReLU variants used in transformers. **Go deeper:** ReLU can "die" (always zero), fixed by Leaky ReLU or GELU.

### Q: What are vanishing and exploding gradients, and how do you fix them?
**Short answer:** Gradients shrink or blow up through many layers. **Go deeper:** Use ReLU-type activations, residual connections, normalisation, good initialisation (He/Xavier), and gradient clipping.

### Q: How do you initialise weights?
**Short answer:** Scale them so activations keep roughly constant variance. **Go deeper:** He init (variance 2/fan-in) for ReLU, Xavier for tanh; small normal(0, 0.02) in transformers.

### Q: Batch norm versus layer norm?
**Short answer:** Batch norm normalises across the batch, layer norm across features within each example. **Go deeper:** Transformers and RL use layer/RMS norm because it doesn't depend on batch size or differ between train and test.

### Q: Why do residual connections help?
**Short answer:** They give gradients a shortcut path so very deep networks train. **Go deeper:** y = x + F(x) makes ∂y/∂x = I + ∂F/∂x; the loss landscape is also smoother.

### Q: What does dropout do?
**Short answer:** Randomly switches neurons off during training to prevent co-adaptation. **Go deeper:** It acts like averaging many sub-networks; it is disabled at inference with scaling handled during training.

### Q: Adam versus AdamW?
**Short answer:** AdamW decouples weight decay from the gradient update. **Go deeper:** It regularises properly and is the default for transformers.

### Q: Why use a learning-rate warm-up and cosine decay?
**Short answer:** Warm-up avoids early instability; decay lets the model settle. **Go deeper:** Large batches and Adam's early second-moment estimates make the first steps risky.

### Q: What is mixed precision training?
**Short answer:** Doing most maths in 16-bit for speed while keeping 32-bit master weights. **Go deeper:** bf16 has fp32's exponent range so it needs no loss scaling; fp16 does.

### Q: How do you debug a network that won't train?
**Short answer:** Overfit one tiny batch first. **Go deeper:** Check data and labels visually, initial loss ≈ ln(classes), learning rate, gradient norms, NaNs, and train/eval mode.

### Q: What is label smoothing?
**Short answer:** Replace hard 0/1 targets with softened ones. **Go deeper:** It reduces over-confidence and improves calibration.

### Q: How do you scale training to many GPUs?
**Short answer:** Data parallelism (copy the model, split the data); for huge models shard (FSDP/ZeRO) or split the model (tensor/pipeline parallel). **Go deeper:** Gradient checkpointing and accumulation trade compute/time for memory.

## Architectures

### Q: How does a convolution work and why is it good for images?
**Short answer:** A small filter slides over the image detecting a pattern at every location. **Go deeper:** Locality plus weight sharing gives few parameters and translation equivariance.

### Q: What is a receptive field?
**Short answer:** The region of the input that influences a unit's output. **Go deeper:** It grows with depth, kernel size, stride and dilation.

### Q: Explain self-attention.
**Short answer:** Each token compares its query with all keys and takes a weighted mix of the values. **Go deeper:** softmax(QKᵀ/√d)V; the √d scaling prevents saturated softmax.

### Q: Why can't RNNs parallelise but transformers can?
**Short answer:** An RNN needs step t before t+1; attention processes all positions with matrix multiplications. **Go deeper:** Transformers pay O(n²) attention cost instead.

### Q: What does multi-head attention add?
**Short answer:** Several attention views in parallel capture different relationships. **Go deeper:** Heads are concatenated and projected; GQA/MQA share keys/values to shrink the KV cache.

### Q: How do transformers know word order?
**Short answer:** Positional information is added (sinusoidal, learned, or RoPE rotations). **Go deeper:** RoPE encodes relative position by rotating queries and keys and extrapolates better.

### Q: Why is attention O(n²) and how is it reduced?
**Short answer:** Every token attends to every token. **Go deeper:** FlashAttention keeps exact attention but avoids materialising the matrix; sliding-window, sparse, linear attention and state-space models (Mamba) change the scaling.

### Q: Encoder-only versus decoder-only versus encoder–decoder?
**Short answer:** Encoder-only (BERT) understands, decoder-only (GPT) generates, encoder–decoder (T5) translates. **Go deeper:** Decoder-only with a causal mask dominates LLMs.

### Q: How does a Vision Transformer work?
**Short answer:** Cut the image into patches, embed them as tokens, run a transformer. **Go deeper:** It lacks CNN inductive bias so needs more data or self-supervised pretraining.

### Q: What does a GNN do?
**Short answer:** Each node updates itself from messages sent by its neighbours. **Go deeper:** Used for scene graphs, multi-robot coordination, molecules and learned physics.

### Q: CNN versus ViT?
**Short answer:** CNNs bake in locality and work well with less data; ViTs are more flexible but data-hungry. **Go deeper:** Hybrid and ConvNeXt-style models close the gap.

### Q: What is a state-space model like Mamba?
**Short answer:** A sequence model based on a linear dynamical system processed in linear time. **Go deeper:** Selective state spaces make parameters input-dependent; promising for very long sequences.

## Generative models and representation learning

### Q: Explain a VAE.
**Short answer:** An autoencoder whose latent code is a distribution, trained to reconstruct while staying close to a prior. **Go deeper:** The loss is reconstruction plus KL (the negative ELBO); the reparameterisation trick lets gradients flow through sampling.

### Q: GAN training problems?
**Short answer:** Unstable and prone to mode collapse. **Go deeper:** WGAN, spectral normalisation and careful balancing help; diffusion models largely replaced GANs for images.

### Q: How do diffusion models work?
**Short answer:** Gradually add noise to data, then train a network to reverse each tiny step. **Go deeper:** Training predicts the noise (ε-prediction); sampling starts from noise and denoises; DDIM accelerates it.

### Q: Why use diffusion or flow matching for robot actions?
**Short answer:** Demonstrations are multimodal; averaging fails but sampling a coherent sequence works. **Go deeper:** Action chunks are generated jointly, giving smooth, consistent trajectories.

### Q: What is flow matching?
**Short answer:** Learn a velocity field that carries noise to data along simple paths. **Go deeper:** Regress v(x_t, t) to (data − noise) on a straight-line interpolation; sampling integrates the ODE in a few steps; used in π0.

### Q: What is contrastive learning (CLIP, SimCLR)?
**Short answer:** Pull matching pairs together and push others apart in embedding space. **Go deeper:** InfoNCE loss; CLIP aligns images with text, enabling zero-shot recognition.

### Q: What is self-supervised learning and why does it matter?
**Short answer:** Learning from labels created from the data itself (masking, augmentation). **Go deeper:** It gives general features (DINOv2, MAE) that make robot vision work with small datasets.

### Q: What is transfer learning and fine-tuning?
**Short answer:** Start from a pretrained model and adapt it to your task. **Go deeper:** Freeze early layers or use LoRA with a small learning rate to avoid forgetting.

### Q: What is knowledge distillation?
**Short answer:** Train a small student to imitate a big teacher. **Go deeper:** Soft targets carry more information than hard labels; used to deploy on edge devices.

### Q: How would you deploy a model on a Jetson?
**Short answer:** Export to ONNX, build a TensorRT engine with FP16/INT8, benchmark latency. **Go deeper:** Calibrate INT8 on real data, pin clocks, and re-validate accuracy after conversion.

### Q: What is the difference between training loss and a metric?
**Short answer:** The loss is what gradient descent minimises; the metric is what you care about. **Go deeper:** They may differ (cross-entropy versus accuracy, or success rate for a robot).

### Q: What is double descent?
**Short answer:** Test error can fall, rise, then fall again as model size grows past the interpolation point. **Go deeper:** Over-parameterised models can still generalise, partly due to implicit regularisation from SGD.

### Q: What are common data augmentations for robot vision?
**Short answer:** Random crops/shifts, colour jitter, blur, noise. **Go deeper:** Avoid flips when left/right matters; augment consistently across multiple cameras.
