# Generador de Cursos

Skill para estructurar, estructurar e iterar la creación de cursos y libros en formato Markdown, optimizados plenamente para el conversor local a EPUB de AIQ®.

## Proceso

1. **Analiza la petición:** Lee el concepto o tema del curso solicitado ($ARGUMENTS).
2. **Plantea el Índice (ToC):** Si no te han proporcionado uno, elabora un índice sólido que progrese de lo básico al nivel experto.
3. **Escritura por Iteración de Capítulos:** Desarrolla el curso utilizando estrictamente `#` para declarar capítulos o partes principales, y `##` para subtemas.
4. **Salida esperada:** Entrega contenido .md listo para ser guardado en la carpeta `libros_draft/` del repositorio, manteniendo la convención de `nombre-del-curso.md` y la portada del curso en formato .jpg en la carpeta 'portadas_draft'.

## Criterios

- **Estilo AIQ® / Rommel Ayala:** Cercano, riguroso, de tú a tú (nivel CTO/Tech Lead). Sin lenguaje corporativo.
- **Filosofía "No-BS":** Menos palabras, más impacto. Si hay una forma sencilla (como un bloque de código corto), prioriza el 5W1H y la regla del 80-20 sobre largas explicaciones a menios que te lo pidan.
- **Claridad Visual:** Apóyate en listas viñetadas, negrillas para énfasis clave y tablas de Markdown para condensar información ten en cuenta que mi mente es visual.

## Restricciones

- **Sintaxis de Cabeceras Estricta:** Pandoc usa las cabeceras `#` y `##` para el índice interactivo del e-book. JAMÁS saltes niveles de jerarquía de forma inconsistente (ej. `#` y luego un `####`).
- **No inventes formatos:** Todo debe ser Markdown estándar nativo; cero tags de HTML personalizados o decoraciones que rompan la traducción de Pandoc.
- **Cero conclusiones robóticas:** Evita muletillas de IA como "En conclusión," o "En resumen,".
