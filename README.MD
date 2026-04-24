# Generador de EPUBs y Audiolibros

Convierte archivos Markdown (`.md`) y PDF (`.pdf`) a **EPUB** con portadas automáticas,
metadata configurable por libro vía YAML, procesamiento en paralelo y generación de **audiolibros M4B**
con chapter markers navegables, portada embebida e intro/outro narrados.

**Versión:** 2.0 | **Última actualización:** 2026-04-24

---

## Índice de Documentación

- **[README.MD](README.MD)** (este archivo) — Uso rápido y guía de inicio
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — Diseño del sistema, decisiones técnicas, flujos de datos
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — Estructura del código, cómo modificar, cambios comunes
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** — Problemas comunes, FAQs, debugging

---

## Precondiciones

| Herramienta | Para qué | Instalar |
|---|---|---|
| **Python 3** | motor principal | preinstalado en macOS/Linux |
| **Pandoc** | convertir `.md` → EPUB | `brew install pandoc` / `sudo apt install pandoc` |
| **Calibre** (`ebook-convert`) | convertir `.pdf` → EPUB (solo si hay PDFs) | `brew install --cask calibre` / `sudo apt install calibre` |

El launcher crea el venv y descarga las fuentes Inter automáticamente en el primer arranque.

---

## Estructura del proyecto

```
genera_epubs/
├── generate_epub.sh          ← entrada: verifica deps, crea venv, lanza Python
├── generate_epub.py          ← orquestador CLI + paralelismo
├── requirements.txt          ← Pillow, PyYAML
├── epub_generator/
│   ├── config.py             ← lee {basename}.yaml → BookConfig
│   ├── cover.py              ← genera portada con Pillow
│   ├── generator.py          ← dispatcher por extensión
│   └── converters/
│       ├── markdown.py       ← pandoc wrapper
│       └── pdf.py            ← ebook-convert wrapper
├── fonts/                    ← Inter Regular + Bold (auto-descargadas)
├── libros_draft/             ← fuentes: .md y/o .pdf + .yaml por libro
├── portadas_draft/           ← portadas generadas o manuales
└── epubs_generados/          ← EPUBs de salida (sin timestamp, git controla versiones)
```

---

## Uso

```bash
# Todos los libros en libros_draft/ (paralelo)
./generate_epub.sh

# Libro específico (con o sin extensión, con o sin path)
./generate_epub.sh agentes-ia-libro
./generate_epub.sh agentes-ia-libro.md
./generate_epub.sh libros_draft/agentes-ia-libro.md

# Libro específico con portada manual
./generate_epub.sh agentes-ia-libro.md mi_portada.jpg
```

---

## Configuración por libro (YAML sidecar)

Cada libro puede tener un archivo `libros_draft/{basename}.yaml` con su metadata y
configuración de portada. Si no existe, se usan los defaults globales.

```yaml
# libros_draft/mi-libro.yaml
title: "Título del Libro"
author: "Rommel Ayala - QA Lead"
description: "Descripción opcional"
language: "es-ES"
date: "2026"
cover:
  title: "Título del Libro"   # texto principal de la portada
  subtitle: "Subtítulo"       # línea secundaria (opcional)
  bg_color: "#151515"
  text_color: "#EAEAEA"
  accent_color: "#4A4A4A"
  title_size: 42
  subtitle_size: 24
  footer: "© Rommel Ayala - All rights reserved"
  image: "portada-manual.jpg" # opcional: portada pre-existente en portadas_draft/
```

**Campos mínimos recomendados:**

```yaml
title: "Título del Libro"
cover:
  title: "Título del Libro"
  subtitle: "Subtítulo opcional"
```

---

## Audiolibros

El sistema genera audiolibros M4B con narración TTS (edge-tts), chapter markers navegables,
portada embebida, intro/outro automático y caché por capítulo.

### Precondiciones adicionales para audio

| Herramienta | Para qué | Instalar |
|---|---|---|
| **ffmpeg** + **ffprobe** | ensamblar M4B, chapter markers, portada | `brew install ffmpeg` / `sudo apt install ffmpeg` |

### Uso

```bash
# Todos los libros como audiolibro
./generate_epub.sh --format audio

# Libro específico
./generate_epub.sh --format audio agentes-ia-libro

# Forzar re-narración (ignorar caché)
./generate_epub.sh --format audio --no-cache agentes-ia-libro
```

### Configuración de audio (YAML sidecar)

```yaml
# libros_draft/mi-libro.yaml
audio:
  voice: ""              # vacío = auto por idioma (es-ES-AlvaroNeural)
  rate: "-5%"            # velocidad: ligeramente lento para mejor comprensión
  volume: "+0%"          # volumen: neutro
  pitch: "+0Hz"          # tono: neutro
  bitrate: "96k"         # calidad AAC: 96k es estándar para voz hablada
  chapter_pause: 1.5     # segundos de silencio entre capítulos
  concurrency: 5         # capítulos narrados en paralelo (semáforo)
  intro: true            # narrar intro automático ("Este es el audiolibro...")
  outro: true            # narrar outro automático ("Fin del audiolibro...")
```

**Voces disponibles por idioma:**

| Idioma | Voz default |
|---|---|
| es-ES | es-ES-AlvaroNeural |
| es-MX | es-MX-JorgeNeural |
| en-US | en-US-GuyNeural |
| en-GB | en-GB-RyanNeural |

### Caché

Los capítulos narrados se cachean por hash SHA-256 del texto limpio. Al re-generar un
audiolibro, solo se re-narran los capítulos que cambiaron. El manifiesto se guarda en
`audios_generados/{libro}_chapters/cache_manifest.json`. Usa `--no-cache` para forzar
re-narración completa.

### Salida

```
audios_generados/
├── mi-libro.m4b                    ← audiolibro con chapters + portada
└── mi-libro_chapters/
    ├── 00_intro.mp3                ← intro narrado
    ├── 01_capitulo-uno.mp3
    ├── 02_capitulo-dos.mp3
    ├── 99_outro.mp3                ← outro narrado
    └── cache_manifest.json         ← caché de hashes
```

---

## Precedencia de portadas

El sistema resuelve la portada en este orden (gana el primero que exista):

1. Segundo argumento CLI → `./generate_epub.sh libro.md mi.jpg`
2. Campo `cover.image` en el YAML → `portadas_draft/mi.jpg`
3. Auto-discovery → `portadas_draft/{basename}.jpg` / `.jpeg` / `.png`
4. Generada con Pillow desde los valores `cover:` del YAML

---

## Output de consola

```
🔧 Instalando dependencias Python...
🚀 Ejecutando generate_epub.py...
📚 Descubiertos 3 libros: 2 markdown, 1 PDF.
🚀 Procesando en paralelo...

[claude-uso-maestro]    🖼️  Portada: claude-uso-maestro.jpg
[claude-uso-maestro]    🔄 Convirtiendo (.md)...
[claude-uso-maestro]    ✅ epubs_generados/claude-uso-maestro.epub
[agentes-ia-libro]      🖼️  Portada: agentes-ia-libro.jpg
[agentes-ia-libro]      🔄 Convirtiendo (.md)...
[agentes-ia-libro]      ✅ epubs_generados/agentes-ia-libro.epub
[manual-legado]         🖼️  Portada: manual-legado.jpg
[manual-legado]         🔄 Convirtiendo (.pdf)...
[manual-legado]         ✅ epubs_generados/manual-legado.epub

✨ 3/3 libros generados
```

---

## Notas

- Los EPUBs se generan **sin timestamp**. Git controla las versiones.
- Los PDFs deben tener capa de texto. PDFs escaneados (solo imágenes) no están soportados.
- Si dos archivos comparten el mismo nombre base con distinta extensión
  (`libro.md` y `libro.pdf`), el último en terminar pisa al otro en disco. Evitar.
