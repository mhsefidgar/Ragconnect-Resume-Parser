from pypdf import PdfReader
from resume_parser.interfaces import FileParser

class PDFParser(FileParser):
    """
    Concrete implementation of FileParser for PDF files using pypdf.
    """
    def parse_file(self, file_path: str) -> str:
        try:
            reader = PdfReader(file_path)
            text = []
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text.append(extracted)
            return "\n".join(text)
        except Exception as e:
            raise ValueError(f"Failed to parse PDF file '{file_path}': {str(e)}")
