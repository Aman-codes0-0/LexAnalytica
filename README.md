# LexAnalytica — Advanced AI Legal Document Intelligence

LexAnalytica is a premium, institutional-grade legal document analysis platform. It combines **FastAPI** performance with a **React-lite** modern interface to provide high-precision entity extraction, document synthesis, and bi-lingual support for legal professionals.

## 🌟 Enhanced Features
- **Professional Document Export**: 
  - **PDF Reports**: Beautifully formatted reports with full **Devanagari (Hindi) Unicode support**.
  - **DOCX Synthesis**: Editable Word documents for seamless legal drafting.
- **Bi-lingual Intelligence**: Full native support for English and Hindi (Devanagari) document processing.
- **Micro-document Processing**: Advanced safeguards to accurately handle everything from single-sentence documents to full-length court judgments.
- **Deep Legal NER**: Precision identification of Judges, Case Numbers, Statutes, Dates, and Parties using optimized NLP models.
- **Premium UI/UX**: Dark-themed SaaS aesthetic with real-time processing feedback and localized controls.

## 🏗️ Architecture
- **Frontend**: React + Vite + Lucide Icons (Dark Theme, Responsive).
- **Backend**: FastAPI + Uvicorn (Asynchronous, High-Performance).
- **Intelligence**: SpaCy (NER), BART (Summarization), Google Translate (Localization).
- **Generators**: ReportLab (Unicode PDF), Python-Docx (Word).

## 📁 Project Structure
- `frontend/`: Source code for the React dashboard.
- `nlp/`: Modular intelligence layer (summarizers, extractors, generators).
- `app.py`: Main API gateway and production build server.
- `server.log`: Dedicated background execution logs.
- `uploads/`: Secured temporary processing staging.

## 🛠️ Installation & Execution

### 1. Backend Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Frontend Build
```bash
cd frontend
npm install
npm run build
```

### 3. Launch System
```bash
# In the root directory
python3 app.py
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser.

---
**Institutional Accuracy. Engineered for Legal Intelligence.**
