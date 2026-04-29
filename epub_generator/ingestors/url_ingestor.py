from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

from epub_generator.config import SourceConfig, BookConfig
from epub_generator.ingestors.base import BaseIngestor

log = logging.getLogger(__name__)


class UrlIngestor(BaseIngestor):
    def extract(self, source: SourceConfig, project_root: Path, book_config: Optional[BookConfig] = None) -> str:
        import requests
        from bs4 import BeautifulSoup
        from markdownify import MarkdownConverter

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(source.url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            if source.on_error == "skip":
                log.warning(f"No se pudo descargar {source.url}: {e}. Omitiendo.")
                return ""
            raise RuntimeError(f"Error al descargar {source.url}: {e}") from e

        soup = BeautifulSoup(response.text, "html.parser")

        # Normalize relative URLs to absolute so links and images work
        for tag in soup.find_all(href=True):
            tag["href"] = urljoin(source.url, tag["href"])
        for tag in soup.find_all(src=True):
            tag["src"] = urljoin(source.url, tag["src"])

        if source.selector:
            selected = soup.select_one(source.selector)
            if not selected:
                if source.on_error == "skip":
                    log.warning(
                        f"Selector '{source.selector}' no encontró nada en {source.url}. Omitiendo."
                    )
                    return ""
                raise ValueError(
                    f"Selector '{source.selector}' no encontró nada en {source.url}"
                )
            # Create a new soup with just the selected element to maintain structure
            soup = BeautifulSoup(str(selected), "html.parser")

        # Limpiar tags de ruido
        noise_tags = ["script", "style", "nav", "footer", "aside", "header", "form"]
        for tag in soup(noise_tags):
            tag.decompose()

        class ImageReplacingConverter(MarkdownConverter):
            def convert_img(self, el, text, *args, **kwargs):
                src = el.get("src", "")
                if not src:
                    return ""
                return f"[Ver imagen en la fuente original]({src})"

        # Convertir a Markdown
        converter = ImageReplacingConverter(heading_style="ATX")
        md_text = converter.convert_soup(soup)

        return md_text.strip()
