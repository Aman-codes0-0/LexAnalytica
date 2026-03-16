"""
Text preprocessing module for legal documents.
Handles cleaning, tokenization, sentence splitting, and stopword removal.
"""

import re
import nltk

# Download required NLTK data (silent if already present)
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from langdetect import detect, DetectorFactory

# Ensure consistent results for language detection
DetectorFactory.seed = 0


def get_language(text: str) -> str:
    """Detect the language of the text. Returns 'hi' for Hindi, 'en' for English (default)."""
    try:
        lang = detect(text)
        return lang if lang in ["hi", "en"] else "en"
    except:
        return "en"


def preprocess(text: str, lang: str = "en") -> str:
    """
    Clean and preprocess legal text based on language.
    
    Steps:
        1. Lowercase the text (for English)
        2. Remove special characters (keep alphanumeric + spaces + language-specific punctuation)
        3. Tokenize into words
        4. Remove stopwords
        5. Rejoin into cleaned text
    
    Args:
        text: Raw legal text.
        lang: Language of the text ('en' for English, 'hi' for Hindi).
    
    Returns:
        Cleaned and preprocessed text.
    """
    # Lowercase if English
    if lang == "en":
        text = text.lower()

    # Define cleanup pattern based on language
    if lang == "hi":
        # Preserve Devanagari, digits, and Purna Viram (।)
        text = re.sub(r"[^\u0900-\u097F0-9\s।]", "", text)
        stop_words = set(stopwords.words("hindi")) if "hindi" in stopwords.fileids() else set()
    else:
        # Preserve English alphabet, digits, and periods
        text = re.sub(r"[^a-z0-9\s.]", "", text)
        stop_words = set(stopwords.words("english"))

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords
    filtered_tokens = [t for t in tokens if t not in stop_words or t in (".", "।")]

    return " ".join(filtered_tokens)


def split_sentences(text: str, lang: str = "en") -> list:
    """
    Split text into individual sentences.
    
    Args:
        text: Raw text (not preprocessed — use original text for better splitting).
        lang: Language of the text ('en' for English, 'hi' for Hindi).
    
    Returns:
        List of sentence strings.
    """
    if lang == "hi":
        # Simple sentence splitter for Hindi based on । and \n
        sentences = re.split(r'[।\n]', text)
    else:
        sentences = sent_tokenize(text)
    
    # Clean up each sentence
    cleaned = [s.strip() for s in sentences if len(s.strip()) > 10]
    return cleaned


def get_word_frequencies(text: str, lang: str = "en") -> dict:
    """
    Calculate word frequencies from preprocessed text (excluding stopwords).
    
    Args:
        text: Raw text.
        lang: Language of the text ('en' for English, 'hi' for Hindi).
    
    Returns:
        Dictionary mapping words to their frequency counts.
    """
    if lang == "en":
        text_lower = text.lower()
        text_clean = re.sub(r"[^a-z0-9\s]", "", text_lower)
        stop_words = set(stopwords.words("english"))
    else:
        # For Hindi, we don't lowercase as it might affect Devanagari characters if not handled carefully,
        # and often not necessary for frequency counting in the same way as English.
        text_clean = re.sub(r"[^\u0900-\u097F0-9\s]", "", text)
        stop_words = set(stopwords.words("hindi")) if "hindi" in stopwords.fileids() else set()

    tokens = word_tokenize(text_clean)
    
    freq = {}
    for token in tokens:
        if token not in stop_words and len(token) > 1:
            freq[token] = freq.get(token, 0) + 1
    
    return freq
