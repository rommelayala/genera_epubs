Plan y Prompt para RTM Agnóstico e Híbrido
Este documento contiene el plan arquitectónico agnóstico y el prompt exacto que puedes copiar y pegar en tu IA local (Ollama con Qwen, Llama 3, etc.) para implementar este sistema en cualquier proyecto, independientemente del lenguaje de programación.

1. El Plan Arquitectónico (Totalmente Agnóstico)
   Para que el sistema de RTM no sea intrusivo ni ensucie el código de tus proyectos (ya sean de React, Python, Go, etc.), se basará en convenciones de carpetas y un único script independiente.

Estructura de Directorios Propuesta
text
/tu-proyecto
├── docs/
│ ├── features/ # (Humano) Aquí escribes el "Qué". Archivos .md
│ │ └── FEAT-001_login.md # Contiene frontmatter YAML con el ID de la feature
│ └── RTM.md # (Generado) La matriz final de trazabilidad cruzada
├── .agents/ # (Opcional/Agnóstico) Carpeta para outputs de IAs
│ └── prd.json # (IA) Archivo JSON generado por Ralph u otros agentes
└── scripts/
└── generate_rtm.py # Script Python sin dependencias externas (solo stdlib)
Reglas de Integración
El Humano: Escribe Markdown en docs/features/\*.md. El único requisito es que al inicio del archivo haya un bloque YAML (Frontmatter) indicando id: FEAT-XXX y title: "...".
El Agente (IA): En su prd.json, en el bloque de cada User Story (US), debe incluir un campo "trace_to": "FEAT-XXX".
El Script: generate_rtm.py es un script puro de Python (viene preinstalado en Mac/Linux). Lee los .md, lee el .json y genera un RTM.md con una tabla de trazabilidad. 2. El Prompt para tu IA Local (Qwen / Ollama)
Copia el siguiente texto desde aquí y pégalo en el chat de tu IA local. Está diseñado para darle contexto estricto de ingeniería y obligarla a generar código robusto sin dependencias de terceros.

TIP

Copia a partir de la siguiente línea:

System Prompt / User Prompt:

Eres un Arquitecto de Software y Tooling Engineer. Mi objetivo es implementar un sistema híbrido de "Matriz de Trazabilidad de Requisitos (RTM)" en mi proyecto. Este proyecto debe ser 100% agnóstico al lenguaje principal de mi repositorio y totalmente no intrusivo.

El flujo es el siguiente:

Yo (humano) escribo los requerimientos en la carpeta docs/features/ usando archivos Markdown.
Mis agentes autónomos de IA generan y actualizan un archivo prd.json con sus User Stories y estado técnico.
Necesito un script en Python (usando SOLO la librería estándar) que lea ambos mundos y genere un docs/RTM.md consolidado.
Requisitos exactos de lo que debes generar:

1. Estructura de Ejemplo: Genera un ejemplo mínimo viable de cómo debe lucir un archivo docs/features/FEAT-001.md usando YAML Frontmatter al inicio (que incluya id y title).

2. Estructura de JSON: Genera un ejemplo de cómo debe estructurarse el archivo prd.json de los agentes. Debe tener un array de userStories donde cada objeto incluya los campos: id (ej. US-001), title, y un campo clave trace_to (ej. "FEAT-001") para enlazar con el requerimiento humano. Además, debe incluir impl_status (valores: "implementado", "no implementado", "partial") y test_coverage (un array de strings, ej. ["UNIT", "Regression", "e2e"]).

3. El Script Generador (Python): Escribe el código completo de un script llamado scripts/generate_rtm.py. Este script debe:

Usar solo dependencias estándar (json, pathlib, re, etc. ¡NADA de PyYAML, haz un parseo simple con RegEx para extraer el id y title del frontmatter de los .md!).
Leer todos los .md en docs/features/ y extraer su ID y Título.
Leer el archivo prd.json (puedes parametrizar la ruta o ponerla por defecto en la raíz o en .agents/prd.json).
Cruzar los datos usando el campo trace_to del JSON con el ID del Markdown.
Generar (sobrescribir) el archivo docs/RTM.md.
El archivo generado debe incluir una tabla en formato Markdown con las columnas: [Feature ID] | [Feature Title] | [User Story ID] | [US Title] | [Impl Status] | [Test Coverage].
Asegúrate de que el código sea defensivo (que maneje graceful failures si las carpetas no existen o si un JSON está mal formado). No me des explicaciones largas, muéstrame el código, los ejemplos y las instrucciones para ejecutarlo.
