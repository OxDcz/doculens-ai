# DocuLens AI

Document analysis toolkit. Extract text, tables, and structure from PDFs and scanned documents. Ask questions about your documents. Get answers with citations.

## What it does

DocuLens takes PDFs (including scanned ones) and gives you:
- Full text extraction with layout preservation
- Table detection and extraction to CSV/JSON
- Semantic search across document collections
- Q&A with source citations
- Summarization (extractive + abstractive)

It runs locally. No cloud APIs required for the core pipeline.

## Quick start

```bash
pip install doculens-ai
doculens analyze paper.pdf
```

For OCR on scanned docs:
```bash
sudo apt install tesseract-ocr
doculens analyze scanned.pdf --ocr
```

Q&A mode:
```bash
doculens ask "what were the main findings?" --docs ./papers/
```

## Architecture

FastAPI backend + React frontend. Models run locally via HuggingFace Transformers.

```
PDF/Image  ->  OCR/Text  ->  Chunking  ->  Embeddings  ->  Vector DB
                                                          |
                                               Q&A Engine <- Query
```

Embedding model: `all-MiniLM-L6-v2` (default, configurable)
QA model: `deepset/roberta-base-squad2` (default)

## Docker

```bash
docker compose up
# Open http://localhost:3000
```

GPU passthrough for faster inference:
```bash
docker compose -f docker-compose.yml -f docker-compose.gpu.yml up
```

## API

```python
from doculens import DocuLens

dl = DocuLens()
doc = dl.load("report.pdf")
print(doc.tables[0].to_csv())
answer = dl.ask("what is the revenue?", docs=[doc])
print(answer.text, answer.sources)
```

## Status

Experimental. I use this daily for my own work but it's not battle-tested for production. The table extraction is hit-or-miss with complex layouts. OCR quality depends heavily on scan quality.

Contributions welcome — especially for better table detection models.

MIT License.


## Hardware Tested
- AMD RX 7800 XT (RDNA3)
- AMD RX 7900 XTX (RDNA3)

## Recent Updates
- Performance improvements for batch processing
- Better error messages for common issues