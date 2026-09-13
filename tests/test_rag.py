from rag.chunking import semantic_chunks
from rag.evaluation import recall_at_k, reciprocal_rank
from rag.retrieval import bm25_like


def test_chunking_is_stable_and_non_empty():
    chunks = semantic_chunks("doc", "Python\n\nFastAPI\n\nRAG", chunk_size=20, overlap=4)
    assert chunks
    assert [c.id for c in chunks] == ["doc:0", "doc:1", "doc:2"]
    assert all(c.text.strip() for c in chunks)


def test_retrieval_and_metrics():
    chunks = semantic_chunks("doc", "Python FastAPI\n\nPostgreSQL vector search\n\nPython testing")
    results = bm25_like("Python", chunks, k=2)
    relevant = {chunks[0].id, chunks[2].id}
    assert recall_at_k(results, relevant, 2) > 0
    assert reciprocal_rank(results, relevant) > 0
