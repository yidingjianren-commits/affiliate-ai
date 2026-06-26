# PromoAgent Integration

LangGraph-powered autonomous Reddit marketing agent.
Discusses relevant threads, generates context-aware replies, and posts without getting blocked.

## Setup

```bash
# From affiliate-ai root
mkdir -p tools
git clone https://github.com/haroon0x/PromoAgent.git tools/PromoAgent
cd tools/PromoAgent
pip install -r requirements.txt

# Configure Reddit API credentials
export REDDIT_CLIENT_ID=your_id
export REDDIT_CLIENT_SECRET=your_secret
export REDDIT_USERNAME=your_username
export REDDIT_PASSWORD=your_password
```

## Configuration

Create `tools/PromoAgent/config.yaml`:

```yaml
brand_voice: "Technical developer sharing genuine experience"
target_subreddits:
  - r/ChatGPT
  - r/ClaudeAI
  - r/SideProject
  - r/SaaS
monitor_keywords:
  - "cursor"
  - "windsurf"
  - "AI coding"
  - "best IDE"
reply_strategy: "value_first"  # Provide value, mention product naturally
max_replies_per_hour: 3
safety_mode: "strict"  # Avoids ban-prone behavior
```

## Usage with affiliate-ai

PromoAgent works best as a **complement** to affiliate-ai's content generation:

1. **affiliate-ai** generates the source content (tutorials, reviews, comparisons)
2. **PromoAgent** identifies Reddit threads where that content would be valuable
3. PromoAgent generates context-aware replies referencing the content

This two-step approach is safer and more effective than automated posting.

## Safety Rules

- Never post direct affiliate links in Reddit comments
- Add value first, mention tools naturally
- Max 3 replies/hour per account
- Use different phrasing each time (no templates)
- Let 30+ seconds between actions
