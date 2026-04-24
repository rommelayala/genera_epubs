# Genera Ebook (Cursos y Libros)

Skill para estructurar e iterar la creación de cursos y libros en formato Markdown, optimizados para el conversor local a EPUB de AIQ®. Genera un libro-curso completo en formato EPUB (y opcionalmente audiolibro M4B) desde cero o desde un borrador existente.

## Proceso

### 1. Analizar la petición

Lee el tema o concepto solicitado en $ARGUMENTS. Si es un tema nuevo, elabora un índice (ToC) sólido que progrese de lo básico al nivel experto antes de escribir. Si ya existe un borrador en `libros_draft/`, léelo primero.

### 2. Generar o actualizar el contenido Markdown

**Reglas de cabeceras (CRÍTICO — Pandoc las usa para el TOC):**
- `#` = Capítulos o partes principales
- `##` = Subtemas dentro de un capítulo
- `###` = Secciones dentro de un subtema
- NUNCA saltar niveles de jerarquía
- NUNCA usar `#` para el título del libro (va en el YAML)

**Estilo AIQ / Rommel Ayala:**
- Tono cercano, riguroso, de tú a tú (nivel CTO/Tech Lead)
- Sin lenguaje corporativo ni muletillas de IA
- Filosofía "No-BS": menos palabras, más impacto
- Framework 5W1H y regla 80-20
- Claridad visual: listas, negrillas, tablas, diagramas ASCII

**Restricciones de Markdown:**
- Solo Markdown estándar — cero tags HTML
- Bloques de código con triple backtick + lenguaje
- Tablas de Markdown para datos comparativos
- Horizontal rules `---` solo como separador visual

**Guardar en:** `libros_draft/{nombre-del-libro}.md` (kebab-case)

### 3. Generar el YAML sidecar

Crear `libros_draft/{nombre-del-libro}.yaml` con TODOS los campos:

```yaml
title: "Título Completo del Libro"
author: "Rommel Ayala"
description: "Descripción breve del contenido"
language: "es-ES"
date: "Fehca de generacion"
cover:
  title: "Título Corto para Portada"
  subtitle: "Subtítulo"
```

### 4. Generar el EPUB

Ejecutar:
```bash
./generate_epub.sh {nombre-del-libro}
```

Verificar que:
- El EPUB se generó en `epubs_generados/`
- La portada se ve correcta
- El TOC tiene la estructura esperada
- La numeración de páginas aparece (ej: `2/40`)

### 5. (Opcional) Generar audiolibro

Si el usuario lo pide:
```bash
./generate_epub.sh --format audio {nombre-del-libro}
```

Para configurar la voz/velocidad, agregar sección `audio:` al YAML:
```yaml
audio:
  voice: ""           # auto por idioma
  rate: "-5%"         # ligeramente lento
  intro: true         # narrar intro automático
  outro: true         # narrar outro automático
```

### 6. Verificar resultado

- Abrir el EPUB en un lector (Apple Books, Calibre)
- Verificar numeración de páginas
- Verificar TOC interactivo
- Si es audiolibro, verificar chapter markers con: `ffprobe -show_chapters audios_generados/{nombre}.m4b`

## Ejemplo de uso

```
/genera-ebook playwright-ts-avanzado
/genera-ebook "Guía completa de testing con Cypress"
/genera-ebook actualizar agentes-ia-libro
```

## Convenciones de Nombres

- Markdown: `libros_draft/{kebab-case}.md`
- YAML: `libros_draft/{kebab-case}.yaml`
- Portada: `portadas_draft/{kebab-case}.jpg`
- EPUB: `epubs_generados/{kebab-case}.epub`
- M4B: `audios_generados/{kebab-case}.m4b`
