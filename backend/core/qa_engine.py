"""Question answering over document chunks."""

from typing import Any, Optional

from transformers import pipeline

from backend.config import settings


class QAEngine:
    """Answer questions using a QA pipeline grounded in provided context."""

    _pipeline: Optional[pipeline] = None

    def _load(self) -> pipeline:
        if self._pipeline is None:
            try:
                device = 0 if settings.device == "cuda" else -1
                self._pipeline = pipeline(
                    "question-answering",
                    model="distilbert-base-cased-distilled-squad",
                    device=device,
                )
            except Exception:
                self._pipeline = pipeline(
                    "question-answering",
                    model="distilbert-base-uncased-distilled-squad",
                    device=-1,
                )
        return self._pipeline

    def answer(self, question: str, context_chunks: list[str]) -> dict[str, Any]:
        """Answer a question using the concatenated context chunks."""
        pipe = self._load()

        context = " ".join(context_chunks)
        max_len = pipe.tokenizer.model_max_length if pipe.tokenizer else 512
        if len(context) > max_len:
            context = context[:max_len]

        result = pipe(question=question, context=context)
        return {
            "answer": result["answer"],
            "score": round(result["score"], 4),
        }
