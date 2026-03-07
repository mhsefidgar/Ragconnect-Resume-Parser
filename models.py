from dataclasses import dataclass
from typing import List

@dataclass
class ResumeData:
    """
    Data Class representing the structured information extracted from a resume.
    """
    name: str
    email: str
    skills: List[str]
