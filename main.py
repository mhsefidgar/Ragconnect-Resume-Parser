import os
import argparse
from dotenv import load_dotenv
from resume_parser.framework import ResumeParserFramework
from utils.api_validator import validate_gemini_api_key

def main():
    """
    Main entry point for the Resume Parser Demo.
    """
    parser = argparse.ArgumentParser(description="Resume Parser Tool")
    parser.add_argument("file_path", help="Path to the resume file (.pdf or .docx)")
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    print("--- Resume Parser Demo ---")
    
    # Check API Key
    if validate_gemini_api_key():
        print("✅ Gemini API Key is valid.")
    else:
        print("⚠️  Gemini API Key missing or invalid. Skills extraction may fail.")
    
    if not os.path.exists(args.file_path):
        print(f"❌ File not found: {args.file_path}")
        return

    try:
        framework = ResumeParserFramework()
        result = framework.parse_resume(args.file_path)
        
        print("\n--- Extraction Results ---")
        print(f"Name: {result.name}")
        print(f"Email: {result.email}")
        print(f"Skills: {result.skills}")
        
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
