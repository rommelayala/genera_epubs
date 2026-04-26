from __future__ import annotations

from typing import Dict, Type

from epub_generator.ingestors.base import BaseIngestor
from epub_generator.ingestors.markdown_ingestor import MarkdownIngestor
from epub_generator.ingestors.pdf_ingestor import PdfIngestor

INGESTORS: Dict[str, Type[BaseIngestor]] = {
    "markdown": MarkdownIngestor,
    "pdf": PdfIngestor,
}
