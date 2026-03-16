# LexAnalytica — AI Legal Document Summarization System
## Project Documentation & Architecture Overview

LexAnalytica is a modern, professional legal document analysis platform. It leverages state-of-the-art NLP (Natural Language Processing) to provide legal intelligence through automated entity extraction and document synthesis in both **Hindi and English**.

---

### 📂 Directory Structure

```text
/legal
├── app.py                # Main Flask Application (API Endpoints & Routing)
├── requirements.txt      # Project Dependencies (Libraries)
├── .gitignore            # Files excluded from GitHub (Heavy models, uploads)
├── README.md             # Project documentation (this file)
├── uploads/              # Temporary storage for uploaded documents
├── templates/
│   └── index.html        # Frontend (UI Structure & Layout)
├── static/
│   ├── style.css         # Custom Styling (Professional SaaS Theme)
│   └── script.js         # Frontend Logic (AJAX, Loading states, Rendering)
└── nlp/                   # Core NLP Pipeline
    ├── __init__.py
    ├── extractor.py       # Text extraction from PDF, DOCX, and TXT
    ├── preprocessor.py    # Text cleaning, Language detection, & Tokenization
    ├── entities.py        # Legal Entity Extraction (NER)
    └── summarizer.py      # Abstractive & Extractive Summarization Logic
```

---

### 🧠 Core Logic & AI Models

#### 1. Language Detection (`nlp/preprocessor.py`)
- **Library**: `langdetect`
- **Logic**: Automatically identifies if a document is in Hindi (`hi`) or English (`en`). It routes the document to the corresponding language-specific cleaning and analysis pipeline.

#### 2. Text Preprocessing (`nlp/preprocessor.py`)
- **Library**: `nltk`
- **Logic**: 
  - **English**: Lowercasing, stopword removal, and alphanumeric cleaning.
  - **Hindi**: Preserves Devanagari script (`\u0900-\u097F`) and Devanagari punctuation (Purna Viram `।`).

#### 3. Entity Extraction (`nlp/entities.py`)
- **Technology**: `spaCy` (State-of-the-art NER)
- **Models**:
  - `en_core_web_sm` (English)
  - `hi_core_news_sm` (Hindi - Fallback used for script hygiene)
- **Logic**: Extracts Judges, Court names, Case Numbers, Dates, and Section references using a mix of AI models and Custom Regex patterns.

#### 4. Document Summarization (`nlp/summarizer.py`)
- **Extractive Summary**: ranks sentences based on TF-IDF scoring (frequency/importance).
- **Abstractive Summary (Synthesis)**:
  - **Model**: `sshleifer/distilbart-cnn-6-6` (via HuggingFace Transformers).
  - **Logic**: A lightweight sequence-to-sequence model optimized for CPU inference. It "understands" the text and rewrites it into a human-like summary.

---

### 🛠️ Technologies Used

- **Backend**: Python 3, Flask (Web framework)
- **PDF/Doc Handling**: `PyPDF2`, `python-docx`
- **NLP/AI**: `transformers`, `torch`, `spacy`, `nltk`, `langdetect`
- **Frontend**: HTML5, Vanilla CSS3 (modern glassmorphism), JavaScript (ES6+), Inter Font (Google Fonts)

---

### 🚀 Setup Instructions

#### 1. Create a Virtual Environment (Recommended)
Developing in a virtual environment keeps your system clean.
```bash
# Create the environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Linux/macOS
# venv\Scripts\activate  # On Windows
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Download NLP Models
```bash
python3 -m spacy download en_core_web_sm
# Hindi and Summarization models download automatically on first run
```

#### 4. Run the Application
```bash
python3 app.py
```
Open `http://localhost:5000` in your browser.

---

### 🌐 Free Deployment Guide (Hugging Face Spaces)

Since this project uses heavy AI models (Transformers/PyTorch), standard free hosts like Render or Vercel may run out of memory. **Hugging Face Spaces** is the best free option.

#### Step-by-Step Process:
1. **Create an Account**: Sign up at [huggingface.co](https://huggingface.co/).
2. **Create a New Space**:
   - Click "New" -> "Space".
   - Give it a name (e.g., `lex-analytica`).
   - Select **Docker** as the SDK.
   - Select **Blank** template.
   - Choose the "Free" tier (CPU is enough).
3. **Upload Files**:
   - Upload all project files (`app.py`, `nlp/`, `static/`, `templates/`, `requirements.txt`).
4. **Create a Dockerfile**:
   Hugging Face Docker Spaces need a `Dockerfile`. Create a file named `Dockerfile` in the root with this content:
   ```dockerfile
   FROM python:3.10
   WORKDIR /code
   COPY ./requirements.txt /code/requirements.txt
   RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
   RUN python -m spacy download en_core_web_sm
   COPY . .
   CMD ["python", "app.py"]
   ```
5. **Set Environment Variable**:
   In `app.py`, ensure the host is set to `0.0.0.0` and port is `7860` (Hugging Face's default).
   ```python
   app.run(host="0.0.0.0", port=7860)
   ```
6. **Deploy**: Once you commit the files, Hugging Face will automatically build and start your "Legal Assistant" online!

---

### ✨ Features
- **Professional SaaS UI**: Modern dark/slate theme tailored for legal professionals.
- **Bi-lingual Support**: Full support for English and Hindi documents.
- **Synthesis Engine**: Uses AI to write summaries, not just copy-paste sentences.
- **Legal Intelligence**: Automatically finds case numbers and law sections.
