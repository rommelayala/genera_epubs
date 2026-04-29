# Plan de Implementación: Compilador Multi-Fuente (Ingestion Pipeline)

## Objetivo

Extender genera_epubs para que un YAML pueda declarar múltiples fuentes (PDF, URL, EPUB, Video, Markdown), ingerirlas, extraerlas y unificarlas en un "Master Markdown" que alimenta al pipeline existente (EPUB / Audiolibro) sin romper la compatibilidad actual.

---

## Decisiones Pendientes

(esto aun no lo haremos) ### 1. Transcripción de Video/Audio

**Opciones:**

| Opción                 | Pros                             | Contras                                      |
| ---------------------- | -------------------------------- | -------------------------------------------- |
| `openai-whisper` local | Sin costos, privacidad total     | Pesado (~1.5 GB modelo medium), lento en CPU |
| API OpenAI Whisper     | Rápido, preciso                  | Costo por minuto, requiere API key           |
| API Gemini             | Acepta video directo, multimodal | Costo, dependencia Google                    |

**Recomendación:** Campo `transcription_service` en el YAML (`whisper`, `openai`, `gemini`). Default: `whisper` si está instalado, sino error con mensaje claro.

### 2. URLs de YouTube

Considerar soporte de `yt-dlp` para descargar transcripciones/subtítulos de YouTube sin necesidad de transcribir audio. Es más rápido y gratuito cuando el video ya tiene subtítulos.

---

## Compatibilidad hacia Atrás

El flujo actual funciona así:

1. `generate_epub.py` recibe un nombre (ej. `git-libro`)
2. `_resolve_input()` busca `libros_draft/git-libro.md`
3. `load_config()` busca `libros_draft/git-libro.yaml` a partir del path del `.md`
4. Se pasa el `.md` + config al converter

**Regla:** Si el YAML NO tiene campo `sources`, todo funciona exactamente igual. El pipeline multi-fuente solo se activa cuando `sources` existe en el YAML.

**Cambio de flujo con sources:** El YAML se convierte en el punto de entrada principal. Se puede pasar `git-libro.yaml` directamente, y el sistema genera el Master Markdown antes de entrar al converter.

---

## Dependencias Nuevas

```
# requirements.txt - agregar:
beautifulsoup4        # Parsing HTML desde URLs
markdownify           # HTML -> Markdown
pypdf                 # Extracción texto de PDFs
requests              # Descargas HTTP
ebooklib              # Lectura de EPUBs externos
```

**Opcionales (solo si se usa video):**

```
openai-whisper        # Transcripción local
yt-dlp                # Subtítulos de YouTube
# ffmpeg debe estar instalado en el sistema (ya lo tenemos para audio)
```

---

## Estructura YAML Propuesta

```yaml
title: "Git Uso Maestro"
author: "Rommel Ayala"
description: "Guía completa de Git"
language: "es-ES"
date: "2026"

# --- Multi-fuente (opcional) ---
sources:
  - type: markdown
    path: "libros_draft/git-libro-base.md" # relativo al proyecto

  - type: pdf
    path: "/Users/rommel/Downloads/Git-Notes.pdf" # absoluto también vale

  - type: url
    url: "https://example.com/git-tutorial"
    selector: "article" # CSS selector para extraer solo el contenido útil

  - type: epub
    path: "~/Downloads/pro-git.epub"

  - type: video
    path: "/Users/rommel/Videos/git-talk.mp4"
    transcription_service: whisper # whisper | openai | gemini

  - type: youtube
    url: "https://youtube.com/watch?v=xxxxx"
    prefer_subtitles: true # usar subs existentes antes de transcribir

cover:
  title: "Git Uso Maestro"
  subtitle: "De Principiante a Casi Experto"
```

**Notas sobre el YAML:**

- El orden de `sources` define el orden en el Master Markdown
- Cada source se inserta como un H1: usa `source.title` si está definido; si no, default = basename del path o dominio de la URL. Esto convierte cada fuente en un capítulo del EPUB y aparece en el TOC. **No se usan separadores `---` adicionales**, las cabeceras hacen ese trabajo
- Paths relativos se resuelven desde `_PROJECT_ROOT`; `~` se expande al home del usuario
- Si no hay `sources`, se usa el `.md` asociado al YAML (flujo actual)

---

## Cambios Propuestos

### Fase 1: Infraestructura base + Markdown/PDF (MVP)

#### 1.1 Nuevo dataclass `SourceConfig` en `config.py`

```python
@dataclass
class SourceConfig:
    type: str            # markdown | pdf | url | epub | video | youtube
    path: str = ""
    url: str = ""
    selector: str = ""   # CSS selector para URLs
    transcription_service: str = "whisper"
    prefer_subtitles: bool = True
    title: str = ""      # Opcional: cabecera al inicio. Si el contenido ya empieza por una cabecera del mismo nivel, se omite la inyección para no duplicar
    title_level: int = 1 # Nivel de cabecera (1 = #, 2 = ##)
    on_error: str = "skip"  # skip | abort — qué hacer si la ingestión falla en runtime (timeout, PDF corrupto, etc.)
```

Agregar a `BookConfig`:

```python
sources: list[SourceConfig] = field(default_factory=list)
```

Y su builder `_build_sources(data: list[dict]) -> list[SourceConfig]` en `load_config()`.

#### 1.2 Módulo `epub_generator/ingestors/`

```
epub_generator/ingestors/
    __init__.py          # Registry: INGESTORS = {"markdown": MarkdownIngestor, ...}
    base.py              # Clase abstracta
    markdown_ingestor.py
    pdf_ingestor.py
```

**Clase base:**

```python
class BaseIngestor(ABC):
    @abstractmethod
    def extract(self, source: SourceConfig, project_root: Path) -> str:
        """Devuelve contenido Markdown limpio."""
        ...

    def resolve_path(self, source: SourceConfig, project_root: Path) -> Path:
        """Resuelve paths relativos y expande ~."""
        p = Path(source.path).expanduser()
        if not p.is_absolute():
            p = project_root / source.path
        if not p.exists():
            raise FileNotFoundError(f"Fuente no encontrada: {p}")
        return p
```

**Notas por ingestor (Fase 1):**

- `markdown_ingestor`: lectura directa, sin transformación. Asume UTF-8.
- `pdf_ingestor`:
  - `pypdf.PdfReader` con extracción página a página, separadas por doble salto de línea
  - **Imágenes**: `pypdf` no extrae imágenes embebidas, se ignoran silenciosamente. Si una página no devuelve texto (PDF escaneado), se loguea warning y se continúa con las siguientes. Para libros muy ilustrados o escaneados, considerar `pdfplumber` o un paso de OCR fuera del pipeline (no entra en este alcance)

#### 1.3 Orquestador de ingestión en `epub_generator/compiler.py`

Crear un orquestador dedicado para mantener `generate_epub.py` limpio.

**Nuevo archivo `compiler.py`:**
- Exporta función `compile_book(config, basename) -> Path`
- **Validación temprana** (antes de tocar ningún source): tipo soportado, campos requeridos por type (`url`/`youtube` requieren `url`; el resto requiere `path`), paths existentes y expandibles. Si alguna falla, aborta antes de ingerir nada para no malgastar tiempo en un build que ya está roto.
- Itera `config.sources` en orden y llama al ingestor correspondiente por `source.type`
- Inyecta cabecera si `source.title` está definido (usando `title_level` para generar `#` o `##`). **Si el contenido ya empieza por una cabecera del mismo nivel, omite la inyección para no duplicar.**
- Si no hay `source.title`, el ingestor genera un default: basename del archivo o dominio de la URL
- Concatena resultados separando con la cabecera H1 de cada fuente. **No usar `---`**: con cabeceras reales se obtiene el TOC del EPUB
- Escribe **`libros_draft/{basename}_compiled.md`** (con sufijo `_compiled` para evitar sobreescribir archivos manuales del usuario)
- **Errores de runtime** (URL caída, PDF corrupto, etc.): comportamiento según `source.on_error`. Por defecto `skip` con warning; si `abort`, propaga la excepción y aborta el libro entero
- **Logging por fuente**: `[basename] (1/4) ingiriendo pdf: Git-Notes.pdf` — clave para entender builds en paralelo

**Integración en `generate_epub.py`:**
Nuevo paso en `_process_book()`, ANTES del `generate()`:

```python
if config.sources:
    input_path = compile_book(config, basename) # devuelve path al _compiled.md
```

#### 1.4 Adaptar `load_config()` y descubrimiento para aceptar YAML directo

Actualmente `load_config(input_path)` deriva el YAML del `.md`. Necesitamos que también funcione al revés: si se pasa un `.yaml`, usarlo directamente. Cambio en `_resolve_input()`:

```python
# Si el input es un .yaml con sources, es válido como punto de entrada
if p.suffix == ".yaml" and p.exists():
    return p
```

Y en `_process_book()`, si `input_path` es `.yaml`, cargar config directamente de él. **El `basename` se sigue derivando con `input_path.stem`**, por lo que `git-libro.yaml` → `git-libro.epub`. El sufijo `_compiled` solo aparece en el archivo intermedio dentro de `libros_draft/`, no en la salida.

**Auto-descubrimiento sin argumento** (`generate_epub.py main()`, glob actual sobre `INPUT_EXTENSIONS`):
- Añadir `.yaml` al glob, pero solo aceptar los que tengan `sources` (los YAMLs de configuración pura asociados a un `.md` se ignoran como entrada propia).
- Si existen `git-libro.yaml` (con `sources`) y `git-libro.md` a la vez, gana el `.yaml` como punto de entrada multi-fuente. **Deduplicar por `stem`** antes de lanzar al `ThreadPoolExecutor` para no procesar el mismo libro dos veces.

### Fase 2: URL + EPUB

#### 2.1 `epub_generator/ingestors/url_ingestor.py`

- `requests.get()` con timeout de 10s y User-Agent razonable
- `BeautifulSoup` para parsear + `source.selector` para filtrar contenido
- `markdownify` para convertir a Markdown
- Limpiar: eliminar scripts, styles, navs, footers
- **Imágenes**: En caso de no poder descargar la imagen, sustituir por cita: `[Ver imagen en la fuente original]({url})`.

#### 2.2 `epub_generator/ingestors/epub_ingestor.py`

- `ebooklib` (o alternativamente `zipfile` nativo) para leer el EPUB
- Iterar items de tipo `EpubHtml` en orden spine
- Convertir cada capítulo HTML a Markdown con `markdownify`
- **Imágenes**: Extraer assets localmente, o reemplazar por cita/enlace si falla.

### Fase 3: Video/Audio + YouTube

#### 3.1 `epub_generator/ingestors/video_ingestor.py`

- Extraer audio con `ffmpeg` (subprocess, ya lo usamos en el proyecto)
- Según `transcription_service`: Whisper local, API OpenAI, o API Gemini
- Generar Markdown con timestamps como headers

#### 3.2 `epub_generator/ingestors/youtube_ingestor.py`

- Si `prefer_subtitles=true`: intentar `yt-dlp --write-subs` primero
- Fallback: descargar audio y transcribir como video_ingestor

---

## Manejo de Errores

| Escenario                              | Fase       | Comportamiento por defecto                                                |
| -------------------------------------- | ---------- | ------------------------------------------------------------------------- |
| Tipo de source no soportado            | Validación | Error: aborta antes de ingerir                                            |
| Campo requerido ausente (`url`/`path`) | Validación | Error: aborta antes de ingerir                                            |
| Path inexistente                       | Validación | Error: aborta antes de ingerir                                            |
| URL no responde / timeout              | Runtime    | `on_error=skip` → warning y se salta. `on_error=abort` → propaga          |
| PDF sin texto (escaneado)              | Runtime    | Warning: "PDF parece ser imagen, contenido vacío" (respeta `on_error`)    |
| Whisper no instalado                   | Validación | Error claro: "instala openai-whisper o cambia transcription_service"      |
| YAML sin sources ni .md asociado       | Validación | Error: "No hay contenido fuente"                                          |

---

## Consideraciones de Concurrencia

`generate_epub.py` procesa libros en paralelo con `ThreadPoolExecutor` (un libro por hilo). Con multi-fuente:

- Una transcripción de video puede tardar minutos y bloquea el hilo del libro completo.
- Varios libros con video en paralelo pueden saturar CPU/red.
- **Recomendación Fase 3**: limitar `max_workers` cuando algún libro tenga sources de tipo `video`/`youtube`, o procesar esos libros secuencialmente. Documentar el trade-off cuando se aborde.
- Para Fase 1/2 no hay cambios necesarios: PDFs y URLs son rápidos y compatibles con el modelo actual de paralelismo.

---

## Archivos a Crear/Modificar

| Archivo                                         | Acción                                       | Fase |
| ----------------------------------------------- | -------------------------------------------- | ---- |
| `epub_generator/config.py`                      | MODIFICAR - agregar `SourceConfig` y parsing | 1    |
| `epub_generator/ingestors/__init__.py`          | CREAR - registry de ingestors                | 1    |
| `epub_generator/ingestors/base.py`              | CREAR - clase abstracta                      | 1    |
| `epub_generator/ingestors/markdown_ingestor.py` | CREAR                                        | 1    |
| `epub_generator/ingestors/pdf_ingestor.py`      | CREAR                                        | 1    |
| `epub_generator/compiler.py`                    | CREAR - lógica de ensamblaje (`compile_book`)| 1    |
| `generate_epub.py`                              | MODIFICAR - llamar a `compile_book`          | 1    |
| `epub_generator/generator.py`                   | MODIFICAR - aceptar `.yaml` como input       | 1    |
| `requirements.txt`                              | MODIFICAR - nuevas deps                      | 1    |
| `epub_generator/ingestors/url_ingestor.py`      | CREAR                                        | 2    |
| `epub_generator/ingestors/epub_ingestor.py`     | CREAR                                        | 2    |
| `epub_generator/ingestors/video_ingestor.py`    | CREAR                                        | 3    |
| `epub_generator/ingestors/youtube_ingestor.py`  | CREAR                                        | 3    |

---

## Tests y Fixtures

Estructura propuesta (espejo del módulo):

```
tests/
    ingestors/
        test_markdown_ingestor.py
        test_pdf_ingestor.py
        test_url_ingestor.py        # con responses/httpretty para mockear HTTP
        test_epub_ingestor.py
    test_compiler.py                # orquestación + validación + on_error
    test_resolve_input.py           # discovery de .yaml + dedup con .md
    fixtures/
        sample.pdf                  # 2-3 páginas, texto extraíble
        sample-scanned.pdf          # opcional: simular PDF imagen
        sample.epub                 # mini EPUB con 2 capítulos
        sample.html                 # snapshot HTML para URL ingestor
        compiled-expected/          # golden files del Master Markdown
```

Cobertura mínima:

- Cada ingestor por separado contra su fixture.
- `compile_book()` con combinaciones representativas: una sola fuente, `md+pdf`, fuente que falla con `on_error=skip` vs `abort`, validación temprana (path inexistente, tipo no soportado).
- **Regresión**: YAML sin `sources` produce el mismo EPUB que el flujo previo. Comparar hash del `.epub` o del Master Markdown intermedio entre ramas.

---

## Plan de Verificación

### Fase 1

- [ ] YAML sin `sources` sigue funcionando igual (regresión)
- [ ] YAML con un source `markdown` genera el mismo resultado que el flujo directo
- [ ] YAML con source `pdf` extrae texto y genera EPUB válido
- [ ] YAML con `markdown` + `pdf` combina ambos en orden correcto
- [ ] Paths relativos y absolutos se resuelven correctamente
- [ ] Source con path inexistente da error claro

### Fase 2

- [ ] URL válida se descarga y convierte a Markdown limpio
- [ ] `selector` filtra correctamente el contenido
- [ ] URL caída genera warning pero no aborta el libro
- [ ] EPUB externo se lee y sus capítulos se integran en orden

### Fase 3

- [ ] Video local se transcribe con Whisper
- [ ] YouTube con subtítulos usa subs directamente
- [ ] YouTube sin subtítulos hace fallback a transcripción
- [ ] `transcription_service` alterna entre whisper/openai/gemini
