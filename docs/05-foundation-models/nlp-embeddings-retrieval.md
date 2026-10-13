---
title: NLP Basics, Embeddings & Retrieval
---

# NLP Basics, Embeddings and Retrieval

:::tip[The 30-second version]
Computers can't read words, so we turn text into **numbers**: first into **tokens**, then into **embeddings** (vectors where similar meanings sit close together). With embeddings you can **search by meaning**, build **RAG** systems, cluster documents, and feed language to robots. This page is the toolkit behind the LLM chapter.
:::

## From text to numbers

| Step | What happens | Example |
|---|---|---|
| **Normalise** | lower-case, fix spacing, handle Unicode | "Pick-Up" → "pick-up" |
| **Tokenise** | split into tokens (words, subwords, bytes) | "unpicked" → "un", "pick", "ed" |
| **Map to IDs** | each token gets an integer | "pick" → 3721 |
| **Embed** | each ID becomes a learned vector | 3721 → [0.12, −0.8, …] |

**Tokenisation methods:** word-level (large vocabularies, unknown words), **BPE** (merge frequent pairs; GPT/LLaMA), **WordPiece** (BERT), **SentencePiece/Unigram**, **byte-level** (never an unknown token). Subwords balance vocabulary size against sequence length; numbers and rare languages tokenise inefficiently.

## Embeddings: meaning as geometry

An **embedding** maps an item to a vector so that similar items are near each other.

| Type | Examples | Notes |
|---|---|---|
| **Word embeddings** | Word2Vec, GloVe, fastText | one vector per word, context-free |
| **Contextual embeddings** | BERT, transformer hidden states | the same word gets different vectors in different sentences |
| **Sentence / document embeddings** | sentence-transformers, OpenAI/other embedding models, E5, BGE | one vector per passage; used for search |
| **Multimodal embeddings** | CLIP, SigLIP | text and images in one space |

**Similarity measures**

$$ \cos(a,b)=\frac{a\cdot b}{\|a\|\,\|b\|} $$

> **In words:** cosine similarity is the angle between two vectors; 1 means pointing the same way (same meaning), 0 unrelated.

Dot product and Euclidean distance are alternatives (equivalent for normalised vectors).

## Classic text representations (still useful)

| Method | Idea | Use |
|---|---|---|
| **Bag of words** | count words, ignore order | baselines |
| **TF-IDF** | boost words frequent here, rare elsewhere | keyword search, classifiers |
| **BM25** | improved TF-IDF ranking function | the standard keyword ranker |
| **n-grams** | sequences of n tokens | language models before neural nets |

## Retrieval: finding the right text

### Vector search
Store each document chunk's embedding in an index, embed the query, return the nearest neighbours.

| Index | Idea | Trade-off |
|---|---|---|
| **Flat (exact)** | compare with everything | exact but slow for millions |
| **IVF** | cluster vectors, search the nearest clusters | fast, slight recall loss |
| **HNSW** | layered small-world graph | very fast, high recall, more memory |
| **Product quantisation** | compress vectors | memory savings |

Tools: **FAISS**, HNSWlib, pgvector, Qdrant, Milvus, Weaviate, Elasticsearch/OpenSearch (hybrid).

### A good retrieval pipeline
1. **Chunk** documents (200–1000 tokens, with overlap; respect headings).
2. **Embed** chunks and store them with metadata.
3. **Hybrid search:** combine BM25 (exact terms) and dense vectors (meaning).
4. **Re-rank** the top results with a cross-encoder.
5. **Generate** the answer from the top passages with citations (RAG).
6. **Evaluate**: retrieval recall@k and MRR; answer faithfulness and relevance.

## Core NLP tasks

| Task | Typical approach |
|---|---|
| **Classification** (intent, sentiment) | fine-tune an encoder or prompt an LLM |
| **Named-entity recognition** | token classification |
| **Question answering** | extractive (span) or generative (LLM) |
| **Summarisation / translation** | encoder–decoder or LLM |
| **Semantic search / clustering** | embeddings + nearest neighbours / k-means |
| **Information extraction to JSON** | LLM with constrained decoding |
| **Speech** | Whisper-style encoder–decoder for ASR; TTS models for synthesis |

**Metrics:** accuracy/F1, BLEU/ROUGE (overlap, weak for generation), BERTScore, human or LLM-judge rubrics, retrieval recall@k, perplexity (language models).

## Language for robots

- **Instruction following:** VLAs embed the instruction with the VLM's text tower.
- **Open-vocabulary perception:** CLIP-style embeddings let "the red mug" match image regions.
- **Semantic maps and memory:** store embeddings of what the robot saw (ConceptFusion, VLMaps) and query them by language.
- **Speech interfaces:** ASR → intent → planner → TTS, with confirmation for risky actions.

## Interview Q&A

**What is an embedding?**
*Simply:* a vector where similar things are close. *Deeper:* learned so that distances reflect semantic similarity.

**Dense versus sparse retrieval?**
*Simply:* dense matches meaning; sparse (BM25) matches exact words. *Deeper:* hybrid usually wins; rerank with a cross-encoder.

**Why chunk documents?**
*Simply:* embeddings and context windows work best on focused passages. *Deeper:* chunk size and overlap trade precision against context.

**TF-IDF intuition?**
*Simply:* words that are frequent in this document but rare overall are the informative ones.

**How do you evaluate RAG?**
*Simply:* measure retrieval and generation separately. *Deeper:* recall@k, faithfulness to sources, answer relevance, latency and cost.

**Why does tokenisation matter?**
*Simply:* it sets sequence length and how well rare words and numbers are handled.
