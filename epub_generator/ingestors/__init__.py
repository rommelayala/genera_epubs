from __future__ import annotations

from typing import Dict, Type

from epub_generator.ingestors.base import BaseIngestor

INGESTORS: Dict[str, Type[BaseIngestor]] = {}
