"""
AI Powered Legal Document Summarization System
Flask API Server
"""

import os
from flask import Flask, request, jsonify, render_template
from nlp.extractor import extract_text
from nlp.preprocessor import preprocess, split_sentences, get_language
from nlp.entities import extract_entities
from nlp.summarizer import summarize

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max upload

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def allowed_file(filename: str) -> bool:
    """Check if the uploaded file has an allowed extension."""
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    """Serve the main frontend page."""
    return render_template("index.html")


@app.route("/api/summarize", methods=["POST"])
def api_summarize():
    """
    Handle document upload and return summarization results.
    
    Expects: multipart/form-data with 'file' field and optional 'mode' field.
    Mode: 'extractive', 'abstractive', or 'both' (default: 'both')
    
    Returns JSON:
    {
        "filename": str,
        "original_text": str (preview),
        "text_length": int,
        "sentence_count": int,
        "entities": dict,
        "summary": dict
    }
    """
    # Validate file
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded. Please select a document."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"}), 400

    # Save file
    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    try:
        # Step 1: Extract text
        raw_text = extract_text(file_path)
        if not raw_text or len(raw_text.strip()) < 20:
            return jsonify({"error": "Could not extract sufficient text from the document."}), 400

        # Step 2: Detect Language
        lang = get_language(raw_text)

        # Step 3: Get sentence count
        sentences = split_sentences(raw_text, lang=lang)

        # Step 4: Extract entities
        entities = extract_entities(raw_text, lang=lang)

        # Step 5: Summarize
        mode = request.form.get("mode", "both")
        if mode not in ("extractive", "abstractive", "both"):
            mode = "both"

        summary_result = summarize(raw_text, mode=mode, lang=lang)

        # Build response
        response = {
            "filename": filename,
            "language": "Hindi" if lang == "hi" else "English",
            "original_text": raw_text[:3000] + ("..." if len(raw_text) > 3000 else ""),
            "text_length": len(raw_text),
            "word_count": len(raw_text.split()),
            "sentence_count": len(sentences),
            "entities": entities,
            "summary": summary_result
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500

    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)


if __name__ == "__main__":
    print("=" * 60)
    print("  AI Legal Document Summarization System")
    print("  Open: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host="0.0.0.0", port=5000)
