#!/bin/bash
# One-click install of all open-source tools
set -e

echo "=========================================="
echo "  Installing open-source tools"
echo "=========================================="

# --- Affitor Skills ---
echo ""
echo "[1/3] Installing Affitor Skills..."
if command -v npx &> /dev/null; then
    npx skills add Affitor/affiliate-skills
    echo "  ✅ Affitor Skills installed"
    echo "  Usage: /affiliate in Claude Code"
else
    echo "  ⚠️  npx not found. Install Node.js first:"
    echo "     brew install node"
fi

# --- PromoAgent ---
echo ""
echo "[2/3] Setting up PromoAgent..."
if [ ! -d "tools/PromoAgent" ]; then
    mkdir -p tools
    git clone https://github.com/haroon0x/PromoAgent.git tools/PromoAgent 2>/dev/null || {
        echo "  ⚠️  Clone failed. Get it manually:"
        echo "     git clone https://github.com/haroon0x/PromoAgent.git"
    }
    if [ -d "tools/PromoAgent" ]; then
        cd tools/PromoAgent
        pip install -r requirements.txt 2>/dev/null || true
        cd ../..
        echo "  ✅ PromoAgent ready at tools/PromoAgent"
        echo "  See integrations/promoagent_bridge.md for config"
    fi
else
    echo "  ✅ PromoAgent already installed"
fi

# --- Springy ---
echo ""
echo "[3/3] Checking Springy..."
if command -v npx &> /dev/null; then
    # Springy is used via npx, no install needed
    echo "  ✅ Springy available via npx"
    echo "  Usage: npx springy"
else
    echo "  ⚠️  npx not found"
fi

echo ""
echo "=========================================="
echo "  Installation complete"
echo "=========================================="
echo ""
echo "See each bridge file for usage:"
echo "  integrations/affitor_bridge.sh"
echo "  integrations/promoagent_bridge.md"
echo "  integrations/springy_bridge.md"
