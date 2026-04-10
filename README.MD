# Generador de EPUBs desde Markdown

Este directorio contiene un script en Bash (`generate_epub.sh`) configurado para transformar cualquier archivo Markdown (`.md`) en un e-book (EPUB) con formato profesional, utilizando **Pandoc** como motor principal debido a su inmenso poder de conversión y personalización.

---

## 🛠 Precondiciones

Para asegurar el correcto funcionamiento del script generador de EPUB, tu entorno macOS debe cumplir con lo siguiente:

1. **Tener instalado Pandoc**:
   Pandoc es la herramienta base que realiza la conversión por debajo. Si no lo tienes, abre tu terminal y ejecuta:
   ```bash
   brew install pandoc
   ```
2. **Permisos de Ejecución**:
   El script necesita permisos para ejecutarse en tu máquina local. Si la terminal te marca un error de permisos, córrelo por primera y única vez con:
   ```bash
   chmod +x ./generate_epub.sh
   ```
3. **Un archivo Markdown válido**:
   Debes contar con el documento Markdown (`.md`) finalizado. Es altamente recomendable que este posea su estructura limpia de cabeceras (`#`, `##`) dado que Pandoc los usará para trazar el **Índice Interactivo (ToC)** de tu libro.

---

## 🚀 Uso (Acción)

Invocar al script es tan simple como pasarle dos argumentos: la **ruta del archivo Markdown** a evaluar y el **nombre preferido** (sin extensión) que quieres para el output. 

**Estructura del comando:**
```bash
./generate_epub.sh <ruta_al_archivo.md> <nombre_deseado_del_libro>
```

**Ejemplo de uso:**
Asumiendo la siguiente estructura de carpetas (la cual es la actual del proyecto) y estando tú posicionado sobre la carpeta `geneara_epubs`:

```text
geneara_epubs/
├── context
│   ├── CONTEXT.md -> retoma el trabajo con cualquier AI assitant   
│
├── Documentation -> Documentacion del proyecto
│   ├── planes 
│   │     ├── planes propuestos
│   │
│   ├──tasks.md -> tareas pendientes y hechas
│
├── epubs_generados
│   └── playwright-ts-intermedio-avanzado.epub
│
├── libros_draft
│   └── playwright-ts-intermedio-avanzado.md
│
├── generate_epub.sh       ← El corazon y cerebro de la app
│
├── README.MD

```

Ejecutarías:
```bash
-> Todos los libros
./generate_epub.sh

-> Libro especifico
./generate_epub.sh [playwright-ts-intermedio-avanzado.md] [manual_avanzado_qa]
```

---

## 📦 Salida (Output)

Una vez ejecutado el comando con éxito, el script realizará en automático las siguientes acciones en el sistema de archivos: 

1. **Creación del directorio**: Verificará la existencia del directorio base `/epubs_generados` en la ruta donde estés corriendo el script. Si de casualidad no existe, lo creará por ti automáticamente.
2. **Añadido de Timestamp Fijo**: Construirá un nombre de archivo uniendo tu `<nombre_deseado_del_libro>` con un timestamp de generación único (`YYYYMMDD_HHMMSS`). Esto evitará conflictos de sobrescritura de e-books si compilas varias veces el mismo libro el mismo día.
3. **Generación del Archivo Final**: Insertará el EPUB procesado y navegable (que incluye Metadata como el Título y el Autor nativos) directamente en esa ruta. 

**Salida en consola:**
```text
🔄 Convirtiendo: agentes-ia-libro.md...
✅ Generado: ./epubs_generados/agentes-ia-libro_20260410_212651.epub
```

> **Portadas Automáticas**: El script crea y utiliza una carpeta `portadas_draft`. Para añadir una portada a tu libro, coloca una imagen (`.jpg` o `.png`) en esta carpeta con el **mismo nombre exacto** que tu archivo `.md`. El script la detectará e integrará automáticamente en el EPUB. Si no se encuentra una imagen, se utilizará la portada por defecto de Pandoc.
> 
> **Personalización Extra**: Dentro de las llamadas internas de Pandoc en el script fuente `generate_epub.sh`, existe un parámetro comentado que te permitirá añadir rápidamente reglas de estilos inyectables **(`--css`)**.
