"""
Main orchestrator: ties content generation, tracking, and open-source tools together.

Daily workflow:
  1. Load product config + keywords
  2. Generate content batch (multi-platform, multi-region)
  3. Save to output/ with tracking log
  4. Print summary with next steps

Integration with open-source tools:
  - Affitor: for advanced content strategy and SEO skills
  - PromoAgent: for Reddit opportunity discovery and reply generation
  - Springy: for multi-platform content distribution

See integrations/ for setup instructions for each tool.
"""

import json
import random
from pathlib import Path
from datetime import datetime
from typing import Optional

from .rewriter import ContentPipeline
from .free_model import FreeModelClient
from .tracker import Tracker
from .keyword_research import KeywordResearch
from .sources import MaterialManager

BASE = Path(__file__).parent.parent
CONFIG_DIR = BASE / "config"
OUTPUT_DIR = BASE / "output"


class AffiliatePipeline:
    """Main pipeline orchestrator."""

    def __init__(self):
        self.model = FreeModelClient()
        self.content = ContentPipeline()
        self.tracker = Tracker()
        self.materials = MaterialManager()

    def load_settings(self) -> dict:
        """Load global settings with defaults."""
        path = CONFIG_DIR / "settings.json"
        if path.exists():
            with open(path) as f:
                return json.load(f).get("settings", {})
        return {}

    def load_products(self) -> list:
        """Load product configurations."""
        path = CONFIG_DIR / "products.json"
        if not path.exists():
            print("[ERR] 缺少 config/products.json")
            return []
        with open(path) as f:
            return json.load(f)["products"]

    def load_keywords(self) -> dict:
        """Load keyword configurations."""
        path = CONFIG_DIR / "keywords.json"
        if not path.exists():
            return {}
        with open(path) as f:
            return json.load(f)

    def daily_generate(self, products: Optional[list] = None,
                       count_per_product: int = 3) -> list:
        """
        Daily content generation run.

        Generates content across multiple platforms for each product.
        Skips products with missing affiliate links.
        """
        if products is None:
            products = self.load_products()

        if not products:
            print("[ERR] 没有产品配置，编辑 config/products.json")
            return []

        if not self.model.has_provider():
            print("[WARN] 未设置 API Key，使用模拟模式")
            print("       设置 GEMINI_API_KEY 启用免费模型\n")

        keywords = self.load_keywords()
        results = []

        for product in products:
            name = product["name"]
            display = product["display"]
            link = product["affiliate_link"]

            if "YOUR_CODE" in link:
                print(f"  [SKIP] {display}: 未配置推广链接")
                continue

            available_platforms = product.get("platforms", ["reddit", "quora", "twitter"])
            regions = product.get("regions", ["us"])
            product_keywords = keywords.get(name, {})

            # Mix primary and Chinese keywords
            all_kws = (product_keywords.get("primary", []) +
                      product_keywords.get("chinese", []))

            if not all_kws:
                # Auto-generate keywords via research
                kp = KeywordResearch()
                clusters = kp.generate_keywords(product)
                all_kws = []
                for kws in clusters.values():
                    all_kws.extend(kws[:2])

            if not all_kws:
                all_kws = [f"best {display} tutorial", f"how to use {display}"]

            settings = self.load_settings()
            de_ai_enabled = settings.get("de_ai", {}).get("enabled", True)

            # Generate content for this product
            for i in range(count_per_product):
                for platform in available_platforms:
                    keyword = random.choice(all_kws)
                    region = random.choice(regions)

                    # Generate
                    result = self.content.generate(
                        source_text=f"产品：{display}\n关键词：{keyword}",
                        product_name=display,
                        affiliate_link=link,
                        platform=platform,
                        region=region,
                        keyword=keyword,
                        de_ai_enabled=de_ai_enabled,
                    )

                    # Save to file
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    out_dir = OUTPUT_DIR / name
                    out_dir.mkdir(parents=True, exist_ok=True)
                    filename = f"{platform}_{region}_{timestamp}.md"
                    filepath = out_dir / filename

                    filepath.write_text(
                        f"# {result['title']}\n\n"
                        f"**产品**: {display}  **平台**: {platform}  **地区**: {region}\n"
                        f"**关键词**: {keyword}\n"
                        f"**质量评分**: {result['engagement_score']}/100\n\n"
                        f"---\n\n"
                        f"{result['content']}\n\n"
                        f"---\n"
                        f"推广链接：{link}"
                    )

                    # Track
                    content_id = self.tracker.log_generation(
                        product=name,
                        platform=platform,
                        title=result["title"],
                        file_path=str(filepath),
                        keyword=keyword,
                        region=region,
                        word_count=result["word_count"],
                    )

                    result["content_id"] = content_id
                    result["filepath"] = str(filepath)
                    results.append(result)

                    print(f"  [{len(results)}] {platform:8s} | {region:4s} | {result['title'][:50]}")

        return results

    def daily_run(self) -> dict:
        """Full daily pipeline: generate + report."""
        print("=" * 56)
        print("  AI Affiliate - 每日内容生成")
        print("=" * 56)
        print()

        if not self.model.has_provider():
            print("  ⚠️  未设置 API Key，使用模拟模式")
            print()

        results = self.daily_generate()
        stats = self.tracker.get_stats()

        print()
        print("-" * 56)
        print("  今日摘要")
        print("-" * 56)
        print(f"  生成内容: {len(results)} 篇")
        print(f"  累计内容: {stats['total_content']} 篇")
        print(f"  累计转化: ${stats['total_commission']:.2f}")
        print()
        print("  按产品分布:")
        for product, count in stats.get("by_product", {}).items():
            print(f"    - {product}: {count} 篇")

        # Tips for next steps
        if results:
            print()
            print("  下一步操作:")
            print(f"    1. 查看 output/ 目录下的生成内容")
            print(f"    2. 审核后手动发布到对应平台")
            print(f"    3. 运行 python3 run.py publish 记录发布情况")
            print(f"    4. 安装开源工具实现半自动化发布")
            print(f"       → 查看 integrations/README.md")

        return {"generated": len(results), "stats": stats}

    def check_status(self) -> dict:
        """Print full system status."""
        products = self.load_products()
        stats = self.tracker.get_stats()

        print("=" * 56)
        print("  AI Affiliate - 系统状态")
        print("=" * 56)
        print()

        # API status
        print("  API 状态:")
        print(f"    Gemini:    {'✅ 已配置' if self.model._detect_providers() else '❌ 未配置'}")
        print(f"    DeepSeek:  {'✅ 已配置' if 'deepseek' in self.model._detect_providers() else '❌ 未配置'}")
        print()

        # Products
        print(f"  产品 ({len(products)}):")
        for p in products:
            link_ok = "YOUR_CODE" not in p["affiliate_link"]
            print(f"    {'✅' if link_ok else '⚠️'} {p['display']:15s} | {p['category']:15s} | 佣金: {p['commission']}")
        print()

        # Stats
        print(f"  数据统计:")
        print(f"    内容总量:  {stats['total_content']} 篇")
        print(f"    已发布:    {stats['total_published']} 篇")
        print(f"    点击:      {stats['total_clicks']} 次")
        print(f"    转化:      {stats['total_conversions']} 次")
        print(f"    收入:      ${stats['total_commission']:.2f}")
        print()

        best = self.tracker.get_best_performers()
        if best:
            print(f"  表现最好的内容:")
            for b in best:
                print(f"    {b['product']:15s} | {b['platform']:10s} | {b['clicks']} 次点击")

        print()
        if not self.model.has_provider():
            print("  💡 设置 API Key 启用真实 AI 模型:")
            print("     export GEMINI_API_KEY=your_key")
            print("     export DEEPSEEK_API_KEY=your_key")

        return stats
