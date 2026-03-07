import unittest
import sys
import os

# Add root directory to path to import create_samples
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import create_samples

def run_tests():
    print("--- Preparing Test Environment ---")
    sample_dir = "sample_resumes"
    pdf_path = os.path.join(sample_dir, "sample.pdf")
    docx_path = os.path.join(sample_dir, "sample.docx")

    # Ensure the directory exists
    os.makedirs(sample_dir, exist_ok=True)

    # Generate real files if they don't exist
    if not os.path.exists(pdf_path) or not os.path.exists(docx_path):
        print("Generating real PDF and DOCX samples...")
        create_samples.create_sample_pdf(pdf_path)
        create_samples.create_sample_docx(docx_path)

    print("--- Running Unit Tests ---")
    start_dir = os.path.dirname(os.path.abspath(__file__))
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir, pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if not result.wasSuccessful():
        sys.exit(1)
    else:
        print("\n✅ All unit tests passed using real files!")

if __name__ == "__main__":
    run_tests()