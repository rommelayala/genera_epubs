from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from epub_generator.config import SourceConfig


class BaseIngestor(ABC):
    @abstractmethod
    def extract(self, source: SourceConfig, project_root: Path) -> str:
        """Extract content from source and return as Markdown string."""
        ...

    def resolve_path(self, source: SourceConfig, project_root: Path) -> Path:
        """Resolve source.path to an absolute Path, raising FileNotFoundError if missing."""
        p = Path(source.path).expanduser()
        if not p.is_absolute():
            p = project_root / p
        p = p.resolve()
        if not p.exists():
            raise FileNotFoundError(f"Source path not found: {p}")
        return p
