# LexAnalytica: Project Synopsis & Methodology

## 1. Project Synopsis

**LexAnalytica** is an advanced, institutional-grade AI platform designed specifically for the legal domain. Legal professionals spend countless hours manually reading, analyzing, and finding connections across massive volumes of case laws, contracts, and filings. LexAnalytica automates this process by providing instant document summarization, extraction of critical legal entities, cross-document reasoning, and automatic quality evaluation of every analysis.

Upgraded with next-generation AI architectures — including **Graph RAG (Retrieval-Augmented Generation)**, **Legal-BERT**, **Neurosymbolic AI**, and an **Automatic Metric Evaluation Engine** — the system doesn't just read documents; it understands the complex relationships between laws, people, and precedents, measures the quality of its own output, and deduces legal outcomes with high accuracy. It natively supports both English and Hindi (Devanagari), seamlessly breaking language barriers in the Indian legal context.

---

## 2. System Requirements

### Hardware Requirements
- **CPU:** Multi-core processor (Intel i5/Ryzen 5 or higher recommended).
- **RAM:** Minimum 8 GB (16 GB strongly recommended due to large Transformer models in memory).
- **Storage:** At least 5 GB of free space to cache Hugging Face models (Legal-LED, Legal-BERT) and PaddleOCR models.

### Software Requirements
- **OS:** Windows 10/11.
- **Backend:** Python 3.9+
- **Frontend:** Node.js 16+ and npm
- **Core Dependencies (Python):** `fastapi`, `uvicorn`, `transformers`, `torch`, `networkx`, `paddleocr`, `langdetect`, `nltk`, `PyPDF2`, `reportlab`, `textstat`.

---

## 3. Methodology & AI Pipeline Architecture

LexAnalytica operates on a sophisticated multi-layered pipeline. Here is exactly how the underlying models work together:

### A. The Extraction Layer (`backend/nlp/extractor.py`)
When a user uploads a document, the system first extracts raw text based on the file type:
- **PDF** → `PyPDF2` reads the digital text stream directly, page by page.
- **TXT** → Read directly with UTF-8 encoding.
- **PNG / JPG / JPEG** → **PaddleOCR**, a deep learning-powered OCR engine, visually scans and transcribes the text — supporting both English and Hindi scripts.

### B. The Preprocessing Layer (`backend/nlp/preprocessor.py`)
Raw text is cleaned and prepared for AI models:
- **Language Detection**: `langdetect` identifies whether the document is in English or Hindi.
- **Text Cleaning**: Language-specific regex strips noise — preserving Devanagari Unicode (`\u0900–\u097F`) for Hindi, alphanumeric for English.
- **Sentence Splitting**: NLTK `sent_tokenize` for English; Purna Viram (`।`) splitting for Hindi.
- **Stopword Removal**: NLTK stopwords used for word frequency computation in extractive summarization.

### C. The Perception Layer — Legal-BERT NER (`backend/nlp/entities.py`)
To identify legal markers in the text, the system uses fine-tuned Hugging Face NER models:
- **English**: `dslim/bert-base-NER` — a BERT model trained on CoNLL-2003 for high-accuracy entity detection.
- **Hindi**: `Babelscape/wikineural-multilingual-ner` — a multilingual NER model.

The pipeline extracts `Persons`, `Organizations`, and `Locations`. Custom **regex fallbacks** extract structured legal entities — `Case Numbers` and `Law Sections` — from the full text with perfect reliability. Raw confidence scores from the HuggingFace pipeline are stored internally and passed to the Metric Evaluation Engine.

### D. The Synthesis Layer — Dual Summarization (`backend/nlp/summarizer.py`)
Two complementary summarization techniques run in parallel:

1. **Extractive Summary (TF-IDF)**: A mathematical approach — sentences are scored by normalized word frequency and ranked. The top-N sentences are returned in their original order. Works for both English and Hindi. No model download needed.

2. **Abstractive Summary (Legal-LED-16384)**: Uses the `nsi319/legal-led-base-16384` Longformer-Encoder-Decoder model fine-tuned on legal corpora. Standard models cap at 512 tokens (~400 words); Legal-LED handles **16,384 tokens (~12,000 words)** using sparse attention, enabling full-document understanding without truncation. It generates a brand-new, human-like summary in its own words. For Hindi documents, the system falls back to extractive summarization (the LED model is English-only).

### E. The Knowledge Layer — Graph RAG (`backend/nlp/graph_engine.py`)
Traditional AI systems have no memory across documents. LexAnalytica builds a **persistent in-memory Knowledge Graph** using `NetworkX DiGraph`:
- Each uploaded document becomes a central node.
- Every extracted entity (persons, orgs, case numbers, law sections) becomes a connected node.
- Relationships are typed: `MENTIONS_PERSON`, `CITES_CASE`, `REFERENCES_LAW`, etc.
- If multiple documents reference the same "Section 420" or "Company X", the graph connects them — enabling cross-document precedent retrieval via the `/api/query_graph` endpoint.

### F. The Reasoning Layer — Neurosymbolic AI (`backend/nlp/reasoning.py`)
Neural networks are excellent at reading but prone to hallucination. LexAnalytica mitigates this by combining neural extraction with **Symbolic Logic**:
- The `NeuroSymbolicEngine` contains strict forward-chaining rules defined as Python `lambda` conditions.
- Rules evaluate the extracted entity dictionary and fire deterministic conclusions:
  - `RULE_1_FRAUD`: Fraud-related sections + persons → HIGH severity flag
  - `RULE_2_NDA_BREACH`: Confidentiality context + persons → MEDIUM severity flag
  - `RULE_3_CORPORATE_DISPUTE`: Multiple organizations + law sections → INFO flag
- No hallucination possible — conclusions are only fired when conditions are strictly met.

### G. The Evaluation Layer — Metric Engine (`backend/nlp/metrics.py`)
A new addition: after every analysis, the system automatically evaluates the quality of its own output across 5 categories — **no reference summary required**:

| Category | Metrics |
|----------|---------|
| **Summarization** | Compression Ratio, Sentence Coverage % |
| **Document Quality** | Flesch-Kincaid Readability Score, Grade Level, Lexical Diversity |
| **NER Confidence** | Avg / Min / Max confidence scores, Entity Category Coverage |
| **Performance** | Per-step processing time (Extraction, NER, Summarization, Reasoning, Total) |
| **Graph RAG** | Graph Density, Connected Components, Node/Edge counts |

Results are shown in a color-coded **Evaluation Metrics** panel in the dashboard.

---

## 4. Codebase Explanation (File-by-File)

LexAnalytica follows a clean **decoupled architecture** with a dedicated `backend/` and `frontend/` folder.

### Backend (`backend/` directory)

#### `backend/app.py`
The central API gateway. Runs the FastAPI web server on port 8000. It:
- Exposes `/api/summarize`, `/api/query_graph`, and `/api/download/pdf` endpoints.
- Wraps every pipeline step with `time.perf_counter()` for precise timing.
- Orchestrates the full pipeline: extraction → NER → summarization → graph → reasoning → metrics.
- Strips the internal `_raw_ner` key before returning the API response.
- Serves the React build from `../frontend/dist/` as static files.

#### `backend/requirements.txt`
All Python dependencies:
- `fastapi` & `uvicorn`: High-performance async web server.
- `python-multipart`: File upload handling.
- `transformers` & `torch`: Loads and runs Legal-BERT and Legal-LED neural networks.
- `PyPDF2`: Extracts text from digital PDF files.
- `nltk`: Sentence tokenization and stopword removal.
- `langdetect`: Automatic language detection (English vs Hindi).
- `deep-translator`: Google Translate integration for bilingual output.
- `paddlepaddle` & `paddleocr`: Deep learning OCR for scanned images.
- `reportlab`: Generates downloadable Unicode PDF reports with Devanagari support.
- `numpy`: Mathematical array operations for AI models.
- `networkx`: In-memory directed Knowledge Graph for Graph RAG.
- `textstat`: Flesch-Kincaid readability and grade level computation.

### The NLP Intelligence Layer (`backend/nlp/`)

- **`extractor.py`**: Routes files by extension to the correct reader — PyPDF2 for PDFs, UTF-8 for TXT, PaddleOCR for images.
- **`preprocessor.py`**: Language detection, Unicode-aware text cleaning, sentence splitting, and word frequency computation for extractive summarization.
- **`entities.py`**: HuggingFace NER pipeline (lazy-loaded) + regex fallbacks for case numbers and law sections. Stores raw NER confidence scores in `_raw_ner` for the metrics engine.
- **`summarizer.py`**: TF-IDF extractive summarization + Legal-LED-16384 abstractive summarization with global attention mask and beam search decoding.
- **`graph_engine.py`**: Singleton `GraphEngine` class. Builds a `nx.DiGraph` from entities, supports typed relationship edges, and provides `query_graph()` for keyword-based entity-document retrieval.
- **`reasoning.py`**: Singleton `NeuroSymbolicEngine` with 3 forward-chaining rules. Evaluates entity facts and returns severity-tagged legal deductions.
- **`generator.py`**: ReportLab PDF builder. Auto-registers Devanagari Unicode fonts (Noto, Lohit, FreeSerif) for Hindi output, falls back to Helvetica for English-only.
- **`metrics.py`**: Master metric evaluation module. Computes compression ratio, sentence coverage, Flesch-Kincaid, lexical diversity, NER confidence stats, entity coverage, processing time dict, and graph density stats. All metrics are self-contained — no external reference needed.

### The Frontend Dashboard (`frontend/` directory)

- **`frontend/src/App.jsx`**: Single-page React application. Manages the full UI lifecycle — upload form → loading indicator with step progress → results dashboard. Renders entity pills, dual summaries, neurosymbolic deduction cards, and the new color-coded **Evaluation Metrics** panel (`MetricsPanel` component). PDF download is handled via a Blob fetch from `/api/download/pdf`.
- **`frontend/src/index.css`**: Global dark-theme CSS with glassmorphism variables, custom component classes, and animation utilities.
- **`frontend/src/App.css`**: Component-level CSS overrides.
- **`frontend/package.json`** & **`vite.config.js`**: Vite 5 + React 18 configuration. The built `dist/` folder is served by FastAPI as static files.
