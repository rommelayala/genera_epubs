from __future__ import annotations

import base64
import json
import logging
import time
from pathlib import Path
from typing import Optional

from epub_generator.config import SourceConfig, BookConfig
from epub_generator.ingestors.base import BaseIngestor

log = logging.getLogger(__name__)


class OllamaPdfIngestor(BaseIngestor):
    """
    Extract perfectly formatted Markdown from a PDF by taking pictures of each page
    and sending them to a local Vision Language Model via Ollama.
    """

    def extract(
        self,
        source: SourceConfig,
        project_root: Path,
        book_config: Optional[BookConfig] = None,
    ) -> str:
        import fitz  # PyMuPDF
        import requests

        path = self.resolve_path(source, project_root)
        log.info(f"OllamaPdfIngestor leyendo: {path.name}")

        # Resolve which model to use
        # Precedencia: 1) CLI global (book_config.ai_model) -> 2) Source yaml -> 3) Default
        model_name = "qwen2.5"  # Fallback razonable
        if source.model:
            model_name = source.model
        if book_config and getattr(book_config, "ai_model", None):
            model_name = book_config.ai_model

        log.info(f"📸 Usando el modelo de IA local: {model_name}")

        ollama_url = "http://localhost:11434/api/generate"
        prompt = (
            "Eres un experto transcribiendo documentos. Convierte exactamente el contenido de esta "
            "imagen a formato Markdown. Preserva la estructura de las tablas usando sintaxis de "
            "tablas Markdown. Respeta estrictamente los bloques de código y su indentación. Incluye "
            "las cabeceras tal cual aparecen. Si ves imágenes que no son texto, ignorarlas. "
            "IMPORTANTE: No agregues saludos, explicaciones ni notas finales, devuelve ÚNICAMENTE "
            "el código Markdown del contenido."
        )

        extracted_chunks = []

        try:
            doc = fitz.open(path)
        except Exception as e:
            msg = f"Error abriendo PDF con PyMuPDF {path}: {e}"
            if source.on_error == "skip":
                log.warning(msg)
                return ""
            raise RuntimeError(msg)

        total_pages = len(doc)
        max_retries = 3

        for i, page in enumerate(doc, 1):
            log.info(f"  -> Procesando página {i}/{total_pages} con Ollama...")

            page_success = False
            last_error = None

            for attempt in range(1, max_retries + 1):
                try:
                    # 1. Render page to image
                    # dpi=150 es un buen balance entre calidad y peso para el modelo
                    pix = page.get_pixmap(dpi=150)
                    img_bytes = pix.tobytes("png")
                    b64_image = base64.b64encode(img_bytes).decode("utf-8")

                    # 2. Prepare request
                    payload = {
                        "model": model_name,
                        "prompt": prompt,
                        "images": [b64_image],
                        "stream": False
                    }

                    # 3. Request to Ollama con reintentos
                    response = requests.post(ollama_url, json=payload, timeout=300)
                    response.raise_for_status()

                    data = response.json()
                    page_md = data.get("response", "").strip()

                    # A veces los modelos devuelven el markdown envuelto en ```markdown
                    if page_md.startswith("```markdown"):
                        page_md = page_md[11:]
                    if page_md.endswith("```"):
                        page_md = page_md[:-3]

                    extracted_chunks.append(page_md.strip())
                    page_success = True
                    break

                except requests.exceptions.Timeout as req_e:
                    last_error = req_e
                    if attempt < max_retries:
                        wait_time = 2 ** (attempt - 1)  # 1s, 2s, 4s
                        log.warning(f"⏱️  Timeout en página {i} (intento {attempt}/{max_retries}), esperando {wait_time}s...")
                        time.sleep(wait_time)
                    continue

                except requests.exceptions.RequestException as req_e:
                    last_error = req_e
                    if attempt < max_retries:
                        wait_time = 2 ** (attempt - 1)
                        log.warning(f"⚠️  Error Ollama en página {i} (intento {attempt}/{max_retries}), esperando {wait_time}s...")
                        time.sleep(wait_time)
                    continue

                except Exception as e:
                    last_error = e
                    if attempt < max_retries:
                        wait_time = 2 ** (attempt - 1)
                        log.warning(f"⚠️  Error inesperado en página {i} (intento {attempt}/{max_retries}), esperando {wait_time}s...")
                        time.sleep(wait_time)
                    continue

            if not page_success:
                msg = f"Error procesando página {i} después de {max_retries} intentos: {last_error}"
                if source.on_error == "skip":
                    log.warning(msg)
                else:
                    raise RuntimeError(msg)

        doc.close()
        return "\n\n".join(extracted_chunks)
