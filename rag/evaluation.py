from typing import Iterable, Sequence, Set

from .models import RetrievedChunk


def recall_at_k(results: Sequence[RetrievedChunk], relevant_ids: Set[str], k: int) -> float:
    if not relevant_ids:
        return 0.0
    found = {r.chunk.id for r in results[:k]}
    return len(found & relevant_ids) / len(relevant_ids)


def reciprocal_rank(results: Sequence[RetrievedChunk], relevant_ids: Set[str]) -> float:
    for result in results:
        if result.chunk.id in relevant_ids:
            return 1.0 / result.rank
    return 0.0


def mean_reciprocal_rank(cases: Iterable[tuple[Sequence[RetrievedChunk], Set[str]]]) -> float:
    values = [reciprocal_rank(results, relevant) for results, relevant in cases]
    return sum(values) / len(values) if values else 0.0
