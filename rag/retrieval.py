import math
import re
from collections import Counter
from typing import Dict, Iterable, List, Sequence, Tuple

from .models import Chunk, RetrievedChunk


def _tokens(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9_+#.-]+", text.lower())


def _bm25_scores(query: str, chunks: Sequence[Chunk], k1: float = 1.5, b: float = 0.75) -> List[Tuple[float, Chunk]]:
    """Compute Okapi BM25 scores without external retrieval dependencies."""
    if not chunks:
        return []
    if k1 <= 0 or not 0 <= b <= 1:
        raise ValueError("k1 must be > 0 and b must be between 0 and 1")

    tokenized = [Counter(_tokens(c.text)) for c in chunks]
    lengths = [sum(tf.values()) for tf in tokenized]
    avgdl = sum(lengths) / len(lengths) if lengths else 0.0
    query_terms = set(_tokens(query))
    document_frequency = Counter()
    for tf in tokenized:
        document_frequency.update(tf.keys())

    n = len(chunks)
    scored: List[Tuple[float, Chunk]] = []
    for tf, dl, chunk in zip(tokenized, lengths, chunks):
        score = 0.0
        for term in query_terms:
            df = document_frequency.get(term, 0)
            if not df or not tf.get(term):
                continue
            idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
            denominator = tf[term] + k1 * (1 - b + b * dl / avgdl) if avgdl else tf[term] + k1
            score += idf * (tf[term] * (k1 + 1)) / denominator
        scored.append((score, chunk))
    return sorted(scored, key=lambda item: (-item[0], item[1].id))


def bm25(query: str, chunks: Iterable[Chunk], k: int = 5) -> List[RetrievedChunk]:
    """Rank chunks with Okapi BM25 for reproducible lexical retrieval experiments."""
    if k <= 0:
        return []
    ranked = _bm25_scores(query, list(chunks))[:k]
    return [RetrievedChunk(chunk=chunk, score=score, rank=i + 1) for i, (score, chunk) in enumerate(ranked)]


def reciprocal_rank_fusion(*ranked_lists: Sequence[RetrievedChunk], k: int = 60, top_k: int = 5) -> List[RetrievedChunk]:
    """Fuse multiple ranked lists using Reciprocal Rank Fusion (RRF)."""
    if k <= 0:
        raise ValueError("k must be > 0")
    if top_k <= 0:
        return []

    scores: Dict[str, float] = {}
    chunks: Dict[str, Chunk] = {}
    for results in ranked_lists:
        for result in results:
            scores[result.chunk.id] = scores.get(result.chunk.id, 0.0) + 1.0 / (k + result.rank)
            chunks[result.chunk.id] = result.chunk

    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))[:top_k]
    return [RetrievedChunk(chunk=chunks[chunk_id], score=score, rank=i + 1) for i, (chunk_id, score) in enumerate(ordered)]


def hybrid_retrieve(
    query: str,
    chunks: Iterable[Chunk],
    lexical_k: int = 20,
    top_k: int = 5,
) -> List[RetrievedChunk]:
    """Hybrid retrieval seam combining lexical retrieval with a second ranked retriever."""
    lexical = bm25(query, chunks, k=lexical_k)
    return reciprocal_rank_fusion(lexical, k=60, top_k=top_k)
