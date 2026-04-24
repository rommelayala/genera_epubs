# Numeración de Páginas en EPUB

A partir de v2.1, los EPUBs generados incluyen numeración de páginas en formato `página_actual/total_páginas` (ej: `2/40`).

## Cómo funciona

### Proceso

1. **Pandoc genera el EPUB** con estructura HTML estándar
2. **Post-procesador analiza** los archivos HTML dentro del EPUB (que es un ZIP)
3. **Cuenta total de páginas** basado en número de archivos HTML de contenido
4. **Inyecta un `<div class="page-number">` en cada página con el número**
5. **Agrega CSS** para estilizar los números (centrados, gris claro, borde superior)
6. **Reempaqueta el EPUB** con los cambios

### Apariencia

```
┌─────────────────────────────┐
│                             │
│    Contenido de la página   │
│                             │
│                             │
│                             │
│───────────────────────────── │
│         2/40                │  ← pie de página con numeración
└─────────────────────────────┘
```

**Estilos CSS:**
- Fuente: 0.9em, cursiva, gris (#999)
- Posición: centrado, con border-top (#eee)
- Margen: separado del contenido

---

## Configuración

### Activar/Desactivar

Actualmente está **activado por defecto** para todos los EPUBs. Para desactivar, comentar la línea en `converters/markdown.py`:

```python
# Post-process: add page numbers (e.g., "2/40")
# add_page_numbers(output)  ← comentar para desactivar
```

### Personalizar estilos

Editar CSS en `postprocessors/page_numbering.py`:

```python
page_number_css = """
.page-number {
    font-size: 0.85em;        # cambiar tamaño
    color: #666;              # cambiar color
    border-top: 2px solid #ddd;  # cambiar borde
}
"""
```

---

## Limitaciones

1. **Basado en archivos HTML, no en páginas reales** — La numeración se basa en cuántos archivos `.xhtml` tiene el EPUB, no en cómo se renderiza en el dispositivo final. Por ejemplo:
   - Un EPUB de 100 capítulos = 100 archivos HTML = "1/100" a "100/100"
   - El reproductor ereader puede mostrar esto como 5 páginas físicas por capítulo

2. **No respeta saltos de página** — Si usas `<page-break>` en el HTML, la numeración no se ajusta

3. **Los reproductores pueden ocultarlo** — Algunos ereaders (Apple Books, Kindle) pueden no mostrar el footer personalizado si tienen su propio sistema de numeración

---

## Casos de Uso

### ✓ Bueno para:
- Documentos de referencia (guías, tutoriales)
- Libros académicos o técnicos
- Documentos que citan por página ("ver página 42")

### ✗ Malo para:
- Novelas (confunde al lector con "páginas reales" del libro)
- Ebooks optimizados por dispositivo (donde cada lector ve diferente número de páginas)

---

## Cómo funciona internamente

### EPUB = ZIP + HTML

Un EPUB es simplemente un archivo ZIP con esta estructura:

```
mi-libro.epub
├── mimetype
├── META-INF/
│   └── container.xml
├── OEBPS/
│   ├── content.opf
│   ├── toc.xhtml
│   ├── cover.xhtml
│   ├── styles.css
│   ├── chapter-01.xhtml
│   ├── chapter-02.xhtml
│   └── chapter-03.xhtml
└── ... (otros recursos)
```

### Post-procesador

El `page_numbering.py`:

1. Extrae el ZIP a directorio temporal
2. Busca archivos `.xhtml` (excluyendo cover, toc, nav)
3. Cuenta cuántos hay (ej: 40 archivos)
4. Para cada archivo:
   - Inyecta `<div class="page-number">2/40</div>` antes de `</body>`
5. Actualiza `styles.css` con estilos `.page-number`
6. Re-comprime a ZIP

### Por qué se inyecta así

- **No modifica Pandoc** — Pandoc genera EPUB estándar sin cambios
- **Post-procesa el resultado** — Limpio, no invasivo
- **Compatible** — Funciona con cualquier versión de Pandoc
- **Reversible** — Si quieres quitarlo, solo comenta la línea

---

## Troubleshooting

### No aparecen números en mi lector

**Causa:** El lector tiene su propio sistema de numeración o no muestra footers personalizados.

**Solución:** Es normal en algunos ereaders (Apple Books, Kindle). Desactiva la numeración si no la necesitas:

```python
# En converters/markdown.py
# add_page_numbers(output)
```

### Los números están en lugar incorrecto

**Causa:** El HTML tiene estructura no estándar (falta `</body>` o está en lugar raro).

**Solución:** El post-procesador trata de inyectar antes de `</body>`, y si no existe, lo añade al final. Si sigue sin funcionar, revisar estructura del HTML generado.

### Proceso lento para EPUB grande

**Causa:** El ZIP extracción/recompresión es lenta para EPUBs de 1000+ archivos.

**Solución:** Es normal (pero raro). Si necesitas optimizar, usar bibliotecas de manejo de ZIP más eficientes.

---

## Ejemplos

### EPUB pequeño (3 capítulos)
```
Página 1: "1/3"
Página 2: "2/3"
Página 3: "3/3"
```

### EPUB grande (40 capítulos)
```
Página 1: "1/40"
Página 2: "2/40"
...
Página 40: "40/40"
```

---

## Futuras Mejoras

- [ ] Opción en YAML para habilitar/deshabilitar numeración
- [ ] Personalizar formato (`Página 2 de 40` vs `2/40`)
- [ ] Saltar cover, prefacio, índice (no contar como páginas)
- [ ] Integrar con verdadera paginación CSS (si EPUB 4.0 lo soporta)
- [ ] Detectar saltos de página y ajustar numeración
