# LexAnalytica: Project Synopsis & Methodology

## 1. Project Synopsis
**LexAnalytica** is an advanced, institutional-grade AI platform designed specifically for the legal domain. Legal professionals spend countless hours manually reading, analyzing, and finding connections across massive volumes of case laws, contracts, and filings. LexAnalytica automates this process by providing instant document summarization, extraction of critical legal entities, and cross-document reasoning. 

Recently upgraded with next-generation AI architectures—including **Graph RAG (Retrieval-Augmented Generation)**, **Legal-BERT**, and **Neurosymbolic AI**—the system doesn't just read documents; it understands the complex relationships between laws, people, and precedents, allowing it to deduce legal outcomes with high accuracy. Furthermore, it natively supports both English and Hindi (Devanagari), seamlessly breaking language barriers in the Indian legal context.

---

## 2. System Requirements

### Hardware Requirements
- **CPU:** Multi-core processor (Intel i5/Ryzen 5 or higher recommended).
- **RAM:** Minimum 8 GB (16 GB strongly recommended due to large Transformer models in memory).
- **Storage:** At least 5 GB of free space to cache large Hugging Face neural network models (Legal-LED, Legal-BERT) and PaddleOCR models.

### Software Requirements
- **OS:** Windows 10/11, macOS, or Linux.
- **Backend:** Python 3.9+
- **Frontend:** Node.js 16+ and npm
- **Core Dependencies (Python):** `fastapi`, `uvicorn`, `transformers`, `torch`, `networkx`, `paddleocr`, `langdetect`, `nltk`, `PyPDF2`, `reportlab`.

---

## 3. Methodology & AI Model Architecture
LexAnalytica operates on a sophisticated multi-layered pipeline. Here is exactly how the underlying models work together:

### A. The Extraction Layer (PaddleOCR & PyPDF2)
When a user uploads a document, the system first needs to extract raw text. Digital PDFs and text files are processed instantly via `PyPDF2`. If the user uploads a scanned image (PNG/JPG), the system utilizes **PaddleOCR**—a highly accurate Optical Character Recognition engine powered by deep learning—to visually scan and transcribe the text, supporting both English and Hindi scripts.

### B. The Perception Layer (Legal-BERT)
To understand the legal markers in the text, the system uses a fine-tuned Hugging Face Transformer model: **Legal-BERT**. 
* **How it works:** Unlike generic models, Legal-BERT was trained on millions of legal documents. Using a Token Classification pipeline (NER), it scans the text and accurately tags entities such as `Judges`, `Case Numbers`, `Locations`, `Organizations`, and `Persons`. It intelligently distinguishes between a regular person and a legal plaintiff based on contextual embeddings.

### C. The Knowledge Layer (Graph RAG)
Traditional AI systems forget documents as soon as they process them. LexAnalytica uses **Graph RAG**.
* **How it works:** Extracted entities are piped into an in-memory graph database built with `NetworkX`. The document becomes a central node, and all entities become connected branches. If multiple documents mention the same "Section 420" or "Company X," the graph connects them. This allows the system to perform relational queries, retrieving past precedents connected to current entities.

### D. The Reasoning Layer (Neurosymbolic AI)
Neural networks (like BERT) are great at reading, but they cannot perform strict logical reasoning (they hallucinate). LexAnalytica solves this by passing the extracted facts from Legal-BERT into a **Symbolic Logic Engine**.
* **How it works:** The engine contains hard-coded, strict legal rules (e.g., `IF "Fraud" AND "Persons > 0" THEN "Flag for High Severity"`). By combining Neural extraction with Symbolic logic, the system deduces bulletproof legal conclusions without the risk of AI hallucination.

### E. The Synthesis Layer (Legal-LED-16384)
For summarization, the system uses the **Longformer-Encoder-Decoder (LED)** model fine-tuned for the legal domain.
* **How it works:** Standard AI models (like basic BERT) can only read about 1.5 pages of text at a time (512 tokens). Legal-LED uses a "sparse attention mechanism" allowing it to ingest up to **16,384 tokens** (roughly 40 pages) at once, generating a cohesive, human-like abstractive summary of massive court judgments.

---

## 4. Codebase Explanation (File-by-File)

LexAnalytica is built with a decoupled architecture. Below is a detailed explanation of every crucial file in the repository.

### Backend Orchestration
* **`app.py`**: The central brain of the application. It runs the FastAPI web server. It exposes endpoints like `/api/summarize` and `/api/query_graph`. When a file is uploaded, this script sequentially routes the data through the extraction, preprocessing, NER, summarization, graph-building, and reasoning modules. Finally, it serves the React frontend.
* **`requirements.txt`**: A critical file containing all the Python libraries required for the project. Here is a breakdown of what each dependency does:
  * `fastapi` & `uvicorn`: Creates the high-performance asynchronous web server and API endpoints.
  * `python-multipart`: Allows FastAPI to handle raw file uploads (PDFs, Images) from the frontend.
  * `jinja2`: Handles template rendering if the React frontend is unavailable.
  * `transformers` & `torch`: The core AI libraries. They load and run the massive Hugging Face neural networks (`Legal-BERT` for entities and `Legal-LED` for summarization).
  * `PyPDF2`: A utility to extract raw text streams from digital PDF documents.
  * `nltk`: The Natural Language Toolkit. Used to split text into sentences and strip out useless "stop words" before AI processing.
  * `langdetect`: Automatically identifies if the uploaded document is written in English or Hindi.
  * `deep-translator`: Connects to Google Translate to seamlessly convert summaries and entities between English and Hindi.
  * `paddlepaddle` & `paddleocr`: The deep learning framework and Optical Character Recognition models used to extract text from scanned images.
  * `reportlab`: A powerful graphics library used to draw and generate the final downloadable PDF reports.
  * `numpy`: Handles the complex mathematical arrays required by the AI models.
  * `networkx`: Creates the in-memory directed Knowledge Graph, linking extracted entities together for the Graph RAG engine.

### The NLP Intelligence Layer (`nlp/` directory)
* **`nlp/extractor.py`**: Handles file parsing. It determines the file extension. If it's a digital PDF or TXT, it reads it directly. If it's an image, it initializes the `PaddleOCR` neural network to extract the text visually.
* **`nlp/preprocessor.py`**: Prepares the raw text for the AI models. It uses `langdetect` to figure out if the document is in English or Hindi. It then uses `NLTK` to strip out "stopwords" (useless filler words), remove noisy special characters, and split the text into an array of clean sentences.
* **`nlp/entities.py`**: The Named Entity Recognition (NER) module. It dynamically loads a Hugging Face `transformers` pipeline. It processes the text to find Persons, Organizations, and Locations. It also includes robust Regex fallbacks to extract structured `case_numbers` and `law_sections` perfectly every time.
* **`nlp/graph_engine.py`**: The memory module. It uses the `networkx` library to build a directed graph (`nx.DiGraph`). It takes the entities found by `entities.py` and creates "Nodes" and "Edges", linking documents to the entities they mention. It powers the `/api/query_graph` endpoint.
* **`nlp/reasoning.py`**: The logic engine. It defines a `NeuroSymbolicEngine` class containing strict conditional rules (`lambda` functions). It evaluates the dictionary of entities and returns definitive legal deductions and severity flags.
* **`nlp/summarizer.py`**: Contains two distinct summarization techniques.
  1. `extractive_summary`: Uses mathematics (TF-IDF) to rank the most important existing sentences in the document and returns them.
  2. `abstractive_summary`: Uses the massive `Legal-LED-16384` PyTorch model to read the entire document and write a brand-new, cohesive summary in its own words.
* **`nlp/generator.py`**: Uses the `ReportLab` library to take the final structured output (Summaries + Entities + Deductions) and format them into a downloadable PDF report. It includes special font-handling to correctly render Devanagari (Hindi) text.

### The Frontend Dashboard (`frontend/` directory)
* **`frontend/src/App.jsx`**: The main React component. It provides the premium, dark-themed User Interface. It handles the drag-and-drop file upload, validates file sizes, and provides real-time loading feedback while the heavy Python AI models run in the background. Once the API returns the JSON response, this file dynamically renders the entity "pills", the text summaries, the Graph Node counts, and the color-coded Neurosymbolic deductions.
* **`frontend/index.css` & `frontend/src/App.css`**: Contains custom CSS variables and styling classes to create a beautiful, modern aesthetic (often referred to as glassmorphism and neon-dark mode) using standard CSS paired with `clsx` for dynamic class merging.
* **`frontend/package.json` & `vite.config.js`**: Configuration files for Vite and Node.js to quickly bundle the React application into static files that `app.py` can serve.
