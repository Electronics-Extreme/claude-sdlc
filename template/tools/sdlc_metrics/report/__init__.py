"""Report formatters: text, json, markdown, html-standalone."""
from __future__ import annotations

from .text import format_text
from .json_ import format_json
from .markdown import format_markdown
from .html import format_html

__all__ = ["format_text", "format_json", "format_markdown", "format_html"]
