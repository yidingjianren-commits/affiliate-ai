# Open-Source Tool Integrations

This directory contains setup and usage guides for open-source tools
that extend the affiliate-ai core engine.

## Available Integrations

| Tool | Purpose | Status | Setup |
|------|---------|--------|-------|
| **Affitor Skills** | 52 AI agent skills for full affiliate funnel | Ready | `bash install_affitor.sh` |
| **PromoAgent** | Autonomous Reddit marketing agent | Ready | See promoagent_bridge.md |
| **Springy** | Multi-platform content distribution | Ready | See springy_bridge.md |

## Why These Tools

Rather than building everything from scratch, we leverage existing
open-source ecosystems. Each tool covers a specific gap:

- **Affitor**: Content strategy, SEO research, trend discovery
- **PromoAgent**: Safe Reddit engagement (context-aware replies, anti-ban)
- **Springy**: 14-platform distribution pipeline

## Architecture

```
affiliate-ai engine (config + generation + tracking)
        |
        v
Integrations layer (bridges to open-source tools)
        |
        +---> Affitor Skills (content strategy)
        +---> PromoAgent (Reddit automation)
        +---> Springy (cross-platform publishing)
```

## Adding a New Tool

1. Create a bridge file in this directory
2. Document setup steps + configuration
3. Update this README
