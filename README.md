# AI Affiliate

AI-driven affiliate marketing distribution system. Generate content, distribute across platforms, track conversions.

## Quick Start

```bash
# 1. Install
pip3 install -r requirements.txt

# 2. Set API key (free)
export GEMINI_API_KEY=your_key_here

# 3. Edit products with your affiliate links
#    config/products.json → replace YOUR_CODE

# 4. Run
python3 run.py           # Daily content generation
python3 run.py status    # System overview
python3 run.py plan      # Content strategy
```

## Architecture

```
config/ ──── products, keywords, settings
    │
engine/ ──── core pipeline
    ├── pipeline.py         # Main orchestrator
    ├── free_model.py       # Free LLM client (Gemini/DeepSeek)
    ├── rewriter.py         # Content rewriting engine
    ├── keyword_research.py # Keyword analysis
    ├── sources.py          # Source content fetching
    └── tracker.py          # SQLite conversion tracking
    │
integrations/ ── open-source tool bridges
    ├── install_opensource.sh   # One-click install
    ├── affitor_bridge.sh       # Affitor Skills (50+ AI skills)
    ├── promoagent_bridge.md    # PromoAgent (Reddit agent)
    └── springy_bridge.md       # Springy (multi-platform dist)
    │
output/ ──── generated content by product
data/   ──── tracking database
```

## Products

| Product | Commission | Category | Status |
|---------|-----------|----------|--------|
| Cursor | 30% recurring ($6/mo) | AI Coding | ⚠️ Needs link |
| Windsurf | 20% recurring ($3-5/mo) | AI Coding | ⚠️ Needs link |
| Vultr | $50-200 one-time | Cloud | ⚠️ Needs link |
| n8n | 20% recurring | Automation | ⚠️ Needs link |
| AdsPower | 30% recurring | Browser | ⚠️ Needs link |

## Key Design Decisions

1. **Free models first** — Gemini free tier (1500 req/day), DeepSeek ($0.14/1M tokens)
2. **Semi-automated** — Content generation is automated, publishing requires human review
3. **Track everything** — SQLite tracking to know what's working
4. **Open-source over custom** — Leverage Affitor/PromoAgent/Springy instead of building

## Commands

```bash
python3 run.py           # Daily generation
python3 run.py status    # System + stats
python3 run.py plan      # Content plan
python3 run.py publish   # Record a publish event
```

## Cost (Monthly)

| Item | Cost | Note |
|------|------|------|
| Gemini API | $0 | 1500 free req/day |
| DeepSeek API | ~$1 | Backup model |
| **Total** | **~$1** | |

## Repository

https://github.com/yidingjianren-commits/affiliate-ai
