# LexAnalytica — AI-Powered Legal Document Intelligence

> **Institutional-grade AI platform for legal document summarization, entity extraction, and bi-lingual analysis.**

LexAnalytica is a full-stack web application that combines a **FastAPI** backend with a **React + Vite** frontend to help legal professionals analyze documents in seconds. Upload a PDF, DOCX, TXT, or **scanned image (PNG/JPG)** and get a professional AI-generated report with key findings, entity extraction, and downloadable PDF output — with full **English & Hindi (Devanagari)** support.

Recently upgraded with **Graph RAG** and **Neurosymbolic AI**, the system now connects precedents across documents and evaluates hard facts using strict statutory logic.

---

## 🌟 Features

| Feature | Description |
|---|---|
| 🧠 **Neural Summarization** | Specialized **Legal-LED-16384** model (16k context) for high-accuracy AI synthesis. |
| 🏷️ **Legal-BERT NER** | Extracts Judges, Case Numbers, Sections of Law, Parties, Dates, and Organizations using Hugging Face pipelines. |
| 🕸️ **Graph RAG** | Connects all extracted documents and entities into an in-memory Knowledge Graph (NetworkX) for relational queries. |
| ⚖️ **Neurosymbolic Logic** | Forward-chaining reasoning engine applies strict legal logic to extracted facts to deduce outcomes without hallucination. |
| 🌐 **Bi-lingual Support** | Native Hindi (Devanagari) & English document processing + cross-language translation. |
| 🖼️ **OCR Support** | Scanned image files (PNG, JPG, JPEG) processed via PaddleOCR. |
| 📄 **PDF Export** | Professional Unicode PDF reports with full Devanagari rendering. |
| 🌙 **Dark UI** | Premium dark-themed React dashboard with real-time feedback and logic deduction visualization. |

---

## 🏗️ Tech Stack & Architecture

```
LexAnalytica/
├── app.py                  # FastAPI main server & API gateway
├── requirements.txt        # Python dependencies
├── uploads/                # Temporary file staging (auto-cleaned)
│
├── nlp/                    # Modular NLP intelligence layer
│   ├── __init__.py
│   ├── extractor.py        # PDF/DOCX/TXT/Image (OCR) text extraction
│   ├── preprocessor.py     # Text cleaning, sentence splitting, language detection
│   ├── entities.py         # Hugging Face Legal-BERT Named Entity Recognition
│   ├── summarizer.py       # Legal-LED-16384 summarization
│   ├── graph_engine.py     # NetworkX Knowledge Graph & Graph RAG
│   ├── reasoning.py        # Neurosymbolic Forward-Chaining Logic Engine
│   └── generator.py        # PDF (ReportLab) report generation
│
└── frontend/               # React + Vite UI
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        └── App.jsx         # Main React application
```

**Backend:** FastAPI · Uvicorn · Hugging Face Transformers (Legal-BERT, Legal-LED) · NetworkX · Deep-Translator · PaddleOCR
**Frontend:** React 18 · Vite 5 · Lucide Icons · Tailwind utilities via custom CSS

---

## 📋 Prerequisites

Make sure the following are installed on your system:

| Requirement | Version | Download |
|---|---|---|
| Python | 3.9 or higher | [python.org](https://www.python.org/downloads/) |
| Node.js | 16 or higher | [nodejs.org](https://nodejs.org/) |
| npm | comes with Node.js | — |
| Git | any | [git-scm.com](https://git-scm.com/) |

---

## 🚀 How to Run — Step by Step

### 🐧 Linux / macOS

**Step 1 — Clone the repository**
```bash
git clone https://github.com/your-username/LexAnalytica.git
cd LexAnalytica
```

**Step 2 — Create and activate a Python virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```
> You will see `(venv)` appear at the start of your terminal prompt.

**Step 3 — Install Python dependencies**
```bash
pip install -r requirements.txt
```
> ⚠️ The AI models (Transformers, PyTorch, PaddleOCR) are large. It may take **5–15 minutes** on the first run. The Hugging Face models will automatically download the first time you analyze a document.

**Step 4 — Install frontend dependencies and build the React UI**
```bash
cd frontend
npm install
npm run build
cd ..
```

**Step 5 — Run the application**
```bash
python3 app.py
```

**Step 6 — Open in browser**
Go to: [http://localhost:8000](http://localhost:8000)

---

### 🪟 Windows

**Step 1 — Clone the repository**
Open **Command Prompt** or **PowerShell** and run:
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
pip install -r requirements.txt
```

**Step 4 — Install frontend dependencies and build the React UI**
```cmd
cd frontend
npm install
npm run build
cd ..
```

**Step 5 — Run the application**
```cmd
python app.py
```

**Step 6 — Open in browser**
Go to: [http://localhost:8000](http://localhost:8000)

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/summarize` | Upload a document for full analysis (Extraction, RAG, Reasoning) |
| `GET`  | `/api/query_graph` | Query the NetworkX Knowledge Graph for related entities/docs |
| `POST` | `/api/download/pdf`| Download analysis as PDF |

---

## 🔧 Troubleshooting

**`ModuleNotFoundError: No module named 'transformers'`**
→ Make sure your virtual environment is activated and you ran `pip install -r requirements.txt`.

**Frontend shows a blank page**
→ Make sure you ran `npm run build` inside the `frontend/` directory. The `frontend/dist/` folder must exist.

**Port 8000 already in use**
→ Kill the existing process or change the port in `app.py` (`uvicorn.run(app, host="0.0.0.0", port=8000)`).

**Model Download Failed (HuggingFace)**
→ Ensure you have a stable internet connection. Models are downloaded on the first run and cached locally.

---

## 🌐 Languages Supported

| Language | Input | Output |
|---|---|---|
| English | ✅ | ✅ |
| Hindi (Devanagari) | ✅ | ✅ |

---

**Institutional Accuracy. Engineered for Legal Intelligence.**
