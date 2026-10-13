---
title: "Q&A 4: LLM, VLM & VLA"
---

# Interview Q&A: LLM, VLM, VLA and Foundation Models

:::tip[How to use]
Chapters: [LLM](../05-foundation-models/llm.md) · [VLM & VLA](../05-foundation-models/vlm-vla.md) · [Build an AI model](../build-your-own/01-build-an-ai-model.md) · [Build a VLM](../build-your-own/02-build-a-vlm.md) · [Build a VLA](../build-your-own/03-build-a-vla.md).
:::

## LLMs

### Q: How is an LLM trained?
**Short answer:** Pretrain to predict the next token on huge text, then fine-tune on instructions, then align with human preferences. **Go deeper:** Pretraining → SFT → RLHF/DPO → (optionally) RL with verifiable rewards for reasoning.

### Q: What are scaling laws?
**Short answer:** Loss falls smoothly as a power law with more parameters, data and compute. **Go deeper:** Chinchilla: scale data with model size (~20 tokens per parameter for compute-optimal); in practice small models are over-trained for cheaper inference.

### Q: How much compute does training take?
**Short answer:** About 6 × N × D FLOPs (parameters × tokens). **Go deeper:** Divide by GPU peak FLOPs × utilisation (30–50 %) for time.

### Q: What is tokenisation and why subwords?
**Short answer:** Text is split into pieces (BPE) that balance vocabulary size and sequence length. **Go deeper:** Subwords handle rare words without unknown tokens; tokenisation quirks affect arithmetic and non-English text.

### Q: What is the KV cache?
**Short answer:** Stored keys and values of past tokens so decoding doesn't recompute them. **Go deeper:** Memory ≈ 2 × layers × tokens × KV heads × head size × bytes; GQA/MQA shrink it; paged attention manages it.

### Q: Why is LLM decoding memory-bandwidth-bound?
**Short answer:** Each step makes one token but must read all weights and the KV cache. **Go deeper:** Batching amortises weight reads; speculative decoding and quantisation help.

### Q: What is speculative decoding?
**Short answer:** A small model drafts several tokens and the big model verifies them in one pass. **Go deeper:** Output is identical in distribution but latency drops when drafts are accepted.

### Q: What are top-k, top-p and temperature?
**Short answer:** Sampling controls: restrict to the k best tokens, to the smallest set with probability p, and scale randomness. **Go deeper:** Low temperature is more deterministic; top-p adapts the cut-off.

### Q: How does LoRA work?
**Short answer:** Freeze the model and learn small low-rank matrices added to its weights. **Go deeper:** W + BA with rank r ≪ d; trains ~0.1–1 % of parameters, mergeable at inference; QLoRA adds a 4-bit base.

### Q: SFT, RLHF, DPO: how do they differ?
**Short answer:** SFT imitates good answers; RLHF optimises a learned reward from human preferences; DPO optimises preferences directly with a simple loss. **Go deeper:** DPO is offline and simpler; RLHF with PPO can explore online but is more complex.

### Q: How do reasoning models differ?
**Short answer:** They are trained with RL on checkable tasks to produce long chains of thought. **Go deeper:** They use more test-time compute (longer thinking, sampling, search) to improve accuracy.

### Q: What is RAG and when does it fail?
**Short answer:** Retrieve relevant documents and give them to the model as context. **Go deeper:** Failures: bad chunking, retrieval misses, answer buried in the middle, stale index; evaluate retrieval and generation separately.

### Q: RAG versus fine-tuning?
**Short answer:** RAG adds knowledge at query time; fine-tuning changes behaviour and style. **Go deeper:** Use RAG for fresh or private facts; fine-tune for format, tone and skills; often use both.

### Q: How do you reduce hallucinations?
**Short answer:** Ground answers in retrieved sources or tools, require citations, verify, and allow "I don't know". **Go deeper:** Constrained decoding, self-consistency, and calibrated abstention also help.

### Q: What is a mixture of experts?
**Short answer:** Many expert sub-networks with a router that activates a few per token. **Go deeper:** Large total parameters but low compute per token; issues are load balancing and expert-parallel communication.

### Q: What is quantisation and what are the trade-offs?
**Short answer:** Storing weights in fewer bits (8, 4) to save memory and speed up inference. **Go deeper:** AWQ/GPTQ/FP8 lose little accuracy; always re-evaluate after quantising.

### Q: How would you evaluate an LLM application?
**Short answer:** Build a held-out set of real tasks with clear scoring, compare against baselines, and review failures. **Go deeper:** Use exact match or rubrics; LLM-as-judge has length/position bias; track regression on each change.

### Q: What is prompt injection?
**Short answer:** Untrusted text overriding the model's instructions. **Go deeper:** Mitigate by separating data from instructions, least-privilege tools, output validation and human confirmation for risky actions.

### Q: What is an agent?
**Short answer:** An LLM in a loop that thinks, calls tools, reads results and repeats. **Go deeper:** Components: tools/function calling, memory, planner, guardrails; evaluate end to end (SWE-bench, tau-bench).

### Q: How can LLMs help in robotics safely?
**Short answer:** Let the LLM propose, a validator or simulator verify, and classical control execute. **Go deeper:** Examples: SayCan, Code-as-Policies, LLM+P with PDDL validation, Eureka for reward design.

## VLMs

### Q: What are the parts of a VLM?
**Short answer:** A vision encoder, a connector and an LLM. **Go deeper:** SigLIP/CLIP encoder → MLP or Q-Former → LLM; image tokens are spliced into the text sequence.

### Q: How is a VLM trained?
**Short answer:** Stage 1 aligns the connector on captions; stage 2 instruction-tunes on visual Q&A. **Go deeper:** LLaVA-1.5: stage 1 trains only the connector (lr 1e-3), stage 2 trains connector + LLM (lr 2e-5).

### Q: Why freeze the vision encoder?
**Short answer:** It is already a strong pretrained feature extractor; training it on small data can damage it. **Go deeper:** Don't freeze an untrained encoder (shown in this book's tiny-VLM experiments).

### Q: How many tokens does an image use?
**Short answer:** Hundreds: a 384 px image with patch 14 gives 729. **Go deeper:** Pixel-shuffle reduces by 4×; AnyRes tiling multiplies tokens for high resolution.

### Q: What is loss masking in VLM training?
**Short answer:** Compute loss only on the answer tokens. **Go deeper:** Mask prompt, image placeholders and padding with −100 labels.

### Q: How do you test that a VLM really uses the image?
**Short answer:** Replace the image with a blank or wrong one and see whether the answer changes. **Go deeper:** If it doesn't, the model relies on language priors.

### Q: What causes VLM hallucination and how do you reduce it?
**Short answer:** Language priors and weak grounding. **Go deeper:** Add negative examples, POPE-style data, higher resolution, and preference tuning on hallucination pairs.

### Q: What is CLIP and why does it matter?
**Short answer:** A model that embeds images and text in one space via contrastive training. **Go deeper:** It enables zero-shot classification and open-vocabulary perception for robots.

### Q: What does a connector do?
**Short answer:** It translates vision features into the LLM's embedding space. **Go deeper:** An MLP is simple and strong; Q-Former or resamplers produce a fixed number of tokens.

## VLAs

### Q: VLM versus VLA?
**Short answer:** A VLM outputs text; a VLA outputs robot actions. **Go deeper:** A VLA adds an action head and trains on robot trajectories.

### Q: How do VLAs represent actions?
**Short answer:** As discrete tokens, as regressed values, or via a diffusion/flow-matching head. **Go deeper:** Tokens (RT-2, OpenVLA, FAST) reuse the LLM head; flow matching (π0) gives smooth continuous chunks.

### Q: Why action chunking?
**Short answer:** Predicting several steps at once gives smoother motion, fewer model calls and less compounding error. **Go deeper:** Tested here: chunk length 8 raised success from 83 % to 98 % in a toy task.

### Q: Why use a dual-system design?
**Short answer:** A big model is too slow for control, so a slow reasoner guides a fast action policy. **Go deeper:** E.g. ~10 Hz VLM plus ~100+ Hz policy (Helix, GR00T N1).

### Q: Why flow matching or diffusion for the action head?
**Short answer:** Demonstrations are multimodal; generative heads sample coherent actions instead of averaging. **Go deeper:** π0's action expert attends to VLM features and takes ~10 flow steps.

### Q: How did RT-2 transfer web knowledge to control?
**Short answer:** It co-trained on web VQA and robot data with actions written as text tokens. **Go deeper:** Semantic reasoning ("pick the extinct animal") reuses language knowledge.

### Q: What data do VLAs need?
**Short answer:** Teleoperated demonstrations, ideally diverse, plus language labels. **Go deeper:** Also human video, simulation (MimicGen, Isaac Lab Mimic), and pooled datasets (Open X-Embodiment, DROID).

### Q: How do you evaluate a VLA?
**Short answer:** Many closed-loop trials with success rates and confidence intervals on new objects, positions, lighting and phrasing. **Go deeper:** Use benchmarks (LIBERO, SimplerEnv) and tag failure types.

### Q: Typical VLA failure modes?
**Short answer:** Ignoring the instruction, poor spatial precision, out-of-distribution fragility, compounding errors. **Go deeper:** Run a "wrong instruction" test and a perturbation suite.

### Q: How would you add touch or force to a VLA?
**Short answer:** Add tactile/force history as tokens and keep a compliant low-level controller. **Go deeper:** Contact-rich tasks benefit from impedance control plus tactile feedback.

### Q: What is the data flywheel?
**Short answer:** Deploy, collect failures, add targeted data, retrain, repeat. **Go deeper:** Human takeover segments (HG-DAgger) are especially valuable.

### Q: What is a world model for robotics?
**Short answer:** A model that predicts what happens next, used for planning, data generation and policy evaluation. **Go deeper:** Cosmos, Dreamer, V-JEPA 2.

### Q: How would you fine-tune a VLA for a new robot arm?
**Short answer:** Collect ~50–200 demos, fine-tune a pretrained policy (SmolVLA/π0/ACT) with matched action spaces and normalisation. **Go deeper:** Validate with ACT first, then compare against the VLA with an identical evaluation protocol.

### Q: Why is asynchronous inference useful?
**Short answer:** The robot keeps executing the current chunk while the next one is computed. **Go deeper:** It hides model latency; blend chunk boundaries to avoid jerks.
