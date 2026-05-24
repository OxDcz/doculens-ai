"""Document parsing: read PDFs and plain text, extract metadata, chunk."""

import io
from dataclasses import dataclass, field
from typing import Any

import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter


@dataclass
class ParsedDocument:
    text: str
    num_pages: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


class DocumentParser:
    """Parse documents into text, with metadata extraction."""

    SUPPORTED_TYPES = {".pdf", ".txt", ".md", ".html"}

    def parse_bytes(self, content: bytes, filename: str = "document.pdf") -> ParsedDocument:
        """Parse raw bytes based on file extension."""
        ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else "txt"

        if ext == "pdf":
            return self._parse_pdf(content)
        elif ext in ("txt", "md", "html"):
            text = content.decode("utf-8", errors="replace")
            return ParsedDocument(text=text, num_pages=1)
        else:
            raise ValueError(f"Unsupported file type: .{ext}")

    def _parse_pdf(self, content: bytes) -> ParsedDocument:
        """Extract text from PDF using pdfplumber."""
        all_text: list[str] = []
        metadata: dict[str, Any] = {}
        num_pages = 0

        with pdfplumber.open(io.BytesIO(content)) as pdf:
            num_pages = len(pdf.pages)
            if pdf.metadata:
                metadata = {
                    "title": pdf.metadata.get("Title"),
                    "author": pdf.metadata.get("Author"),
                    "subject": pdf.metadata.get("Subject"),
                    "creator": pdf.metadata.get("Creator"),
                }

            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    all_text.append(page_text)

        return ParsedDocument(
            text="\n\n".join(all_text),
            num_pages=num_pages,
            metadata=metadata,
        )

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
    ) -> list[str]:
        """Split text into overlapping chunks for embedding."""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        return splitter.split_text(text)
