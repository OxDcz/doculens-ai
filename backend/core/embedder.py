"""Embedding generation via sentence-transformers."""

from typing import Optional

import torch
from sentence_transformers import SentenceTransformer

from backend.config import settings


class Embedder:
    """Generate embeddings for text chunks and queries."""

    _instance: Optional["Embedder"] = None
    _model: Optional[SentenceTransformer] = None

    def __new__(cls) -> "Embedder":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _load_model(self) -> SentenceTransformer:
        if self._model is None:
            device = settings.device
            if device == "cuda" and not torch.cuda.is_available():
                print("Warning: CUDA requested but not available. Falling back to CPU.")
                device = "cpu"

            self._model = SentenceTransformer(
                settings.embed_model,
                device=device,
                token=settings.hf_api_token,
            )
        return self._model

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts."""
        model = self._load_model()
        embeddings = model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return embeddings.tolist()

    @property
    def dimension(self) -> int:
        model = self._load_model()
        return model.get_sentence_embedding_dimension()
