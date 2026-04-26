from __future__ import annotations

import logging
from pathlib import Path

from epub_generator.config import SourceConfig
from epub_generator.ingestors.base import BaseIngestor

logger = logging.getLogger(__name__)


class PdfIngestor(BaseIngestor):
    """Extract text from local PDF files using pypdf. Scanned pages and embedded images are skipped."""

    def extract(self, source: SourceConfig, project_root: Path) -> str:
        import pypdf

        path = self.resolve_path(source, project_root)
        reader = pypdf.PdfReader(str(path))
        pages: list[str] = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if not text.strip():
                logger.warning("PDF page %d has no extractable text, skipping: %s", i, path)
                continue
            pages.append(text)
        return "\n\n".join(pages)
