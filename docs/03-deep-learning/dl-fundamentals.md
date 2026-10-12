---
title: DL Fundamentals & Training
---

# Deep Learning Fundamentals

:::tip[The 30-second version]
A neural network is a **stack of simple "blend-and-squash" steps**. Each layer mixes its inputs with adjustable weights, then squashes the result through a bend (an activation function). With enough layers, this can approximate almost any function: recognise a cup, steer a car, write a sentence.
**Training** = show examples, measure the error, and nudge every weight a tiny bit to reduce it. The "nudge direction" is computed by **backpropagation**.
:::

## One neuron, one layer

A neuron takes inputs $x$, multiplies each by a weight, adds them up, and applies a bend:

$$ a = \phi\,(w^\top x + b) $$

> **In words:** "weigh the evidence, add a bias, then decide how strongly to fire."

A **layer** is many neurons in parallel; a **network** is layers in a row. The bend $\phi$ is essential: without it, stacking layers collapses into one big linear function.

![activations](/img/fig/activations.svg)
*Common activation functions. ReLU is the fast default; GELU and SiLU are the smooth versions used in transformers and LLMs.*

## How it learns: the forward and backward pass

![backprop](/img/fig/backprop-flow.svg)
*Forward: compute the prediction and the error. Backward: send blame back through the layers.*

1. **Forward pass:** push the input through all layers, get a prediction.
2. **Loss:** one number saying how wrong it was (e.g. mean squared error, cross-entropy).
3. **Backward pass (backpropagation):** use the chain rule to ask each weight "how much did *you* contribute to the error?"
4. **Update:** nudge every weight against its blame (gradient descent / Adam).

$$ \frac{\partial L}{\partial W^{\ell}} = \delta^{\ell}\,(a^{\ell-1})^\top,\qquad \delta^{\ell}=\big((W^{\ell+1})^\top\delta^{\ell+1}\big)\odot\phi'(z^{\ell}) $$

> **In words:** the blame at a layer = the blame from the layer above, passed back through the same weights, scaled by how "awake" each neuron was.

## The training recipe (what to say in interviews)

![lr curves](/img/fig/lr-curves.svg)
*Learning rate is the most important knob. Too small: slow. Too big: unstable. A warm-up followed by a gradual decay (cosine) is the standard schedule.*

| Ingredient | Plain meaning | Go-to choice |
|---|---|---|
| **Optimizer** | how to use the gradients | **AdamW** (SGD + momentum for some vision) |
| **Learning-rate schedule** | change step size over time | warm-up → cosine decay |
| **Initialisation** | starting weights that keep signals healthy | He (ReLU) / Xavier (tanh) |
| **Normalisation** | keep activations well-scaled | **LayerNorm / RMSNorm** (transformers), BatchNorm (CNNs) |
| **Regularisation** | stop memorising | weight decay, dropout, data augmentation, label smoothing |
| **Mixed precision** | faster math with fewer bits | **bf16** (no loss-scaling needed) |
| **Gradient clipping** | cap crazy updates | clip norm at 1.0 |

### Debugging checklist (very interview-friendly)
1. **Overfit a single tiny batch first.** If it can't, you have a bug.
2. Look at the data and labels with your own eyes.
3. Loss at the start should be about $\log(\text{number of classes})$.
4. Watch grad-norm; NaNs usually mean learning rate too high, log(0), or bad data.
5. Compare train and validation curves (overfitting vs underfitting).

### Vanishing and exploding gradients
In a deep net, the blame signal is multiplied layer after layer. If each factor is < 1 it fades to nothing (**vanishing**); if > 1 it blows up (**exploding**). Cures: ReLU-family activations, **residual (skip) connections**, normalisation, sensible initialisation, gradient clipping.

## Scaling up training

| Technique | Plain idea |
|---|---|
| **Data parallel (DDP)** | each GPU holds a full model copy, sees different data, average gradients |
| **FSDP / ZeRO** | shard the model/optimizer state across GPUs to save memory |
| **Tensor / pipeline parallel** | split a huge model across GPUs (by matrix or by layer) |
| **Gradient checkpointing** | recompute instead of storing activations (memory ↔ compute trade) |
| **Gradient accumulation** | pretend to have a bigger batch by summing several small ones |
| **FlashAttention / `torch.compile`** | faster kernels, same math |

## Interview Q&A

**Why do residual connections help?**
*Simply:* they give the gradient a shortcut lane so deep networks stay trainable. *Deeper:* $y=x+F(x)$ gives $\partial y/\partial x = I+\partial F/\partial x$, so the identity path keeps gradients alive.

**BatchNorm vs LayerNorm?**
*Simply:* BatchNorm normalises across the batch; LayerNorm normalises within each example. *Deeper:* transformers and RL prefer LayerNorm because it doesn't depend on batch size or differ between train and test.

**Why Adam instead of plain SGD?**
*Simply:* Adam gives each weight its own step size, so it copes with messy landscapes with little tuning.

**What does dropout do at test time?**
*Simply:* nothing; it is switched off. (Scaling is handled during training.)

**What is label smoothing?**
*Simply:* instead of "100 % cat", say "90 % cat, 10 % spread elsewhere" so the model doesn't become over-confident.

**What is mixed precision?**
*Simply:* do most maths in a smaller number format for speed, keep a full-precision master copy of the weights for accuracy.
