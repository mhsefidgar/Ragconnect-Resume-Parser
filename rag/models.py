from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Chunk:
    id: str
    document_id: str
    text: str
    metadata: Dict[str, str]


@dataclass(frozen=True)
class RetrievedChunk:
    chunk: Chunk
    score: float
    rank: int


@dataclass(frozen=True)
class Citation:
    chunk_id: str
    document_id: str
    source: str
    page: Optional[int]
    score: float
