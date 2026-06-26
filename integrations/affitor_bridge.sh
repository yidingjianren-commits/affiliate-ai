#!/bin/bash
# Affitor Skills - Setup & Usage Guide
#
# Affitor provides 50+ AI agent skills for the full affiliate marketing funnel.
# Skills include: trending research, content generation, SEO, landing pages,
# analytics, and automation.
#
# Prerequisites: Node.js (for npx)
#   brew install node

echo "=== Affitor Skills ==="
echo ""

# Install
if ! npx skills list 2>/dev/null | grep -q affiliate; then
    echo "Installing Affitor Skills..."
    npx skills add Affitor/affiliate-skills
else
    echo "✅ Affitor Skills already installed"
fi

echo ""
echo "=== Available Skills ==="
echo "Run these in Claude Code:"
echo ""
echo "  /affiliate-research          - Find trending affiliate programs"
echo "  /affiliate-content           - Generate content for any product"
echo "  /affiliate-seo               - SEO analysis for content"
echo "  /affiliate-analytics         - Track performance"
echo ""
echo "=== Integration with affiliate-ai ==="
echo ""
echo "The affiliate-ai engine handles daily content generation."
echo "Use Affitor Skills for:"
echo "  1. Discovering new product opportunities"
echo "  2. Deep keyword research for specific niches"
echo "  3. Content strategy optimization"
echo "  4. Landing page copywriting"
echo ""
echo "Workflow:"
echo "  Affitor Research → affiliate-ai Generate → PromoAgent Distribute"
echo ""
