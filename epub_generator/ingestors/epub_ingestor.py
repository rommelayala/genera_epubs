from __future__ import annotations

import logging
from pathlib import Path

from epub_generator.config import SourceConfig
from epub_generator.ingestors.base import BaseIngestor

log = logging.getLogger(__name__)


class EpubIngestor(BaseIngestor):
    """Extraer texto Markdown de un archivo EPUB usando ebooklib."""

    def extract(self, source: SourceConfig, project_root: Path) -> str:
        import ebooklib
        from ebooklib import epub
        from markdownify import MarkdownConverter

        class _ImageReplacingConverter(MarkdownConverter):  # type: ignore[misc]
            def convert_img(self, el, text, *args, **kwargs):  # type: ignore[override]
                src = el.get("src", "") or el.get("xlink:href", "")
                name = Path(src).name if src else "imagen"
                return f"[Imagen omitida: {name}]"

        path = self.resolve_path(source, project_root)
        book = epub.read_epub(str(path), options={"ignore_ncx": True})
        converter = _ImageReplacingConverter(heading_style="ATX")

        parts: list[str] = []
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            try:
                html = item.get_content().decode("utf-8", errors="replace")
                md = converter.convert(html).strip()
                if md:
                    parts.append(md)
            except Exception as e:
                log.warning("No se pudo convertir capítulo %s: %s. Omitiendo.", item.get_name(), e)

        return "\n\n".join(parts)
