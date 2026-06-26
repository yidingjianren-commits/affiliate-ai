# CLAUDE.md - AI Affiliate Project Guide

## Project Context
AI-driven affiliate marketing system. Generates content using free LLMs,
distributes to Reddit/Quora/Medium/Twitter, tracks conversions.

## Commands
```
python3 run.py              # Daily content generation
python3 run.py status       # System status + stats
python3 run.py plan         # Content plan
python3 run.py publish      # Record publish events
```

## Key Configs
- `config/products.json` — Add/modify products and affiliate links
- `config/keywords.json` — Keywords per product per region
- `config/settings.json` — Global settings

## Architecture
- `engine/pipeline.py` — Main orchestrator
- `engine/free_model.py` — Free LLM client (Gemini/DeepSeek fallback)
- `engine/rewriter.py` — Content rewriting per platform
- `engine/tracker.py` — SQLite conversion tracking
- `output/{product}/` — Generated content

## Memory System
- `MEMORY.md` — Detailed project memory for AI context reload
- `integrations/` — Open-source tool bridge docs

## Rules
- Never commit API keys or .env files
- Output content goes to output/{product}/{platform}_{region}_{timestamp}.md
- Tracking DB is data/tracking.db (gitignored)
- MEMORY.md is the primary AI context index
