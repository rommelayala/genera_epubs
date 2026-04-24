---

Prioridad 1 — Publicar los libros que ya están listos (Alto impacto, bajo esfuerzo)

fundamentos-ia-libro.md y playwright-ts-intermedio-avanzado.md están al 85-90%. Son los más cercanos a ser productos distribuibles.

Acciones concretas:

1. Revisar y cerrar los capítulos finales de ambos libros.
2. Ejecutar generate_epub.sh para generar los EPUBs.
3. Opcionalmente generar PDFs con Pandoc también.  


Esto te da productos reales para mostrar, vender o distribuir con poco trabajo adicional.

---

Prioridad 2 — Terminar los libros incompletos (Alto impacto, esfuerzo medio)

agentes-ia-libro.md y skills-libro.md necesitan 50-70% más contenido. Son los más estratégicos dado tu posicionamiento en IA.

Acciones:

- Completar secciones faltantes (WHY, HOW, ejemplos prácticos, conclusión).
- Luego publicar igual que Prioridad 1.

---

Prioridad 3 — Crear el sitio web AIQ® (Impacto de marca, esfuerzo medio-alto)

Tienes la especificación completa en Promt.md. Solo falta ejecutarla.

Acciones:

- Inicializar el proyecto Next.js.
- Implementar la landing page según las guías de marca que ya documentaste.
- Desplegar en Vercel.  


---

Prioridad 4 — Inicializar git en el vault (Bajo esfuerzo, riesgo mitigado)

Sin control de versiones, cualquier error puede costarte trabajo ya hecho.

Acción única:  
 git init && git add . && git commit -m "Initial vault commit"

---

Prioridad 5 — Gestor de proyectos con IA (Esfuerzo alto, valor futuro)

Es el proyecto más ambicioso. Dejarlo para cuando los libros y el sitio estén listos.

---

Resumen visual

┌─────┬───────────────────────────────┬────────────┬─────────┐  
 │ # │ Tarea │ Esfuerzo │ Impacto │  
 ├─────┼───────────────────────────────┼────────────┼─────────┤  
 │ 1 │ Publicar libros listos (EPUB) │ Bajo │ Alto │  
 ├─────┼───────────────────────────────┼────────────┼─────────┤  
 │ 2 │ Terminar libros incompletos │ Medio │ Alto │  
 ├─────┼───────────────────────────────┼────────────┼─────────┤  
 │ 3 │ Crear sitio web AIQ® │ Medio-alto │ Alto │  
 ├─────┼───────────────────────────────┼────────────┼─────────┤  
 │ 4 │ Git en el vault │ Muy bajo │ Medio │  
 ├─────┼───────────────────────────────┼────────────┼─────────┤  
 │ 5 │ Gestor de proyectos IA │ Alto │ Futuro │
└─────┴───────────────────────────────┴────────────┴─────────┘

---

¿Por cuál quieres empezar? Puedo ayudarte directamente — por ejemplo, revisar un libro para cerrarlo, ejecutar el script de EPUB, o
inicializar el proyecto Next.js.
