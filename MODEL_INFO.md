# LexAnalytica — Model Intelligence Report

This document explains the AI model used for abstractive summarization in this project.

## 🧠 Model: Legal-LED-16384
- **Full Name**: `nsi319/legal-led-base-16384`
- **Architecture**: LED (Longformer Encoder-Decoder)
- **Specialization**: Fine-tuned on massive datasets of legal documents (court judgments, contracts, and filings).

### 🚀 Key Advantages
1. **Long Context Support**: 
   - Traditional models (like BART) can only process ~1,000 words.
   - **Legal-LED** supports up to **16,384 tokens** (approx. 12,000–15,000 words).
   - This prevents "context truncation" where the end of a long legal document is ignored.
2. **Domain-Specific Vocabulary**: 
   - It understands legal jargon, case citations, and judicial language much better than general-purpose AI models.

---

## 🛠️ Implementation Details

### 1. Where is it used?
The model logic is encapsulated in:
- **`nlp/summarizer.py`**: Contains the loading logic and the abstractive summarization pipeline.
- **`requirements.txt`**: Includes `transformers` and `torch` which are required to run the model locally.

### 2. Integration Logic
Instead of a simple "one-shot" call, we use specialized logic for Longformer models:

#### A. Global Attention Mask
Because the model is designed for long documents, it uses **Sparse Attention** to save memory. We manually set "Global Attention" on the very first token (`BOS token`). This tells the model to look at the entire document structure while generating the summary.

```python
# Implementation excerpt from nlp/summarizer.py
global_attention_mask = torch.zeros_like(attention_mask)
global_attention_mask[:, 0] = 1  # Global attention on the first token
```

#### B. Decoding Strategy
We use **Beam Search** with 4 beams and a **Length Penalty** of 2.0.
- **Beam Search**: Helps the model explore multiple possible word sequences to find the most coherent sentence.
- **Length Penalty**: Encourages the model to provide a more detailed summary rather than a very short one.

#### C. Lazy Loading
To save system RAM, the model is not loaded until the user actually requests an "Abstractive" summary. This makes the initial application startup very fast.

---

## 📊 Summary Logic Flow
1. **Extraction**: `extractor.py` gets raw text from the file.
2. **Tokenization**: `summarizer.py` converts text into numbers (tokens) that the AI understands.
3. **Inference**: The `Legal-LED` model processes the tokens.
4. **Decoding**: The model outputs tokens, which are converted back into a human-readable summary.
