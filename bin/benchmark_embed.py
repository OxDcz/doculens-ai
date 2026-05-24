#!/usr/bin/env python3
"""Micro-benchmark: measure embedding throughput on CPU vs GPU.

Usage:
    python scripts/benchmark_embed.py --device cpu --num-texts 1000
    python scripts/benchmark_embed.py --device cuda --num-texts 1000
"""

import argparse
import time
import random


def generate_texts(n: int, length: int) -> list[str]:
    """Generate random text samples for benchmarking."""
    words = ["the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog",
             "machine", "learning", "transformer", "attention", "neural",
             "network", "document", "extraction", "semantic", "search"]
    texts = []
    for _ in range(n):
        text = " ".join(random.choice(words) for _ in range(length // 4))
        texts.append(text)
    return texts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cpu", choices=["cpu", "cuda"])
    parser.add_argument("--num-texts", type=int, default=500)
    parser.add_argument("--text-length", type=int, default=256)
    parser.add_argument("--model", default="BAAI/bge-small-en-v1.5")
    args = parser.parse_args()

    from backend.core.embedder import Embedder
    from backend.config import settings

    settings.device = args.device

    print(f"Benchmark: {args.model} on {args.device}")
    print(f"   Texts: {args.num_texts} x ~{args.text_length} chars")

    texts = generate_texts(args.num_texts, args.text_length)

    embedder = Embedder()

    _ = embedder.embed(texts[:10])

    t0 = time.time()
    embeddings = embedder.embed(texts)
    elapsed = time.time() - t0

    throughput = args.num_texts / elapsed
    print(f"\nResults:")
    print(f"   Total time: {elapsed:.2f}s")
    print(f"   Throughput: {throughput:.1f} texts/sec")
    print(f"   Embedding dim: {len(embeddings[0])}")
    print(f"   Per-text: {elapsed/args.num_texts*1000:.1f} ms")


if __name__ == "__main__":
    main()
