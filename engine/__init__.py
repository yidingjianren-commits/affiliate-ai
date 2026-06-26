"""
affiliate-ai engine: AI-powered affiliate content generation & distribution.

Architecture:
  pipeline.py         - Main orchestrator (the entry point for all operations)
  free_model.py       - Free/cheap LLM client (Gemini, DeepSeek, mock fallback)
  rewriter.py         - Content rewriting & multi-platform adaptation
  sources.py          - Source content fetching (web, materials)
  keyword_research.py - Keyword discovery and analysis
  tracker.py          - SQLite-based conversion tracking & analytics

Usage:
  from engine.pipeline import AffiliatePipeline
  pipeline = AffiliatePipeline()
  pipeline.daily_run()  # Full daily generation + tracking
"""

from .pipeline import AffiliatePipeline
from .free_model import FreeModelClient
from .rewriter import ContentPipeline
from .tracker import Tracker
