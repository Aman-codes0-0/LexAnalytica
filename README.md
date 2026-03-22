# LexAnalytica — AI-Powered Legal Document Intelligence

> **Institutional-grade AI platform for legal document summarization, entity extraction, and bi-lingual analysis.**

LexAnalytica is a full-stack web application that combines a **FastAPI** backend with a **React + Vite** frontend to help legal professionals analyze documents in seconds. Upload a PDF, DOCX, TXT, or **scanned image (PNG/JPG)** and get a professional AI-generated report with key findings, entity extraction, and downloadable PDF output — with full **English & Hindi (Devanagari)** support.

---

## 🌟 Features

| Feature | Description |
|---|---|
| 🧠 **Neural Summarization** | Specialized **Legal-LED-16384** model (16k context) for high-accuracy AI synthesis |
| 🏷️ **Legal NER** | Extracts Judges, Case Numbers, Sections of Law, Parties, Dates, Organizations |
| 🌐 **Bi-lingual Support** | Native Hindi (Devanagari) & English document processing + cross-language translation |
| 🖼️ **OCR Support** | Scanned image files (PNG, JPG, JPEG) processed via PaddleOCR |
| 📄 **PDF Export** | Professional Unicode PDF reports with full Devanagari rendering |
| ⚡ **Async API** | FastAPI + Uvicorn for high-performance, non-blocking processing |
| 🌙 **Dark UI** | Premium dark-themed React dashboard with real-time feedback |

---

## 🏗️ Tech Stack & Architecture

```
LexAnalytica/
├── app.py                  # FastAPI main server & API gateway
├── requirements.txt        # Python dependencies
├── uploads/                # Temporary file staging (auto-cleaned)
├── server.log              # Background execution logs
│
├── nlp/                    # Modular NLP intelligence layer
│   ├── __init__.py
│   ├── extractor.py        # PDF/DOCX/TXT/Image (OCR) text extraction
│   ├── preprocessor.py     # Text cleaning, sentence splitting, language detection
│   ├── entities.py         # Legal Named Entity Recognition (SpaCy)
│   ├── summarizer.py       # Legal-LED-16384 summarization (extractive + abstractive)
│   └── generator.py        # PDF (ReportLab) report generation
│
└── frontend/               # React + Vite UI
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        └── main.jsx        # Main React application
```

**Backend:** FastAPI · Uvicorn · SpaCy (NER) · Legal-LED (Summarization) · LangDetect · Deep-Translator · ReportLab · **PaddleOCR** (Image OCR)

**Frontend:** React 18 · Vite 5 · Lucide Icons · Dark Theme

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

### 🐧 Linux

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
> You will see `(venv)` appear at the start of your terminal prompt. This means the environment is active.

**Step 3 — Install Python dependencies**
```bash
pip install -r requirements.txt
```
> ⚠️ This step downloads large AI models (**Legal-LED**, SpaCy). It may take **5–15 minutes** on the first run.

**Step 4 — Download the SpaCy English language model**
```bash
python3 -m spacy download en_core_web_sm
```

**Step 5 — Install frontend dependencies and build the React UI**
```bash
cd frontend
npm install
npm run build
cd ..
```

**Step 6 — Run the application**
```bash
python3 app.py
```

**Step 7 — Open in browser**

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
> You will see `(venv)` appear at the start of your prompt. This means the environment is active.
>
> ⚠️ If you get a PowerShell execution policy error, run this first:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

**Step 3 — Install Python dependencies**
```cmd
pip install -r requirements.txt
```
> ⚠️ This step downloads large AI models (**Legal-LED**, SpaCy). It may take **5–15 minutes** on the first run.

**Step 4 — Download the SpaCy English language model**
```cmd
python -m spacy download en_core_web_sm
```

**Step 5 — Install frontend dependencies and build the React UI**
```cmd
cd frontend
npm install
npm run build
cd ..
```

**Step 6 — Run the application**
```cmd
python app.py
```

**Step 7 — Open in browser**

Go to: [http://localhost:8000](http://localhost:8000)

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/summarize` | Upload a document for full analysis |
| `POST` | `/api/download/pdf` | Download analysis as PDF |

### `/api/summarize` — Form Parameters

| Parameter | Type | Values | Description |
|---|---|---|---|
| `file` | File | `.pdf`, `.docx`, `.txt`, `.png`, `.jpg`, `.jpeg` | Document to analyze |
| `mode` | String | `extractive`, `abstractive`, `both` | Summary type |
| `output_lang` | String | `en`, `hi` | Output language |

---

## 🔧 Troubleshooting

**`ModuleNotFoundError: No module named 'spacy'`**
→ Make sure your virtual environment is activated (`source venv/bin/activate` on Linux, `venv\Scripts\activate` on Windows) before running.

**`OSError: [E050] Can't find model 'en_core_web_sm'`**
→ Run: `python -m spacy download en_core_web_sm`

**`npm: command not found`**
→ Install Node.js from [nodejs.org](https://nodejs.org/).

**Frontend shows a blank page**
→ Make sure you ran `npm run build` inside the `frontend/` directory. The `frontend/dist/` folder must exist.

**Port 8000 already in use**
→ Kill the existing process or change the port in `app.py` (line: `uvicorn.run(app, host="0.0.0.0", port=8000)`).

**OCR output is empty or garbled**
→ Make sure the image is clear and well-lit. PaddleOCR works best with high-resolution scans (150 DPI or higher).

---

## 🗂️ Supported File Formats

| Format | Extension | Notes |
|---|---|---|
| PDF | `.pdf` | Scanned + digital PDFs |
| Plain Text | `.txt` | UTF-8 encoded text |
| PNG Image | `.png` | Scanned documents via OCR |
| JPEG Image | `.jpg`, `.jpeg` | Scanned documents via OCR |

---

## 🌐 Languages Supported

| Language | Input | Output |
|---|---|---|
| English | ✅ | ✅ |
| Hindi (Devanagari) | ✅ | ✅ |

---

## 📜 License

This project is for educational/research purposes.

---

**Institutional Accuracy. Engineered for Legal Intelligence.**
