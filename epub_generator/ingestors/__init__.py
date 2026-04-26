from __future__ import annotations

from typing import Dict, Type

from epub_generator.ingestors.base import BaseIngestor
from epub_generator.ingestors.markdown_ingestor import MarkdownIngestor

INGESTORS: Dict[str, Type[BaseIngestor]] = {
    "markdown": MarkdownIngestor,
}
