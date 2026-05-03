# LexAnalytica — AI-Powered Legal Document Intelligence

> **Institutional-grade AI platform for legal document summarization, entity extraction, bi-lingual analysis, and automatic metric evaluation.**

LexAnalytica is a full-stack web application that combines a **FastAPI** backend with a **React + Vite** frontend to help legal professionals analyze documents in seconds. Upload a PDF, DOCX, TXT, or **scanned image (PNG/JPG)** and get a professional AI-generated report with key findings, entity extraction, neurosymbolic deductions, and downloadable PDF output — with full **English & Hindi (Devanagari)** support.

Upgraded with **Graph RAG**, **Neurosymbolic AI**, and an **Automatic Metric Evaluation Engine** — the system now connects precedents across documents, deduces legal outcomes without hallucination, and measures the quality of every analysis automatically.

---

## 🌟 Features

| Feature | Description |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 🧠 **Neural Summarization** | Specialized **Legal-LED-16384** model (16k context) for high-accuracy AI synthesis. |
| 🏷️ **Legal-BERT NER** | Extracts Judges, Case Numbers, Sections of Law, Parties, Dates, and Organizations using Hugging Face pipelines. |
| 🕸️ **Graph RAG** | Connects all extracted documents and entities into an in-memory Knowledge Graph (NetworkX) for relational queries. |
| ⚖️ **Neurosymbolic Logic** | Forward-chaining reasoning engine applies strict legal logic to extracted facts to deduce outcomes without hallucination. |
| 📊 **Metric Evaluation** | Auto-computes 8 quality metrics per analysis — readability, NER confidence, compression ratio, processing time & more. |
| 🌐 **Bi-lingual Support** | Native Hindi (Devanagari) & English document processing + cross-language translation. |
| 🖼️ **OCR Support** | Scanned image files (PNG, JPG, JPEG) processed via PaddleOCR. |
| 📄 **PDF Export** | Professional Unicode PDF reports with full Devanagari rendering. |
| 🌙 **Dark UI** | Premium dark-themed React dashboard with real-time feedback and color-coded metric visualization. |

---

## 🏗️ Tech Stack & Architecture

```
LexAnalytica/
│
├── backend/                        # All server-side code
│   ├── app.py                      # FastAPI main server & API gateway
│   ├── requirements.txt            # Python dependencies
│   ├── uploads/                    # Temporary file staging (auto-cleaned)
│   │
│   └── nlp/                        # Modular NLP intelligence layer
│       ├── __init__.py
│       ├── extractor.py            # PDF/DOCX/TXT/Image (OCR) text extraction
│       ├── preprocessor.py         # Text cleaning, sentence splitting, language detection
│       ├── entities.py             # Hugging Face Legal-BERT Named Entity Recognition
│       ├── summarizer.py           # Legal-LED-16384 summarization (extractive + abstractive)
│       ├── graph_engine.py         # NetworkX Knowledge Graph & Graph RAG
│       ├── reasoning.py            # Neurosymbolic Forward-Chaining Logic Engine
│       ├── generator.py            # PDF (ReportLab) report generation
│       └── metrics.py              # Automatic Metric Evaluation Engine (8 metrics)
│
└── frontend/                       # React + Vite UI
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.jsx                # React entry point
        ├── App.jsx                 # Main React application & MetricsPanel component
        ├── index.css               # Global dark-theme CSS
        └── App.css
```

**Backend:** FastAPI · Uvicorn · Hugging Face Transformers (Legal-BERT, Legal-LED) · NetworkX · Deep-Translator · PaddleOCR · textstat · ReportLab  
**Frontend:** React 18 · Vite 5 · Lucide Icons · Custom CSS (glassmorphism dark theme)

---

## 📊 Metric Evaluation Engine

Every document analysis automatically computes the following metrics — **no reference summary required**:

| Category | Metric | Description |
| ------------------- | ---------------------- | ----------------------------------------------------- |
| **Summarization** | Compression Ratio | % of original text length the summary occupies |
| **Summarization** | Sentence Coverage | % of original sentences referenced in the summary |
| **Document Quality** | Flesch-Kincaid Score | Readability score (0–100, higher = easier to read) |
| **Document Quality** | Grade Level | Estimated reading grade level |
| **Document Quality** | Lexical Diversity | Unique words / Total words (Type-Token Ratio) |
| **NER Confidence** | Avg / Min / Max Score | HuggingFace model confidence for entity predictions |
| **NER Confidence** | Entity Coverage | How many of the 6 entity categories were populated |
| **Processing Time** | Per-step timing | Extraction, NER, Summarization, Reasoning durations |
| **Graph RAG** | Graph Density | Edge density of the knowledge graph |
| **Graph RAG** | Connected Components | Number of disconnected subgraphs |

Metrics are displayed in a color-coded panel in the results dashboard: 🟢 green = good, 🟡 amber = acceptable, 🔴 red = needs attention.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| ------ | ------------------- | --------------------------------------------------------------------------- |
| `POST` | `/api/summarize` | Upload a document — returns analysis + entities + deductions + **metrics** |
| `GET` | `/api/query_graph` | Query the NetworkX Knowledge Graph for related entities/docs |
| `POST` | `/api/download/pdf` | Download analysis as PDF |

### Sample Response Structure (`/api/summarize`)

```json
{
  "filename": "contract.pdf",
  "language": "English",
  "word_count": 4231,
  "sentence_count": 187,
  "entities": { "persons": [...], "organizations": [...], ... },
  "summary": { "extractive": "...", "abstractive": "..." },
  "reasoning_deductions": [ { "rule_id": "RULE_1_FRAUD", "severity": "HIGH", "conclusion": "..." } ],
  "graph_stats": { "total_nodes": 12, "total_edges": 9 },
  "metrics": {
    "summarization": { "compression_ratio_pct": 12.4, "sentence_coverage_pct": 68.0 },
    "document_quality": { "flesch_kincaid": { "score": 42.1, "label": "Difficult", "grade": "College" }, "lexical_diversity": 0.61 },
    "ner_confidence": { "avg": 91.2, "min": 74.5, "max": 99.1, "count": 14 },
    "entity_coverage": { "filled_categories": 4, "total_categories": 6, "coverage_pct": 66.7 },
    "processing_time_sec": { "extraction_sec": 0.3, "ner_sec": 1.2, "summarization_sec": 8.4, "reasoning_sec": 0.01, "total_sec": 9.91 },
    "graph": { "density": 0.43, "connected_components": 1, "total_nodes": 12, "total_edges": 9 }
  }
}
```

---

## 📋 Prerequisites

| Requirement | Version | Download |
| ----------- | ------------------ | ----------------------------------------------- |
| Python | 3.9 or higher | [python.org](https://www.python.org/downloads/) |
| Node.js | 16 or higher | [nodejs.org](https://nodejs.org/) |
| npm | comes with Node.js | — |
| Git | any | [git-scm.com](https://git-scm.com/) |

---

## 🚀 How to Run — Step by Step

### 🪟 Windows

**Step 1 — Clone the repository**
```cmd
git clone https://github.com/your-username/LexAnalytica.git
cd LexAnalytica
```

**Step 2 — Create and activate a Python virtual environment**
```cmd
python -m venv venv
venv\Scripts\activate
```

> ⚠️ If you get a PowerShell execution policy error, run this first:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Step 3 — Install Python dependencies**
```cmd
cd backend
pip install -r requirements.txt
```

**Step 4 — Install frontend dependencies and build the React UI**
```cmd
cd ..\frontend
npm install
npm run build
```

**Step 5 — Run the application**
```cmd
cd ..\backend
python app.py
```

**Step 6 — Open in browser**  
Go to: [http://localhost:8000](http://localhost:8000)

---

## 🔧 Troubleshooting

**`ModuleNotFoundError: No module named 'transformers'`**  
→ Make sure your virtual environment is activated and you ran `pip install -r requirements.txt` from inside the `backend/` folder.

**`ModuleNotFoundError: No module named 'textstat'`**  
→ Run `pip install textstat` or reinstall requirements: `pip install -r backend/requirements.txt`.

**Frontend shows a blank page**  
→ Make sure you ran `npm run build` inside the `frontend/` directory. The `frontend/dist/` folder must exist.

**Port 8000 already in use**  
→ Kill the existing process or change the port in `backend/app.py` (`uvicorn.run(app, host="0.0.0.0", port=8000)`).

**Model Download Failed (HuggingFace)**  
→ Ensure you have a stable internet connection. Models are downloaded on the first run and cached locally (~5 GB).

**Metrics panel shows `—` (dash) values**  
→ This can happen if NER model failed to load. Check the server console for `[ERROR]` messages.

---

## 🌐 Languages Supported

| Language | Input | Output |
| ------------------ | ----- | ------ |
| English | ✅ | ✅ |
| Hindi (Devanagari) | ✅ | ✅ |

> Note: Flesch-Kincaid readability and Sentence Coverage metrics are computed for **English documents only**. Hindi documents show Lexical Diversity and NER Confidence metrics.

---

**Institutional Accuracy. Engineered for Legal Intelligence.**
