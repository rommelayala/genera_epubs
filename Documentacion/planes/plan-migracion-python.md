# Plan: Migración a Python — Generador de EPUBs

---

## Objetivo

Reemplazar `generate_epub.sh` como motor de generación por un CLI en Python extensible,
manteniendo la invocación por comandos y añadiendo:
- Metadata enriquecida por libro via archivo YAML sidecar
- Portadas configurables desde el mismo YAML
- **Soporte multi-formato de entrada**: genera EPUB desde `.md` (Pandoc) **y desde `.pdf`**
  (ebook-convert de Calibre)

---

## Principios

- **DRY**: Bash solo lanza. Python posee toda la lógica.
- **SOLID**: cada módulo tiene una sola responsabilidad.
- **80-20**: lo que da mayor valor primero — metadata + portada configurable.

---

## Estructura de archivos resultante

```
genera_epubs/
├── generate_epub.sh          ← launcher: deps + pandoc + calibre → delega a Python
├── generate_epub.py          ← entry point CLI + orquestación paralela
├── requirements.txt          ← Pillow, PyYAML (y lo que se añada en el futuro)
├── epub_generator/
│   ├── __init__.py
│   ├── generator.py          ← dispatcher por extensión (.md / .pdf)
│   ├── converters/
│   │   ├── __init__.py
│   │   ├── markdown.py       ← wrapper de pandoc
│   │   └── pdf.py            ← wrapper de ebook-convert (Calibre)
│   ├── cover.py              ← generación de portadas con Pillow
│   └── config.py             ← lectura de YAML sidecar por libro
├── libros_draft/             ← Ejemplos:
│                               claude-uso-maestro.md  + claude-uso-maestro.yaml
│                               manual-legado.pdf      + manual-legado.yaml
├── portadas_draft/           ← portadas generadas o manuales
                              ← Ejemplos:
│                               claude-uso-maestro.jpg

└── epubs_generados/          ← output final
```

> `generate_minimal_covers.py` queda **deprecado** — su lógica pasa a `cover.py`.

---

## Responsabilidades por módulo

### `generate_epub.sh` — Launcher
- Detecta OS (Linux / macOS) y verifica dependencias del sistema:
  - `pandoc` (para `.md`)
  - `ebook-convert` de Calibre (para `.pdf`) — opcional, solo falla si hay `.pdf` en el batch
- Si falta una dependencia, imprime el comando exacto para instalarla y sale.
- Crea venv Python si no existe y ejecuta `pip install -r requirements.txt`.
- Pasa todos los argumentos sin modificar a `generate_epub.py`.
- **Sin lógica de negocio.**

**Ejemplo de error cuando falta pandoc (Linux):**
```
❌ pandoc no está instalado.
   Instálalo con:
       sudo apt install pandoc
```

**Ejemplo de error cuando falta Calibre y hay un .pdf en el batch:**
```
❌ ebook-convert (Calibre) no está instalado. Se requiere para procesar PDFs.
   Instálalo con:
       sudo apt install calibre
   O ejecuta sin los .pdf para procesar solo los .md.
```

**Ejemplo de primer arranque (venv se crea solo, sin sudo):**
```
🔧 Creando venv en .venv/...
🔧 Instalando dependencias Python (Pillow, PyYAML)...
🚀 Ejecutando generate_epub.py...
```

### `generate_epub.py` — Entry point + Orquestador
- Parsea argumentos con `argparse`:
  - Sin args → todos los `.md` **y** `.pdf` en `libros_draft/`
  - Con arg → archivo específico (auto-detecta extensión)
- Descubre archivos de entrada soportados (`.md`, `.pdf`).
- Lanza `generator.py` en paralelo con `ThreadPoolExecutor`.
- Reporta progreso y errores.
- **Nota**: se asume que no existen dos archivos con el mismo basename pero
  distinta extensión en `libros_draft/` (responsabilidad del usuario).

### `epub_generator/config.py` — Configuración
- Lee el archivo `libros_draft/{basename}.yaml` junto al `.md` o `.pdf` del mismo nombre.
- Devuelve un dataclass `BookConfig` con defaults si el `.yaml` no existe o falta algún campo.
- Ejemplos:
  - `claude-uso-maestro.md` → `claude-uso-maestro.yaml`
  - `manual-legado.pdf` → `manual-legado.yaml`

**Ejemplo del dataclass con defaults:**
```python
@dataclass
class CoverConfig:
    title: str = ""                              # fallback al BookConfig.title
    subtitle: str = ""
    bg_color: str = "#151515"
    text_color: str = "#EAEAEA"
    accent_color: str = "#4A4A4A"
    title_size: int = 42
    subtitle_size: int = 24
    footer: str = "© Rommel Ayala - All rights reserved"

@dataclass
class BookConfig:
    title: str = "Untitled"
    author: str = "Rommel Ayala - QA Lead"
    description: str = ""
    language: str = "es-ES"
    date: str = ""
    cover: CoverConfig = field(default_factory=CoverConfig)
```

```yaml
# claude-uso-maestro.yaml
title: "Claude: Uso Maestro"
author: "Rommel Ayala - QA Lead"
description: "Guía práctica sobre agentes de inteligencia artificial"
language: "es-ES"
date: "2026"
cover:
  title: "Claude: Uso Maestro"  # texto principal de la portada
  subtitle: "Guía Práctica"     # línea secundaria (opcional)
  bg_color: "#151515"
  text_color: "#EAEAEA"
  accent_color: "#4A4A4A"
  title_size: 42
  subtitle_size: 24
  footer: "© Rommel Ayala - All rights reserved - (fecha de generacion)"
```

- Si no existe el `.yaml` o falta un campo → fallback a defaults globales.
- El `.md` no lleva frontmatter — contenido puro.

### `epub_generator/cover.py` — Generación de portadas
- Recibe un `BookConfig` y genera la portada usando Pillow.
- Usa los valores del bloque `cover:` del YAML.
- Guarda en `portadas_draft/{basename}.jpg`.
- Si ya existe una portada manual → la respeta, no la sobreescribe.
- Lógica extraída de `generate_minimal_covers.py`.

**Ejemplo visual del resultado para `claude-uso-maestro.yaml`:**
```
┌─────────────────────────────────────────┐
│                                         │
│                                         │
│                                         │
│     Claude: Uso Maestro                 │  ← title (42pt, #EAEAEA)
│       Guía Práctica                     │  ← subtitle (24pt, #EAEAEA)
│                                         │
│                                         │
│                                         │
│  ─────────────────────────              │  ← línea accent (#4A4A4A)
│  © Rommel Ayala - ARR - 16/03/2026      │  ← footer (16pt, #4A4A4A)
└─────────────────────────────────────────┘
  fondo: #151515 (600x800px)
```

### `epub_generator/generator.py` — Dispatcher
- Recibe `BookConfig` + ruta del archivo de entrada + portada + output.
- Inspecciona la extensión del input y delega al converter correspondiente:
  - `.md`  → `converters/markdown.py`
  - `.pdf` → `converters/pdf.py`
- Output: `epubs_generados/{basename}.epub` — sin timestamp. Git controla versiones.
- Devuelve éxito/error con mensaje unificado.
- **Open/Closed**: añadir un nuevo formato = nuevo módulo en `converters/` +
  una entrada en el dispatcher. El resto del sistema no cambia.

**Ejemplo del dispatcher (pseudocódigo):**
```python
CONVERTERS = {
    ".md":  convert_markdown,
    ".pdf": convert_pdf,
}

def generate(input_path: Path, config: BookConfig, cover: Path, output: Path) -> Result:
    ext = input_path.suffix.lower()
    converter = CONVERTERS.get(ext)
    if converter is None:
        return Result.error(f"Formato no soportado: {ext}")
    return converter(input_path, config, cover, output)
```

Añadir `.docx` en el futuro = una línea en `CONVERTERS` + un módulo nuevo. Nada más.

### `epub_generator/converters/markdown.py` — Pandoc
- Convierte `.md` → `.epub` con pandoc.
- Aplica metadata, ToC, cover, syntax highlighting.
- Ejecuta vía `subprocess.run`.

**Ejemplo del comando que construye internamente:**
```bash
pandoc libros_draft/claude-uso-maestro.md \
    --output=epubs_generados/claude-uso-maestro.epub \
    --to=epub3 \
    --toc --toc-depth=2 \
    --metadata title="Claude: Uso Maestro" \
    --metadata author="Rommel Ayala - QA Lead" \
    --metadata language="es-ES" \
    --epub-cover-image=portadas_draft/claude-uso-maestro.jpg \
    --syntax-highlighting=espresso
```

### `epub_generator/converters/pdf.py` — ebook-convert (Calibre)
- Convierte `.pdf` → `.epub` con `ebook-convert` de Calibre.
- Aplica metadata via flags CLI de Calibre (`--title`, `--authors`, `--language`,
  `--cover`, `--comments`).
- Ejecuta vía `subprocess.run`.
- **Limitación conocida**: asume PDFs con capa de texto (no escaneados).
  Los PDFs escaneados requieren OCR y quedan fuera de alcance.

**Ejemplo del comando que construye internamente:**
```bash
ebook-convert libros_draft/manual-legado.pdf \
    epubs_generados/manual-legado.epub \
    --title "Manual Legado" \
    --authors "Rommel Ayala - QA Lead" \
    --language "es-ES" \
    --cover portadas_draft/manual-legado.jpg \
    --comments "Migración del manual legado 2018"
```

---

## Ejemplo real — estructura y ejecución

**Estructura en `libros_draft/` con libros reales:**
```
libros_draft/
├── claude-uso-maestro.md          ← contenido markdown
├── claude-uso-maestro.yaml        ← metadata + cover config
├── agentes-ia-libro.md
├── agentes-ia-libro.yaml
├── manual-legado.pdf              ← PDF legado
└── manual-legado.yaml             ← metadata + cover para el PDF
```

**Ejemplo de output del comando `./generate_epub.sh` (todo en paralelo):**
```
🔧 venv OK, dependencias OK.
📚 Descubiertos 3 libros: 2 markdown, 1 PDF.
🚀 Procesando en paralelo...

[claude-uso-maestro]    🔄 Convirtiendo (.md → pandoc)...
[agentes-ia-libro]      🔄 Convirtiendo (.md → pandoc)...
[manual-legado]         🔄 Convirtiendo (.pdf → ebook-convert)...
[claude-uso-maestro]    🖼️  Portada generada desde YAML
[agentes-ia-libro]      🖼️  Portada manual detectada, respetada
[claude-uso-maestro]    ✅ epubs_generados/claude-uso-maestro.epub
[agentes-ia-libro]      ✅ epubs_generados/agentes-ia-libro.epub
[manual-legado]         ✅ epubs_generados/manual-legado.epub

✨ 3/3 libros generados en 4.2s
```

**Ejemplo de error parcial (un libro falla, el resto continúa):**
```
[claude-uso-maestro]    ✅ epubs_generados/claude-uso-maestro.epub
[agentes-ia-libro]      ❌ YAML inválido: agentes-ia-libro.yaml línea 7 (sintaxis)
[manual-legado]         ✅ epubs_generados/manual-legado.epub

⚠️  2/3 libros generados. Revisa los errores arriba.
```

---

## Flujo de ejecución

```
./generate_epub.sh [args]
        │
        ├── check pandoc        → sugiere instalación si falta
        ├── check ebook-convert → sugiere instalación si falta (solo si hay .pdf)
        ├── check venv          → crea e instala requirements.txt si falta
        └── python generate_epub.py [args]
                │
                ├── parse args
                ├── descubrir .md y .pdf files
                └── ThreadPoolExecutor (paralelo por libro)
                        │
                        ├── config.py    → lee {basename}.yaml → BookConfig
                        ├── cover.py     → genera portada desde BookConfig.cover
                        └── generator.py → dispatch por extensión
                                │
                                ├── .md  → converters/markdown.py (pandoc)
                                └── .pdf → converters/pdf.py (ebook-convert)
```

---

## Fases de implementación

### Fase 1 — Base funcional (esta iteración)
- [ ] `requirements.txt` (Pillow + PyYAML)
- [ ] `generate_epub.sh` actualizado (launcher + check pandoc + check calibre + venv)
- [ ] `epub_generator/config.py` — lectura de YAML sidecar con defaults
- [ ] `epub_generator/cover.py` — portada desde YAML `cover:`
- [ ] `epub_generator/generator.py` — dispatcher por extensión
- [ ] `epub_generator/converters/markdown.py` — pandoc wrapper
- [ ] `epub_generator/converters/pdf.py` — ebook-convert wrapper
- [ ] `generate_epub.py` — CLI + paralelismo + descubrimiento `.md`/`.pdf`
- [ ] Deprecar `generate_minimal_covers.py`
- [ ] `.gitignore` actualizado

### Fase 2 — Mejoras incrementales (próximas iteraciones)
- [ ] CSS personalizado por libro (inyectable via pandoc `--css`)
- [ ] Generación de PDF como **output** además de EPUB
- [ ] Soporte para `.docx` / `.html` como formatos de entrada adicionales
- [ ] Soporte para múltiples autores en metadata
- [ ] Output configurable (directorio destino)
- [ ] Modo `--dry-run` para validar sin generar

---

## Comportamiento de la CLI

```bash
# Todos los libros (.md + .pdf) en paralelo
./generate_epub.sh

# Libro markdown específico
./generate_epub.sh agentes-ia-libro.md

# Libro PDF específico
./generate_epub.sh manual-legado.pdf

# Libro específico con portada manual (precedencia sobre YAML)
./generate_epub.sh agentes-ia-libro.md mi_portada.jpg
```

---

## YAML mínimo recomendado por libro

```yaml
# libros_draft/mi-libro.yaml
title: "Título del Libro"
author: "Rommel Ayala - QA Lead"
language: "es-ES"
cover:
  title: "Título del Libro"
  subtitle: "Subtítulo opcional"
```

Sin `.yaml`, el libro se genera igualmente con los defaults globales.

---

## Revisión — puntos pendientes de resolver

Revisión del plan antes de implementar. Cada punto necesita decisión.

### 🔴 Críticos — resolver antes de codear

#### 1. Limpiar menciones obsoletas de "frontmatter"
Ya decidimos usar YAML sidecar (`libros_draft/{basename}.yaml`), pero el plan
todavía dice "frontmatter" en:
- Línea 32 (comentario del árbol de archivos)
- Línea 125 (checklist Fase 1)
- ~~Sección "Frontmatter mínimo recomendado"~~ (ya actualizada arriba)

**Decisión**: reemplazar todas las menciones por "YAML sidecar".

#### 2. `PyYAML` falta en `requirements.txt`
Solo se menciona Pillow, pero leer el `.yaml` requiere `PyYAML`.

**Decisión**: `requirements.txt` debe incluir al menos:
```
Pillow>=10.0.0
PyYAML>=6.0
```

#### 3. Fuentes cross-platform (bloqueante en Linux) ✅ RESUELTO
`generate_minimal_covers.py` usa `/System/Library/Fonts/Helvetica.ttc` (macOS).
En Linux eso no existe → revienta.

**Opciones**:
- (A) Incluir un `.ttf` libre en el repo (`fonts/Inter-Regular.ttf`, `Inter-Bold.ttf`)
- (B) Usar DejaVu Sans (`/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`)
- (C) Usar `fc-match` para encontrar una fuente del sistema en runtime

**Decisión final**: **(A) TTF libre en el repo**. Garantiza reproducibilidad
bit-a-bit entre máquinas (mismo binario de fuente en Mac y Linux → misma
portada). Coste: ~300KB en el repo. Fuente elegida: **Inter** (Regular + Bold)
por licencia OFL permisiva y legibilidad. Ubicación: `fonts/Inter-Regular.ttf`
y `fonts/Inter-Bold.ttf`. `cover.py` las carga por ruta relativa al proyecto.

#### 4. Dónde viven los defaults globales ✅ RESUELTO
El plan menciona "defaults globales" pero no dónde.

**Opciones**:
- (A) Hardcoded en `config.py` como constantes
- (B) `epub_generator/defaults.yaml` — archivo separado
- (C) Dataclass `BookConfig` con valores default en los fields

**Decisión final**: **(C) Dataclass con defaults en los fields**. Un solo lugar,
tipado fuerte, simple. Para cambiar un default → se edita una línea del
dataclass. Sin archivo YAML extra, sin constantes sueltas. Ya está bosquejado
en la sección `config.py` más arriba.

#### 5. Precedencia del segundo arg de portada manual ✅ RESUELTO
Línea del CLI: `./generate_epub.sh mi-libro.md mi_portada.jpg`

- (A) Eliminar el segundo arg — todo va por YAML
- (B) Mantenerlo con precedencia clara

**Decisión final**: **(B)**. Se mantiene el 2º argumento CLI para no romper el
uso actual y para facilitar pruebas rápidas de portadas sin editar el YAML.

**Cadena de precedencia (gana el primero que exista)**:
```
1. CLI arg (2º argumento)                  → ./generate_epub.sh libro.md mi.jpg
2. YAML: cover.image                       → campo opcional dentro del .yaml
3. Auto-discovery: portadas_draft/{basename}.jpg
4. Generada con Pillow desde cover:        → último recurso
```

#### 6. Herramienta para convertir PDF → EPUB ✅ RESUELTO
Pandoc **no** lee PDF nativamente. Opciones:
- (A) **`ebook-convert` de Calibre** — estándar de facto, alta calidad, maneja
  metadata y cover por flags CLI.
- (B) **`pdftotext` (poppler-utils) + pandoc** — ligero, pero calidad inferior.
- (C) **PyMuPDF (fitz)** — extracción programática, hay que escribir el extractor.

**Decisión final**: **(A) Calibre**. Battle-tested, diseñado exactamente para
esto, cumple 80-20. Dependencia asumida.

#### 7. PDFs escaneados (sin capa de texto) ✅ RESUELTO
Un PDF escaneado es una colección de imágenes. Sin OCR, no se puede convertir.
- (A) **No soportar** — fallar con mensaje claro.
- (B) **Integrar OCR** — Tesseract vía `ocrmypdf`.

**Decisión final**: **(A) No soportar en Fase 1**. El converter PDF falla con
mensaje claro si el PDF no tiene capa de texto. OCR queda para una futura fase
solo si aparece la necesidad real.

#### 8. Colisión de basename entre `.md` y `.pdf` ✅ RESUELTO
¿Qué pasa si existen `mi-libro.md` y `mi-libro.pdf` en `libros_draft/`?

**Decisión final**: **no es responsabilidad del CLI**. El usuario garantiza que
no habrá dos archivos con el mismo basename y distinta extensión. El
descubrimiento en `generate_epub.py` procesa ambos como libros independientes
(el último en terminar pisa al otro en disco). Documentado como precondición
en el README.

---

### 🟡 Importantes — impactan UX o robustez

#### 6. Logging con threads
`ThreadPoolExecutor` + `print()` mezcla outputs paralelos.

**Decisión**: usar `logging.Logger` con formato `[{book_name}] {message}` para
que cada línea se identifique con su libro origen.

#### 7. Sudo en el launcher
`apt install pandoc` requiere sudo. El bash debe:
- Detectar si pandoc falta
- Si falta, imprimir el comando exacto (`sudo apt install pandoc`) y salir con error claro
- **No** ejecutar sudo automáticamente (sorpresas malas)

**Decisión**: el bash detecta y sugiere, no instala automáticamente. El venv
Python sí se crea solo (no requiere sudo).

#### 8. Path del venv y `.gitignore`
- Venv en `.venv/` (convención estándar Python)
- `.gitignore` debe incluir: `.venv/`, `__pycache__/`, `*.pyc`, `.DS_Store`
- `epubs_generados/` **sí** entra a git (git controla versiones)
- `portadas_draft/*.jpg` generadas **sí** entran a git (reproducibilidad)

#### 9. Error handling del YAML
Si un `.yaml` tiene sintaxis mal:
- **Decisión**: fallar solo ese libro con mensaje claro (`[mi-libro] ❌ YAML inválido: línea X`), continuar con el resto del batch.

#### 10. Text wrapping en portadas
Si el título es largo, Pillow no hace wrap automático → se sale de la portada.

**Decisión**: usar `textwrap.wrap()` con ancho máximo calculado por el `title_size`
y el width del canvas.

#### 11. UX del CLI — formato del argumento
¿Acepta con o sin extensión? ¿Acepta path absoluto?

**Decisión**: aceptar ambos:
- `./generate_epub.sh mi-libro` → busca `mi-libro.md`
- `./generate_epub.sh mi-libro.md` → igual
- `./generate_epub.sh libros_draft/mi-libro.md` → igual

Normalizar a basename internamente.

---

### 🟢 Nice-to-have — Fase 2 o posterior

#### 12. Tests con pytest
Tests unitarios de `config.py` (parse YAML + defaults) y `cover.py` (genera
imagen válida). `generator.py` es harder to test (depende de pandoc), skip.

#### 13. Caching / detección de cambios
Regenerar solo si el `.md` o el `.yaml` cambió. Usar mtime o hash. Para 7 libros
no es crítico; mencionado como decisión consciente: **por ahora regeneramos todo**.

#### 14. Logging a archivo
`logs/generate-{timestamp}.log` para post-mortem en ejecuciones paralelas.

#### 15. Modo `--dry-run` y `--verbose`
Ya mencionado en Fase 2. Añadir también `--verbose` para debug.

---

## Checklist de decisiones pendientes

Antes de empezar Fase 1, resolver:

- [x] #3 — Fuentes Inter (TTF libre en `fonts/`) para reproducibilidad cross-platform
- [x] #4 — Defaults en dataclass (C)
- [x] #5 — Precedencia de portada: CLI > YAML > auto-discovery > generada (B)
- [x] #6 — Calibre (`ebook-convert`) como herramienta PDF→EPUB
- [x] #7 — PDFs escaneados fuera de alcance en Fase 1
- [x] #8 — Colisión de basename: responsabilidad del usuario
- [x] Los demás puntos 🔴 son mecánicos, no requieren decisión del usuario

**Todas las decisiones críticas resueltas → Fase 1 lista para codear.**
