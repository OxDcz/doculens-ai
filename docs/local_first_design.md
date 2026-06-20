# Local-First Design Philosophy

## Why local-first?

1. **Privacy**: Documents stay on your machine
2. **Speed**: No network latency for processing
3. **Reliability**: Works offline
4. **Cost**: No API fees

## Trade-offs

| Aspect | Local | Cloud |
|--------|-------|-------|
| Privacy | ✅ Full | ❌ Data leaves machine |
| Speed | ✅ No network | ❌ API latency |
| Quality | ⚠️ Depends on local models | ✅ Best models |
| Setup | ❌ More work | ✅ Just API key |
| Cost | ✅ Free after setup | ❌ Per-document fees |

## Design decisions

1. **No external API calls**: Not even for optional features
2. **Plain file formats**: JSON for index, plain text for content
3. **Incremental processing**: Don't re-process unchanged documents
4. **Graceful degradation**: If OCR fails, still extract what we can

## What this means in practice

- OCR quality is lower than cloud services (Tesseract vs Google Vision)
- Search is simpler (TF-IDF vs vector DB with embeddings)
- No fancy UI (CLI only, for now)

But: my documents never leave my machine, and I can process 1000 PDFs without worrying about API costs.
