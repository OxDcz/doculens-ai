"""Vector store abstraction using ChromaDB."""

import uuid
from typing import Any, Optional

import chromadb
from chromadb.config import Settings as ChromaSettings

from backend.config import settings


class VectorStore:
    """Manages document chunk embeddings using ChromaDB."""

    _client: Optional[chromadb.ClientAPI] = None
    _collection: Optional[Any] = None

    def _init(self):
        if self._client is None:
            self._client = chromadb.PersistentClient(
                path=str(settings.chroma_path),
                settings=ChromaSettings(anonymized_telemetry=False),
            )
            self._collection = self._client.get_or_create_collection(
                name="doculens_documents",
                metadata={"hnsw:space": "cosine"},
            )

    @property
    def collection(self):
        self._init()
        return self._collection

    def add(
        self,
        doc_id: str,
        chunks: list[str],
        embeddings: list[list[float]],
    ) -> None:
        """Add document chunks with embeddings to the store."""
        chunk_ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {"doc_id": doc_id, "chunk_index": i} for i in range(len(chunks))
        ]

        self.collection.add(
            ids=chunk_ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        doc_id: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """Search for similar chunks."""
        where_filter = None
        if doc_id:
            where_filter = {"doc_id": doc_id}

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        hits = []
        if results and results["ids"] and results["ids"][0]:
            for i, chunk_id in enumerate(results["ids"][0]):
                hits.append({
                    "chunk_id": chunk_id,
                    "doc_id": results["metadatas"][0][i]["doc_id"],
                    "chunk": results["documents"][0][i],
                    "score": round(1.0 - results["distances"][0][i], 4),
                })

        return hits

    def get_all_chunks(self, doc_id: str) -> list[str]:
        """Retrieve all chunks for a document."""
        results = self.collection.get(
            where={"doc_id": doc_id},
            include=["documents"],
        )
        return results["documents"] if results and results["documents"] else []

    def get_metadata(self, doc_id: str) -> Optional[dict[str, Any]]:
        """Get document metadata from stored chunks."""
        results = self.collection.get(
            where={"doc_id": doc_id},
            include=["metadatas"],
            limit=1,
        )
        if results and results["metadatas"]:
            return {"document_id": doc_id, "num_chunks": len(results["ids"])}
        return None

    def delete(self, doc_id: str) -> bool:
        """Remove all chunks for a document."""
        results = self.collection.get(
            where={"doc_id": doc_id},
            include=[],
        )
        if results and results["ids"]:
            self.collection.delete(ids=results["ids"])
            return True
        return False
