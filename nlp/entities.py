"""
Legal entity extraction module using spaCy NER.
Extracts persons, organizations, dates, and other legal-relevant entities.
"""

import re
import spacy

# Load NLP models lazily
_nlp_models = {
    "en": None,
    "hi": None
}

def _get_nlp(lang: str):
    """Lazy-load the appropriate spaCy model."""
    global _nlp_models
    model_name = "en_core_web_sm" if lang == "en" else "hi_core_news_sm"
    
    if _nlp_models.get(lang) is None:
        try:
            print(f"[INFO] Loading spaCy model: {model_name} ...")
            _nlp_models[lang] = spacy.load(model_name)
        except OSError:
            print(f"[ERROR] spaCy model {model_name} not found.")
            return None
    return _nlp_models[lang]


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
    Extract legal entities from text using spaCy NER + custom patterns.
    """
    nlp_model = _get_nlp(lang)
    
    if nlp_model is None:
        model_name = "en_core_web_sm" if lang == "en" else "hi_core_news_sm"
        return {"error": f"spaCy model '{model_name}' not installed."}

    doc = nlp_model(text[:100000])  # Limit text length for performance

    entities = {
        "persons": [],
        "organizations": [],
        "dates": [],
        "locations": [],
        "case_numbers": [],
        "law_sections": [],
    }

    # spaCy NER extraction
    # Labels vary slightly by model, but PERSON, ORG, GPE are common in both
    for ent in doc.ents:
        value = ent.text.strip()
        if len(value) < 2:
            continue

        if ent.label_ == "PERSON" and value not in entities["persons"]:
            entities["persons"].append(value)
        elif ent.label_ == "ORG" and value not in entities["organizations"]:
            entities["organizations"].append(value)
        elif ent.label_ == "DATE" and value not in entities["dates"]:
            entities["dates"].append(value)
        elif ent.label_ == "GPE" and value not in entities["locations"]:
            entities["locations"].append(value)

    # Custom regex-based extraction (regex patterns are script-agnostic for numbers)
    case_matches = CASE_NUMBER_PATTERN.findall(text)
    entities["case_numbers"] = list(set(m.strip() for m in case_matches if m.strip()))

    section_matches = SECTION_PATTERN.findall(text)
    entities["law_sections"] = list(set(m.strip() for m in section_matches if m.strip()))

    # Limit results for cleaner output
    for key in entities:
        entities[key] = entities[key][:15]

    return entities
