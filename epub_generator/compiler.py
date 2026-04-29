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
    import logging
    from urllib.parse import urlparse
    
    log = logging.getLogger(__name__)
    
    if not config.sources:
        raise ValueError("No hay sources definidos")
    if project_root is None:
        project_root = Path.cwd()
        
    _validate_sources(config.sources, project_root)
    
    compiled_lines = []
    total = len(config.sources)
    
    for i, source in enumerate(config.sources, 1):
        display_path = source.url if source.type in _URL_TYPES else source.path
        log.info(f"[{basename}] ({i}/{total}) ingiriendo {source.type}: {display_path}")
        
        try:
            ingestor_cls = INGESTORS[source.type]
            ingestor = ingestor_cls()
            content = ingestor.extract(source, project_root, book_config=config)
            
            # Header injection
            title = source.title
            if not title:
                if source.type in _URL_TYPES:
                    parsed = urlparse(source.url)
                    title = parsed.netloc
                else:
                    title = Path(source.path).name
            
            header_prefix = "#" * source.title_level
            expected_header = f"{header_prefix} "
            
            # Inject header if content does not already start with a header of that level
            if not content.lstrip().startswith(expected_header):
                compiled_lines.append(f"{header_prefix} {title}\n")
            
            compiled_lines.append(content)
            
        except Exception as e:
            if source.on_error == "skip":
                log.warning(f"[{basename}] Error ingiriendo {display_path}: {e}. Omitiendo.")
                continue
            else:
                log.error(f"[{basename}] Error crítico ingiriendo {display_path}: {e}")
                raise
    
    # Write to _compiled.md
    drafts_dir = project_root / "libros_draft"
    drafts_dir.mkdir(parents=True, exist_ok=True)
    out_path = drafts_dir / f"{basename}_compiled.md"
    
    # Concat with double newlines
    final_content = "\n\n".join(line.strip() for line in compiled_lines if line.strip())
    out_path.write_text(final_content + "\n", encoding="utf-8")
    
    return out_path
