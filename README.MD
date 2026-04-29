# Generador de EPUBs y Audiolibros

Convierte archivos Markdown (`.md`) y PDF (`.pdf`) a **EPUB** con portadas automáticas,
metadata configurable por libro vía YAML, procesamiento en paralelo y generación de **audiolibros M4B**
con chapter markers navegables, portada embebida e intro/outro narrados.

**Versión:** 2.1 | **Última actualización:** 2026-04-29

---

## Índice de Documentación

- **[README.MD](README.MD)** (este archivo) — Uso rápido y guía de inicio
- **[docs/context.md](docs/context.md)** — Contexto AIQ e identidad del autor (Crucial para Inteligencias Artificiales)
- **[docs/architecture.md](docs/architecture.md)** — Diseño del sistema, soporte Multi-IA y arquitectura de directorios
- **[docs/page-numbering.md](docs/page-numbering.md)** — Sistema de inyección automática de numeración en EPUBs
- **[docs/troubleshooting.md](docs/troubleshooting.md)** — Diagnóstico de errores, FAQs, debugging
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — Reglas para contribuidores, pull requests y desarrollo
- **[AGENTS.md](AGENTS.md)** — Reglas OBLIGATORIAS para IAs sobre generación y estilo

---

## Precondiciones

| Herramienta                   | Para qué                                   | Instalar                                                   |
| ----------------------------- | ------------------------------------------ | ---------------------------------------------------------- |
| **Python 3**                  | motor principal                            | preinstalado en macOS/Linux                                |
| **Pandoc**                    | convertir `.md` → EPUB                     | `brew install pandoc` / `sudo apt install pandoc`          |
| **Calibre** (`ebook-convert`) | convertir `.pdf` → EPUB (solo si hay PDFs) | `brew install --cask calibre` / `sudo apt install calibre` |
| **Ollama**                    | OCR de PDFs                                | `brew install --cask ollama`                               |
| **Qwen2.5** (o qwen2.5-vl)    | OCR de PDFs con visión                    | `ollama pull qwen2.5-vl`                                   |
| **Llama3.2-Vision**           | OCR de PDFs                                | `ollama pull llama3.2-vision`                              |

El launcher crea el venv y descarga las fuentes Inter automáticamente en el primer arranque.

**Verificar que Ollama está corriendo:**

```bash
ollama list                          # Lista modelos descargados
curl http://localhost:11434/api/version  # Comprueba que el servidor responde
```

**Si Ollama no responde:**

```bash
brew services restart ollama         # Reiniciar vía Homebrew
# o manualmente:
killall ollama
/Applications/Ollama.app/Contents/MacOS/ollama serve
```

---

## Estructura del Proyecto y Soporte Multi-IA

El repositorio está diseñado bajo las mejores prácticas universales tanto para un impecable pipeline local de operaciones (EPUB/M4B) como para asegurar la interacción libre de fricciones con sistemas Multi-IA (Gemini, Claude 3.5, Cursor, Windsurf).

```text
genera_epubs/
├── .cursorrules              ← Archivo pivot universal. Orquesta a la IA para leer el contexto
├── AGENTS.md                 ← Reglas maestras (Fuente de la verdad técnica para los LLM)
├── docs/                     ← Documentación centralizada y estructurada
│   ├── context.md            ← Identidad, prioridades y filosofía de trabajo de Rommel
│   ├── architecture.md       ← Diseño del sistema y flujos de arquitectura
│   └── tasks/                ← Tareas pendientes y planes de implementación a futuro
├── .claude/commands/         ← Skills personalizadas para la app desktop de Claude
├── libros_draft/             ← Fuentes (input): archivos .md, .pdf y YAML sidecar
├── portadas_draft/           ← Diseño: portadas estáticas manuales o autogeneradas
├── epubs_generados/          ← Salida (output): EPUBs finales compilados
├── audios_generados/         ← Salida (output): Audiolibros M4B nativos
├── generate_epub.sh          ← Lanzador CLI principal (verifica dependencias y lanza Python)
├── generate_epub.py          ← Orquestador y manejador por procesos
└── epub_generator/           ← Motor pesado interno (pandoc wrappers, EdgeTTS, Pillow)
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

# Sobrescribir el modelo de IA local para extracción visual de PDFs
./generate_epub.sh git-libro.yaml --ai-model llama3.2-vision
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
  title: "Título del Libro" # texto principal de la portada
  subtitle: "Subtítulo" # línea secundaria (opcional)
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

## Compilador Multi-Fuente e Integración Visual (Ollama)

El sistema ahora soporta compilación multi-fuente. En tu YAML, puedes definir un bloque `sources:` para unir archivos Markdown, URLs web y PDFs en un solo libro.

Para extraer el contenido de un PDF con máxima fidelidad (preservando tablas y código), el sistema no usa librerías rotas de texto crudo, sino un **Ingestor Visual (`ollama_pdf`)** que toma fotos de cada página y usa tu modelo VLM local.

### Precondiciones para Extracción Visual

1. Instalar [Ollama](https://ollama.com/) (`brew install --cask ollama`).
2. Descargar un modelo con capacidades visuales (ej. `qwen3.5` o `llama3.2-vision`):
   ```bash
   ollama pull qwen3.5
   ```
3. Mantener la aplicación de Ollama ejecutándose (o el servidor con `ollama serve`).

### Uso de fuentes

```yaml
sources:
  - type: markdown
    path: libros_draft/git-libro.md
  - type: ollama_pdf
    path: /Rutas/a/tus/notas.pdf
    model: qwen2.5-vl   # Se puede omitir si usas el flag --ai-model
    on_error: skip
```

**Ingestores disponibles:**

| Tipo | Descripción |
|---|---|
| `markdown` | Archivo `.md` local |
| `ollama_pdf` | PDF → Markdown vía VLM local (Ollama + visión) |
| `url` | Página web → Markdown (BeautifulSoup + markdownify) |
| `html` | Archivo HTML local → Markdown |
| `text` | Archivo `.txt` plano |
| `word` | Archivo `.docx` (python-docx) |
| `epub` | Recompilar un EPUB existente (ebooklib) |
| `pdf` | PDF con capa de texto (PyMuPDF, sin IA) |
| `ncx` / `opf` | Metadatos de EPUB internos |

### El Flag `--ai-model`

Si estás probando qué modelo entiende mejor tus diagramas, no necesitas editar el YAML constantemente. Usa el flag en la terminal para inyectar dinámicamente el modelo a usar:

```bash
# Probar con Qwen (visión)
./generate_epub.sh libros_draft/git-libro.yaml --ai-model qwen2.5-vl

# Probar con Llama Vision
./generate_epub.sh libros_draft/git-libro.yaml --ai-model llama3.2-vision
```

---

## Audiolibros

El sistema genera audiolibros M4B con narración TTS (edge-tts), chapter markers navegables,
portada embebida, intro/outro automático y caché por capítulo.

### Precondiciones adicionales para audio

| Herramienta              | Para qué                                | Instalar                                          |
| ------------------------ | --------------------------------------- | ------------------------------------------------- |
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
  voice: "" # vacío = auto por idioma (es-ES-AlvaroNeural)
  rate: "-5%" # velocidad: ligeramente lento para mejor comprensión
  volume: "+0%" # volumen: neutro
  pitch: "+0Hz" # tono: neutro
  bitrate: "96k" # calidad AAC: 96k es estándar para voz hablada
  chapter_pause: 1.5 # segundos de silencio entre capítulos
  concurrency: 5 # capítulos narrados en paralelo (semáforo)
  intro: true # narrar intro automático ("Este es el audiolibro...")
  outro: true # narrar outro automático ("Fin del audiolibro...")
```

**Voces disponibles por idioma:**

| Idioma | Voz default        |
| ------ | ------------------ |
| es-ES  | es-ES-AlvaroNeural |
| es-MX  | es-MX-JorgeNeural  |
| en-US  | en-US-GuyNeural    |
| en-GB  | en-GB-RyanNeural   |

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
