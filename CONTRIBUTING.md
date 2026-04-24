# Guía de Contribución

## Estructura del Proyecto

```
genera_epubs/
├── generate_epub.sh              # Launcher (verifica deps, venv, lanza Python)
├── generate_epub.py              # CLI principal + orquestación paralela
├── requirements.txt              # Dependencias Python
├── README.MD                      # Documentación principal
├── CONTRIBUTING.md               # Esta guía
├── .gitignore                    # Git ignore rules
├── epub_generator/               # Paquete principal
│   ├── __init__.py
│   ├── config.py                 # BookConfig, AudioConfig, CoverConfig
│   ├── cover.py                  # Generación de portadas con Pillow
│   ├── generator.py              # Dispatcher por extensión/formato
│   ├── styles/
│   │   └── epub.css              # Estilos CSS para EPUBs
│   ├── converters/               # Conversores específicos
│   │   ├── __init__.py
│   │   ├── markdown.py           # Pandoc wrapper (MD → EPUB/Audio)
│   │   ├── pdf.py                # Ebook-convert wrapper (PDF → EPUB)
│   │   └── audio.py              # Edge-TTS wrapper (MD → M4B)
│   └── preprocessors/            # Preparación de contenido
│       ├── __init__.py
│       └── markdown_cleaner.py   # Limpieza de markdown para TTS
├── libros_draft/                 # Fuentes de libros (.md + .yaml)
├── portadas_draft/               # Portadas (generadas o manuales)
├── epubs_generados/              # EPUBs de salida
├── audios_generados/             # M4B audiolibros de salida
├── fonts/                        # Fuentes Inter (auto-descargadas)
└── ralph/                        # Ralph agent (PRD + scripts)
    ├── prd.json
    ├── progress.txt
    ├── CLAUDE.md
    ├── prompt.md
    └── ralph.sh
```

## Archivos Clave y Sus Responsabilidades

### `generate_epub.sh`
- Verifica dependencias del sistema (pandoc, ebook-convert, ffmpeg)
- Descarga fuentes Inter si no existen
- Crea/actualiza venv
- Instala Python dependencies
- Lanza `generate_epub.py` con argumentos parados

**No tocar:** Lógica de negocio — solo setup/checks.

### `generate_epub.py`
- CLI con argparse (soporta `--format epub|audio` y `--no-cache`)
- Descubre libros en `libros_draft/`
- Paraleliza generación con ThreadPoolExecutor
- Maneja logging por libro
- Resuelve portadas (CLI arg → YAML → auto-discovery → generar)

**Responsabilidades:** Orquestación y paralelismo. **No tocar:** Conversión real (eso es del `generator.py`).

### `epub_generator/config.py`
- **BookConfig:** title, author, description, language, date, cover, audio
- **CoverConfig:** colores, tamaños, footer, imagen
- **AudioConfig:** voz, rate, volume, pitch, bitrate, pausas, concurrencia, intro/outro
- `load_config()` lee YAML sidecar, usa defaults si faltan campos

**Contrato:** Los dataclasses definen la "fuente de verdad" de configuración. Todo lo que necesita config va aquí.

### `epub_generator/converters/audio.py`
**TTS pipeline:**

1. `convert_audio()` — Entry point. Verifica ffmpeg/ffprobe, lee chapters, sintetiza con caché
2. `_synthesize_all()` — Paraleliza N capítulos con semáforo (concurrency)
3. `_synthesize_with_cache()` — Lee caché JSON, compara SHA-256, salta si no cambió
4. `_synthesize_intro_outro()` — Genera intro/outro narrados si `config.audio.intro/outro` es true
5. `_assemble_m4b()` — Ensambla M4B: concat.txt + metadata ffmpeg + portada embebida + pausas

**Parámetros tuneables:**
- `config.audio.concurrency` (default 5): máximo de capítulos narrados en paralelo
- `config.audio.rate` (default "-5%"): velocidad de narración
- `config.audio.chapter_pause` (default 1.5s): silencio entre capítulos
- `config.audio.bitrate` (default "96k"): calidad AAC

### `epub_generator/preprocessors/markdown_cleaner.py`
**Limpieza de markdown para TTS:**

1. `extract_chapters()` — Divide por `# H1 Headings`, extrae frontmatter
2. `clean_for_tts()` — Elimina:
   - Code blocks → "Para ver código, consulta el EPUB"
   - Inline code, tablas → redirects
   - HTML, URLs sueltas, emojis, caracteres unicode decorativos
   - Blockquotes, listas (preserva el contenido)
3. Preserva: caracteres hispanicos (tildes, ñ, signos invertidos)

**Importante:** El caché de audio (US-011) usa SHA-256 del texto **post-limpieza**, no del markdown original. Así cambios cosméticos no invalidan el caché.

### `epub_generator/converters/markdown.py` (EPUB)
- Wrapper de pandoc con opciones profesionales
- CSS personalizado (`--css=styles/epub.css`)
- Metadata: title, author, language, description, date, cover
- TOC generado automáticamente
- Syntax highlighting con Espresso

### `epub_generator/cover.py`
- Genera portadas JPG (600×800px) con Pillow
- Lee config de `CoverConfig` (colores, texto, tamaños)
- Text wrapping automático con `textwrap`
- Carga fuentes Inter Regular/Bold
- Idempotent: no sobrescribe portadas existentes

---

## Flujo de Generación

### EPUB
```
markdown.md + markdown.yaml
    ↓
load_config() → BookConfig
    ↓
generate_cover() → portada.jpg (si no existe)
    ↓
pandoc (--css, metadata, toc, cover) → EPUB
```

### Audiolibro M4B
```
markdown.md + markdown.yaml
    ↓
load_config() → BookConfig (lee config.audio)
    ↓
extract_chapters() → [Chapter, Chapter, ...]
    ↓
clean_for_tts() → texto limpio
    ↓
_synthesize_with_cache()
  ├─ read cache_manifest.json
  ├─ para cada capítulo:
  │  ├─ SHA-256(texto_limpio)
  │  ├─ if hash en caché y archivo existe → skip
  │  └─ else → edge-tts + update caché
  └─ save cache_manifest.json
    ↓
_synthesize_intro_outro() (si config.audio.intro/outro)
    ↓
_assemble_m4b()
  ├─ silence.mp3 (config.audio.chapter_pause segundos)
  ├─ concat.txt (interleave capítulos + silencio)
  ├─ metadata.txt (ffmpeg [CHAPTER] entries con timestamps)
  ├─ ffmpeg: concat + metadata + cover (si existe)
  └─ limpiar temp files
    ↓
audiolibro.m4b (con chapter markers, portada, metadata)
```

---

## Desarrollo Local

### Setup
```bash
# Clonar repo
git clone <url>
cd genera_epubs

# Primer run (setup automático)
./generate_epub.sh agentes-ia-libro

# O manual
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python generate_epub.py agentes-ia-libro
```

### Testing Manual

```bash
# Generar un EPUB
./generate_epub.sh --format epub agentes-ia-libro

# Generar un audiolibro
./generate_epub.sh --format audio agentes-ia-libro

# Forzar re-narración (ignora caché)
./generate_epub.sh --format audio --no-cache agentes-ia-libro

# Verificar M4B con ffprobe
ffprobe -show_chapters audios_generados/agentes-ia-libro.m4b
```

### Verificación de Calidad

```bash
# Typecheck
.venv/bin/python -m mypy epub_generator/ --ignore-missing-imports

# Linter (si aplica)
.venv/bin/python -m pylint epub_generator/ || true
```

---

## Cambios Comunes

### Agregar nueva voz para idioma
**Archivo:** `epub_generator/converters/audio.py`
```python
SUPPORTED_VOICES = {
    "es-ES": "es-ES-AlvaroNeural",
    "es-MX": "es-MX-JorgeNeural",
    "en-US": "en-US-GuyNeural",
    "en-GB": "en-GB-RyanNeural",
    "fr-FR": "fr-FR-DeniseNeural",  # ← agregar aquí
}
```

### Cambiar estilos de EPUB
**Archivo:** `epub_generator/styles/epub.css`
- Cambiar colores de headings, backgrounds, márgenes
- El CSS se pasa a pandoc con `--css=`

### Agregar más opciones de audio
1. Agregar campo a `AudioConfig` en `config.py`
2. Actualizar `_build_audio()` con default
3. Leer en `convert_audio()` / `_synthesize()`
4. Documentar en README.MD

Ejemplo: agregar `audio.voice_rate_multiplier` (factor adicional de velocidad):
```python
# config.py
@dataclass
class AudioConfig:
    ...
    voice_rate_multiplier: float = 1.0

# audio.py
actual_rate = f"{config.audio.rate} * {config.audio.voice_rate_multiplier}"
# (depende de si edge-tts lo soporta)
```

### Cambiar bitrate de audiolibro
**Archivo:** `epub_generator/converters/audio.py`, función `_assemble_m4b()`
```python
bitrate = config.audio.bitrate  # default "96k"
cmd.extend(["-c:a", "aac", "-b:a", bitrate, str(output)])
```

---

## Troubleshooting

### "ffmpeg no está instalado"
```bash
brew install ffmpeg        # macOS
sudo apt install ffmpeg    # Linux
```

### "pandoc no está instalado"
```bash
brew install pandoc        # macOS
sudo apt install pandoc    # Linux
```

### EPUB sin estilos
Verificar que `epub_generator/styles/epub.css` existe:
```bash
ls -l epub_generator/styles/epub.css
```

Si falta, regenerar con uno de los primeros tres stories (Ralph).

### M4B sin chapter markers
Verificar ffprobe:
```bash
ffprobe -show_chapters audios_generados/libro.m4b
# Debe mostrar [CHAPTER] entries
```

Si está vacío, revisar que `_generate_chapter_metadata()` se ejecutó (check logs).

### Cache no funciona / siempre re-narra
Verificar archivo de caché:
```bash
cat audios_generados/libro_chapters/cache_manifest.json
```

Si está vacío o malformado, usar `--no-cache` y regenerar:
```bash
./generate_epub.sh --format audio --no-cache libro
```

---

## Performance

| Operación | Tiempo (estimado) |
|---|---|
| EPUB (1 libro) | 5-10s (pandoc) |
| M4B (20 capítulos, concurrencia=5) | 3-5 min (edge-tts) |
| M4B (caché hit 19/20 capítulos) | 20s (solo 1 narrado) |

**Cuellos de botella:**
1. Edge-tts (TTS, no hay mucho que hacer — el semáforo lo mantiene bajo control)
2. Pandoc (para EPUBs grandes, pero generalmente rápido)
3. ffmpeg ensamblado (depende de tamaño del audio)

---

## Próximos Pasos (P1/P2)

- [ ] Caché por portada (re-generar solo si config cambió)
- [ ] Soporte para múltiples voces dentro de un capítulo (dialogos)
- [ ] Jingle/música de entrada (audio.intro_music)
- [ ] EPUBCheck validación post-generación
- [ ] Soporte para .rst, .asciidoc (además de .md)
- [ ] Webhook para disparar generación automática (CI)
