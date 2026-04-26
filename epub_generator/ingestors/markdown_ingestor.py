from __future__ import annotations

from pathlib import Path

from epub_generator.config import SourceConfig
from epub_generator.ingestors.base import BaseIngestor


class MarkdownIngestor(BaseIngestor):
    def extract(self, source: SourceConfig, project_root: Path) -> str:
        path = self.resolve_path(source, project_root)
        return path.read_text(encoding="utf-8")
