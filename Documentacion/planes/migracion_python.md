Arquitectura propuesta

generate_epub.sh          ← launcher SOLO (deps + pandoc check → llama al .py)
generate_epub.py          ← entry point CLI + orquestacion paralela
epub_generator/
  __init__.py
  generator.py            ← pandoc wrapper (una responsabilidad)
  cover.py                ← generacion de portadas con Pillow (absorbe generate_minimal_covers.py)
  config.py               ← carga de metadata por libro (YAML o frontmatter del .md)
requirements.txt
Responsabilidades claras (SOLID / DRY)
generate_epub.sh — cero logica de negocio. Solo:

Verifica pandoc, si no lo tiene → apt install / brew install automatico segun OS
Verifica Python y el venv, si no existe → crea e instala requirements.txt
Pasa todos los args tal cual a generate_epub.py
generate_epub.py — solo orquestacion:

Parsea args (argparse)
Descubre archivos .md
Lanza generator.py en paralelo (ThreadPoolExecutor) por cada libro
generator.py — solo sabe llamar pandoc con los parametros correctos

cover.py — solo sabe generar portadas. Absorbe generate_minimal_covers.py sin duplicar

config.py — solo sabe leer metadata (del frontmatter YAML del .md o de un .yaml por libro)

Parallelismo

# Sin args: todos los libros en paralelo
./generate_epub.sh

# Con args: libro especifico
./generate_epub.sh agentes-ia-libro.md
Usa ThreadPoolExecutor — pandoc es I/O bound, no necesitamos multiprocessing.

Metadata (80-20)
La opcion mas simple que da el mayor valor: frontmatter YAML en el .md:


---
title: "Agentes IA"
author: "Rommel Ayala - QA Lead"
description: "..."
language: "es-ES"
cover: "agentes-ia-libro.jpg"
---
Si no tiene frontmatter → fallback a los defaults actuales. Sin archivos extra, sin config separado.

Una pregunta antes de arrancar: ¿generate_minimal_covers.py lo eliminamos y su logica pasa a cover.py, o quieres mantenerlo como script independiente por ahora?

