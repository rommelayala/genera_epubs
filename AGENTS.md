# AGENTS.md — Reglas de Generación de Ebooks y Audiolibros

> **Contexto Principal (AI):** Antes de seguir estas instrucciones técnicas, por favor lee `docs/context.md` para asimilar la identidad, prioridades y el flujo de trabajo personal de Rommel.

Este archivo define las reglas que TODO agente (Ralph, Claude, o cualquier LLM) debe seguir al trabajar en este proyecto.

---

## Reglas de Markdown para EPUB

### Cabeceras (CRÍTICO — Pandoc las usa para el TOC)

- `#` = Capítulos o partes principales (generan entradas de nivel 1 en el TOC)
- `##` = Subtemas dentro de un capítulo (entradas de nivel 2 en el TOC)
- `###` = Secciones dentro de un subtema (NO aparecen en el TOC, solo en contenido)
- NUNCA saltar niveles de jerarquía (ej: `#` seguido de `####`)
- NUNCA usar `#` para el título del libro (eso va en el YAML sidecar `title:`)

### Formato Markdown

- Solo Markdown estándar nativo — cero tags HTML personalizados
- Usar tablas de Markdown para datos comparativos (Pandoc las convierte bien)
- Bloques de código con triple backtick + lenguaje (``` ```python ```)
- Imágenes con `![alt](ruta)` — las rutas deben ser relativas al markdown
- Horizontal rules `---` solo como separador visual, no como frontmatter (eso va en el YAML)

### Estilo de Escritura (AIQ/Rommel Ayala)

- Tono: cercano, riguroso, de tú a tú (nivel CTO/Tech Lead)
- Sin lenguaje corporativo ni muletillas de IA ("En conclusión,", "En resumen,", "Es importante destacar")
- Filosofía "No-BS": menos palabras, más impacto
- Framework 5W1H y regla 80-20 sobre largas explicaciones
- Claridad visual: listas viñetadas, negrillas para énfasis clave, tablas para condensar
- Mente visual: preferir diagramas ASCII, tablas comparativas, listas sobre párrafos largos

---

## Reglas de YAML Sidecar

### Ubicación y Nombre

- Archivo: `libros_draft/{basename}.yaml` (mismo nombre que el `.md`, extensión `.yaml`)
- Si no existe, se usan defaults de `BookConfig` — pero SIEMPRE debe existir

### Campos Obligatorios

```yaml
title: "Título Completo del Libro"     # OBLIGATORIO — se usa en metadata EPUB y M4B
author: "Rommel Ayala"                  # OBLIGATORIO
description: "Descripción breve"        # OBLIGATORIO — Apple Books y Google Play lo muestran
language: "es-ES"                       # OBLIGATORIO — determina voz TTS y metadata
date: "2026"                            # OBLIGATORIO — año de publicación
```

### Campos de Portada (Opcionales pero Recomendados)

```yaml
cover:
  title: "Título Corto"                 # Texto principal de la portada (puede diferir del title)
  subtitle: "Subtítulo"                 # Línea secundaria
  bg_color: "#151515"                   # Fondo oscuro por defecto
  text_color: "#EAEAEA"                 # Texto claro
  accent_color: "#4A4A4A"              # Línea decorativa y footer
  image: "mi-portada.jpg"              # Si existe en portadas_draft/, se usa en vez de generar
```

### Campos de Audio (Opcionales)

```yaml
audio:
  voice: ""                             # Vacío = auto por idioma
  rate: "-5%"                           # Ligeramente lento para comprensión
  volume: "+0%"                         # Neutro
  pitch: "+0Hz"                         # Neutro
  bitrate: "96k"                        # Estándar para voz hablada
  chapter_pause: 1.5                    # Segundos de silencio entre capítulos
  concurrency: 5                        # Capítulos en paralelo
  intro: true                           # "Este es el audiolibro..."
  outro: true                           # "Fin del audiolibro..."

### Fuentes Multi-Fuente (Compilación)

```yaml
sources:
  - type: markdown            # Tipos: markdown, pdf, ollama_pdf, url
    path: "archivo.md"
  - type: ollama_pdf          # Ingestión visual con IA (Ollama)
    path: "mi-nota.pdf"
    model: "qwen3.5"          # Modelo IA local (opcional)
    title_level: 1            # H1, H2, etc. en el master
```
```

---

## Reglas de Portadas

### Convención de Nombres

- Portadas en `portadas_draft/{basename}.jpg` (o `.jpeg`, `.png`)
- El nombre DEBE coincidir exactamente con el basename del markdown
- Ejemplo: `agentes-ia-libro.md` → `agentes-ia-libro.jpg`

### Resolución (orden de prioridad)

1. Argumento CLI (segundo parámetro)
2. Campo `cover.image` en YAML sidecar
3. Auto-discovery en `portadas_draft/{basename}.{jpg,jpeg,png}`
4. Generada automáticamente con Pillow desde config de `cover:` del YAML

### Formato

- Resolución: 600×800px (estándar ebook)
- Formato: JPG (quality=95) o PNG
- Diseño: minimalista, fondo oscuro (#151515), texto claro (#EAEAEA)
- Tipografía: Inter Regular/Bold

---

## Reglas de Generación EPUB

### Pandoc

- Siempre generar EPUB3 (`--to=epub3`)
- Siempre incluir TOC (`--toc --toc-depth=2`)
- Siempre usar CSS personalizado (`--css=epub_generator/styles/epub.css`)
- Siempre usar syntax highlighting espresso (`--syntax-highlighting=espresso`)
- Siempre incluir portada (`--epub-cover-image=`)
- Metadata completa: title, author, language, description, date

### Post-Procesamiento

- Numeración de páginas: se inyecta automáticamente (`page_numbering.py`)
- Formato: `{pagina_actual}/{total_paginas}` (ej: `2/40`)
- Posición: centrado al pie de cada página de contenido
- Excluye: cover, TOC, nav, title_page

### Nombres de Archivos

- EPUBs en `epubs_generados/{basename}.epub` (sin timestamp, git controla versiones)
- Basename = nombre del markdown sin extensión
- Todo en kebab-case: `agentes-ia-libro.epub`, NO `Agentes IA Libro.epub`

---

## Reglas de Generación de Audio (M4B)

### Requisitos

- ffmpeg y ffprobe deben estar en PATH (se valida al inicio)
- Solo markdown como entrada (no PDF)

### Limpieza de Texto para TTS

- Eliminar frontmatter YAML (`---\n...\n---`) del inicio
- Code blocks → "Para ver este ejemplo de código, consulta el libro en formato epub."
- Tablas → "Consulta la tabla completa en el libro en formato epub."
- Eliminar: emojis, URLs sueltas, HTML tags, caracteres decorativos unicode
- Preservar: headings (como texto), listas (como texto), caracteres hispanicos

### Ensamblado M4B

- Codec: AAC (`-c:a aac`)
- Bitrate: configurable, default 96k
- Silencio entre capítulos: configurable, default 1.5s
- Chapter markers: ffmpeg metadata con TIMEBASE=1/1000, timestamps en ms
- Portada: embebida como `attached_pic` (mjpeg para JPG, png para PNG)
- Intro/outro: narrados automáticamente si `audio.intro`/`audio.outro` es true

### Caché

- Manifiesto: `{chapters_dir}/cache_manifest.json`
- Hash: SHA-256 del texto post-limpieza (no del markdown original)
- Si hash coincide y MP3 existe → skip
- Flag `--no-cache` para forzar re-narración

### Nombres de Archivos

- M4B en `audios_generados/{basename}.m4b`
- Capítulos en `audios_generados/{basename}_chapters/`
- Formato: `{nn}_{slug}.mp3` (ej: `01_introduccion.mp3`)
- Intro: `00_intro.mp3`, Outro: `99_outro.mp3`

---

## Reglas de Código Python

### Convenciones

- `from __future__ import annotations` en todos los archivos
- Type hints en firmas de funciones públicas
- Logging con `logging.getLogger(__name__)`
- Paths con `pathlib.Path` (nunca `os.path`)
- Subprocesses con listas (nunca `shell=True`)
- Imports al inicio del archivo (nunca imports inline)

### Estructura de Paquete

```
epub_generator/
├── config.py               # Dataclasses de configuración
├── cover.py                # Generación de portadas
├── generator.py            # Dispatcher por (extensión, formato)
├── styles/
│   └── epub.css            # CSS para EPUB
├── converters/
│   ├── markdown.py         # MD → EPUB (pandoc)
│   ├── pdf.py              # PDF → EPUB (ebook-convert)
│   └── audio.py            # MD → M4B (edge-tts + ffmpeg)
├── ingestors/              # [NUEVO] Extracción de contenido
│   ├── base.py             # Clase base abstracta
│   ├── markdown_ingestor.py
│   ├── ollama_pdf_ingestor.py # VLM Vision OCR
│   └── url_ingestor.py     # Scraper de URLs
├── preprocessors/
    └── markdown_cleaner.py # Limpieza de texto para TTS
```

### Agregar Nuevo Converter

1. Crear `converters/{nombre}.py` con función `convert_{nombre}(input, config, cover, output)`
2. Registrar en `CONVERTERS` dict en `generator.py`
3. Agregar check de dependencias en `generate_epub.sh`

### Agregar Nuevo Campo de Config

1. Agregar field a dataclass en `config.py` (BookConfig, CoverConfig, o AudioConfig)
2. Actualizar `_build_{cover|audio}()` en `config.py`
3. Leer en el converter correspondiente
4. Documentar en README.MD
