from docx import Document
from resume_parser.interfaces import FileParser

class WordParser(FileParser):
    """
    Concrete implementation of FileParser for Word (.docx) files using python-docx.
    """
    def parse_file(self, file_path: str) -> str:
        try:
            doc = Document(file_path)
            # Combine all paragraphs into a single text string
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return "\n".join(full_text)
        except Exception as e:
            raise ValueError(f"Failed to parse Word file '{file_path}': {str(e)}")
