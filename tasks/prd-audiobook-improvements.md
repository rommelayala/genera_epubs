# PRD: Mejoras Completas al Sistema de Audiolibros

## Introduction

El sistema actual genera audiolibros desde markdown usando edge-tts, pero lo hace de forma secuencial, sin chapter markers en M4B, sin portada embebida, sin limpieza adecuada del texto para TTS y sin configurabilidad. Esta mejora transforma el generador de audiolibros de un prototipo funcional a un producto de calidad profesional comparable con audiolibros comerciales.

Archivos base:
- `epub_generator/converters/audio.py` — converter principal
- `epub_generator/preprocessors/markdown_cleaner.py` — limpieza de texto para TTS
- `epub_generator/config.py` — configuracion BookConfig/CoverConfig
- `generate_epub.py` — CLI entry point

## Goals

- Reducir el tiempo de generacion de audiolibros paralelizando la sintesis TTS (target: 3-5x mas rapido)
- Generar M4B con chapter markers navegables en reproductores (Apple Books, Audiobookshelf, VLC)
- Embeber portada del libro en el archivo M4B
- Producir audio limpio sin artefactos de markdown, emojis, URLs o frontmatter
- Permitir configuracion de voz, velocidad, volumen y pitch por libro via YAML
- Implementar cache por capitulo para evitar re-narrar contenido sin cambios
- Agregar intro/outro narrado automatico para toque profesional

## User Stories

### US-001: Paralelizar sintesis TTS con asyncio.gather
**Description:** Como usuario, quiero que los capitulos se narren en paralelo para que un libro de 20 capitulos no tarde 20x lo que tarda uno solo.

**Acceptance Criteria:**
- [ ] Reemplazar el loop secuencial con `asyncio.run()` por capitulo por un unico `asyncio.run()` que ejecute `asyncio.gather()` con todas las tareas
- [ ] Usar `asyncio.Semaphore(5)` como default para no saturar edge-tts (configurable)
- [ ] Mostrar progreso en log: "Narrando capitulo X de N"
- [ ] Si un capitulo falla, los demas continuan y se reporta el error al final
- [ ] Typecheck passes

### US-002: Chapter markers reales en M4B
**Description:** Como oyente, quiero navegar entre capitulos en mi reproductor de audiolibros para saltar a secciones especificas.

**Acceptance Criteria:**
- [ ] Generar archivo de metadata ffmpeg con entries `[CHAPTER]` que incluyan `TIMEBASE=1/1000`, `START`, `END` y `title` por capitulo
- [ ] Calcular duracion de cada MP3 con ffprobe para determinar los timestamps de inicio/fin
- [ ] Pasar `-i metadata.txt -map_metadata 1` al comando ffmpeg de ensamblado
- [ ] Verificar que VLC o ffprobe muestra los capitulos correctamente
- [ ] Typecheck passes

### US-003: Portada embebida en M4B
**Description:** Como oyente, quiero ver la portada del libro en mi reproductor de audiolibros.

**Acceptance Criteria:**
- [ ] El parametro `cover` (actualmente ignorado con `_cover`) se usa en `_assemble_m4b`
- [ ] Pasar la portada a ffmpeg con `-i cover.jpg -map 0:a -map 1:v -c:v mjpeg -disposition:v attached_pic`
- [ ] Si la portada no existe o no es JPG/PNG, omitir sin error (warning en log)
- [ ] Verificar que Apple Books / Audiobookshelf muestra la portada
- [ ] Typecheck passes

### US-004: Pausas entre capitulos
**Description:** Como oyente, quiero pausas naturales entre capitulos para que la transicion no sea abrupta.

**Acceptance Criteria:**
- [ ] Insertar silencio de 1.5 segundos (default) entre capitulos al ensamblar el M4B
- [ ] Usar ffmpeg `anullsrc` para generar el silencio, o insertar un archivo de silencio pre-generado
- [ ] Duracion del silencio configurable via YAML: `audio.chapter_pause` (default: 1.5 segundos)
- [ ] Las pausas se reflejan correctamente en los chapter markers (no desplazan los timestamps)
- [ ] Typecheck passes

### US-005: Limpiar frontmatter YAML del texto antes de TTS
**Description:** Como oyente, no quiero escuchar "guion guion guion title dos puntos..." al inicio del libro.

**Acceptance Criteria:**
- [ ] Detectar y eliminar bloque YAML frontmatter (`---\n...\n---`) al inicio del markdown antes de extraer capitulos
- [ ] Agregar regex en `clean_for_tts()` o como paso previo en `extract_chapters()`
- [ ] No afectar el contenido que usa `---` como separador horizontal (solo el frontmatter al inicio)
- [ ] Typecheck passes

### US-006: Limpiar emojis y caracteres especiales para TTS
**Description:** Como oyente, no quiero que el narrador diga "cara sonriente" o caracteres unicode raros.

**Acceptance Criteria:**
- [ ] Eliminar emojis unicode del texto antes de TTS (regex para rangos emoji)
- [ ] Eliminar caracteres especiales que no aportan a la narracion: flechas unicode, bullets decorativos, etc.
- [ ] Preservar caracteres hispanicos (tildes, ene, signos de interrogacion/exclamacion invertidos)
- [ ] Agregar al modulo `markdown_cleaner.py`
- [ ] Typecheck passes

### US-007: Limpiar URLs sueltas para TTS
**Description:** Como oyente, no quiero que el narrador deletree "hache te te pe ese dos puntos barra barra..."

**Acceptance Criteria:**
- [ ] Detectar URLs sueltas (no envueltas en sintaxis markdown `[texto](url)`) con regex
- [ ] Reemplazar por "enlace disponible en el libro en formato epub" o simplemente eliminar
- [ ] No afectar URLs que ya estan dentro de links markdown (esas ya se limpian por la regex de links existente)
- [ ] Agregar al modulo `markdown_cleaner.py`
- [ ] Typecheck passes

### US-008: Configuracion de audio por libro via YAML
**Description:** Como autor, quiero configurar la voz, velocidad, volumen y pitch del audiolibro desde el YAML sidecar de cada libro.

**Acceptance Criteria:**
- [ ] Agregar `AudioConfig` dataclass en `config.py` con campos: `voice` (default: auto por idioma), `rate` (default: "-5%"), `volume` (default: "+0%"), `pitch` (default: "+0Hz"), `chapter_pause` (default: 1.5), `concurrency` (default: 5)
- [ ] Agregar campo `audio: AudioConfig` en `BookConfig` con `field(default_factory=AudioConfig)`
- [ ] Parsear seccion `audio:` del YAML sidecar en `load_config()`
- [ ] `audio.py` lee estos valores y los pasa a `edge_tts.Communicate(text, voice, rate=rate, volume=volume, pitch=pitch)`
- [ ] Si `audio.voice` esta vacio, usar el mapeo automatico por idioma existente (`SUPPORTED_VOICES`)
- [ ] Defaults siguen best practices: rate ligeramente lento para comprension, volumen neutro, pitch neutro
- [ ] Documentar los campos en README.MD
- [ ] Typecheck passes

### US-009: Cache por capitulo
**Description:** Como usuario, quiero que al re-generar un audiolibro tras editar un solo capitulo, solo se re-narre ese capitulo y no los 20.

**Acceptance Criteria:**
- [ ] Crear archivo `{chapters_dir}/cache_manifest.json` que mapee `{filename: {hash: sha256, duration_ms: int}}`
- [ ] Antes de narrar un capitulo, calcular SHA-256 del texto limpio (post `clean_for_tts`)
- [ ] Si el hash coincide con el del manifiesto Y el archivo MP3 existe, saltar la narracion
- [ ] Si el hash no coincide o el MP3 no existe, narrar y actualizar el manifiesto
- [ ] Log informativo: "Capitulo X sin cambios, usando cache" vs "Capitulo X modificado, re-narrando"
- [ ] Si se pasa `--no-cache` en CLI, ignorar el manifiesto y re-narrar todo
- [ ] Agregar argumento `--no-cache` a `argparse` en `generate_epub.py`
- [ ] Typecheck passes

### US-010: Intro y outro narrados automaticos
**Description:** Como oyente, quiero que el audiolibro comience con "Este es el libro X, escrito por Y" y termine con un cierre, como un audiolibro profesional.

**Acceptance Criteria:**
- [ ] Generar texto de intro automatico: "Este es el audiolibro: {title}. Escrito por {author}. {description}"
- [ ] Generar texto de outro automatico: "Fin del audiolibro: {title}. Gracias por escuchar."
- [ ] Narrar intro y outro como capitulos especiales (00_intro.mp3 y 99_outro.mp3)
- [ ] Incluir intro y outro en los chapter markers del M4B con titulos "Introduccion" y "Cierre"
- [ ] Configurable via YAML: `audio.intro` (default: true), `audio.outro` (default: true)
- [ ] Si `audio.intro` o `audio.outro` es false, omitir
- [ ] Typecheck passes

### US-011: Requerir ffmpeg para formato audio
**Description:** Como usuario, quiero un error claro al inicio si ffmpeg no esta instalado, en lugar de que falle a mitad del proceso.

**Acceptance Criteria:**
- [ ] Verificar que `ffmpeg` y `ffprobe` estan en PATH al inicio de `convert_audio()`
- [ ] Si no estan disponibles, lanzar error claro: "ffmpeg y ffprobe son requeridos para generar audiolibros. Instala con: brew install ffmpeg / sudo apt install ffmpeg"
- [ ] Agregar check de ffmpeg en `generate_epub.sh` (similar al check de pandoc/calibre)
- [ ] Typecheck passes

### US-012: Subir bitrate default a 96k
**Description:** Como oyente, quiero calidad de audio adecuada para voz hablada.

**Acceptance Criteria:**
- [ ] Cambiar bitrate de AAC de 64k a 96k en `_assemble_m4b`
- [ ] Hacer bitrate configurable via `audio.bitrate` (default: "96k")
- [ ] Agregar campo `bitrate` a `AudioConfig`
- [ ] Typecheck passes

## Functional Requirements

- FR-1: `convert_audio()` debe verificar ffmpeg/ffprobe al inicio y fallar con error descriptivo si no estan disponibles
- FR-2: La sintesis TTS debe ejecutarse en paralelo con `asyncio.gather()` y semaforo configurable (default: 5)
- FR-3: El M4B resultante debe contener chapter markers con timestamps correctos, navegables en reproductores estandar
- FR-4: La portada del libro debe embeberse como `attached_pic` en el M4B
- FR-5: Debe haber silencio configurable (default 1.5s) entre capitulos
- FR-6: El texto debe limpiarse de: frontmatter YAML, emojis, URLs sueltas, caracteres decorativos unicode
- FR-7: Voz, velocidad, volumen, pitch, bitrate y pausas deben ser configurables por libro via seccion `audio:` del YAML sidecar
- FR-8: Los capitulos narrados deben cachearse por hash SHA-256 del texto limpio, con manifiesto JSON
- FR-9: El audiolibro debe incluir intro y outro narrados automaticamente (desactivables)
- FR-10: El bitrate default de AAC debe ser 96k

## Non-Goals

- No se implementa streaming de audio en tiempo real
- No se soporta multiples voces alternando dentro de un mismo capitulo (ej: dialogos)
- No se genera DAISY ni otros formatos de accesibilidad
- No se agrega musica de fondo ni efectos de sonido
- No se soporta input PDF para audio (solo markdown)
- No se implementa interfaz grafica ni web

## Technical Considerations

- **edge-tts** es gratuito pero tiene rate limiting implicito — el semaforo de concurrencia (default 5) previene saturacion
- **ffprobe** es necesario para calcular duraciones de MP3 y generar chapter markers correctos
- El formato de metadata de capitulos de ffmpeg usa `TIMEBASE=1/1000` con `START`/`END` en milisegundos
- Para portada embebida en M4B: ffmpeg requiere `-c:v mjpeg` para JPG o `-c:v png` para PNG con `-disposition:v attached_pic`
- El cache usa SHA-256 del texto post-limpieza, no del markdown original (asi cambios cosmeticos en markdown que no afectan la narracion no invalidan el cache)
- `AudioConfig` defaults basados en best practices de audiolibros: rate="-5%" (ligeramente mas lento que natural para comprension), volume="+0%", pitch="+0Hz", bitrate="96k", chapter_pause=1.5

## Success Metrics

- Generacion de audiolibro de 20 capitulos tarda menos de 5 minutos (vs 15+ actual)
- M4B navegable por capitulos en al menos 2 reproductores (VLC + Apple Books/Audiobookshelf)
- Portada visible en reproductor al abrir el M4B
- Re-generacion con 1 capitulo editado tarda menos de 30 segundos (cache hit en los otros 19)
- Audio limpio: cero instancias de frontmatter, emojis o URLs narradas

## Open Questions

- Ninguna — todas las decisiones fueron tomadas con el usuario.
