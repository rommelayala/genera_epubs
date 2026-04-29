---
name: US-005-LocalCompilationComplete
description: Documentación de compilación de archivos locales con validación temprana
type: project
---

**Fact:** `compile_book()` en `epub_generator/compiler.py` ahora soporta compilación de archivos locales (markdown, pdf).

**Why:** US-005 completado - `compile_book()` implementado con:
- Validación temprana de fuentes (tipo, path existente)
- Manejo de errores con parámetros skip/abort
- Carga dinámica de ingestors
- Compilación en lote con progreso

**How to apply:** 
- `compile_book(config, output_name, project_root, on_error="skip")`
- Soporte para: markdown, pdf, url (future)
- Validación fallará antes de intentar compilar si hay fuentes inválidas
- Errores en una fuente no detienen la compilación si `on_error="skip"`

**Completion:** 2026-05-24 - 10/10 tests passing