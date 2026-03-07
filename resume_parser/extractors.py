import re
import os
import json
import logging
from typing import List, Any
from google import genai
from resume_parser.interfaces import FieldExtractor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailExtractor(FieldExtractor):
    """
    Extracts email addresses using regex patterns.
    """
    def extract(self, text: str) -> str:
        # Robust email regex
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(email_pattern, text)
        if match:
            return match.group(0)
        return ""

class NameExtractor(FieldExtractor):
    """
    Extracts candidate name using heuristics.
    Fallback to simple rules since we want to avoid heavy NLP libs if possible for this assignment scope,
    or we can assume first few lines contain the name.
    """
    def extract(self, text: str) -> str:
        # Heuristic: Name is usually on the first few non-empty lines.
        # It's typically short (2-4 words) and Title Cased.
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        for line in lines[:10]:
            # Remove common labels if present (e.g., "Name: John Doe")
            if line.lower().startswith("name:"):
                return line[5:].strip()
            
            words = line.split()
            # Simple check: 2-4 words, all start with uppercase (ignoring small words like 'de', 'van' could be improved)
            if 2 <= len(words) <= 4:
                # Check if it looks like a name (mostly alpha methods)
                if all(w.isalpha() or ('.' in w) for w in words):
                     return line
        return ""

class SkillsExtractor(FieldExtractor):
    """
    Extracts skills using Google Gemini LLM (google-genai SDK).
    Requires GEMINI_API_KEY environment variable.
    """
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY not found. Skills extraction will fail or return empty.")
            self.client = None
        else:
            try:
                self.client = genai.Client(api_key=api_key)
            except Exception as e:
                 logger.error(f"Failed to configure Gemini Client: {e}")
                 self.client = None

    def extract(self, text: str) -> List[str]:
        if not self.client:
            logger.error("LLM client not initialized. Missing API Key?")
            return []

        # Truncate text to avoid context limits (approx 10k chars is plenty for skills)
        truncated_text = text[:10000]

        prompt = f"""
        You are a Resume Parsing Assistant.
        Task: Extract a list of technical skills from the resume text provided below.
        Output Format: Return valid JSON array of strings ONLY. No markdown backticks.
        Example: ["Python", "Machine Learning", "AWS"]
        
        Resume Text:
        {truncated_text}
        """
        
        try:
            # Using the new SDK generate_content method
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            raw_text = response.text.strip()
            
            # Clean up markdown if present
            if raw_text.startswith("```json"):
                raw_text = raw_text.replace("```json", "").replace("```", "")
            elif raw_text.startswith("```"):
                raw_text = raw_text.replace("```", "")
            
            raw_text = raw_text.strip()
            
            skills = json.loads(raw_text)
            if isinstance(skills, list):
                return [str(s) for s in skills]
            return []
            
        except Exception as e:
            logger.error(f"LLM Extraction failed: {e}")
            return []

