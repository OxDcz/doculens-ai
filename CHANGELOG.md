# Changelog

## 0.3.1 — 2025-06-02
- Fix: table extraction crash on multi-page PDFs with rotated tables
- Fix: memory leak in embedder when processing large document batches
- Improved OCR accuracy for Indonesian documents (tesseract trained data update)

## 0.3.0 — 2025-05-18
- Added Q&A engine with source citations
- New: React frontend with document viewer and search
- Docker compose setup for one-command deployment
- Breaking: `DocuLens.query()` renamed to `DocuLens.ask()`

## 0.2.0 — 2025-04-22
- Semantic search across document collections
- Embedding model configurable (was hardcoded to MiniLM)
- Added REST API endpoints for document upload and search
- Fixed: PaddleOCR compatibility with ROCm

## 0.1.0 — 2025-03-15
- Initial release
- PDF text extraction with layout preservation
- Table detection (experimental)
- Tesseract OCR integration
