# Search Output Example

## Query

```
python doculens.py search report_2019.json "revenue growth asia pacific"
```

## Results

```
Found 5 matches for "revenue growth asia pacific":

1. [Score: 0.89] Page 3, Chunk 7
   "Revenue increased by 12% compared to the previous quarter, driven 
   primarily by strong performance in the Asia-Pacific region. The 
   region contributed $1.8B in total revenue..."

2. [Score: 0.76] Page 15, Chunk 42
   "Asia-Pacific growth was led by Japan (+18%) and Australia (+14%). 
   China revenue was flat due to regulatory headwinds..."

3. [Score: 0.71] Page 8, Chunk 23
   "Looking ahead, we expect continued momentum in APAC driven by 
   new product launches scheduled for Q4..."

4. [Score: 0.65] Page 1, Chunk 2
   "Q3 2024 Financial Highlights: Total revenue $4.2B (+12% QoQ)..."

5. [Score: 0.58] Page 22, Chunk 67
   "Risk factors: Currency fluctuations in APAC markets may impact 
   reported revenue in future quarters..."
```

## Notes

- TF-IDF works surprisingly well for keyword queries
- Semantic search (embeddings) would catch "sales in eastern markets" as related — that's the next step
- Results include page number and chunk ID for easy navigation
