"""
Legal document summarization module.
Supports both extractive (TF-IDF sentence ranking) and abstractive (BART) summarization.
"""

import math
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
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
    
    model_name = "nsi319/legal-led-base-16384"
    print(f"[INFO] Loading specialized legal summarization model: {model_name} ...")
    _abstractive_tokenizer = AutoTokenizer.from_pretrained(model_name)
    _abstractive_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    print("[INFO] Legal model loaded successfully.")


def abstractive_summary(text: str, max_length: int = 250, min_length: int = 50, lang: str = "en") -> str:
    """
    Generate an abstractive summary using Legal-LED.
    LED is optimized for long legal documents (up to 16,384 tokens).
    """
    if lang != "en":
        return extractive_summary(text, num_sentences=6, lang=lang)

    # Safeguard for extremely short text
    if len(text.strip()) < 50:
        return extractive_summary(text, num_sentences=3, lang=lang)

    _load_abstractive_model()
    
    # LED supports up to 16,384 tokens
    inputs = _abstractive_tokenizer(
        text,
        return_tensors="pt",
        max_length=16384,
        truncation=True
    )
    
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]
    
    # For LED, we specify global attention on the first token (BOS)
    global_attention_mask = torch.zeros_like(attention_mask)
    global_attention_mask[:, 0] = 1
    
    # Generate summary with specialized legal model parameters
    summary_ids = _abstractive_model.generate(
        input_ids,
        attention_mask=attention_mask,
        global_attention_mask=global_attention_mask,
        max_length=max_length,
        min_length=min_length,
        num_beams=4,
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
