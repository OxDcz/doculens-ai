# doculens-ai

DocuLens is my attempt at building a local-first document pipeline for messy PDFs: extract text, detect structure, chunk pages, and make the content searchable without sending documents to external APIs.

## The problem I'm solving

I have a bunch of scanned PDFs — old reports, receipts, academic papers — that are painful to search through. Cloud OCR services work, but I don't want to upload sensitive documents to someone else's server. I wanted something that runs entirely on my machine.

## What it does

1. **Extract text** from PDFs (scanned or digital)
2. **Detect structure**: headings, paragraphs, lists, tables
3. **Chunk content** into searchable segments
4. **Local search** across your document collection

## Current state

- Text extraction: works for digital PDFs, basic OCR for scanned docs
- Structure detection: simple heuristic (font size, position) — not ML-based yet
- Chunking: paragraph-level, with configurable overlap
- Search: TF-IDF based, no vector DB yet

## What I'm working on next

- Better table extraction (see `docs/pdf_structure_notes.md`)
- Hybrid search: TF-IDF + sentence embeddings
- Processing pipelines for batch jobs

## Design decisions

- **Local-first**: No API calls, no cloud dependencies
- **Plain Python**: No heavy frameworks — just PyMuPDF, scikit-learn, and stdlib
- **Incremental**: Process one document at a time, cache results

See `docs/local_first_design.md` for more on the philosophy.

## Quick start

```bash
pip install -r requirements.txt
python doculens.py scan ./my_pdfs/ --output index.json
python doculens.py search index.json "quarterly revenue"
```

## Examples

- `examples/messy_pdf_pipeline.md` — processing a badly scanned report
- `examples/chunking_example.md` — how text gets split
- `examples/search_output.md` — what search results look like


## Hardware Tested
- AMD RX 7800 XT (RDNA3)
- AMD RX 7900 XTX (RDNA3)

## Troubleshooting
**Q: Getting OOM errors?**
A: Reduce batch size or enable gradient checkpointing.