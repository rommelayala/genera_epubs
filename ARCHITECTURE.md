# Arquitectura — Genera EPUBs

## Visión General

**Genera EPUBs** es un generador de libros digitales (EPUB) y audiolibros (M4B) de calidad profesional desde Markdown o PDF. Está diseñado para producir salida lista para plataformas como Apple Books, Google Play Books, Kobo, Amazon KDP y Audiobookshelf.

**Filosofía:**
- **Configuración declarativa** (YAML sidecar por libro)
- **Paralelismo** (generar múltiples libros simultáneamente)
- **Caché inteligente** (re-narración incremental para audios)
- **Defaults sensatos** (funciona sin configuración, pero altamente customizable)
- **Calidad profesional** (CSS, chapter markers, portadas, metadata)

---

## Capas de Arquitectura

### 1. Capa de Configuración (`config.py`)

**Responsabilidad:** Definir el contrato entre usuario (YAML) y código (Python).

**Flujo:**
```
YAML sidecar (libros_draft/libro.yaml)
    ↓
load_config(path) → BookConfig
    ├─ _build_cover(data) → CoverConfig
    └─ _build_audio(data) → AudioConfig
```

**Dataclasses:**
- **BookConfig** — Metadatos del libro (title, author, description, language, date)
- **CoverConfig** — Diseño de portada (colores, tamaños, fuentes, imagen)
- **AudioConfig** — Parámetros de TTS (voz, rate, volume, pitch, bitrate, pausas, caché, intro/outro)

**Decisión de diseño:** Usar dataclasses + defaults en lugar de diccionarios, para:
- Type hints y verificación estática
- Defaults claros y documentados
- No confundir campos faltantes con `None`

---

### 2. Capa de Conversión (`converters/`)

**Responsabilidad:** Transformar markdown/PDF a EPUB/Audio usando herramientas externas.

#### `markdown.py` — Pandoc Wrapper (MD → EPUB)

```python
convert_markdown(input, config, cover, output)
  ↓
cmd = ["pandoc", ..., "--css=styles/epub.css", "--metadata=...", ...]
  ↓
subprocess.run(cmd)
```

**Opciones clave:**
- `--to=epub3` — EPUB 3 (estándar)
- `--toc --toc-depth=2` — Tabla de contenidos
- `--css=` — Estilos personalizados (tipografía, código, tablas)
- `--metadata title/author/language/description/date` — Metadata
- `--epub-cover-image=` — Portada embebida
- `--syntax-highlighting=espresso` — Colores de código

**Decisión:** Usar pandoc como "compilador" de markdown a EPUB en lugar de una librería Python. Razones:
- Pandoc es el estándar de facto para conversión de documentos
- Manejo robusto de markdown complejo
- Mejor control de output (CSS, metadata, TOC)

#### `pdf.py` — Ebook-Convert Wrapper (PDF → EPUB)

```python
convert_pdf(input, config, cover, output)
  ↓
cmd = ["ebook-convert", ..., "--title=", "--cover=", ...]
  ↓
subprocess.run(cmd)
```

**Nota:** PDF debe tener capa de texto (no escaneado). Para OCR, usar Tesseract antes de pasar a esta herramienta.

#### `audio.py` — Edge-TTS Pipeline (MD → M4B)

**Componentes:**

```
extract_chapters(markdown)
    ↓ regex por H1 headings
[Chapter(title, body), ...]
    ↓
clean_for_tts(body)  ← elimina markdown, código, emojis, URLs
    ↓
_synthesize_with_cache()
  ├─ SHA-256(texto_limpio)
  ├─ check cache_manifest.json
  ├─ if no hit: edge_tts.Communicate(..., rate, volume, pitch)
  └─ save caché
    ↓
[MP3, MP3, MP3]  (+ intro/outro si aplica)
    ↓
_assemble_m4b()
  ├─ anullsrc (generar silencio)
  ├─ concat.txt (concat + interleave)
  ├─ metadata.txt (ffmpeg [CHAPTER])
  └─ ffmpeg (concat + metadata + cover)
    ↓
audiolibro.m4b (con chapter markers, portada)
```

**Decisiones de diseño:**

1. **Paralelismo con semáforo:** `asyncio.Semaphore(concurrency)` limita llamadas simultáneas a edge-tts (rate limiting):
   ```python
   async def _chapter_to_mp3_async(..., semaphore):
       async with semaphore:  # max 5 en paralelo
           await _synthesize(...)
   ```
   Sin semáforo, 20 capítulos = 20 requests simultáneos → throttling de edge-tts.

2. **Caché SHA-256:** El hash es del texto **post-limpieza**, no del markdown original:
   ```python
   clean = clean_for_tts(chapter.body)
   text_h = _text_hash(clean)  # hash del texto limpio
   ```
   Así cambios de formato (espacios, markdown) no invalidan el caché.

3. **Intro/Outro generados:** No son archivos, sino texto generado y narrado:
   ```python
   intro_text = f"Este es el audiolibro: {title}. Escrito por {author}."
   await _synthesize(intro_text, voice, "00_intro.mp3")
   ```
   Se insertan en índice 0 (intro) e índice -1 (outro) de la lista de MP3s.

4. **Metadata ffmpeg con TIMEBASE=1/1000:**
   ```
   [CHAPTER]
   TIMEBASE=1/1000
   START=0
   END=45000
   title=Introducción
   ```
   Los timestamps están en milisegundos. Se calculan sumando duraciones de MP3 + pausas.

---

### 3. Capa de Preprocesamiento (`preprocessors/`)

**Responsabilidad:** Preparar contenido para diferentes formatos (EPUB vs. TTS).

#### `markdown_cleaner.py`

**Para EPUB:** No se usa (pandoc maneja markdown nativamente).

**Para TTS:** Elimina elementos que no se pueden narrar:
- Code blocks → "Para ver código, consulta el EPUB"
- Inline code, tablas → redirecciones
- HTML, imágenes → elimina
- Emojis, caracteres unicode decorativos
- URLs sueltas
- Blockquotes, listas, headings (preserva contenido)

**Preserva:**
- Caracteres hispanicos (tildes, ñ, ¡ ¿)
- Puntuación normal

**Orden de limpieza:** Importa, porque regex posterior asume ya no hay ciertos elementos.

---

### 4. Capa de Portadas (`cover.py`)

**Responsabilidad:** Generar portadas profesionales con Pillow.

```python
generate_cover(basename, config, output_dir)
  ├─ load fonts (Inter Regular/Bold)
  ├─ create 600x800 RGB image
  ├─ draw title (centrado, con text wrapping)
  ├─ draw subtitle (si existe)
  ├─ draw línea horizontal (accent color)
  ├─ draw footer (copyright)
  └─ save JPG (quality=95)
```

**Decisión:** Generar en runtime (no pre-renderizar) porque:
- Customizable por libro (colores, tamaños)
- Idempotent (revisar si existe antes de generar)
- Las portadas son datos del libro, no arte estático

**Tipografía:**
- Inter Regular/Bold (font variable moderna)
- Auto-descargada desde GitHub en primer run
- Fallback a default font del sistema si falla

---

### 5. Capa de Orquestación (`generate_epub.py`)

**Responsabilidad:** CLI, descubrimiento de libros, paralelismo.

```
argparse (--format, --no-cache)
    ↓
glob libros_draft/*
    ↓
ThreadPoolExecutor (procesamiento paralelo)
  ├─ Book 1: _process_book()
  ├─ Book 2: _process_book()
  └─ Book 3: _process_book()
    ↓
    cada _process_book():
    ├─ load_config()
    ├─ _resolve_cover()
    ├─ generate() → dispatcher
    └─ log resultado
    ↓
reporter final
```

**Logging por libro:** Cada libro tiene su logger independiente con prefijo:
```python
logger = logging.getLogger(book_name)
handler = StreamHandler()
handler.setFormatter(f"[{book_name}] %(message)s")
logger.addHandler(handler)
```

Así en paralelismo, logs de diferentes libros no se mezclan.

---

### 6. Dispatcher (`generator.py`)

**Responsabilidad:** Rutear a converter correcto según (extensión, formato).

```python
CONVERTERS = {
    (".md",  "epub"): convert_markdown,
    (".pdf", "epub"): convert_pdf,
    (".md",  "audio"): convert_audio,
}

def generate(..., output_format):
    key = (input_path.suffix, output_format)
    converter = CONVERTERS[key]
    converter(...)
```

**Extensibilidad:** Para agregar nuevo formato:
1. Crear `converters/formato.py` con `def convert_formato(...)`
2. Registrar en `CONVERTERS`
3. Actualizar `generate_epub.sh` con checks de deps

---

## Decisiones Clave

### 1. YAML Sidecar vs. Frontmatter
**Decisión:** YAML sidecar (`libro.yaml` junto a `libro.md`)

**Razones:**
- Separación clara entre contenido y metadata
- Facilita edición de contenido sin tocar config
- Supporta múltiples formatos (MD y PDF)
- Pandoc lee frontmatter, pero YAML sidecar es agnóstico

**Trade-off:** Un archivo extra por libro, pero evita duplicación en .md + .pdf.

### 2. Pandoc vs. Librería Python
**Decisión:** Pandoc (subprocess)

**Razones:**
- Estándar de facto para conversión de documentos
- Mejor soporte para markdown complejo
- CSS personalizado (no disponible en librerías Python)
- Mantenido por comunidad activa

### 3. Edge-TTS vs. Alternativas
**Decisión:** Edge-TTS (gratuito, de Microsoft)

**Razones:**
- Gratuito (sin API keys)
- Voces naturales de buena calidad
- Soporte para múltiples idiomas
- Rate params (rate, volume, pitch)

**Limitaciones:**
- Rate limiting implicito (por eso el semáforo)
- No es offline (requiere internet)

### 4. M4B (AAC) vs. MP3
**Decisión:** M4B con codec AAC

**Razones:**
- M4B = MP4 audio container estándar para audiobooks
- Soporta chapter markers nativamente
- Mejor compresión que MP3 a misma calidad
- Compatible con todos los reproductores principales

### 5. Caché SHA-256
**Decisión:** Hash del texto post-limpieza, manifiesto JSON local

**Razones:**
- Re-narración incremental (solo capítulos que cambiaron)
- SHA-256 es rápido y determinístico
- Manifiesto JSON es legible y debuggable
- No requiere base de datos externa

**Alternativa descartada:** Caché global en base de datos → complejidad, cloud dependency.

---

## Flujos de Datos

### Generación EPUB
```
YAML (title, author, cover config)
  ↓
load_config() → BookConfig
  ↓ BookConfig.cover
generate_cover() → cover.jpg
  ↓
Markdown
  ↓ pandoc (--css, metadata, cover, toc)
  ↓
EPUB (con portada, TOC, estilos)
```

### Generación M4B
```
YAML (audio: voz, rate, intro, outro, ...)
  ↓
load_config() → BookConfig.audio
  ↓
Markdown
  ↓
extract_chapters() → [Chapter]
  ↓
clean_for_tts() → [Chapter con texto limpio]
  ↓
_synthesize_with_cache()
  ├─ check cache_manifest.json
  ├─ edge-tts (paralelo, semáforo)
  └─ [MP3 files]
    ↓
_synthesize_intro_outro() → [intro.mp3, outro.mp3]
  ↓ merge
[intro.mp3, cap1.mp3, cap2.mp3, ..., outro.mp3]
  ↓
_assemble_m4b()
  ├─ generate silence.mp3
  ├─ concat.txt (interleave)
  ├─ metadata.txt ([CHAPTER] con timestamps)
  ├─ ffmpeg concat + metadata + cover
  └─ cleanup
    ↓
M4B (chapter markers, portada, metadata)
```

---

## Extensibilidad

### Agregar nuevo formato de salida
Ejemplo: Generar PDF con WeasyPrint.

```python
# converters/weasyprint.py
def convert_html_pdf(input, config, cover, output):
    html = f"<h1>{config.title}</h1>..."
    HTML(string=html).write_pdf(output)

# generator.py
CONVERTERS[(".md", "pdf")] = convert_html_pdf
```

### Agregar nuevo idioma/voz
```python
# config.py
SUPPORTED_VOICES["pt-BR"] = "pt-BR-AntonioNeural"
```

### Agregar opción de audio
```python
# config.py: agregar field a AudioConfig
# audio.py: leer config.audio.nuevo_campo
# README.MD: documentar
```

---

## Performance y Escalabilidad

### Benchmarks Típicos
- **EPUB (1 libro, ~100 páginas):** 5-10 segundos
- **M4B (20 capítulos, 5h audio):** 3-5 minutos (edge-tts)
- **M4B con caché (1 capítulo editado):** 20 segundos

### Cuellos de botella
1. **Edge-TTS:** Tasa más lenta. Semáforo mantiene throughput bajo control.
2. **Pandoc:** Generalmente rápido, pero lento en markdown muy grandes (1000+ páginas).
3. **FFmpeg ensamblado:** Lineal con tamaño del audio (pero rápido en SSD).

### Paralelismo
- **ThreadPoolExecutor:** Usado para generar múltiples libros simultáneamente.
- **asyncio.gather:** Usado para narrar múltiples capítulos en paralelo (dentro de un libro).

---

## Seguridad y Validación

### Inyección de comandos
**Riesgo:** Metadata con caracteres especiales pasada a pandoc/ffmpeg.

**Mitigación:** Usar listas de argumentos (no `shell=True`):
```python
subprocess.run(["pandoc", str(input_path), f"--metadata=title={config.title}"])
# Safe: argumento es pasado como-está, no interpretado por shell
```

### Paths absolutos vs. relativos
**Decisión:** Usar `Path` de pathlib y resolver a absolutos cuando sea necesario.

```python
cover_path = _COVERS_DIR / f"{basename}.jpg"  # relativo
subprocess.run(["ffmpeg", ..., str(cover_path.resolve())])  # absoluto
```

### Validación de YAML
**Decisión:** `yaml.safe_load()` (evita arbitrary code execution).

---

## Logging

**Estrategia:**
- Un logger por libro en modo paralelo
- Prefijo `[book_name]` para rastrear qué sale de dónde
- Niveles: INFO (normal), WARNING (problemas no fatales), ERROR (fallo)

**Ejemplo:**
```
📚 Descubiertos 3 libros: 2 markdown, 1 PDF.
🚀 Procesando en paralelo...

[claude-uso-maestro]    🖼️  Portada: claude-uso-maestro.jpg
[claude-uso-maestro]    🔄 Convirtiendo (.md → epub)...
[claude-uso-maestro]    ✅ epubs_generados/claude-uso-maestro.epub
[agentes-ia-libro]      🖼️  Portada: agentes-ia-libro.jpg
[agentes-ia-libro]      🔄 Convirtiendo (.md → audio)...
[agentes-ia-libro]      Voz: es-ES-AlvaroNeural | 25 capítulos | concurrencia: 5
[agentes-ia-libro]      Narrando capítulo 1 de 25: Introducción
...
```

---

## Roadmap Técnico

- [ ] Caché de portadas (re-generar solo si config cambió)
- [ ] Validación EPUB con EPUBCheck
- [ ] Soporte para .rst, .asciidoc
- [ ] Webhook para CI/CD (auto-generar en push)
- [ ] API REST (generar libros bajo demanda)
- [ ] Interfaz web (upload, generar, descargar)
- [ ] Soporte para múltiples voces en audio (dialogos)
- [ ] OCR para PDFs escaneados (Tesseract)
