import unittest
import sys
import os

# Add project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resume_parser.extractors import EmailExtractor, NameExtractor

class TestExtractors(unittest.TestCase):
    def test_email_extractor(self):
        extractor = EmailExtractor()
        # Happy Path
        self.assertEqual(extractor.extract("Contact me at user@test.com"), "user@test.com")
        self.assertEqual(extractor.extract("Email: valid.email+tag@example.co.uk"), "valid.email+tag@example.co.uk")
        # Edge Case: No email
        self.assertEqual(extractor.extract("No email here"), "")
        
    def test_name_extractor(self):
        extractor = NameExtractor()
        # Heuristic test cases
        
        # Case 1: Name: Prefix
        self.assertEqual(extractor.extract("Name: Alice Wonder\n..."), "Alice Wonder")
        
        # Case 2: Top line simple name
        self.assertEqual(extractor.extract("Bob Builder\nSoftware Engineer"), "Bob Builder")
        
        # Case 3: Skip metadata if possible (though my simple heuristic loops first 10 lines)
        self.assertEqual(extractor.extract("\n\nCharlie Day\n"), "Charlie Day")
        
        # Edge Case: Sentence not a name
        # "Hello world this is a long sentence" -> 7 words -> ignored by 2-4 word rule
        self.assertEqual(extractor.extract("Hello world this is a long sentence"), "")
