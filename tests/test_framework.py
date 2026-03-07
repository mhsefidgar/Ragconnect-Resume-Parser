import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from resume_parser.framework import ResumeParserFramework
from models import ResumeData

class TestFramework(unittest.TestCase):
    def test_orchestration_with_real_file(self):
        framework = ResumeParserFramework()
        real_pdf = "sample_resumes/sample.pdf"
        
        self.assertTrue(os.path.exists(real_pdf), "Real PDF must exist for integration test")
            
        # Parse the real file through the actual framework pipeline
        result = framework.parse_resume(real_pdf)
        
        self.assertIsInstance(result, ResumeData)
        # Verify extraction logic worked on real file content
        self.assertEqual(result.name, "John Doe")
        self.assertEqual(result.email, "john.doe@example.com")