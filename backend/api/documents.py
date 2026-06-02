"""Document ingestion, retrieval, and processing endpoints."""

import uuid
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from backend.core.embedder import Embedder
from backend.core.extractor import Extractor
from backend.core.parser import DocumentParser
from backend.core.qa_engine import QAEngine
from backend.core.summarizer import Summarizer
from backend.db.vector_store import VectorStore
from backend.models.schemas import (
    DocumentMetadata,
    DocumentUploadResponse,
    QuestionRequest,
    QuestionResponse,
    SummarizeResponse,
)

router = APIRouter()

parser = DocumentParser()
embedder = Embedder()
vector_store = VectorStore()
summarizer = Summarizer()
qa_engine = QAEngine()
extractor = Extractor()


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    chunk_size: int = Form(512),
    chunk_overlap: int = Form(50),
):
    """Upload and process a document: parse -> chunk -> embed -> index."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    allowed_extensions = {".pdf", ".txt", ".md", ".html"}
    ext = file.filename.lower().rsplit(".", 1)[-1] if "." in file.filename else ""
    if f".{ext}" not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: .{ext}. Supported: {allowed_extensions}",
        )

    content = await file.read()
    doc_id = str(uuid.uuid4())

    parsed = parser.parse_bytes(content, filename=file.filename)
    chunks = parser.chunk_text(parsed.text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    embeddings = embedder.embed(chunks)
    vector_store.add(doc_id=doc_id, chunks=chunks, embeddings=embeddings)

    return DocumentUploadResponse(
        document_id=doc_id,
        filename=file.filename,
        num_chunks=len(chunks),
        num_pages=parsed.num_pages,
        metadata=DocumentMetadata(
            title=parsed.metadata.get("title"),
            author=parsed.metadata.get("author"),
            num_pages=parsed.num_pages,
        ),
    )


@router.get("/{document_id}", response_model=DocumentMetadata)
async def get_document(document_id: str):
    """Retrieve metadata for a previously uploaded document."""
    meta = vector_store.get_metadata(document_id)
    if meta is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return meta


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """Remove a document and its embeddings."""
    success = vector_store.delete(document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "deleted", "document_id": document_id}


@router.post("/{document_id}/query", response_model=QuestionResponse)
async def query_document(document_id: str, request: QuestionRequest):
    """Ask a question and get an answer grounded in the document."""
    query_embedding = embedder.embed([request.question])[0]
    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=request.top_k,
        doc_id=document_id,
    )

    if not results:
        raise HTTPException(status_code=404, detail="No relevant content found")

    context_chunks = [r["chunk"] for r in results]
    answer = qa_engine.answer(request.question, context_chunks)

    return QuestionResponse(
        question=request.question,
        answer=answer,
        sources=[r["chunk_id"] for r in results],
        confidence=answer.get("score"),
    )


@router.post("/{document_id}/summarize", response_model=SummarizeResponse)
async def summarize_document(
    document_id: str,
    max_length: int = 150,
    min_length: int = 40,
):
    """Generate a summary of the document."""
    chunks = vector_store.get_all_chunks(document_id)
    if not chunks:
        raise HTTPException(status_code=404, detail="Document not found")

    full_text = "\n\n".join(chunks)
    summary = summarizer.summarize(full_text, max_length=max_length, min_length=min_length)

    return SummarizeResponse(
        document_id=document_id,
        summary=summary,
        original_length=len(full_text),
        summary_length=len(summary),
    )
