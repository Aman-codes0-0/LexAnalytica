"""
AI Powered Legal Document Summarization System
FastAPI API Server
"""

import os
import shutil
from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from deep_translator import GoogleTranslator
from nlp.extractor import extract_text
from nlp.preprocessor import preprocess, split_sentences, get_language
from nlp.entities import extract_entities
from nlp.summarizer import summarize
from nlp.generator import generate_pdf, generate_docx

app = FastAPI(title="AI Legal Document Summarization System")

@app.post("/api/download/pdf")
async def download_pdf(data: dict):
    """Generate and return a PDF version of the analysis."""
    try:
        pdf_buffer = generate_pdf(data)
        filename = data.get("filename", "analysis")
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}_analysis.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@app.post("/api/download/docx")
async def download_docx(data: dict):
    """Generate and return a DOCX version of the analysis."""
    try:
        docx_buffer = generate_docx(data)
        filename = data.get("filename", "analysis")
        return StreamingResponse(
            docx_buffer,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={filename}_analysis.docx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DOCX generation failed: {str(e)}")

# ... (rest of the file remains same)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper functions
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def allowed_file(filename: str) -> bool:
    """Check if the uploaded file has an allowed extension."""
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def translate_results(data: dict, target_lang: str) -> dict:
    """Translate summaries and entities to the target language."""
    translator = GoogleTranslator(source='auto', target=target_lang)
    
    # 1. Translate Summaries
    if "summary" in data:
        for key in ["extractive", "abstractive"]:
            if key in data["summary"] and data["summary"][key]:
                try:
                    # Deep translator has a limit per request, but summaries should fit
                    data["summary"][key] = translator.translate(data["summary"][key])
                except Exception as e:
                    print(f"[ERROR] Translation failed for {key}: {e}")

    # 2. Translate Entities
    if "entities" in data:
        for key, entity_list in data["entities"].items():
            if isinstance(entity_list, list) and entity_list:
                translated_list = []
                for item in entity_list:
                    try:
                        translated_list.append(translator.translate(item))
                    except:
                        translated_list.append(item)
                data["entities"][key] = translated_list
                
    return data


@app.post("/api/summarize")
async def api_summarize(
    file: UploadFile = File(...),
    mode: str = Form("both"),
    output_lang: str = Form("en")
):
    """
    Handle document upload and return summarization results.
    """
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected.")

    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Save file temporarily
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Step 1: Extract text
        raw_text = extract_text(file_path)
        if not raw_text or len(raw_text.strip()) < 2:
            raise HTTPException(status_code=400, detail="Could not extract sufficient text from the document.")

        # Step 2: Detect Language
        doc_lang = get_language(raw_text)

        # Step 3: Get sentence count
        sentences = split_sentences(raw_text, lang=doc_lang)

        # Step 4: Extract entities
        entities = extract_entities(raw_text, lang=doc_lang)

        # Step 5: Summarize
        if mode not in ("extractive", "abstractive", "both"):
            mode = "both"

        summary_result = summarize(raw_text, mode=mode, lang=doc_lang)

        # Build initial response
        response = {
            "filename": file.filename,
            "language": "Hindi" if doc_lang == "hi" else "English",
            "original_text": raw_text[:3000] + ("..." if len(raw_text) > 3000 else ""),
            "text_length": len(raw_text),
            "word_count": len(raw_text.split()),
            "sentence_count": len(sentences),
            "entities": entities,
            "summary": summary_result
        }

        # Step 6: Translate if output_lang is different from doc_lang or if specifically requested
        if output_lang != doc_lang:
            response = translate_results(response, output_lang)
            response["output_language"] = "Hindi" if output_lang == "hi" else "English"
        else:
            response["output_language"] = response["language"]

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

# --------------------------------------------------------------------------
# Static file serving (React build or fallback)
# --------------------------------------------------------------------------
FRONTEND_DIST = os.path.join(BASE_DIR, "frontend", "dist")

if os.path.exists(FRONTEND_DIST):
    # Mount the React build. This is defined LAST so it doesn't hijack API routes
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
else:
    # Serve old static files if frontend/dist is missing
    STATIC_DIR = os.path.join(BASE_DIR, "static")
    TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

    if os.path.exists(STATIC_DIR):
        app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    
    if os.path.exists(TEMPLATES_DIR):
        templates = Jinja2Templates(directory=TEMPLATES_DIR)

        @app.get("/", response_class=HTMLResponse)
        async def index(request: Request):
            return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("  AI Legal Document Summarization System (FastAPI)")
    print("  Open: http://localhost:8000")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)
