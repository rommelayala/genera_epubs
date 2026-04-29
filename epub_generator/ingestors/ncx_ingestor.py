from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List

from epub_generator.config import SourceConfig
from epub_generator.ingestors.base import BaseIngestor, Metadata, Chapter


logger = logging.getLogger(__name__)


class NcxIngestor(BaseIngestor):
    """Parsear archivos NCX de EPUB extrayendo tabla de contenidos."""

    def extract(self, source: SourceConfig, project_root: Path) -> tuple[Metadata, List[Chapter]]:
        """
        Extraer metadatos y estructura de un archivo NCX.

        Metadatos extraídos de <head> > <meta>:
        - title: Título del documento EPUB
        - author: Autor del documento
        - lang/language: Idioma del contenido

        NavPoints (capítulos y TOC):
        - navPoint: Nodo recursivo que representa un capítulo
        - ncla:type="toc": Nodo de tabla de contenidos
        - ncla:type="ntoc": Nodo de tabla de contenidos no cubierta
        - fileRef: Referencia al archivo del capítulo
        - playOrder: Orden de presentación
        - navLabel: Etiqueta del nodo (nombre del capítulo)
        """
        path = self.resolve_path(source, project_root)

        tree = ET.parse(str(path))
        root = tree.getroot()

        # El namespace NCX es opcional
        ns = {'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}

        # Extraer metadatos
        metadata = self._extract_metadata(root, ns)

        # Extraer capítulos del navMap
        chapters = self._extract_chapters(root, ns)

        return metadata, chapters

    def _extract_metadata(self, root: ET.Element, ns: dict) -> Metadata:
        """Extraer metadatos de los elementos <meta>."""
        head = root.find('.//head')
        if head is None:
            head = root

        title = self._find_meta(head, 'Title', ns)
        language = self._find_meta(head, 'Language', ns)

        # Buscar autor en varios lugares
        author = None
        creator = self._find_meta(head, 'Creator', ns)
        if creator:
            author = creator

        return Metadata(
            title=title or "Sin título",
            author=author or None,
            language=language or None,
        )

    def _find_meta(self, element: ET.Element, name: str, ns: dict) -> str | None:
        """Buscar elemento <meta> con nombre específico."""
        # Intentar con namespace
        meta_path = f'.//{ns.get("ncx", "")}meta[@{ns.get("ncx", "")}name="{name}"]'
        meta = element.find(meta_path)

        if meta is not None and 'content' in meta.attrib:
            return meta.get('content', '').strip()

        # Intentar sin namespace
        meta = element.find(f'.//meta[@name="{name}"]')
        if meta is not None and 'content' in meta.attrib:
            return meta.get('content', '').strip()

        return None

    def _extract_chapters(self, root: ET.Element, ns: dict) -> List[Chapter]:
        """Extraer capítulos del navMap en orden de presentación."""
        chapters = []

        # Buscar navMap
        navmap_path = f'.//{ns.get("ncx", "")}navMap' if ns.get('ncx') else './/navMap'
        navmap = root.find(navmap_path)

        if navmap is None:
            return chapters

        # Buscar navPoints recursivamente
        navpoints = navmap.findall(f'.//{ns.get("ncx", "")}navPoint')
        if not navpoints:
            navpoints = navmap.findall('.//navPoint')

        for navpoint in navpoints:
            chapter = self._parse_navpoint(navpoint, ns)
            if chapter:
                chapters.append(chapter)

        return chapters

    def _parse_navpoint(self, navpoint: ET.Element, ns: dict) -> Chapter | None:
        """Parsear un navPoint individual."""
        # Obtener playOrder (puede ser decimal)
        play_order = navpoint.get(f'{{{ns.get("ncx", "")}playOrder}}', navpoint.get('playOrder', '0'))
        try:
            play_order = float(play_order)
        except (ValueError, TypeError):
            play_order = 0

        # Buscar fileRef
        file_ref = navpoint.get(f'{{{ns.get("ncx", "")}fileRef}}', navpoint.get('fileRef', ''))
        if not file_ref:
            return None

        # Obtener label (nombre del capítulo)
        label = self._find_text(navpoint, 'navLabel', ns)
        if not label:
            label = file_ref

        # Buscar tipo (toc, ntoc, etc.)
        content_type = navpoint.get(f'{{{ns.get("ncx", "")}content}}', navpoint.get('content', ''))

        # Crear capítulo
        chapter = Chapter(
            title=f"{label} (Capítulo {play_order})" if play_order > 1 else label,
            content=f"Archivo: {file_ref}\nTipo: {content_type}\nOrden: {play_order}"
        )

        return chapter

    def _find_text(self, element: ET.Element, tag: str, ns: dict) -> str | None:
        """Buscar texto en elemento hijo con tag específico."""
        # Intentar con namespace
        child_path = f'.//{ns.get("ncx", "")}{tag}'
        child = element.find(child_path)

        if child is not None and child.text:
            return child.text.strip()

        # Intentar sin namespace
        child = element.find(f'.//{tag}')
        if child is not None and child.text:
            return child.text.strip()

        return None
