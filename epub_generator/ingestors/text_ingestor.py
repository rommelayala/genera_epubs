from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import List

from epub_generator.config import SourceConfig
from epub_generator.ingestors.base import BaseIngestor, Metadata, Chapter


logger = logging.getLogger(__name__)


class TextIngestor(BaseIngestor):
    """Parsear archivos de texto plano (.txt) extrayendo capítulos."""

    def extract(self, source: SourceConfig, project_root: Path) -> tuple[Metadata, List[Chapter]]:
        """
        Extraer metadatos y capítulos de un archivo de texto plano.

        Metadatos:
        - title: Primer bloque significativo del archivo (antes de líneas vacías)
        - author: Buscado en las primeras líneas del archivo
        - language: Inferido del contenido o extraído de comentarios

        Capítulos:
        - Se dividen por líneas vacías (separadores lógicos)
        - Cada bloque separado por líneas vacías es un capítulo
        """
        path = self.resolve_path(source, project_root)

        content = path.read_text(encoding="utf-8")

        # Dividir por líneas vacías para obtener bloques
        blocks = self._split_into_blocks(content)

        if not blocks:
            # Contenido sin separadores, todo es un solo capítulo
            return self._create_single_chapter(
                Metadata(
                    title=self._extract_title(content),
                    author=self._extract_author(content),
                    language=self._extract_language(content),
                ),
                content
            )

        # Procesar cada bloque
        chapters = []
        for block in blocks:
            # Cada bloque puede ser un capítulo
            # Verificar si el bloque parece tener un título integrado
            title = self._extract_block_title(block)
            content = block.strip()

            if content:
                chapters.append(Chapter(title=title, content=content))

        # Crear metadatos globales (del primer bloque)
        title = self._extract_title(content)
        author = self._extract_author(content)
        language = self._extract_language(content)

        metadata = Metadata(
            title=title or "Libro de Texto",
            author=author,
            language=language or "es",
        )

        return metadata, chapters

    def _split_into_blocks(self, content: str) -> List[str]:
        """Dividir contenido por líneas vacías para crear bloques de capítulos."""
        # Dividir por dos o más líneas vacías
        blocks = re.split(r'\n\s*\n\s*\n', content)
        # También dividir por una línea vacía si hay saltos de página marcados
        blocks = re.split(r'\n\s*$', content, flags=re.MULTILINE)

        # Filtrar bloques vacíos
        blocks = [block.strip() for block in blocks if block.strip()]

        return blocks

    def _extract_title(self, content: str) -> str | None:
        """Extraer título del archivo de texto (primer bloque significativo)."""
        # Buscar título en la línea inicial
        lines = content.split('\n')
        first_line = lines[0].strip() if lines else ""

        # Patrones comunes de títulos en archivos de texto
        title_patterns = [
            r'^(?:Título|TITULO|TITLE|Titulo):?\s*(.+)$',
            r'^(?:Nombre del libro|LIBRO|LIBRO):?\s*(.+)$',
            r'^(?:Titulo del):?\s*(.+)$',
        ]

        for pattern in title_patterns:
            match = re.match(pattern, first_line, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        # Si no hay patrón, usar la primera línea como título (si es corta)
        if len(first_line) < 100:
            return first_line.capitalize()

        return None

    def _extract_author(self, content: str) -> str | None:
        """Extraer autor de metadatos o comentarios en el archivo de texto."""
        lines = content.split('\n')

        # Buscar en las primeras líneas por patrones comunes
        author_patterns = [
            (r'^(?:Autor|AUTOR|AUTHOR|Autor por|Autora):?\s*(.+)$', 1),
            (r'^(?:Por|POR|DE|DEPOR|CREADO POR):?\s*(.+)$', 1),
            (r'^(?:Créditos de autor|CRÉDITOS|CREATOR):?\s*(.+)$', 1),
        ]

        for pattern, group in author_patterns:
            for line in lines[:5]:  # Buscar solo en primeras 5 líneas
                match = re.match(pattern, line.strip(), re.IGNORECASE)
                if match:
                    author = match.group(group).strip()
                    if author and len(author) > 2:
                        return author

        return None

    def _extract_language(self, content: str) -> str | None:
        """Extraer idioma del contenido o buscarlo en metadatos."""
        # Buscar declaración de idioma
        lang_patterns = [
            r'(?:\b|_)lang[:=]\s*["\']?(\w{2})["\']?',
            r'(?:ISO 639-1|ISO-639-1|Babel|Idioma):?\s*["\']?(\w{2})["\']?',
            r'(?:language|Lenguaje):?\s*["\']?([a-z]{2})["\']?',
        ]

        for pattern in lang_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                lang = match.group(1).upper()
                if lang in ['ES', 'EN', 'PT', 'FR', 'DE', 'IT', 'JA', 'KO', 'ZH', 'RU']:
                    return lang

        # Inferir idioma del contenido (sencillo)
        es_score = sum(1 for line in content.split('\n') if line.strip() and 'á' in line.lower() or 'é' in line.lower())
        if es_score > 10:
            return 'es'

        return None

    def _extract_block_title(self, block: str) -> str:
        """Extraer o generar título para un bloque de texto."""
        lines = block.split('\n')

        # Buscar línea que parezca un título (corta, sin puntuación inicial)
        for line in lines:
            line = line.strip()
            if len(line) < 80 and not line[0].isnumeric() and not line[0] in '.,;:!?:"\'-()[]{}':
                # Verificar si es una frase completa (termina en . ? !)
                if re.search(r'[\.\?\!]\s*$', line) or len(line.split()) < 20:
                    return line

        # Si no hay título, generar uno basado en el contenido
        return self._generate_block_title(block)

    def _generate_block_title(self, content: str) -> str:
        """Generar título para un bloque sin título explícito."""
        words = content.split()
        if words:
            # Usar primeras palabras significativas
            return " ".join(words[:10]).title()
        return "Capítulo"
