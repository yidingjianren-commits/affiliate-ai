# Springy Integration

Write once, publish everywhere. Springy distributes content to 14+ platforms
with per-platform adaptation.

## Setup

Springy runs via npx, no installation needed:

```bash
npx springy init
```

## Platforms Supported

- LinkedIn
- Twitter / X
- Bluesky
- Threads
- Medium
- Dev.to
- Hashnode
- Substack
- YouTube (descriptions)
- TikTok (scripts)

## Integration Workflow

```
affiliate-ai generates content
        |
        v
Springy anchor essay format
        |
        v
Springy fans out to selected platforms
        |
        v
Per-platform optimization (format, length, tone)
        |
        v
Human review → Publish
```

## Configuration

Create `springy.config.json`:

```json
{
  "anchor": {
    "source": "../output/{product}/{file}.md",
    "voice": "technical_developer"
  },
  "platforms": ["linkedin", "twitter", "medium", "devto"],
  "affiliate_integration": {
    "insert_mode": "natural",
    "max_links_per_post": 2
  }
}
```

## Usage

```bash
# Read content from affiliate-ai output and distribute
cd tools/springy
npx springy distribute ../output/cursor/reddit_*.md

# Or use interactive mode
npx springy
```
