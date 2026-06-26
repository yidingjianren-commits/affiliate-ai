# AI Affiliate - Project Memory

This file is an index for AI agents (Claude Code, etc.) to understand
the project without re-reading every source file.

## Quick Facts

- **Purpose**: AI-driven affiliate marketing content generation & distribution
- **Stack**: Python 3, SQLite, Gemini/DeepSeek API, open-source tools
- **Target platforms**: Reddit, Quora, Medium, Twitter/X, Zhihu
- **Cost**: ~$1/month (free LLM tiers)
- **GitHub**: https://github.com/yidingjianren-commits/affiliate-ai

## Key Files

| File | Purpose |
|------|---------|
| `engine/pipeline.py` | Main orchestrator - daily run, status, tracking |
| `engine/free_model.py` | Free LLM client with auto-fallback |
| `engine/rewriter.py` | Content rewriting per platform/region |
| `engine/keyword_research.py` | Keyword cluster generation |
| `engine/tracker.py` | SQLite conversion tracking |
| `engine/sources.py` | Source content fetching |
| `run.py` | CLI entry point |
| `config/products.json` | Product & affiliate link configs |
| `config/keywords.json` | Keywords per product per region |
| `integrations/` | Open-source tool bridges |

## Product Config

5 products configured (see `config/products.json`):
1. Cursor - AI coding IDE (30% recurring)
2. Windsurf - AI coding IDE (20% recurring)
3. Vultr - Cloud VPS ($50-200 one-time)
4. n8n - Workflow automation (20% recurring)
5. AdsPower - Fingerprint browser (30% recurring)

All products need `YOUR_CODE` replaced with real affiliate codes.

## Content Pipeline Flow

```
Keyword Research → Source Material → Rewriting → Output Files → Track
     (engine/         (engine/        (engine/      (output/     (engine/
   keyword_         sources.py)      rewriter.py)   product/)   tracker.py)
   research.py)

Integration layer (optional):
  Affitor Skills → PromoAgent → Springy → Multi-platform distribution
```

## Open-Source Integrations

Three external tools can be added (see `integrations/`):
1. **Affitor/affiliate-skills** - 52 AI agent skills (`npx skills add`)
2. **PromoAgent** - LangGraph Reddit agent (`git clone`)
3. **Springy** - Multi-platform publishing (`npx springy`)

## Cost Structure

- Gemini API: Free (1500 req/day)
- DeepSeek API: ~$0.14/1M tokens
- PromoAgent: Free (local deployment)
- Affitor Skills: Free (MIT license)

## Current State

- Core engine: Working (generates content, tracks in SQLite)
- API integration: Needs GEMINI_API_KEY or DEEPSEEK_API_KEY
- Affiliate links: Need real codes in config/products.json
- Open-source tools: Not yet installed (optional)

## Common Gotchas

- Always replace `YOUR_CODE` in `config/products.json` before running
- Gemini free tier is enough for 1500+ content pieces/day
- The system runs locally - no external hosting needed
- Content needs human review before publishing (anti-ban)

## Future Expansion

- Add more products (focus on AI tools with recurring commissions)
- Install and configure PromoAgent for Reddit automation
- Set up Springy for cross-platform distribution
- Add Google Sheets webhook for data export
- Build simple dashboard (Streamlit)
