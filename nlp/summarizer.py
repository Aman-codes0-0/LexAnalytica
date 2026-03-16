"""
Legal document summarization module.
Supports both extractive (TF-IDF sentence ranking) and abstractive (BART) summarization.
"""

import math
from .preprocessor import split_sentences, get_word_frequencies


# ─── Extractive Summarization ───────────────────────────────────────────────────

def extractive_summary(text: str, num_sentences: int = 5, lang: str = "en") -> str:
    """
    Generate an extractive summary by ranking sentences using TF-IDF scoring.
    """
    sentences = split_sentences(text, lang=lang)

    if len(sentences) <= num_sentences:
        return " ".join(sentences)

    # Get word frequencies (uses language-specific stopwords)
    word_freq = get_word_frequencies(text, lang=lang)

    if not word_freq:
        return " ".join(sentences[:num_sentences])

    # Normalize frequencies
    max_freq = max(word_freq.values())
    for word in word_freq:
        word_freq[word] = word_freq[word] / max_freq

    # Score each sentence
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        words = sentence.split() # No lower() here for Hindi
        if len(words) < 3:
            continue
        
        score = 0
        for word in words:
            clean_word = word.lower() if lang == "en" else word
            clean_word = "".join(c for c in clean_word if c.isalnum() or (lang == "hi" and "\u0900" <= c <= "\u097F"))
            if clean_word in word_freq:
                score += word_freq[clean_word]
        
        # Normalize by sentence length
        sentence_scores[i] = score / (math.log(len(words) + 1) + 1)

    # Get top sentence indices
    ranked = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    top_indices = sorted(ranked[:num_sentences])

    summary_sentences = [sentences[i] for i in top_indices]
    return " ".join(summary_sentences)


# ─── Abstractive Summarization ──────────────────────────────────────────────────

# Lazy-load the model
_abstractive_model = None
_abstractive_tokenizer = None


def _load_abstractive_model():
    """Lazy-load the BART summarization model."""
    global _abstractive_model, _abstractive_tokenizer
    
    if _abstractive_model is not None:
        return
    
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    
    model_name = "sshleifer/distilbart-cnn-6-6"
    print(f"[INFO] Loading lightweight summarization model: {model_name} ...")
    _abstractive_tokenizer = AutoTokenizer.from_pretrained(model_name)
    _abstractive_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    print("[INFO] Model loaded successfully.")


def abstractive_summary(text: str, max_length: int = 150, min_length: int = 30, lang: str = "en") -> str:
    """
    Generate an abstractive summary. 
    Note: Current model is English focus. For Hindi, we fall back to high-quality extractive 
    to avoid garbled text.
    """
    if lang != "en":
        return extractive_summary(text, num_sentences=6, lang=lang)

    # Safeguard for extremely short text to prevent model hallucination
    if len(text.strip()) < 50:
        return extractive_summary(text, num_sentences=3, lang=lang)

    _load_abstractive_model()
    
    # Truncate input to model's max length (1024 tokens)
    inputs = _abstractive_tokenizer(
        text,
        return_tensors="pt",
        max_length=1024,
        truncation=True
    )
    
    # Generate summary with optimized CPU params
    summary_ids = _abstractive_model.generate(
        inputs["input_ids"],
        max_length=max_length,
        min_length=min_length,
        num_beams=2,
        length_penalty=2.0,
        early_stopping=True,
        no_repeat_ngram_size=3
    )
    
    summary = _abstractive_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


def summarize(text: str, mode: str = "both", num_sentences: int = 5, lang: str = "en") -> dict:
    """
    Run summarization pipeline.
    """
    result = {}
    
    if mode in ("extractive", "both"):
        result["extractive"] = extractive_summary(text, num_sentences, lang=lang)
    
    if mode in ("abstractive", "both"):
        try:
            result["abstractive"] = abstractive_summary(text, lang=lang)
        except Exception as e:
            result["abstractive"] = f"Abstractive summarization failed: {str(e)}"
            result["abstractive_error"] = True
    
    return result
