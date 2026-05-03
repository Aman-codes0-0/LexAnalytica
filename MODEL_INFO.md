# LexAnalytica — Model Intelligence Report

This document explains all AI models and evaluation techniques used in LexAnalytica.

---

## 🧠 Model 1: Legal-LED-16384 (Abstractive Summarization)

- **Full Name**: `nsi319/legal-led-base-16384`
- **File**: `backend/nlp/summarizer.py`
- **Architecture**: LED (Longformer Encoder-Decoder)
- **Specialization**: Fine-tuned on massive datasets of legal documents — court judgments, contracts, and filings.

### Key Advantages
1. **Long Context Support**:
   - Traditional models (like BART) can only process ~1,000 words.
   - **Legal-LED** supports up to **16,384 tokens** (approx. 12,000–15,000 words).
   - This prevents "context truncation" where the end of a long legal document is ignored.
2. **Domain-Specific Vocabulary**:
   - Understands legal jargon, case citations, and judicial language far better than general-purpose AI models.

### Implementation Details

#### A. Global Attention Mask
The model uses **Sparse Attention** to handle long documents efficiently. We manually set **Global Attention** on the first token (`BOS token`) to ensure the model reads the full document structure during generation.

```python
# backend/nlp/summarizer.py
global_attention_mask = torch.zeros_like(attention_mask)
global_attention_mask[:, 0] = 1  # Global attention on the first token
```

#### B. Decoding Strategy
**Beam Search** with 4 beams and a **Length Penalty** of 2.0.
- **Beam Search**: Explores multiple word sequences to find the most coherent summary.
- **Length Penalty**: Encourages more detailed summaries rather than very short ones.
- **No-Repeat N-gram**: `no_repeat_ngram_size=3` prevents repetitive phrases.

#### C. Lazy Loading
The model is not loaded at server startup — it loads only on the first abstractive summarization request. This keeps the initial startup fast and avoids unnecessary RAM usage.

---

## 🏷️ Model 2: Legal-BERT NER (Named Entity Recognition)

- **English Model**: `dslim/bert-base-NER`
- **Hindi Model**: `Babelscape/wikineural-multilingual-ner`
- **File**: `backend/nlp/entities.py`
- **Task**: Token Classification (Named Entity Recognition)
- **Strategy**: `aggregation_strategy="simple"` — merges sub-word tokens into full entity words

### What It Extracts
| Label | Entity Type |
|-------|------------|
| `PER` | Persons (judges, parties, witnesses) |
| `ORG` | Organizations (courts, companies, firms) |
| `LOC` | Locations (cities, states, jurisdictions) |

### Regex Fallbacks
In addition to the NER model, custom regex patterns extract structured legal entities that NER often misses:
- **Case Numbers**: `Civil No. 123/2024`, `Writ Petition 45/2023`
- **Law Sections**: `Section 420 IPC`, `Sec. 302 of IPC`

### Confidence Score Exposure
Raw NER results (with per-entity confidence scores) are stored internally as `_raw_ner` and passed to the **Metric Evaluation Engine** before being stripped from the API response.

---

## 📐 Model 3: Extractive Summarizer (TF-IDF)

- **File**: `backend/nlp/summarizer.py`
- **Type**: Statistical (no neural network required)
- **Algorithm**: TF-IDF sentence scoring with log-normalized length penalty

### How It Works
1. Split text into sentences using NLTK `sent_tokenize`
2. Compute word frequency distribution (stopwords removed)
3. Score each sentence: `score = Σ(word_freq) / log(sentence_length + 1)`
4. Return the top-N highest-scoring sentences in their original order

This is fast, explainable, and works for both English and Hindi documents without requiring a model download.

---

## 📊 Metric Evaluation Engine

- **File**: `backend/nlp/metrics.py`
- **Type**: Automatic (no reference summary required)
- **Library**: `textstat` (Flesch-Kincaid), `networkx` (graph metrics), Pure Python (others)

### Metrics Computed

| Metric | Method | Description |
|--------|--------|-------------|
| **Compression Ratio** | `len(summary) / len(original) × 100` | How compressed the summary is |
| **Sentence Coverage** | Keyword overlap between sentences and summary | How representative the summary is |
| **Flesch-Kincaid Score** | `textstat.flesch_reading_ease()` | Readability of the original document |
| **Grade Level** | `textstat.text_standard()` | Estimated education level needed to read |
| **Lexical Diversity** | `unique_words / total_words` | Vocabulary richness (Type-Token Ratio) |
| **NER Avg Confidence** | Mean of HF pipeline `score` field | Model certainty for entity predictions |
| **Entity Coverage %** | Filled categories / 6 total | Breadth of entity extraction |
| **Processing Time** | `time.perf_counter()` per step | Per-step and total pipeline duration |
| **Graph Density** | `networkx.density(graph)` | Interconnectedness of the knowledge graph |
| **Connected Components** | `nx.number_weakly_connected_components()` | Isolated subgraph count |

### Summary Logic Flow (Full Pipeline)

```
Upload
  │
  ▼
extractor.py       → Raw text (PDF / TXT / OCR)          [t0 → t1]
  │
  ▼
preprocessor.py    → Language detection, sentence split
  │
  ▼
entities.py        → NER entities + _raw_ner scores       [t2 → t3]
  │
  ▼
summarizer.py      → Extractive + Abstractive summary     [t4 → t5]
  │
  ▼
reasoning.py       → Neurosymbolic deductions             [t6 → t7]
  │
  ▼
metrics.py         → 10 automatic quality metrics
  │
  ▼
API Response       → JSON with all results + "metrics" key
```
