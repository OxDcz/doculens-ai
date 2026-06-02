"""Tests for the document parser."""

from backend.core.parser import DocumentParser


def test_parse_plain_text():
    parser = DocumentParser()
    content = b"This is a test document.\n\nIt has multiple paragraphs."
    result = parser.parse_bytes(content, filename="test.txt")
    assert result.num_pages == 1
    assert "test document" in result.text


def test_chunk_text():
    parser = DocumentParser()
    text = "This is a long document. " * 200
    chunks = parser.chunk_text(text, chunk_size=100, chunk_overlap=20)
    assert len(chunks) > 1
    assert all(len(c) <= 100 + 20 for c in chunks)


def test_chunk_text_preserves_content():
    parser = DocumentParser()
    text = "First sentence. Second sentence. Third sentence."
    chunks = parser.chunk_text(text, chunk_size=200, chunk_overlap=0)
    combined = "".join(chunks)
    assert "First sentence" in combined
    assert "Third sentence" in combined
