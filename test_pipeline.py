
"""
Comprehensive test script for the Legal Document Summarization System.
Verifies text extraction, entity recognition, and summarization (extractive).
Note: Abstractive summarization test is separate as it downloads a large model.
"""

import os
from nlp.extractor import extract_text
from nlp.entities import extract_entities
from nlp.summarizer import extractive_summary, summarize

# Test document content
TEST_CONTENT = """
CASE: State of Maharashtra vs. John Doe
Case No: 452/2024
Court: High Court of Bombay
Judge: Justice Malhotra

The plaintiff filed a case against the defendant, John Doe, for breach of contract.
The defendant failed to deliver the construction material as per Section 45 of the Indian Contract Act.
After reviewing the evidence provided by both parties on 12th February 2024, the court found the 
defendant guilty of negligence.

Final Decision: The defendant must pay a penalty of $50,000 to the plaintiff.
"""

def run_test():
    print("--- Starting NLP Pipeline Test ---")
    
    # 1. Create a temporary test file
    test_file = "test_legal_doc.txt"
    with open(test_file, "w") as f:
        f.write(TEST_CONTENT)
    print(f"[1/4] Created test file: {test_file}")

    try:
        # 2. Test Extraction
        text = extract_text(test_file)
        print(f"[2/4] Extraction: Success ({len(text)} characters)")

        # 3. Test Entities
        entities = extract_entities(text)
        print("[3/4] Entity Recognition Results:")
        print(f"    - Persons: {entities.get('persons', [])}")
        print(f"    - Case Nos: {entities.get('case_numbers', [])}")
        print(f"    - Law Sections: {entities.get('law_sections', [])}")
        
        # Verify specific entities were found
        assert "John Doe" in str(entities.get('persons', []))
        assert "452/2024" in str(entities.get('case_numbers', []))

        # 4. Test Extractive Summarization
        summary = extractive_summary(text, num_sentences=2)
        print(f"[4/4] Extractive Summary: {summary[:100]}...")
        assert len(summary) > 20

        print("\n✅ NLP PIPELINE VERIFICATION PASSED!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    run_test()
