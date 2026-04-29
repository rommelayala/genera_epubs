from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup, NavigableString, Comment

from epub_generator.config import SourceConfig
from epub_generator.ingestors.base import BaseIngestor, Metadata, Chapter


logger = logging.getLogger(__name__)


class HtmlIngestor(BaseIngestor):
    """Parsear archivos HTML extraendo metadatos y capítulos."""

    def extract(self, source: SourceConfig, project_root: Path) -> tuple[Metadata, List[Chapter]]:
        """
        Extraer metadatos y capítulos de un archivo HTML.

        Metadatos extraídos de etiquetas:
        - title: de <title> o meta[name="title"]
        - author: de <meta name="author">
        - lang/language: de <html lang="..."> o <meta name="language">

        Capítulos:
        - Se dividen por etiquetas <section>, <h1>, <h2>, <h3>, etc.
        - También se considera div con class/id significativo
        """
        path = self.resolve_path(source, project_root)

        html_content = path.read_text(encoding="utf-8")
        soup = BeautifulSoup(html_content, "html.parser")

        # Extraer metadatos
        title = self._extract_title(soup) or self._extract_title_from_filename(path)
        author = self._extract_author(soup)
        language = self._extract_language(soup)

        metadata = Metadata(
            title=title,
            author=author,
            language=language,
        )

        # Extraer capítulos
        sections = self._extract_sections(soup)
        chapters = self._extract_chapters(sections)

        return metadata, chapters

    def _extract_title(self, soup: BeautifulSoup) -> str | None:
        """Extraer el título de la etiqueta <title> o meta."""
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            return title_tag.string.strip()

        # Buscar en meta tags
        title_meta = soup.find("meta", attrs={"name": ["title", "og:title"]})
        if title_meta and "content" in title_meta.attrs:
            return title_meta["content"].strip()

        return None

    def _extract_author(self, soup: BeautifulSoup) -> str | None:
        """Extraer el autor del documento HTML."""
        # Meta tag de autor
        author_meta = soup.find("meta", attrs={"name": lambda x: x and ("author" in x.lower() or "creator" in x.lower())})
        if author_meta and "content" in author_meta.attrs:
            author = author_meta["content"].strip()
            if author:
                return author

        # Meta tag con propiedad author
        for meta in soup.find_all("meta"):
            if meta.get("property") == "author":
                return meta.get("content", "").strip()

        # Open Graph author
        og_author = soup.find("meta", attrs={"property": "og:site_author"})
        if og_author and "content" in og_author.attrs:
            return og_author["content"].strip()

        return None

    def _extract_language(self, soup: BeautifulSoup) -> str | None:
        """Extraer el idioma del documento HTML."""
        # Tag html con atributo lang
        html_tag = soup.find("html")
        if html_tag and "lang" in html_tag.attrs:
            return html_tag["lang"]

        # Meta tag de lenguaje
        lang_meta = soup.find("meta", attrs={"name": lambda x: x and ("language" in x.lower() or "content-language" in x.lower())})
        if lang_meta and "content" in lang_meta.attrs:
            return lang_meta["content"].strip()

        # Open Graph content-language
        content_lang = soup.find("meta", attrs={"property": "og:locale"})
        if content_lang and "content" in content_lang.attrs:
            return content_lang["content"].strip()

        return None

    def _extract_title_from_filename(self, path: Path) -> str | None:
        """Extraer título del nombre del archivo."""
        name = path.stem.lower()
        # Normalizar guiones y underscores
        name = name.replace("-", " ").replace("_", " ")
        # Capitalizar palabras
        words = re.split(r'[\s_-]+', name)
        return " ".join(word.capitalize() for word in words)

    def _extract_sections(self, soup: BeautifulSoup) -> List[str]:
        """Extraer el contenido de texto de secciones HTML."""
        sections = []

        # Eliminar comentarios
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.replace_with(None)

        # Extraer texto de elementos con estructura de contenido
        elements_to_check = [
            soup.find("body"),
            soup.find("section"),
            soup.find("article"),
            soup.find("div"),
            soup.find("main"),
        ]

        for element in elements_to_check:
            if element:
                # Extraer texto plano ignorando etiquetas de formato
                texts = element.find_all(string=lambda text: isinstance(text, NavigableString))
                content = " ".join(str(t).strip() for t in texts if t.strip())
                if content:
                    sections.append(content)

        # Si no encontramos secciones, usar todo el contenido del body
        if not sections and soup.find("body"):
            texts = soup.find("body").find_all(
                string=lambda text: isinstance(text, NavigableString)
            )
            content = " ".join(str(t).strip() for t in texts if t.strip())
            if content:
                sections.append(content)

        return sections

    def _extract_chapters(self, sections: List[str]) -> List[Chapter]:
        """
        Convertir secciones en capítulos.

        Estrategia:
        - Si hay pocas secciones, cada una es un capítulo
        - Si hay muchas secciones cortas, combinarlas en capítulos lógicos
        """
        if not sections:
            return []

        # Umbral para considerar una sección como capítulo
        long_section_threshold = 500  # caracteres

        chapters: List[Chapter] = []
        current_chapter_content: List[str] = []
        current_chapter_title: str | None = None
        section_count = 0

        for section in sections:
            section_count += 1

            # Si la sección es corta, podría ser parte de un capítulo más grande
            if len(section) < long_section_threshold and section_count < len(sections) - 1:
                current_chapter_content.append(section)
            else:
                # Guardar capítulo si existe uno en progreso
                if current_chapter_content:
                    title = current_chapter_title or self._generate_chapter_title(
                        " ".join(current_chapter_content)
                    )
                    chapters.append(Chapter(title=title, content="\n\n".join(current_chapter_content)))
                else:
                    # Esta sección es un capítulo completo
                    chapters.append(Chapter(
                        title=section_count,  # Usar número como título temporal
                        content=section
                    ))
                current_chapter_content = []
                current_chapter_title = None

        # Guardar último capítulo
        if current_chapter_content:
            title = current_chapter_title or self._generate_chapter_title(
                " ".join(current_chapter_content)
            )
            chapters.append(Chapter(title=title, content="\n\n".join(current_chapter_content)))

        return chapters

    def _generate_chapter_title(self, content: str) -> str:
        """Generar un título para un capítulo."""
        words = content.split()
        if len(words) > 3:
            return " ".join(words[:10]).title()
        return content[:50].title() or "Sin título"
