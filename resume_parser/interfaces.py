from abc import ABC, abstractmethod
from typing import Any

class FileParser(ABC):
    """
    Interface for file parsers. 
    Implementations should handle specific file formats (e.g., PDF, DOCX).
    """
    @abstractmethod
    def parse_file(self, file_path: str) -> str:
        """
        Parses the file at the given path and returns the extracted text.
        
        Args:
            file_path (str): Absolute or relative path to the file.
            
        Returns:
            str: The raw text extracted from the file.
        """
        pass

class FieldExtractor(ABC):
    """
    Interface for field extractors.
    Implementations should handle extraction of specific fields (Name, Email, Skills).
    """
    @abstractmethod
    def extract(self, text: str) -> Any:
        """
        Extracts a specific piece of information from the provided text.
        
        Args:
            text (str): The raw text of the resume.
            
        Returns:
            Any: The extracted data (str, List[str], etc.)
        """
        pass
