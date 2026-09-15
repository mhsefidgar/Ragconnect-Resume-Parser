import re
from typing import List

from .models import Chunk


def semantic_chunks(document_id: str, text: str, chunk_size: int = 900, overlap: int = 120) -> List[Chunk]:
    """Create deterministic, paragraph-aware chunks with stable IDs."""
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Require chunk_size > 0 and 0 <= overlap < chunk_size")

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: List[Chunk] = []
    buffer = ""
    index = 0

    for paragraph in paragraphs:
        candidate = f"{buffer}\n\n{paragraph}".strip() if buffer else paragraph
        if len(candidate) <= chunk_size:
            buffer = candidate
            continue

        if buffer:
            chunks.append(Chunk(f"{document_id}:{index}", document_id, buffer, {"chunk_index": str(index)}))
            index += 1
            buffer = buffer[-overlap:] + "\n\n" + paragraph
        else:
            buffer = paragraph

        while len(buffer) > chunk_size:
            piece = buffer[:chunk_size]
            chunks.append(Chunk(f"{document_id}:{index}", document_id, piece, {"chunk_index": str(index)}))
            index += 1
            buffer = buffer[chunk_size - overlap :]

    if buffer:
        chunks.append(Chunk(f"{document_id}:{index}", document_id, buffer, {"chunk_index": str(index)}))

    return chunks
