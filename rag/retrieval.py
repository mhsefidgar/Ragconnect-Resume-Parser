import math
import re
from collections import Counter
from typing import Iterable, List

from .models import Chunk, RetrievedChunk


def _tokens(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9_+#.-]+", text.lower())


def _cosine(a: Counter, b: Counter) -> float:
    common = set(a) & set(b)
    numerator = sum(a[t] * b[t] for t in common)
    denom = math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values()))
    return numerator / denom if denom else 0.0


def bm25_like(query: str, chunks: Iterable[Chunk], k: int = 5) -> List[RetrievedChunk]:
    """Dependency-free lexical baseline used for reproducible retrieval evaluation."""
    items = list(chunks)
    q = Counter(_tokens(query))
    scored = [(_cosine(q, Counter(_tokens(c.text))), c) for c in items]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [RetrievedChunk(chunk=c, score=s, rank=i + 1) for i, (s, c) in enumerate(scored[:k])]
