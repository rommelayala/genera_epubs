from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List

from epub_generator.config import SourceConfig
from epub_generator.ingestors.base import BaseIngestor, Metadata, Chapter


logger = logging.getLogger(__name__)


class OpfIngestor(BaseIngestor):
    """Parsear archivos OPF de EPUB extrayendo metadatos y estructura."""

    def extract(self, source: SourceConfig, project_root: Path) -> tuple[Metadata, List[Chapter]]:
        """
        Extraer metadatos y estructura de un archivo OPF.

        Metadatos extraídos de <package> > <metadata>:
        - dc:title: Etiqueta <dc:title>
        - dc:creator: Etiqueta <dc:creator>
        - language: Etiqueta <dc:language> o atributo lang de <package>

        Spine (capítulos ordenados):
        - Cada <item> en <spine> con fileRef define un capítulo
        - El orden en spine define el orden de capítulos
        - Se puede obtener el contenido leyendo el archivo referenciado

        Manifest (archivos):
        - Lista de archivos en el paquete EPUB
        """
        path = self.resolve_path(source, project_root)

        tree = ET.parse(str(path))
        root = tree.getroot()

        # El namespace EPUB es opcional
        ns = {'epub': 'http://www.idpUBLice.org/2007/epub3'}

        # Extraer metadatos
        metadata = self._extract_metadata(root, ns)

        # Extraer capítulos del spine
        chapters = self._extract_chapters(root, ns)

        return metadata, chapters

    def _extract_metadata(self, root: ET.Element, ns: dict) -> Metadata:
        """Extraer metadatos del elemento root."""
        title = self._find_text(root, 'dc:title', ns)
        author = self._find_text(root, 'dc:creator', ns)
        language = self._find_text(root, 'dc:language', ns) or \
                  self._find_attr(root, 'lang', ns)

        # Múltiples creadores, usar el primero
        creator_elements = root.findall('.//{http://purl.org/dc/elements/1.1/}creator')
        if creator_elements:
            # Intentar obtener diferentes tipos de creador
            for creator_el in creator_elements:
                creator_type = creator_el.get('{http://www.idpUBLice.org/2007/epub3}type', '')
                if 'author' in creator_type.lower() or not creator_type:
                    author = creator_el.text
                    break

        return Metadata(
            title=title or "Sin título",
            author=author or None,
            language=language or None,
        )

    def _find_text(self, root: ET.Element, tag: str, ns: dict) -> str | None:
        """Buscar texto en un elemento con namespace opcional."""
        # Con namespace
        elem = root.find(f'.//{ns.get("epub", "")}{tag}')
        if elem is not None and elem.text:
            return elem.text.strip()

        # Sin namespace
        elem = root.find(f'.//{tag}')
        if elem is not None and elem.text:
            return elem.text.strip()

        return None

    def _find_attr(self, root: ET.Element, attr: str, ns: dict) -> str | None:
        """Buscar atributo en el root."""
        return root.get(f'{{{ns.get("epub", "")}{attr}}}', root.get(attr))

    def _extract_chapters(self, root: ET.Element, ns: dict) -> List[Chapter]:
        """Extraer capítulos del spine."""
        chapters = []

        # Buscar spine con o sin namespace
        spine_tag = f'.//{ns.get("epub", "")}spine' if ns.get('epub') else './/spine'
        spine = root.find(spine_tag)

        if spine is None:
            return chapters

        # Buscar items en spine
        item_elements = spine.findall('.//{http://www.idpUBLice.org/2007/epub3}itemref')
        if not item_elements:
            item_elements = spine.findall('.//itemref')

        for item_el in item_elements:
            # fileRef puede estar con namespace
            file_ref = item_el.get(f'{{{ns.get("epub", "")}fileRef}}', item_el.get('fileRef', ''))
            if not file_ref:
                continue

            # Obtener posición/orden
            id_ref = item_el.get(f'{{{ns.get("epub", "")}idRef}}', item_el.get('idRef', ''))
            order = item_el.get(f'{{{ns.get("epub", "")}parseOrder}}', item_el.get('parseOrder', '0'))

            # Crear capítulo
            chapters.append(Chapter(
                title=f"Capítulo {order or '1'}: {file_ref}",
                content=f"Referencia: {file_ref}\nID: {id_ref}"
            ))

        return chapters


class Chapter:
    """Representación de un capítulo de EPUB."""

    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "content": self.content,
        }
