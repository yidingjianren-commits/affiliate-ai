#!/bin/bash
# AI Affiliate - 一键部署脚本
set -e

echo "========================================"
echo "  AI Affiliate - 系统部署"
echo "========================================"
echo ""

# 1. Python 依赖
echo "[1/3] 安装 Python 依赖..."
pip3 install -q -r requirements.txt 2>/dev/null || pip install -q -r requirements.txt
echo "      完成"

# 2. 目录结构
echo "[2/3] 创建目录结构..."
mkdir -p output data materials .cache
echo "      完成"

# 3. 环境变量
echo "[3/3] 环境变量检查..."
if [ -z "$GEMINI_API_KEY" ] && [ ! -f .env ]; then
    echo "      ⚠️  未设置 API Key"
    echo "      设置方法："
    echo "      export GEMINI_API_KEY=your_key    # 免费，推荐"
    echo "      export DEEPSEEK_API_KEY=your_key  # 极低价"
    echo ""
    echo "      或创建 .env 文件："
    echo "      echo 'GEMINI_API_KEY=your_key' > .env"
fi

echo ""
echo "========================================"
echo "  ✅ 部署完成"
echo "========================================"
echo ""
echo "  下一步："
echo "  1. 编辑 config/products.json 填写推广链接"
echo "  2. 设置 API Key"
echo "  3. 运行 python3 run.py status  查看状态"
echo "  4. 运行 python3 run.py         开始生成"
echo ""
