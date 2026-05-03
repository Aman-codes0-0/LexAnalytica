"""
Legal entity extraction module using HuggingFace NER.
Extracts persons, organizations, dates, and other legal-relevant entities.
"""

import re

# Load NLP models lazily
_ner_pipelines = {
    "en": None,
    "hi": None
}

def _get_ner_pipeline(lang: str):
    """Lazy-load the appropriate HF NER model."""
    
    if _ner_pipelines.get(lang) is None:
        try:
            from transformers import pipeline
            if lang == "en":
                print("[INFO] Loading Legal-BERT (NER variant) model...")
                _ner_pipelines[lang] = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
            else:
                print("[INFO] Loading generic multilingual NER model...")
                _ner_pipelines[lang] = pipeline("ner", model="Babelscape/wikineural-multilingual-ner", aggregation_strategy="simple")
        except Exception as e:
            print(f"[ERROR] NER model loading failed: {e}")
            return None
    return _ner_pipelines[lang]


# Patterns for legal-specific entity extraction (English focused, can be extended for Hindi)
CASE_NUMBER_PATTERN = re.compile(
    r"(?:Case\s*(?:No\.?|Number)\s*[:\-]?\s*[\w\-/]+)|"
    r"(?:(?:Civil|Criminal|Writ|Appeal)\s*(?:No\.?|Number)\s*[:\-]?\s*[\w\-/]+)|"
    r"(?:\b\d{1,4}\s*/\s*\d{4}\b)",
    re.IGNORECASE
)

SECTION_PATTERN = re.compile(
    r"(?:Section|Sec\.?|S\.?)\s*\d+[A-Za-z]?\s*(?:of\s+[\w\s]+(?:Act|Code))?",
    re.IGNORECASE
)


def extract_entities(text: str, lang: str = "en") -> dict:
    """
    Extract legal entities from text using HuggingFace NER + custom patterns.
    """
    entities = {
        "persons": [],
        "organizations": [],
        "dates": [],
        "locations": [],
        "case_numbers": [],
        "law_sections": [],
        "_raw_ner": [],   # Internal: raw NER results with confidence scores for metrics
    }

    ner_pipeline = _get_ner_pipeline(lang)
    
    if ner_pipeline is not None:
        # Truncate text for the pipeline if necessary
        text_chunk = text[:2000]

        # Hugging Face NER extraction
        try:
            ner_results = ner_pipeline(text_chunk)
            # Store raw results for confidence metric computation
            entities["_raw_ner"] = ner_results

            for ent in ner_results:
                value = ent.get('word', '').strip()
                label = ent.get('entity_group', '')
                
                if len(value) < 2:
                    continue

                if label == "PER" and value not in entities["persons"]:
                    entities["persons"].append(value)
                elif label == "ORG" and value not in entities["organizations"]:
                    entities["organizations"].append(value)
                elif label == "LOC" and value not in entities["locations"]:
                    entities["locations"].append(value)
        except Exception as e:
            print(f"[ERROR] NER pipeline failed: {e}")
            entities["error"] = "NER pipeline failed or model not installed."
    else:
        entities["error"] = "NER model failed to load."

    # Custom regex-based extraction
    case_matches = CASE_NUMBER_PATTERN.findall(text)
    entities["case_numbers"] = list(set(m.strip() for m in case_matches if m.strip()))

    section_matches = SECTION_PATTERN.findall(text)
    entities["law_sections"] = list(set(m.strip() for m in section_matches if m.strip()))

    # Limit results for cleaner output (skip internal _raw_ner key)
    for key in entities:
        if key != "_raw_ner":
            entities[key] = entities[key][:15]

    return entities
