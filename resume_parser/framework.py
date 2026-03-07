import os
import logging
from typing import Dict, Optional
from models import ResumeData
from resume_parser.interfaces import FileParser, FieldExtractor
from resume_parser.pdf_parser import PDFParser
from resume_parser.word_parser import WordParser
from resume_parser.extractors import NameExtractor, EmailExtractor, SkillsExtractor
from utils.text_validator import check_text_length

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeExtractor:
    """
    Coordinator that uses a dictionary of field extractors to populate ResumeData.
    """
    def __init__(self, extractors: Dict[str, FieldExtractor]):
        self.extractors = extractors

    def extract(self, text: str) -> ResumeData:
        # Validate text length
        if not check_text_length(text):
            logger.warning("Resume text exceeds maximum length or is invalid.")
            # We can decide to truncate or fail. For now, let's truncate.
            text = text[:50000]

        data = {"name": "", "email": "", "skills": []}

        for field, extractor in self.extractors.items():
            try:
                 result = extractor.extract(text)
                 data[field] = result
            except Exception as e:
                logger.error(f"Error extracting field '{field}': {e}")
                
        return ResumeData(
            name=data.get("name", ""),
            email=data.get("email", ""),
            skills=data.get("skills", [])
        )

class ResumeParserFramework:
    """
    Main Framework class.
    Orchestrates file parsing and data extraction.
    """
    def __init__(self):
        # Register default parsers
        self.file_parsers: Dict[str, FileParser] = {
            ".pdf": PDFParser(),
            ".docx": WordParser()
        }
        # Register default extractors
        self.resume_extractor = ResumeExtractor({
            "name": NameExtractor(),
            "email": EmailExtractor(),
            "skills": SkillsExtractor()
        })

    def add_custom_parser(self, extension: str, parser: FileParser):
        """Allows adding or overriding file parsers."""
        self.file_parsers[extension.lower()] = parser

    def parse_resume(self, file_path: str) -> ResumeData:
        """
        Parses a resume file and returns structured data.
        
        Args:
            file_path (str): Path to the resume file.
            
        Returns:
            ResumeData: Extracted resume information.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        parser = self.file_parsers.get(ext)
        if not parser:
            supported = list(self.file_parsers.keys())
            raise ValueError(f"Unsupported file format '{ext}'. Supported formats: {supported}")
        
        logger.info(f"Parsing file: {file_path} using {parser.__class__.__name__}")
        try:
            text = parser.parse_file(file_path)
            if not text.strip():
                 logger.warning("Extracted text is empty.")
            
            logger.info("Extracting data from text...")
            return self.resume_extractor.extract(text)
            
        except Exception as e:
            logger.error(f"Failed to process resume: {e}")
            raise
