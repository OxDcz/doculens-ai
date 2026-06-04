# Contributing

Pull requests welcome. Here's how to get started.

## Setup

```bash
git clone https://github.com/OxDcz/doculens-ai.git
cd doculens-ai
pip install -e ".[dev]"
cd frontend && npm install
```

## Running locally

```bash
# Backend
uvicorn backend.main:app --reload

# Frontend
cd frontend && npm run dev
```

## What to work on

Check the issue tracker. Issues labeled `good-first-issue` are good starting points.

Things I'd especially appreciate help with:
- Table detection accuracy on complex layouts
- Non-Latin language OCR support
- Frontend UX improvements
- More export formats

## Guidelines

- Keep PRs focused — one feature or fix per PR
- Include tests for new functionality
- Update the README if you change the public API
- Use conventional commits (feat:, fix:, docs:, etc.)

## Questions

Open a discussion in the Issues tab. I'm responsive during weekdays.
