from rag.chunking import semantic_chunks
from rag.evaluation import recall_at_k, reciprocal_rank
from rag.models import Chunk
from rag.retrieval import bm25, reciprocal_rank_fusion


def test_chunking_is_stable_and_non_empty():
    chunks = semantic_chunks("doc", "Python\n\nFastAPI\n\nRAG", chunk_size=20, overlap=4)
    assert chunks
    assert [c.id for c in chunks] == ["doc:0"]
    assert all(c.text.strip() for c in chunks)


def test_bm25_and_metrics():
    chunks = [
        Chunk("doc:0", "doc", "Python FastAPI", {}),
        Chunk("doc:1", "doc", "PostgreSQL vector search", {}),
        Chunk("doc:2", "doc", "Python testing", {}),
    ]
    results = bm25("Python", chunks, k=2)
    relevant = {"doc:0", "doc:2"}
    assert recall_at_k(results, relevant, 2) == 1.0
    assert reciprocal_rank(results, relevant) == 1.0


def test_reciprocal_rank_fusion_prefers_consistent_results():
    chunks = [
        Chunk("doc:0", "doc", "Python FastAPI", {}),
        Chunk("doc:1", "doc", "PostgreSQL", {}),
        Chunk("doc:2", "doc", "Python testing", {}),
    ]
    lexical = bm25("Python", chunks, k=3)
    fused = reciprocal_rank_fusion(lexical, lexical, k=60, top_k=2)
    assert fused
    assert fused[0].chunk.id == lexical[0].chunk.id
