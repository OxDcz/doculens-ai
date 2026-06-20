# Example: Processing a messy scanned PDF

## Input

A 40-page scanned report from 2019. Issues:
- Mixed orientation (some pages landscape, some portrait)
- Low resolution (~150 DPI)
- Handwritten notes in margins
- Coffee stain on page 12

## Pipeline

```bash
python doculens.py scan ./reports/2019_annual_report.pdf --output report_2019.json
```

## Output

```
Processing: 2019_annual_report.pdf
  Page 1-10: digital text extracted (98% confidence)
  Page 11: scanned image, running OCR...
  Page 12: scanned image, OCR quality: low (coffee stain detected)
  Page 13-40: mixed content
  Total: 40 pages, 12,847 words extracted
  Structure: 12 headings, 47 paragraphs, 3 tables detected
  Chunks: 156 segments created (avg 82 words per chunk)
```

## What worked well

- Digital text extraction is nearly perfect
- Heading detection caught most section breaks
- Chunking keeps paragraphs intact

## What didn't work

- Page 12 (coffee stain): OCR produced garbage for ~40% of the text
- Handwritten margin notes: completely missed
- Table on page 28: detected as "paragraph" — need better table heuristics
