"""
Free/cheap LLM client with automatic fallback.

Priority:
  1. Gemini 2.0 Flash (free tier, 1500 req/day)
  2. DeepSeek Chat (cheap, ~$0.14/1M tokens)
  3. Mock mode (no API key needed, shows structure)

Usage:
  model = FreeModelClient()
  result = model.generate("改写这段文字为Reddit帖子", context="产品名: Cursor")
"""

import os
import json
import requests
from typing import Optional


class FreeModelClient:
    """Multi-provider LLM client. Tries free models first, falls back gracefully."""

    PROVIDERS_CONFIG = {
        "gemini": {
            "env_key": "GEMINI_API_KEY",
            "url_tpl": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}",
            "cost": "free",
            "rate_limit": "1500 req/day",
        },
        "deepseek": {
            "env_key": "DEEPSEEK_API_KEY",
            "url": "https://api.deepseek.com/v1/chat/completions",
            "cost": "$0.14/1M tokens",
            "rate_limit": "500 req/min",
        },
    }

    def __init__(self):
        self._providers = self._detect_providers()

    def _detect_providers(self):
        """Detect available providers from environment variables."""
        available = []
        for name, cfg in self.PROVIDERS_CONFIG.items():
            if os.environ.get(cfg["env_key"]):
                available.append(name)
        return available

    def generate(self, instruction: str, context: str = "") -> str:
        """
        Generate content using best available provider.

        Args:
            instruction: What to do (e.g., "改写为Reddit帖子，语气自然")
            context: Background info (product name, keywords, etc.)

        Returns:
            Generated text content
        """
        prompt = f"{instruction}\n\n背景信息：{context}" if context else instruction

        for provider in self._providers:
            try:
                if provider == "gemini":
                    return self._call_gemini(prompt)
                elif provider == "deepseek":
                    return self._call_deepseek(prompt)
            except Exception as e:
                print(f"  [WARN] {provider} 调用失败: {e}，尝试下一个...")
                continue

        return self._mock_output(instruction)

    def _call_gemini(self, prompt: str) -> str:
        """Call Google Gemini API (free tier)."""
        key = os.environ["GEMINI_API_KEY"]
        url = self.PROVIDERS_CONFIG["gemini"]["url_tpl"].format(key=key)
        resp = requests.post(
            url,
            json={"contents": [{"parts": [{"text": prompt[:8000]}]}]},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    def _call_deepseek(self, prompt: str) -> str:
        """Call DeepSeek Chat API."""
        key = os.environ["DEEPSEEK_API_KEY"]
        resp = requests.post(
            self.PROVIDERS_CONFIG["deepseek"]["url"],
            headers={"Authorization": f"Bearer {key}"},
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt[:6000]}],
                "temperature": 0.7,
            },
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    def _mock_output(self, instruction: str) -> str:
        """Fallback: structured placeholder when no API key is set."""
        return (
            f"# 内容生成（模拟模式）\n\n"
            f"**未检测到 API Key**\n"
            f"设置 GEMINI_API_KEY 或 DEEPSEEK_API_KEY 后自动启用真实模型\n\n"
            f"---\n"
            f"指令: {instruction[:120]}...\n\n"
            f"实际输出格式：\n"
            f"- Reddit 帖子: 300-600字自然语气分享\n"
            f"- Quora 回答: 200-400字结构化回答\n"
            f"- 推文: 150字以内 + 话题标签\n"
            f"- Medium 教程: 1000-1500字完整教程\n"
            f"---\n"
            f"> 设置: export GEMINI_API_KEY=your_key"
        )

    def has_provider(self) -> bool:
        """Check if at least one LLM provider is configured."""
        return len(self._providers) > 0
