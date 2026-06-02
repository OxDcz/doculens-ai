"""Tests for the summarizer module."""

import pytest

from backend.core.summarizer import Summarizer


@pytest.mark.slow
def test_summarize_short_text():
    summarizer = Summarizer()
    text = (
        "Artificial intelligence has transformed many industries. "
        "Machine learning models can now process natural language with "
        "remarkable accuracy. Deep learning has been particularly successful "
        "in tasks like translation and summarization."
    )
    summary = summarizer.summarize(text, max_length=30, min_length=10)
    assert len(summary) > 0
    assert len(summary) < len(text)


def test_summarizer_handles_long_input():
    summarizer = Summarizer()
    long_text = "This is a test. " * 2000
    summary = summarizer.summarize(long_text, max_length=50, min_length=10)
    assert len(summary) > 0
