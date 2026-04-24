# Troubleshooting y FAQs

## Problemas Comunes

### ❌ "pandoc: command not found"

**Causa:** Pandoc no instalado.

**Solución:**
```bash
# macOS
brew install pandoc

# Linux (Debian/Ubuntu)
sudo apt update && sudo apt install pandoc

# Linux (Fedora)
sudo dnf install pandoc

# Verificar
pandoc --version
```

---

### ❌ "ebook-convert: command not found"

**Causa:** Calibre no instalado (solo se requiere si hay PDFs en `libros_draft/`).

**Solución:**
```bash
# macOS
brew install --cask calibre

# Linux (Debian/Ubuntu)
sudo apt install calibre

# Verificar
ebook-convert --version
```

---

### ❌ "ffmpeg/ffprobe: command not found"

**Causa:** FFmpeg no instalado (solo para audiolibros).

**Solución:**
```bash
# macOS
brew install ffmpeg

# Linux (Debian/Ubuntu)
sudo apt install ffmpeg

# Linux (Fedora)
sudo dnf install ffmpeg

# Verificar (debería mostrar ambos)
ffmpeg -version
ffprobe -version
```

---

### ❌ EPUB generado sin estilos CSS

**Síntomas:** El EPUB se ve con formato por defecto, sin tipografía personalizada.

**Causa:** Archivo `epub_generator/styles/epub.css` no existe o no se pasó a pandoc.

**Solución:**
```bash
# 1. Verificar que el archivo existe
ls -l epub_generator/styles/epub.css

# 2. Si no existe, regenerar (usar primer story de Ralph)
# O crear manualmente desde plantilla

# 3. Verificar que pandoc lo usa (revisar logs o comando)
pandoc input.md --css=epub_generator/styles/epub.css --to=epub3 -o output.epub
```

---

### ❌ "No se encontró: agentes-ia-libro"

**Síntomas:** El CLI no encuentra el archivo.

**Causa:** El archivo no existe en `libros_draft/`.

**Solución:**
```bash
# Verificar qué libros existen
ls libros_draft/*.md libros_draft/*.pdf

# Procesar todos (sin especificar nombre)
./generate_epub.sh

# O especificar ruta completa
./generate_epub.sh libros_draft/agentes-ia-libro.md
```

---

### ❌ M4B sin chapter markers

**Síntomas:** `ffprobe -show_chapters libro.m4b` no muestra `[CHAPTER]` entries.

**Causa:**
1. FFmpeg versión antigua (no soporta metadata mapping)
2. `_generate_chapter_metadata()` falló silenciosamente
3. Comando ffmpeg incorrecto

**Solución:**
```bash
# 1. Verificar ffmpeg version (debe ser >= 4.3)
ffmpeg -version | head -1

# 2. Verificar que el archivo de metadata se generó
cat audios_generados/libro_chapters/metadata.txt

# 3. Si está malformado, verificar logs en stderr
# Regenerar con --no-cache para ver logs completos
./generate_epub.sh --format audio --no-cache libro

# 4. Probar ffmpeg manualmente
ffmpeg -i concat.txt -i metadata.txt -i cover.jpg \
  -map 0:a -map 2:v -c:v mjpeg -disposition:v attached_pic \
  -map_metadata 1 -c:a aac -b:a 96k output.m4b
```

---

### ❌ M4B sin portada embebida

**Síntomas:** La portada no aparece en Apple Books o Audiobookshelf.

**Causa:**
1. Portada no existe
2. FFmpeg no embebió la imagen
3. Formato de imagen no soportado

**Solución:**
```bash
# 1. Verificar que la portada existe
ls portadas_draft/libro.jpg

# 2. Si no existe, está en un .yaml
# Verificar YAML sidecar
cat libros_draft/libro.yaml

# 3. Regenerar con --no-cache (verbose logging)
./generate_epub.sh --format audio --no-cache libro

# 4. Probar ffmpeg manualmente con JPG
ffmpeg -i cover.jpg -i audio.m4b -map 1:a -map 0:v \
  -c:v mjpeg -disposition:v attached_pic output.m4b

# 5. Probar ffmpeg manualmente con PNG
ffmpeg -i cover.png -i audio.m4b -map 1:a -map 0:v \
  -c:v png -disposition:v attached_pic output.m4b
```

---

### ❌ Audiolibro muy lento de generar

**Síntomas:** M4B tarda 30+ minutos para 20 capítulos.

**Causa:** `concurrency` demasiado bajo o edge-tts throttling.

**Solución:**
```bash
# 1. Aumentar concurrencia en YAML
# libros_draft/libro.yaml
audio:
  concurrency: 8  # aumentar de 5 a 8

# 2. O desde CLI (no hay opción, requiere YAML)

# 3. Verificar que no hay throttling en logs
# (buscar "429", "Too Many Requests")

# 4. Probar generar menos capítulos primero
# Editar libro.md temporalmente para tener solo 3-5 capítulos
# Generar y verificar que funciona rápido
# Luego restaurar y generar completo
```

---

### ❌ "Capítulo 'X' vacío tras limpiar — omitido"

**Síntomas:** Un capítulo no se narra, se ve warning en logs.

**Causa:** El contenido del capítulo es solo markdown (código, tablas) que se elimina al limpiar.

**Solución:**
```bash
# 1. Verificar contenido del capítulo en markdown
cat libros_draft/libro.md | grep -A 20 "# Capítulo X"

# 2. Agregar texto narrativo además del código/tabla
# Antes:
## Ejemplo de código
\`\`\`python
def foo():
    pass
\`\`\`

# Después:
## Ejemplo de código
A continuación mostramos una función simple:

\`\`\`python
def foo():
    pass
\`\`\`

Para ver el código completo, consulta el EPUB.
```

---

### ❌ Cache "roto" — siempre re-narra

**Síntomas:** Aunque no cambió el contenido, siempre re-narra todos los capítulos.

**Causa:**
1. Archivo `cache_manifest.json` corrupto o malformado
2. Hash incorrecto
3. Flag `--no-cache` activado accidentalmente

**Solución:**
```bash
# 1. Inspeccionar cache
cat audios_generados/libro_chapters/cache_manifest.json | python -m json.tool

# 2. Si está malformado, eliminarlo
rm audios_generados/libro_chapters/cache_manifest.json

# 3. Regenerar con --no-cache (fuerza re-narración)
./generate_epub.sh --format audio --no-cache libro

# 4. En próxima generación, el cache se reconstruirá desde cero
./generate_epub.sh --format audio libro
```

---

### ❌ YAML sidecar no se lee

**Síntomas:** El YAML existe pero la configuración no se aplica.

**Causa:**
1. Nombre incorrecto (debe ser `{basename}.yaml`)
2. YAML syntax error
3. Ruta incorrecta

**Solución:**
```bash
# 1. Verificar nombre — debe coincidir exactamente con markdown
# Markdown: libros_draft/agentes-ia-libro.md
# YAML:    libros_draft/agentes-ia-libro.yaml  ✓
# YAML:    libros_draft/agentes-ia-libros.yaml ✗ (plural)

# 2. Validar YAML syntax
python -c "import yaml; yaml.safe_load(open('libros_draft/libro.yaml'))" && echo "OK" || echo "ERROR"

# 3. Ver qué config se cargó (añadir print en código)
# Alternativa: check logs cuando se genera

# 4. Verificar que no hay BOM UTF-8
hexdump -C libros_draft/libro.yaml | head
# Si ves "ef bb bf", eliminar BOM:
python -c "open('libros_draft/libro.yaml', 'w').write(open('libros_draft/libro.yaml', 'r').read())"
```

---

### ❌ Generación muy lenta en macOS con M1/M2

**Síntomas:** Pandoc o FFmpeg tardan 2-3x más que en Linux.

**Causa:** Compilación universal binary (x86 + ARM). Depende de cómo se instaló.

**Solución:**
```bash
# 1. Verificar arquitectura
uname -m  # arm64 = M1/M2, x86_64 = Intel

# 2. Reinstalar con brew (ARM nativo)
brew install pandoc
brew install ffmpeg

# 3. Verificar que se instaló ARM nativo
file /usr/local/bin/pandoc
# Debe decir "Mach-O 64-bit executable arm64"
```

---

## FAQs

### P: ¿Puedo usar Markdown con frontmatter en lugar de YAML sidecar?

**R:** Actualmente no. Pandoc puede leer frontmatter, pero `load_config()` busca un archivo `.yaml` separado.

**Workaround:**
```yaml
# libros_draft/libro.yaml — copia la metadata aquí
title: "Título"
author: "Autor"
```

**Mejora futura:** Leer frontmatter del markdown como fallback.

---

### P: ¿Cómo agrego múltiples voces dentro de un capítulo (diálogos)?

**R:** No está soportado actualmente. La voz es global para todo el audiolibro.

**Workaround:** Usar un único narrador. Los lectores pueden usar la velocidad variable del reproductor.

**Mejora futura:** Marcar diálogos con tags especiales (`[SPEAKER: Anna]`) y asignarles voces.

---

### P: ¿Puedo agregar música de fondo o jingles?

**R:** No está soportado actualmente. El M4B es solo audio de voz.

**Workaround:** Generar el M4B y luego editarlo manualmente en Audacity o software similar.

**Mejora futura:** Soportar `audio.intro_music` y `audio.outro_music` con archivos pre-grabados.

---

### P: ¿Soporta PDF escaneado (sin capa de texto)?

**R:** No. PDFs deben tener capa de texto OCR.

**Workaround:**
```bash
# Usar Tesseract para OCR
tesseract input-scanned.pdf output.txt -l spa
# Luego copiar texto a markdown

# O usar Calibre con OCR
# Pero eso requiere manual tweak
```

---

### P: ¿Cómo integro esto en CI/CD?

**R:** El script `generate_epub.sh` es agnóstico a CI/CD. Ejemplos:

**GitHub Actions:**
```yaml
name: Generate Books
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install deps
        run: |
          sudo apt install pandoc calibre ffmpeg
      - name: Generate
        run: ./generate_epub.sh
      - name: Upload
        uses: actions/upload-artifact@v2
        with:
          name: books
          path: |
            epubs_generados/
            audios_generados/
```

---

### P: ¿Puedo distribuir los EPUBs en Amazon KDP?

**R:** Parcialmente. Amazon requiere revisión. Algunos puntos:
- EPUB debe estar bien formado (pasar EPUBCheck)
- Metadata correcta (title, author, ISBN opcional)
- Imágenes embebidas correctamente

**Mejora futura:** Agregar validación con EPUBCheck.

---

### P: ¿Cómo cambio la voz del audiolibro?

**R:** En el YAML sidecar:
```yaml
audio:
  voice: "es-MX-JorgeNeural"  # cambia a voz mexicana
```

O dejar vacío para auto-detectar por idioma:
```yaml
audio:
  voice: ""  # usa es-ES-AlvaroNeural
```

**Voces disponibles:**
- `es-ES-AlvaroNeural` (español de España)
- `es-MX-JorgeNeural` (español de México)
- `en-US-GuyNeural` (inglés americano)
- `en-GB-RyanNeural` (inglés británico)

---

### P: ¿Cómo ajusto la velocidad de narración?

**R:** En el YAML sidecar:
```yaml
audio:
  rate: "-10%"  # más lento
  rate: "-5%"   # default (recomendado)
  rate: "+0%"   # velocidad natural
  rate: "+10%"  # más rápido
```

---

### P: ¿Los audiolibros generados tienen derechos de autor?

**R:** Los archivos M4B no tienen protección DRM. Son tuyos para distribuir como quieras.

**Nota:** Asegúrate de tener derechos sobre el contenido del markdown antes de distribuir.

---

### P: ¿Puedo generar sin internet (offline)?

**R:**
- **EPUB:** Sí, completamente offline (pandoc + pillow locales).
- **Audiolibro:** No, requiere edge-tts que es nube.

**Alternativa offline para audio:** Usar TTS local (piper, espeak), pero requiere cambiar código.

---

## Debugging

### Habilitar verbose logging

**Opción 1:** Editar el nivel de logging en `generate_epub.py`:
```python
logging.basicConfig(format="%(message)s", level=logging.DEBUG)  # cambiar de INFO a DEBUG
```

**Opción 2:** Ejecutar Python directamente con logging:
```bash
PYTHONUNBUFFERED=1 python -u generate_epub.py agentes-ia-libro --format audio 2>&1 | tee output.log
```

---

### Inspeccionar archivos temporales

Los archivos temp (silence.mp3, concat.txt, metadata.txt) se eliminan después de `_assemble_m4b()`.

Para debuggear, comentar las líneas de cleanup:
```python
# silence_file.unlink(missing_ok=True)  ← comentar
# concat_file.unlink(missing_ok=True)   ← comentar
# metadata_file.unlink(missing_ok=True) ← comentar
```

Después revisar los archivos en `audios_generados/`:
```bash
cat audios_generados/concat.txt
cat audios_generados/metadata.txt
ls -lh audios_generados/silence.mp3
```

---

### Verificar salida de conversor

Cada convertidor (`pandoc`, `ebook-convert`, `ffmpeg`) puede fallar silenciosamente.

En `audio.py`, cambiar línea:
```python
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print("STDOUT:", result.stdout)  ← agregar esto
    print("STDERR:", result.stderr)  ← agregar esto
    log.warning(...)
```

Así ves el error exacto.

---

## Reportar Bugs

Si encuentras un bug:

1. **Reproducir:** Paso a paso para recrear el problema
2. **Contexto:** OS (macOS/Linux), versiones de herramientas
3. **Logs:** Output completo (usa `2>&1 | tee logs.txt`)
4. **Espectativa vs. Realidad:** Qué esperabas vs. qué pasó

Incluir en reporte:
```bash
# Versions
pandoc --version | head -1
ebook-convert --version 2>/dev/null || echo "Calibre not installed"
ffmpeg -version | head -1
ffprobe -version | head -1
python --version

# Logs
./generate_epub.sh --format audio libro 2>&1
```
