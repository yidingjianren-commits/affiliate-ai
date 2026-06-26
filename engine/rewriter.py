"""
Content rewriting engine.

Transforms source content into platform-optimized formats with
natural affiliate link integration. Supports region-specific adaptation.

Templates are available for:
  - reddit:  Tutorial posts, Q&A, experience sharing
  - quora:   Structured answers with tool recommendations
  - twitter: Short posts with hashtags
  - medium:  Full-length tutorials with sections
  - zhihu:   Chinese Q&A (for Chinese market)
"""

from .free_model import FreeModelClient

# Platform-specific rewriting templates
# Each template instructs the LLM to produce content in a specific format
# The {affiliate_link} placeholder is replaced at generation time
TEMPLATES = {
    "reddit": (
        "你是一个有经验的开发者，在Reddit技术板块分享经验。\n"
        "请按以下要求改写内容：\n"
        "1. 语气自然，以 'I recently found...' 或 'After trying X for Y months...' 开头\n"
        "2. 分享真实使用体验，包含 1-2 个具体细节\n"
        "3. 在推荐工具时自然植入链接：{affiliate_link}\n"
        "4. 300-600 字\n"
        "5. 结尾加 1 个引导互动的问题\n"
        "6. 不要看起来像广告，保持技术分享风格"
    ),
    "quora": (
        "你是一个AI工具深度用户，在Quora上回答问题。\n"
        "请按以下要求改写：\n"
        "1. 开头直接点明答案\n"
        "2. 分 3-5 点说明，每点加粗关键词\n"
        "3. 在推荐具体工具时自然使用：{affiliate_link}\n"
        "4. 200-400 字\n"
        "5. 结尾总结推荐"
    ),
    "twitter": (
        "将以下内容改写为Twitter/X推文：\n"
        "1. 简洁有力，200字以内\n"
        "2. 包含 2-3 个相关话题标签\n"
        "3. 自然加入推荐链接：{affiliate_link}\n"
        "4. 可以加 1 个 emoji 增加可读性\n"
        "5. 语气专业但不生硬"
    ),
    "medium": (
        "将以下内容改写为一篇Medium技术教程：\n"
        "1. 结构：标题 → 引言（问题背景）→ 步骤 → 常见问题 → 总结\n"
        "2. 在总结部分自然推荐工具：{affiliate_link}\n"
        "3. 1000-1500 字\n"
        "4. 每个步骤有小标题\n"
        "5. 包含 1 个代码示例或配置片段"
    ),
    "zhihu": (
        "你是一个有经验的开发者，在知乎上回答问题。\n"
        "请按以下要求改写：\n"
        "1. 开头直接给出结论\n"
        "2. 分点分享经验，包含实际使用场景\n"
        "3. 在推荐工具时自然植入：{affiliate_link}\n"
        "4. 400-800 字\n"
        "5. 语气专业但不广告"
    ),
}


class ContentPipeline:
    """Content production pipeline: source → rewrite → platform-format."""

    def __init__(self):
        self.model = FreeModelClient()

    def generate(self, source_text: str, product_name: str,
                 affiliate_link: str, platform: str = "reddit",
                 region: str = "us", keyword: str = "") -> dict:
        """
        Generate platform-optimized content from source material.

        Args:
            source_text: Original content to rewrite
            product_name: Product being promoted
            affiliate_link: Affiliate tracking link
            platform: Target platform (reddit/quora/twitter/medium/zhihu)
            region: Target region (us/cn/sea)
            keyword: Target keyword this content addresses

        Returns:
            dict with title, content, platform, product, region, engagement
        """
        template = TEMPLATES.get(platform, TEMPLATES["reddit"])
        instruction = template.format(affiliate_link=affiliate_link)
        context = f"产品：{product_name}\n关键词：{keyword}"

        raw_content = self.model.generate(instruction, context)

        # Extract title from first heading or first line
        title = self._extract_title(raw_content, product_name, keyword)

        # Estimate word count
        word_count = len(raw_content.split())

        # Generate engagement predictions (for quality scoring)
        engagement = self._score_engagement_quality(raw_content, platform)

        return {
            "title": title,
            "content": raw_content,
            "platform": platform,
            "product": product_name,
            "region": region,
            "keyword": keyword,
            "affiliate_link": affiliate_link,
            "word_count": word_count,
            "engagement_score": engagement["score"],
            "suggestions": engagement["suggestions"],
        }

    def _extract_title(self, content: str, product: str, keyword: str) -> str:
        """Extract or generate title from generated content."""
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("#"):
                return line.lstrip("#").strip()
            if line.startswith("**") and line.endswith("**"):
                return line.strip("*")
        return f"{product} - {keyword[:40]}" if keyword else f"{product} 使用分享"

    def _score_engagement_quality(self, content: str, platform: str) -> dict:
        """
        Simple quality scoring based on content structure.
        Higher score = more likely to get engagement.
        """
        score = 50  # base
        suggestions = []

        lines = content.strip().split("\n")

        # Check length
        words = len(content.split())
        if platform in ("reddit", "medium") and words < 200:
            suggestions.append("内容偏短，建议增加细节")
        elif platform == "twitter" and words > 50:
            suggestions.append("推文偏长，建议精简")
        else:
            score += 10

        # Check for question (engagement bait)
        if "?" in content:
            score += 10
        else:
            suggestions.append("结尾可以加一个问题引导互动")

        # Check for structure
        if any(line.strip().startswith(("- ", "1. ", "2. ")) for line in lines):
            score += 10
        else:
            suggestions.append("建议使用列表结构增加可读性")

        # Check for call to action
        cta_phrases = ["try", "check out", "recommend", "give it a", "试试", "推荐"]
        if any(p in content.lower() for p in cta_phrases):
            score += 10
        else:
            suggestions.append("缺少明确的推荐引导")

        # Region-specific
        if platform == "zhihu":
            score += 5  # Chinese content platform bonus

        return {"score": min(score, 100), "suggestions": suggestions[:3]}

    def batch_generate(self, items: list) -> list:
        """Generate multiple pieces of content from a list of configs."""
        results = []
        for item in items:
            result = self.generate(**item)
            results.append(result)
        return results
