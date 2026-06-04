"""Document summarization using Hugging Face models."""

from typing import Optional

from transformers import pipeline

from backend.config import settings


class Summarizer:
    """Generate summaries using a pre-trained summarization pipeline."""

    _pipeline: Optional[pipeline] = None

    def _load(self) -> pipeline:
        if self._pipeline is None:
            device = 0 if settings.device == "cuda" else -1
            self._pipeline = pipeline(
                "summarization",
                model=settings.summ_model,
                device=device,
                token=settings.hf_api_token,
            )
        return self._pipeline

    def summarize(
        self,
        text: str,
        max_length: int = 150,
        min_length: int = 40,
    ) -> str:
        """Summarize text, handling long inputs by truncation."""
        pipe = self._load()

        max_input = pipe.tokenizer.model_max_length if pipe.tokenizer else 1024
        if len(text) > max_input:
            text = text[:max_input]

        result = pipe(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
            truncation=True,
        )
        return result[0]["summary_text"]
