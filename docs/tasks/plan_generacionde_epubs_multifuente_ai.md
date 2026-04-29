Plan de Implementación: PDF a Markdown con VLM Local (Agnóstico)
Dado que cuentas con una Mac M1 con 32 GB de RAM, tienes potencia de sobra para procesar imágenes con modelos de visión locales. Este plan detalla la arquitectura para un Ingestor Visual que sea 100% agnóstico al modelo, controlable por CLI y trazable vía prd.json.

1. El Problema Técnico y la Solución Agnóstica
   Extraer texto de PDFs destruye el layout. La solución definitiva es usar la vista real del documento enviando imágenes al modelo. Para hacerlo agnóstico y a prueba de futuro:

Renderizado Visual: Convertiremos cada página del PDF en una imagen internamente.
Control por CLI: En lugar de codificar el modelo o dejarlo solo en el YAML, permitiremos sobrescribirlo vía comando (--ai-model <modelo>).
Petición Agnóstica: La clase leerá el modelo configurado y enviará la imagen codificada en Base64 al servidor de Ollama, sin importar si mañana usas llama4-vision o qwen4. 2. Cambios Arquitectónicos Propuestos
[MODIFY] ralph/prd.json y task.md (Integración de Ralph)
Agregaremos una nueva User Story (US-013: AiPdfIngestor Visual Agnóstico) al prd.json para llevar la trazabilidad del desarrollo tal como solicitaste.

[MODIFY] generate_epub.py (CLI Override)
Añadiremos un nuevo flag opcional al CLI:

bash
python generate_epub.py libros_draft/git-libro.yaml --ai-model qwen3.5
Si se provee, sobrescribirá cualquier modelo definido en el YAML. Si no se provee, usará el del YAML, o un default seguro.

[MODIFY] epub_generator/config.py
Actualizaremos BookConfig y SourceConfig para propagar la variable global del ai_model inyectada desde el CLI.

[NEW] epub_generator/ingestors/ollama_pdf_ingestor.py
Crearemos la clase OllamaPdfIngestor(BaseIngestor):

Abrirá el PDF con pymupdf (requiere instalar pymupdf).
Renderizará cada página a un PNG en memoria.
Hará un POST agnóstico a http://localhost:11434/api/generate inyectando dinámicamente la variable config.ai_model.
Mostrará en consola: [INFO] Analizando página 1/15 con el modelo 'qwen3.5'... 3. Ejemplo de Ejecución Final
Si te equivocas en el YAML o quieres probar un modelo nuevo, simplemente ejecutas:

bash
python generate_epub.py libros_draft/git-libro.yaml --ai-model llava
El script enviará automáticamente las fotos al modelo llava sin tocar una sola línea de código.

User Review Required
IMPORTANT

Al ser tu Mac M1 de 32GB, el rendimiento será excelente (aprox 5-10 segundos por página).
He agregado la integración con Ralph (prd.json) y el flag del CLI (--ai-model).
¿Apruebas este plan actualizado para comenzar a codificar las historias de usuario correspondientes?
