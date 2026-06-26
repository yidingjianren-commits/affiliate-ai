"""
Source content acquisition.

Strategies (in priority order):
  1. Local materials/ directory - manually curated source articles
  2. Web scraping - official docs, tutorials
  3. GitHub READMEs - popular project docs
  4. Manual input - direct text paste

The goal is to collect raw material that the rewriter will transform.
"""

import re
import requests
from pathlib import Path
from typing import Optional


# Known doc URLs for each product (used as source material)
PRODUCT_DOCS = {
    "cursor": "https://docs.cursor.sh/get-started",
    "windsurf": "https://docs.codeium.com/getting-started",
    "vultr": "https://www.vultr.com/docs/",
    "n8n": "https://docs.n8n.io/",
    "adsPower": "https://help.adspower.net/",
}

MATERIALS_DIR = Path(__file__).parent.parent / "materials"


class SourceFetcher:
    """Fetches source content from various origins."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/120.0.0.0 Safari/537.36")
        })

    def fetch_docs(self, product: str) -> str:
        """Fetch official documentation for a product."""
        url = PRODUCT_DOCS.get(product)
        if not url:
            return ""
        return self._fetch_and_extract(url)

    def fetch_url(self, url: str) -> str:
        """Fetch and extract text from any URL."""
        return self._fetch_and_extract(url)

    def _fetch_and_extract(self, url: str) -> str:
        """Fetch URL and extract readable text."""
        try:
            resp = self.session.get(url, timeout=15)
            resp.raise_for_status()
            text = resp.text

            # Strip HTML tags, scripts, styles
            text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', '\n', text)
            text = re.sub(r'\n{4,}', '\n\n', text)
            return text.strip()[:5000]
        except Exception as e:
            print(f"  [WARN] 抓取失败 [{url}]: {e}")
            return ""


class MaterialManager:
    """Manages local source materials (manually saved articles, docs, notes)."""

    def __init__(self):
        self.materials_dir = MATERIALS_DIR
        self.materials_dir.mkdir(parents=True, exist_ok=True)

    def save(self, product: str, title: str, content: str, source_url: str = "") -> Path:
        """Save a piece of source material."""
        safe_name = re.sub(r'[^a-zA-Z0-9_一-鿿]', '_', title)[:50]
        filepath = self.materials_dir / f"{product}_{safe_name}.md"
        header = f"---\nproduct: {product}\nsource: {source_url}\n---\n\n"
        filepath.write_text(header + content)
        return filepath

    def list_recent(self, product: Optional[str] = None, limit: int = 10) -> list:
        """List recent source materials, optionally filtered by product."""
        files = sorted(self.materials_dir.glob("*.md"), reverse=True)
        if product:
            files = [f for f in files if f.name.startswith(product)]
        return [{"path": str(f), "name": f.stem} for f in files[:limit]]

    def get_content(self, filepath: str) -> str:
        """Read material content, stripping YAML frontmatter."""
        text = Path(filepath).read_text()
        # Strip YAML frontmatter
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                text = parts[2].strip()
        return text
