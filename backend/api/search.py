"""Semantic search endpoints."""

from fastapi import APIRouter, HTTPException

from backend.core.embedder import Embedder
from backend.db.vector_store import VectorStore
from backend.models.schemas import SearchRequest, SearchResponse, SearchResult

router = APIRouter()
embedder = Embedder()
vector_store = VectorStore()


@router.post("", response_model=SearchResponse)
async def semantic_search(request: SearchRequest):
    """Search across all indexed documents using semantic similarity."""
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    query_embedding = embedder.embed([request.query])[0]
    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=request.top_k,
    )

    search_results = [
        SearchResult(
            document_id=r["doc_id"],
            chunk_id=r["chunk_id"],
            chunk_text=r["chunk"][:300],
            score=r["score"],
        )
        for r in results
    ]

    return SearchResponse(
        query=request.query,
        results=search_results,
        total_results=len(search_results),
    )
