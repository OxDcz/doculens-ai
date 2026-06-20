# Chunking Example

## How text gets split

Input text from a PDF page:

```
Introduction

This document describes the quarterly financial results for Q3 2024. 
Revenue increased by 12% compared to the previous quarter, driven 
primarily by strong performance in the Asia-Pacific region.

Key Highlights

- Total revenue: $4.2B
- Operating margin: 23.1%
- New customers: 1,247

The board has approved a dividend of $0.85 per share...
```

## Default chunking (paragraph-level)

Chunk 1:
```
Introduction
This document describes the quarterly financial results for Q3 2024. 
Revenue increased by 12% compared to the previous quarter, driven 
primarily by strong performance in the Asia-Pacific region.
```

Chunk 2:
```
Key Highlights
- Total revenue: $4.2B
- Operating margin: 23.1%
- New customers: 1,247
```

Chunk 3:
```
The board has approved a dividend of $0.85 per share...
```

## With overlap (2 sentences)

Chunk 1 ends with: "...strong performance in the Asia-Pacific region."
Chunk 2 starts with: "...driven primarily by strong performance in the Asia-Pacific region. Key Highlights..."

This helps when a query spans paragraph boundaries.

## Config

```python
chunker = Chunker(
    max_words=200,
    overlap_sentences=2,
    respect_headings=True,  # Don't merge across headings
)
```
