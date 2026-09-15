# RAGConnect Resume Parser

**Production-oriented document intelligence and retrieval foundation for senior-level RAG engineering.**

This project started as a pluggable PDF/DOCX resume parser and is being evolved into a modular RAG platform. The codebase separates **ingestion, chunking, retrieval, evaluation, and generation** so retrieval quality can be measured independently from the LLM.

## Why this project

A senior AI engineer portfolio should demonstrate more than calling an LLM. This repository focuses on the engineering problems that determine whether RAG works in production:

- deterministic document ingestion
- stable chunk IDs and metadata
- retrieval baselines that can be evaluated reproducibly
- explicit citations and provenance
- retrieval metrics such as Recall@K and MRR
- clean interfaces for replacing local baselines with vector search, rerankers, and hosted models
- automated tests around the retrieval pipeline

## Architecture

```text
PDF / DOCX / Markdown
        |
        v
  Document Ingestion
        |
        v
   Chunking + Metadata
        |
        +-------------------+
        |                   |
        v                   v
   Lexical Search     Dense Retrieval
        |                   |
        +--------+----------+
                 v
          Hybrid / Rerank
                 |
                 v
        Context Filtering
                 |
                 v
          LLM Generation
                 |
                 v
       Answer + Citations
                 |
                 v
      Evaluation / Tracing
```

The current branch includes a dependency-free lexical retrieval baseline and deterministic evaluation primitives. This is intentional: it gives the project a reproducible foundation before adding infrastructure such as PostgreSQL/pgvector, Redis, reranking, and hosted embeddings.

## Current capabilities

### Document foundation
- PDF and DOCX parsing from the original framework.
- Pluggable parser/extractor interfaces.
- Deterministic semantic/paragraph-aware chunking with stable IDs.
- Metadata attached to every chunk for future provenance and filtering.

### Retrieval
- Reproducible lexical retrieval baseline.
- Ranked `RetrievedChunk` domain model.
- Designed for extension to BM25, dense vector search, hybrid retrieval, and cross-encoder reranking.

### Evaluation
- Recall@K.
- Reciprocal Rank / MRR.
- Test fixtures for chunking and retrieval.
- Retrieval metrics are intentionally independent of the generation model.

## Roadmap

- [ ] Embedding provider interface + batch embedding
- [ ] PostgreSQL + pgvector backend
- [ ] BM25 + dense hybrid retrieval
- [ ] Cross-encoder reranking
- [ ] Page/section-level citations
- [ ] RAG answer generation with structured output
- [ ] Faithfulness, answer relevance, and context relevance evaluation
- [ ] Offline evaluation dataset and experiment reports
- [ ] FastAPI `/ingest`, `/retrieve`, and `/query` APIs
- [ ] Redis-backed job queue and durable task state
- [ ] OpenTelemetry/Langfuse tracing and token/cost tracking
- [ ] Docker + GitHub Actions CI
- [ ] Authentication, rate limiting, and tenant isolation
- [ ] Retrieval/latency/cost benchmark dashboard

## Engineering principles

1. **Measure retrieval before tuning prompts.**
2. **Keep ingestion, retrieval, generation, and evaluation independently testable.**
3. **Make provenance a first-class data model.**
4. **Prefer typed contracts over implicit dictionaries.**
5. **Keep provider-specific code behind interfaces.**
6. **Treat latency, cost, and failure modes as production metrics.**

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pytest
```

The original resume parsing CLI remains available:

```bash
python main.py sample_resumes/sample.pdf
```

## Portfolio positioning

This repository is intended to demonstrate **RAG/retrieval engineering**, complementing a computer-vision production project and an agentic AI project. The target outcome is a system where an interviewer can inspect not only the LLM call, but also the retrieval algorithm, evaluation methodology, provenance model, testing strategy, and production roadmap.

## License

MIT
