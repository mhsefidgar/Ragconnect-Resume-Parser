import unittest
import os
import sys

# Project root setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from resume_parser.pdf_parser import PDFParser
from resume_parser.word_parser import WordParser

class TestParsers(unittest.TestCase):
    def setUp(self):
        # Paths relative to project root where run_all_tests.py is executed
        self.pdf_path = "sample_resumes/sample.pdf"
        self.docx_path = "sample_resumes/sample.docx"
        
    def test_pdf_parser(self):
        self.assertTrue(os.path.exists(self.pdf_path), "Missing real PDF for test")
        parser = PDFParser()
        text = parser.parse_file(self.pdf_path)
        self.assertIn("John Doe", text)

    def test_word_parser(self):
        self.assertTrue(os.path.exists(self.docx_path), "Missing real DOCX for test")
        parser = WordParser()
        text = parser.parse_file(self.docx_path)
        self.assertIn("Jane Smith", text)