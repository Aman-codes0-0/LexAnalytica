"""
Metric Evaluation Module for LexAnalytica.
Computes automatic quality and performance metrics for every document analysis.
No reference summary required — all metrics are self-contained.
"""

import re
import math


# ─── 1. Summarization Metrics ───────────────────────────────────────────────

def compression_ratio(original: str, summary: str) -> float:
    """
    What percentage of the original text length does the summary occupy?
    Lower = more compressed. e.g. 12.4 means summary is 12.4% of original.
    """
    if not original or not summary:
        return 0.0
    ratio = (len(summary) / len(original)) * 100
    return round(ratio, 2)


def sentence_coverage(original_sentences: list, summary: str) -> float:
    """
    What % of original sentences have at least one significant word
    appearing in the summary? Measures how representative the summary is.
    """
    if not original_sentences or not summary:
        return 0.0

    summary_lower = summary.lower()
    covered = 0

    for sent in original_sentences:
        words = [w.lower() for w in sent.split() if len(w) > 4]
        if not words:
            continue
        # A sentence is "covered" if ≥1 significant word appears in summary
        if any(w in summary_lower for w in words):
            covered += 1

    return round((covered / len(original_sentences)) * 100, 2)


# ─── 2. Document Quality Metrics ────────────────────────────────────────────

def flesch_kincaid_score(text: str) -> dict:
    """
    Compute Flesch Reading Ease score for English text.
    Score ranges: 90-100 = Very Easy, 60-70 = Standard, 0-30 = Very Difficult.
    Uses textstat library if available, otherwise computes manually.
    """
    if not text or len(text.strip()) < 10:
        return {"score": 0.0, "grade": "N/A", "label": "Insufficient text"}

    try:
        import textstat
        score = round(textstat.flesch_reading_ease(text), 2)
        grade = textstat.text_standard(text, float_output=False)
        label = _flesch_label(score)
        return {"score": score, "grade": grade, "label": label}
    except ImportError:
        # Manual fallback calculation
        score = _manual_flesch(text)
        label = _flesch_label(score)
        return {"score": score, "grade": "N/A", "label": label}


def _manual_flesch(text: str) -> float:
    """Fallback Flesch-Kincaid calculation without textstat."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    words = text.split()
    
    if not sentences or not words:
        return 0.0

    # Count syllables (approximation for English)
    syllable_count = sum(_count_syllables(w) for w in words)
    
    avg_sentence_length = len(words) / len(sentences)
    avg_syllables_per_word = syllable_count / len(words) if words else 1

    score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
    return round(max(0.0, min(100.0, score)), 2)


def _count_syllables(word: str) -> int:
    """Approximate syllable count for a word."""
    word = word.lower().strip(".,!?;:")
    if not word:
        return 1
    vowels = "aeiouy"
    count = 0
    prev_was_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_was_vowel:
            count += 1
        prev_was_vowel = is_vowel
    if word.endswith("e") and count > 1:
        count -= 1
    return max(1, count)


def _flesch_label(score: float) -> str:
    """Convert Flesch score to human-readable difficulty label."""
    if score >= 90:
        return "Very Easy"
    elif score >= 80:
        return "Easy"
    elif score >= 70:
        return "Fairly Easy"
    elif score >= 60:
        return "Standard"
    elif score >= 50:
        return "Fairly Difficult"
    elif score >= 30:
        return "Difficult"
    else:
        return "Very Difficult"


def lexical_diversity(text: str) -> float:
    """
    Type-Token Ratio (TTR): Unique words / Total words.
    Range: 0.0 to 1.0. Higher = more diverse vocabulary.
    """
    if not text:
        return 0.0
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    if not words:
        return 0.0
    ttr = len(set(words)) / len(words)
    return round(ttr, 4)


# ─── 3. NER Confidence Metrics ──────────────────────────────────────────────

def entity_confidence_stats(raw_ner_results: list) -> dict:
    """
    Compute avg, min, max confidence from raw HuggingFace NER pipeline output.
    Each item in raw_ner_results has a 'score' field (float 0–1).
    """
    if not raw_ner_results:
        return {"avg": 0.0, "min": 0.0, "max": 0.0, "count": 0}

    scores = [item.get("score", 0.0) for item in raw_ner_results if "score" in item]
    if not scores:
        return {"avg": 0.0, "min": 0.0, "max": 0.0, "count": 0}

    return {
        "avg": round(sum(scores) / len(scores) * 100, 2),   # as percentage
        "min": round(min(scores) * 100, 2),
        "max": round(max(scores) * 100, 2),
        "count": len(scores)
    }


def entity_coverage(entities: dict) -> dict:
    """
    How many of the 6 expected entity categories have at least 1 result?
    Returns count of filled categories and percentage.
    """
    expected = ["persons", "organizations", "dates", "locations", "case_numbers", "law_sections"]
    filled = sum(
        1 for k in expected
        if isinstance(entities.get(k), list) and len(entities[k]) > 0
    )
    total = len(expected)
    return {
        "filled_categories": filled,
        "total_categories": total,
        "coverage_pct": round((filled / total) * 100, 2)
    }


# ─── 4. Graph RAG Metrics ───────────────────────────────────────────────────

def graph_metrics(graph) -> dict:
    """
    Compute density and connected component count from the NetworkX graph.
    Density = edges / max_possible_edges. Range: 0.0 (sparse) to 1.0 (fully connected).
    """
    try:
        import networkx as nx
        density = round(nx.density(graph), 4)
        # For directed graphs, weakly connected components
        components = nx.number_weakly_connected_components(graph)
        return {
            "density": density,
            "connected_components": components,
            "total_nodes": graph.number_of_nodes(),
            "total_edges": graph.number_of_edges()
        }
    except Exception as e:
        print(f"[ERROR] Graph metrics failed: {e}")
        return {"density": 0.0, "connected_components": 0, "total_nodes": 0, "total_edges": 0}


# ─── 5. Master Bundle Function ──────────────────────────────────────────────

def bundle_metrics(
    original_text: str,
    original_sentences: list,
    summary: dict,
    entities: dict,
    raw_ner_results: list,
    processing_times: dict,
    graph,
    lang: str = "en"
) -> dict:
    """
    Master function — computes all metrics and returns a single structured dict.
    This is the only function called from app.py.
    """
    combined_summary = " ".join(filter(None, [
        summary.get("extractive", ""),
        summary.get("abstractive", "")
    ]))

    metrics = {
        "summarization": {
            "compression_ratio_pct": compression_ratio(original_text, combined_summary),
            "sentence_coverage_pct": sentence_coverage(original_sentences, combined_summary) if lang == "en" else None,
        },
        "document_quality": {
            "flesch_kincaid": flesch_kincaid_score(original_text) if lang == "en" else None,
            "lexical_diversity": lexical_diversity(original_text),
        },
        "ner_confidence": entity_confidence_stats(raw_ner_results),
        "entity_coverage": entity_coverage(entities),
        "processing_time_sec": processing_times,
        "graph": graph_metrics(graph),
    }

    return metrics
