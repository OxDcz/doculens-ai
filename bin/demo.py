#!/usr/bin/env python3
"""Demo script: process a PDF and run example queries.

Usage:
    python scripts/demo.py path/to/document.pdf
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.core.parser import DocumentParser
from backend.core.embedder import Embedder
from backend.core.summarizer import Summarizer
from backend.db.vector_store import VectorStore


def main(filepath: str):
    path = Path(filepath)
    if not path.exists():
        print(f"File not found: {filepath}")
        sys.exit(1)

    print(f"Processing: {path.name}")
    t0 = time.time()

    parser = DocumentParser()
    content = path.read_bytes()
    parsed = parser.parse_bytes(content, filename=path.name)
    print(f"   Parsed {parsed.num_pages} page(s) -- {len(parsed.text):,} characters")

    chunks = parser.chunk_text(parsed.text, chunk_size=512, chunk_overlap=50)
    print(f"   Created {len(chunks)} chunks")

    embedder = Embedder()
    print(f"   Generating embeddings (dim={embedder.dimension})...")
    embeddings = embedder.embed(chunks)
    print(f"   {len(embeddings)} embeddings generated")

    store = VectorStore()
    doc_id = path.stem
    store.add(doc_id=doc_id, chunks=chunks, embeddings=embeddings)
    print(f"   Indexed under ID: {doc_id}")

    query = "main findings and conclusions"
    print(f"\nSearching: '{query}'")
    query_emb = embedder.embed([query])[0]
    results = store.search(query_embedding=query_emb, top_k=3)
    for i, r in enumerate(results):
        print(f"   [{i+1}] score={r['score']:.3f} -- {r['chunk'][:120]}...")

    print(f"\nGenerating summary...")
    summarizer = Summarizer()
    full_text = " ".join(chunks)
    summary = summarizer.summarize(full_text, max_length=120, min_length=30)
    print(f"   Summary: {summary}")

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s")

    store.delete(doc_id)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/demo.py <path/to/document.pdf>")
        sys.exit(1)
    main(sys.argv[1])
