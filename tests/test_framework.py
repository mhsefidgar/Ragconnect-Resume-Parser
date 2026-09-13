import os
import sys
import tempfile
import unittest

from reportlab.pdfgen import canvas

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import ResumeData
from resume_parser.framework import ResumeParserFramework


class TestFramework(unittest.TestCase):
    def test_orchestration_with_real_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = os.path.join(tmpdir, "sample.pdf")
            pdf = canvas.Canvas(pdf_path)
            pdf.drawString(72, 720, "John Doe")
            pdf.drawString(72, 700, "john.doe@example.com")
            pdf.save()

            framework = ResumeParserFramework()
            result = framework.parse_resume(pdf_path)

            self.assertIsInstance(result, ResumeData)
            self.assertEqual(result.name, "John Doe")
            self.assertEqual(result.email, "john.doe@example.com")
