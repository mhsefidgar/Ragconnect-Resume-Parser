import time
import os
import sys
from tqdm import tqdm

# 1. Get the directory where THIS script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 2. Define the sample directory relative to this script
SAMPLE_DIR = os.path.join(SCRIPT_DIR, "sample_resumes")

# Add project root to path
sys.path.append(os.path.dirname(SCRIPT_DIR))

from resume_parser.pdf_parser import PDFParser
from resume_parser.word_parser import WordParser

def run_speed_test(iterations=50):
    print("--- Speed Benchmark Test ---")
    
    # 3. Use absolute paths for the files
    pdf_path = os.path.join(SAMPLE_DIR, "sample.pdf")
    docx_path = os.path.join(SAMPLE_DIR, "sample.docx")
    
    # Ensure the directory exists
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    
    # Check for samples and auto-generate if missing
    if not os.path.exists(pdf_path) or not os.path.exists(docx_path):
        print("🟡 Sample files not found. Attempting to generate...")
        try:
            import create_samples
            create_samples.create_sample_pdf(pdf_path)
            create_samples.create_sample_docx(docx_path)
            print("✅ Samples generated successfully.")
        except Exception as e:
            print(f"❌ Failed to generate samples: {e}")
            return

    pdf_parser = PDFParser()
    word_parser = WordParser()
    
    print(f"Running {iterations} iterations for each parser...")
    
    # PDF Test
    start_time = time.time()
    for _ in tqdm(range(iterations), desc="PDF Parsing"):
        pdf_parser.parse_file(pdf_path)
    end_time = time.time()
    pdf_avg = (end_time - start_time) / iterations
    
    # DOCX Test
    start_time = time.time()
    for _ in tqdm(range(iterations), desc="DOCX Parsing"):
        word_parser.parse_file(docx_path)
    end_time = time.time()
    docx_avg = (end_time - start_time) / iterations
    
    print(f"\nResults:")
    print(f"📄 PDF Avg Parse Time:  {pdf_avg:.5f} sec/file")
    print(f"📝 DOCX Avg Parse Time: {docx_avg:.5f} sec/file")
    print("--------------------------")

if __name__ == "__main__":
    run_speed_test()
