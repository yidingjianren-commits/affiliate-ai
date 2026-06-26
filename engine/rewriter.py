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
#
# CRITICAL: These templates MUST produce content that doesn't read like AI.
# Every template includes explicit "de-AI" instructions to avoid:
# - Perfect structure (bullet points, numbered lists everywhere)
# - Neutral, personality-free tone
# - Formulaic openings ("In today's digital landscape")
# - Overly grammatically correct (no contractions, no casual language)
# - Generic, vague examples
# - Symmetrical/balanced structure that screams "AI wrote this"

TEMPLATES = {
    "reddit": (
        "你是一个普通开发者，在Reddit上随手发帖分享经验。\n"
        "要求：\n"
        "1. 真人语气，口语化。用 'honestly'、'tbh'、'ngl' 这类词\n"
        "2. 开头不要模板化，直接说事：'Been using X for a month...' 或 'So I tried X because...'\n"
        "3. 内容要有瑕疵，不要完美结构。允许有一两句啰嗦的\n"
        "4. 加入具体数字或细节（不要编得太假，模糊一点也行：'probably saved me ~10 hours'）\n"
        "5. 结尾不要总结，可以加一句抱怨或吐槽\n"
        "6. 链接要像随手贴的：'I used {affiliate_link}'\n"
        "7. 300-600 字\n"
        "8. 禁止：列表项、完美段落、'The future of X is bright' 这类废话\n"
        "9. 最重要：读起来像是一个真人凌晨两点写的，不是营销号"
    ),
    "quora": (
        "你在Quora上回答一个技术问题。\n"
        "要求：\n"
        "1. 开头不用客套，直接回答问题\n"
        "2. 语气像在跟朋友吃饭聊天，不是写论文\n"
        "3. 融入个人经历：'I was in the same boat last month...'\n"
        "4. 推荐时像随口提到：'I ended up going with {affiliate_link}'\n"
        "5. 200-400 字\n"
        "6. 禁止：分点列表、总结段落、'In conclusion'\n"
        "7. 可以有一两处语法不完美的地方\n"
        "8. 结尾自然收住就行"
    ),
    "twitter": (
        "发一条Twitter/X推文。\n"
        "要求：\n"
        "1. 口语化，像在发日常推\n"
        "2. 150字以内\n"
        "3. 不要超过2个标签，标签不要排在最后\n"
        "4. 自然融入：{affiliate_link}\n"
        "5. 禁止：'Revolutionary'、'Game-changing'、'Must-have' 这类营销词\n"
        "6. 可以拼写错误或缩略词（gonna, kinda）\n"
        "7. 像是随手发的，不是精心策划的"
    ),
    "medium": (
        "写一篇Medium技术教程。\n"
        "要求：\n"
        "1. 用第一人称，分享真实踩坑经验\n"
        "2. 结构松散一点，不要严格的 引言-步骤-总结\n"
        "3. 每个小标题是具体的做法，不是名词短语\n"
        "4. 代码示例手写风格，不要太完美\n"
        "5. 在某个步骤里自然地推荐：{affiliate_link}\n"
        "6. 800-1200 字\n"
        "7. 结尾可以说说还有什么问题没解决，显得真实"
    ),
    "zhihu": (
        "你在知乎上回答问题。\n"
        "要求：\n"
        "1. 直接给结论，不要铺垫\n"
        "2. 口语化，带点个人风格（可以加括号吐槽）\n"
        "3. 分享具体经历，不只是理论\n"
        "4. 推荐时像顺便提的：'我用的{affiliate_link}，还行'\n"
        "5. 400-800 字\n"
        "6. 禁止：列表项、'首先其次最后'、'综上所述'\n"
        "7. 结尾可以不太完美，像还没说完"
    ),
}


class ContentPipeline:
    """Content production pipeline: source → rewrite → platform-format."""

    def __init__(self):
        self.model = FreeModelClient()

    def generate(self, source_text: str, product_name: str,
                 affiliate_link: str, platform: str = "reddit",
                 region: str = "us", keyword: str = "",
                 de_ai_enabled: bool = True) -> dict:
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

        raw_content = self.model.generate(instruction, context, temperature=0.9)

        # Post-process: remove AI tells if enabled
        if de_ai_enabled:
            raw_content = self.model.de_ai(raw_content)

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
