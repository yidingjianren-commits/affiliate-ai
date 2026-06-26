"""
Keyword research and content planning.

Generates keyword clusters per product and identifies
content opportunities based on search intent.

Keyword types:
  - informational: "how to use X", "what is X"
  - commercial: "X vs Y", "best X for Z"
  - transactional: "X pricing", "X discount", "X review"
  - navigational: "X login", "X docs"
"""

from typing import List


# Intent-based keyword templates per product type
KEYWORD_PATTERNS = {
    "ai_coding": {
        "informational": [
            "how to use {product}",
            "what is {product}",
            "{product} tutorial for beginners",
            "{product} tips and tricks",
            "getting started with {product}",
        ],
        "commercial": [
            "{product} vs {competitor}",
            "best AI code editor 2026",
            "{product} review",
            "is {product} worth it",
            "alternatives to {product}",
        ],
        "transactional": [
            "{product} pricing",
            "{product} free vs pro",
            "{product} discount",
            "buy {product}",
            "migrate to {product}",
        ],
    },
    "cloud": {
        "informational": [
            "how to deploy on {product}",
            "{product} for beginners",
            "AI deployment guide {product}",
            "setup VPS on {product}",
        ],
        "commercial": [
            "{product} vs {competitor}",
            "best VPS for AI 2026",
            "cheapest cloud provider",
        ],
        "transactional": [
            "{product} pricing",
            "{product} referral bonus",
            "{product} coupon",
        ],
    },
    "automation": {
        "informational": [
            "how to automate with {product}",
            "{product} workflow tutorial",
            "AI automation guide {product}",
        ],
        "commercial": [
            "{product} vs {competitor}",
            "best automation tools 2026",
        ],
        "transactional": [
            "{product} pricing plans",
            "{product} free tier",
        ],
    },
}


class KeywordResearch:
    """Keyword discovery and content planning."""

    @staticmethod
    def generate_keywords(product: dict) -> dict:
        """
        Generate keyword clusters for a product based on its category.

        Args:
            product: Product config dict with name, category, tags, etc.

        Returns:
            dict with keyword clusters by intent type
        """
        category = product.get("category", "ai_coding")
        name = product["display"]
        patterns = KEYWORD_PATTERNS.get(category, KEYWORD_PATTERNS["ai_coding"])

        competitors = {
            "ai_coding": ["Copilot", "Windsurf", "Tabnine"],
            "cloud": ["DigitalOcean", "AWS", "Linode"],
            "automation": ["Zapier", "Make"],
        }.get(category, [])

        clusters = {}
        for intent, templates in patterns.items():
            keywords = []
            for tpl in templates:
                kw = tpl.format(product=name, competitor=competitors[0] if competitors else "other")
                keywords.append(kw)

                # Add variant with second competitor if relevant
                if "{competitor}" in tpl and len(competitors) > 1:
                    kw2 = tpl.format(product=name, competitor=competitors[1])
                    keywords.append(kw2)

            clusters[intent] = keywords[:8]

        return clusters

    @staticmethod
    def plan_content_batch(products: List[dict], count_per_product: int = 3) -> List[dict]:
        """
        Generate a batch content plan: what to write, for which keyword.

        Returns:
            List of content tasks: {product, keyword, intent, platform_recommendation}
        """
        plans = []
        platform_map = {
            "informational": ["medium", "reddit", "zhihu"],
            "commercial": ["quora", "reddit", "twitter"],
            "transactional": ["quora", "medium"],
        }

        for product in products:
            clusters = KeywordResearch.generate_keywords(product)

            # Sample keywords from each intent type
            count_per_intent = max(1, count_per_product // len(clusters))
            for intent, kws in clusters.items():
                for kw in kws[:count_per_intent]:
                    platforms = platform_map.get(intent, ["reddit"])
                    plans.append({
                        "product": product["display"],
                        "product_name": product["name"],
                        "affiliate_link": product["affiliate_link"],
                        "keyword": kw,
                        "intent": intent,
                        "recommended_platforms": platforms,
                        "regions": product.get("regions", ["us"]),
                    })

        return plans
