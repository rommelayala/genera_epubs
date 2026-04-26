from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from epub_generator.config import BookConfig, SourceConfig
from epub_generator.ingestors import INGESTORS

# Types that require 'url' field instead of 'path'
_URL_TYPES = {"url", "youtube"}


def _validate_sources(sources: List[SourceConfig], project_root: Path) -> None:
    """Validate all sources before ingestion starts. Raises ValueError on first failure."""
    for i, source in enumerate(sources):
        if source.type not in INGESTORS:
            raise ValueError(
                f"Source[{i}]: tipo '{source.type}' no reconocido. "
                f"Tipos válidos: {sorted(INGESTORS.keys())}"
            )
        if source.type in _URL_TYPES:
            if not source.url:
                raise ValueError(
                    f"Source[{i}]: tipo '{source.type}' requiere campo 'url'"
                )
        else:
            if not source.path:
                raise ValueError(
                    f"Source[{i}]: tipo '{source.type}' requiere campo 'path'"
                )
            p = Path(source.path).expanduser()
            if not p.is_absolute():
                p = project_root / p
            p = p.resolve()
            if not p.exists():
                raise ValueError(
                    f"Source[{i}]: path '{source.path}' no encontrado en '{p}'"
                )


def compile_book(
    config: BookConfig, basename: str, project_root: Optional[Path] = None
) -> Path:
    """Validate and compile multiple sources into a Master Markdown file."""
    if not config.sources:
        raise ValueError("No hay sources definidos")
    if project_root is None:
        project_root = Path.cwd()
    _validate_sources(config.sources, project_root)
    raise NotImplementedError("Compilación pendiente — ver US-006")
