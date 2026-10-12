---
title: Large Language Models
---

# LLMs End-to-End

:::tip[The 30-second version]
An LLM is a giant **next-word predictor**. It read a huge slice of the internet and learned to guess the next token. That single skill, at huge scale, turns out to produce reasoning, coding and conversation. After that, extra training (fine-tuning and human feedback) makes it *helpful* rather than just fluent.
:::

## From raw text to assistant

![LLM pipeline](/img/fig/llm-training-pipeline.svg)
*The standard recipe. Each stage changes the model's behaviour, not its basic architecture.*

### 1. Pretraining: learn language and world knowledge
Text is cut into **tokens** (word pieces, via BPE/SentencePiece). The model is trained to predict each token from the previous ones.

$$ \mathcal L = -\sum_t \log p(x_t\mid x_{<t}) $$

> **In words:** "reward the model for putting high probability on the word that actually came next."

**Scaling laws:** more parameters, more data and more compute make loss fall smoothly and predictably. *Chinchilla* showed you should scale data with model size (~20 tokens per parameter for compute-optimal; in practice small models are over-trained so they are cheap to run).

![scaling law](/img/fig/scaling-law.svg)
*Bigger model and more data both lower the loss, with diminishing returns.*

Typical modern recipe ("LLaMA-style"): RMSNorm, RoPE positions, SwiGLU, grouped-query attention. **Mixture-of-Experts (MoE)**: many "expert" sub-networks, a router picks a few per token → huge capacity at modest compute (Mixtral, DeepSeek).

Training compute is roughly $6\times N\times D$ FLOPs (N parameters, D tokens).

### 2. Post-training: make it useful and safe
| Stage | What it does |
|---|---|
| **SFT** (supervised fine-tuning) | show good instruction → answer examples |
| **RLHF / DPO** | learn from human preference pairs (A is better than B) |
| **GRPO / RLVR** | RL on tasks with checkable answers (math, code) → strong **reasoning** |
| **PEFT: LoRA / QLoRA** | train tiny add-on matrices instead of all weights |

> **LoRA in words:** freeze the big model; learn a small low-rank correction $W+BA$. A few million trainable numbers can steer a 70B model.

## Serving: why inference is a different problem

![KV cache](/img/fig/kv-cache.svg)
*Without a cache the model recomputes the whole past for every new word. The KV cache stores each token's keys and values so only the new token costs work.*

- **Prefill** (reading the prompt) is compute-bound; **decode** (generating one token at a time) is **memory-bandwidth-bound**.
- Speed-ups: KV cache, **paged attention (vLLM)**, continuous batching, speculative decoding (a small model drafts, the big one verifies), FlashAttention, prefix caching.
- **Quantisation:** store weights in 8/4 bits (GPTQ, AWQ, FP8) to cut memory and cost.
- **Sampling:** greedy, temperature, top-k, top-p (nucleus), constrained decoding for JSON/tool calls.
- **Metrics:** time-to-first-token, tokens/second, cost per million tokens.

## Using LLMs: prompting, RAG, agents

### RAG: give the model an open book

![RAG](/img/fig/rag-flow.svg)
*Search your own documents, hand the best passages to the LLM, and let it answer from them with citations.*

Typical failures: bad chunking, retrieval misses, the answer buried in the middle ("lost in the middle"), stale index. Fixes: hybrid search (BM25 + embeddings), re-ranking, better chunk sizes, evaluating *retrieval* separately from *generation*.

### Agents
An agent loops: **think → call a tool → read the result → think again**, until done. Pieces: tool/function calling, memory, planner, guardrails, MCP (a standard for connecting tools). Benchmarks: SWE-bench, tau-bench.

### LLMs in robotics
- **Task planning:** SayCan, Code-as-Policies, Inner Monologue.
- **Natural language to PDDL:** LLM+P, with a validator that checks the plan.
- **Reward design:** Eureka writes reward functions for RL.
- **Interfaces:** voice control of ROS 2, scene description, failure explanation.
- **Rule of thumb:** let the LLM *propose*, let a symbolic checker or simulator *verify*, let classical control *execute safely*.

## Risks and evaluation
Hallucination (confidently wrong), prompt injection, jailbreaks, data contamination in benchmarks, LLM-as-judge bias (prefers longer answers). Benchmarks: MMLU, GSM8K, HumanEval, GPQA, SWE-bench. Always evaluate on *your* task.

## Interview Q&A

**Why is generation memory-bound?**
*Simply:* each step makes one token but must read all weights and the whole KV cache. Batching shares the weight reads across requests.

**How does LoRA work?**
*Simply:* freeze the model, learn a small correction. *Deeper:* the weight change has low intrinsic rank, so $r(d+k)$ numbers replace $dk$.

**RLHF vs DPO?**
*Simply:* RLHF trains a reward model and then optimises against it with RL; DPO folds that into one simple supervised-style loss on preference pairs. DPO is simpler; RLHF can reach higher with online sampling.

**How do you reduce hallucinations?**
*Simply:* ground the model in retrieved documents or tools, make it cite sources, verify outputs, and allow it to say "I don't know".

**Why top-p sampling?**
*Simply:* cut off the unlikely tail of words dynamically so the output stays sensible but still varied.

**What is the KV cache memory cost?**
*Simply:* it grows with tokens × layers × KV heads; GQA/MQA shrink it by sharing keys and values.
