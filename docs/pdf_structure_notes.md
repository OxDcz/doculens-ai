# PDF Structure Detection Notes

## The challenge

PDFs don't have explicit structure. A "heading" is just text in a larger font. A "table" is just lines and text positioned in a grid. Structure detection requires heuristics.

## Current approach

### Heading detection
- Font size > body text (usually > 14pt for headings)
- Bold weight
- Preceded by whitespace
- Short line length (< 80 chars)

### Paragraph detection
- Consistent font size
- Lines flow left-to-right with consistent indentation
- Separated by blank lines or spacing

### Table detection (WIP)
- Horizontal/vertical lines forming a grid
- Aligned columns of text
- This is the weakest part — lots of false positives

## What I've tried

### Font-based heuristics
Works for well-formatted PDFs. Fails on:
- Scanned documents (no font info)
- PDFs with unusual formatting
- Multi-column layouts

### ML-based detection (haven't implemented yet)
- LayoutLM, DocFormer: need GPU, might be overkill
- PaddleOCR's layout analysis: looks promising but heavy

## Next steps

- Try PaddleOCR layout detection on a sample set
- Add confidence scores to structure detection
- Allow manual correction (user marks headings/tables)
