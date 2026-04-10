# Gemini Uso Maestro — De Usuario Casual a Operador de Élite
### Un libro-curso-tutorial · Framework 5W1H · Perfil QA

---

> **Este curso asume que ya usas alguna IA.** El objetivo es que entiendas qué hace a Gemini diferente — y cuándo esa diferencia importa.

---

# PARTE I — CONTEXTO AMPLIO

---

## WHAT — ¿Qué es Gemini realmente?

Gemini es la familia de modelos de lenguaje multimodal de Google DeepMind, lanzada en diciembre de 2023 como sucesor directo de PaLM 2. Pero entender Gemini solo como "el ChatGPT de Google" es perder lo más importante.

Gemini fue diseñado desde el inicio para ser **nativo multimodal** — no texto que aprendió a ver imágenes, sino un modelo entrenado simultáneamente con texto, código, imágenes, audio y video.

### La familia Gemini — el mapa completo

```
FAMILIA GEMINI (2025)
│
├── Gemini 2.5 Pro          ← El más capaz. Razonamiento profundo.
│   └── Contexto: 1M tokens. Output: hasta 65K tokens.
│
├── Gemini 2.5 Flash        ← El equilibrio velocidad/capacidad.
│   └── Contexto: 1M tokens. Ideal para tareas repetitivas.
│
├── Gemini 2.0 Flash Thinking ← Modo razonamiento explícito (como o1)
│   └── Muestra el proceso de pensamiento antes de responder.
│
└── Gemini Nano             ← On-device. Pixel, Android, Chrome.
    └── Sin contexto de nube — privacidad máxima.
```

**La diferencia que importa:** no es que Gemini tenga más modelos, es entender para qué sirve cada uno. Usar Pro cuando Flash alcanza es como usar un martillo neumático para colgar un cuadro.

### La arquitectura que te importa

```
┌──────────────────────────────────────────────────────────────┐
│                   VENTANA DE CONTEXTO (1M tokens)            │
│                                                              │
│  System │ Historial │ Archivos │ Imágenes │ Video │ Tu msg  │
│                                                              │
│  ← Gemini puede "leer" todo esto en una sola llamada →      │
└──────────────────────────────────────────────────────────────┘
```

**Lo que esto significa para ti:**
- 1M de tokens ≈ todo el código fuente de Linux en un solo contexto
- Puedes subir PDFs, hojas de cálculo, imágenes, videos y código juntos
- A diferencia de Claude o GPT, Gemini fue entrenado con estos modalities de forma nativa — no añadida
- La ventana grande no significa que debas llenarla — el ruido degrada la respuesta igual que en cualquier modelo

### Tokens en Gemini: la misma moneda, diferente denominación

Google usa la misma unidad: 1 token ≈ 0.75 palabras en español. Pero tiene peculiaridades:

| Tipo de contenido | Tokens aproximados |
|---|---|
| 1 imagen (cualquier resolución) | 258 tokens fijos |
| 1 minuto de video | ~1,600 tokens |
| 1 minuto de audio | ~32 tokens |
| 1 página de PDF | ~600–1,000 tokens |
| 1 hora de video completa | ~100,000 tokens |

**La implicación práctica:** Gemini es el único modelo donde analizar un video de 10 minutos en su totalidad es viable y económico.

---

## WHO — El ecosistema Gemini y sus actores

### Los entornos donde vive Gemini

```
GEMINI ECOSYSTEM
│
├── Gemini.google.com      ← Interfaz de chat (equivalente a Claude.ai)
│   └── Gemini Advanced con Pro 2.5
│
├── Google AI Studio       ← El entorno de poder (GRATIS)
│   ├── Playground para prompts
│   ├── Acceso a todos los modelos
│   ├── System Instructions
│   ├── Grounding con Google Search
│   ├── Ejecución de código nativa
│   └── Export directo a API
│
├── Vertex AI              ← Nivel enterprise (Google Cloud)
│   ├── SLAs, privacidad de datos, compliance
│   ├── Fine-tuning de modelos
│   └── Pipelines de producción
│
├── Google Workspace       ← Integración nativa con Drive, Docs, Sheets, Gmail
│   └── Gemini analiza TUS archivos sin subirlos manualmente
│
└── API / SDK              ← Para construir tus propias herramientas
    ├── Python: google-generativeai
    ├── Node.js: @google/generative-ai
    └── REST directo
```

### Tu perfil QA — lo que Gemini te da que otros no

Como QA tienes necesidades específicas donde Gemini sobresale:
- **Analizar logs masivos** — subir un archivo de 10MB de logs y preguntar por patrones
- **Revisar PDFs de especificaciones** — sin copiar y pegar, subir el PDF directo
- **Comparar screenshots** — subir imagen del diseño + screenshot real y pedir un diff visual
- **Analizar videos de bugs** — subir la grabación de la sesión y que Gemini identifique el momento exacto del fallo

---

## WHY — Por qué Gemini, y cuándo importa más que Claude o GPT

### La comparativa honesta

| Capacidad | Gemini 2.5 Pro | Claude Sonnet 4.6 | GPT-4o |
|---|---|---|---|
| Ventana de contexto | 1M tokens ★★★★★ | 200K tokens ★★★★☆ | 128K tokens ★★★☆☆ |
| Multimodalidad nativa | ★★★★★ | ★★★★☆ | ★★★★☆ |
| Razonamiento código | ★★★★★ | ★★★★★ | ★★★★★ |
| Seguir instrucciones complejas | ★★★★☆ | ★★★★★ | ★★★★☆ |
| Grounding con web en tiempo real | ★★★★★ | ★★☆☆☆ | ★★★★☆ |
| Integración ecosistema Google | ★★★★★ | ★☆☆☆☆ | ★★☆☆☆ |
| Ejecución de código nativa | ★★★★★ | ★★★★☆ | ★★★★☆ |
| Velocidad (Flash) | ★★★★★ | ★★★☆☆ | ★★★★☆ |
| Honestidad sobre incertidumbre | ★★★☆☆ | ★★★★★ | ★★★☆☆ |
| CLI de desarrollo (Claude Code) | N/A | ★★★★★ | ★★☆☆☆ |

**La conclusión honesta:** Gemini Pro 2.5 es el mejor modelo para tareas que involucran contextos masivos, multimodalidad o integración con el ecosistema Google. Claude sigue siendo superior para coding workflows y seguir instrucciones complejas con precisión.

### Cuándo elegir Gemini sobre Claude

```
Usa Gemini cuando:
✓ Necesitas analizar documentos largos (>200K tokens)
✓ Tu tarea incluye imágenes, video o audio
✓ Necesitas información actualizada (Google Search grounding)
✓ Trabajas integrado con Google Drive/Docs/Sheets
✓ Quieres ejecutar código Python en el modelo sin setup local
✓ El costo es una restricción (Flash es muy barato)

Usa Claude cuando:
✓ Necesitas seguir instrucciones complejas con precisión
✓ El workflow de coding con CLI es central (Claude Code)
✓ Quieres más honestidad sobre lo que no sabe
✓ La tarea requiere consistencia en outputs multi-paso
```

---

## WHEN — Historia y momento actual

### Línea de tiempo

| Fecha | Hito |
|---|---|
| Dic 2023 | Lanzamiento Gemini 1.0 (Ultra, Pro, Nano) |
| Feb 2024 | Bard se convierte en Gemini |
| May 2024 | Gemini 1.5 Pro — 1M context window |
| Sep 2024 | Gemini 1.5 Flash — velocidad + economía |
| Dic 2024 | Gemini 2.0 Flash — salto generacional |
| Mar 2025 | Gemini 2.5 Pro — benchmark líder en razonamiento |
| 2025 | Project Astra — agente multimodal en tiempo real |

### El momento actual

Gemini 2.5 Pro lidera múltiples benchmarks de razonamiento en 2025, superando a Claude y GPT en tareas de código complejo y matemáticas. Pero los benchmarks no son el campo de batalla real — es la integración con tu workflow.

---

## WHERE — Google AI Studio: tu entorno de poder

### Por qué AI Studio es el primer lugar donde debes ir

Es gratuito, tiene acceso a todos los modelos Gemini, y es donde puedes experimentar antes de pagar. Las características que más te importan:

**1. Contexto de sistema (System Instructions)**
```
El equivalente al CLAUDE.md de Claude Code.
Todo lo que escribas aquí se aplica a TODAS las conversaciones.
```

**2. Grounding con Google Search**
```
Gemini puede buscar en tiempo real antes de responder.
Activa esto cuando necesites información actualizada.
```

**3. Code Execution**
```
Gemini puede escribir y EJECUTAR Python en el sandbox.
No en tu máquina — en el servidor de Google.
Útil para: análisis de datos, transformaciones de archivos, cálculos.
```

**4. File Upload nativo**
```
PDFs, imágenes, videos, hojas de cálculo — se suben directo.
No copias y pegas. Sube el archivo y habla de él.
```

---

## HOW — El framework mental del operador Gemini

### Los 4 modos de operación

```
Modo 1: Chat casual         → gemini.google.com
Modo 2: Experimento         → AI Studio con system instructions
Modo 3: Automatización      → API + SDK en tu código
Modo 4: Enterprise          → Vertex AI con compliance
```

La progresión importa: empieza en AI Studio para prototipar, luego lleva a la API lo que funciona.

---

# PARTE II — ARQUITECTURA DEL PROMPT EN GEMINI

---

## Diferencias clave vs Claude en cómo procesa prompts

Gemini y Claude procesan el lenguaje de forma diferente. Lo que funciona igual:
- XML tags, roles explícitos, ejemplos few-shot, restricciones claras

Lo que es diferente:

### Gemini responde mejor a instrucciones de resultado, Claude a instrucciones de proceso

```
Claude:
"Sigue este proceso: 1) lee el código, 2) identifica el bug,
3) verifica el impacto, 4) propón el fix mínimo."
→ Sigue los pasos al pie de la letra ✓

Gemini:
"Encuentra el bug, dime cuál es y cómo arreglarlo.
Output: { bug: string, fix: string, linea: number }"
→ Llega al mismo lugar por su propio camino ✓
```

**Implicación práctica:** con Gemini especifica más el OUTPUT que el PROCESO.

### Gemini maneja mejor el contexto implícito en archivos

Con Claude necesitas citar el código relevante en el prompt. Con Gemini puedes subir el archivo completo y referenciar por nombre de función o línea.

```
Claude:
"Revisa esta función: [pega el código de la función]"

Gemini (con archivo subido):
"Revisa la función calculateSpread en el archivo adjunto."
```

---

## La anatomía del prompt maestro en Gemini

Misma estructura de 5 componentes, diferente énfasis:

```
[ROL]           ← Igual que Claude — muy efectivo
[CONTEXTO]      ← Puedes referenciar archivos subidos, no solo texto
[TAREA]         ← Orientada a resultado, no a proceso
[FORMATO]       ← Crítico — Gemini es más creativo en formato si no lo defines
[RESTRICCIONES] ← Más importante aún — Gemini tiende a sobre-explicar
```

### Ejemplo: un prompt maestro para QA con archivo adjunto

```
Actúa como QA senior especializado en APIs REST.

CONTEXTO: Adjunté el archivo de especificación funcional (spec.pdf)
y el archivo de tests actuales (wallets.test.ts).

TAREA: Identifica los casos de la especificación que NO tienen cobertura
en los tests actuales.

FORMATO:
| Caso de la spec | Página | ¿Cubierto? | Riesgo si falta |
|---|---|---|---|

RESTRICCIONES:
- Solo lista los casos NO cubiertos, no los que sí están
- El riesgo debe ser: Alto / Medio / Bajo
- Máximo 20 filas — prioriza por riesgo
```

---

## System Instructions — el CLAUDE.md de Gemini

En Google AI Studio y en la API, las System Instructions son el equivalente al `CLAUDE.md` de Claude Code. Se aplican a todas las conversaciones sin repetirlas.

### Para tu perfil QA

```
Eres un asistente especializado en QA y testing para un equipo de desarrollo
de aplicaciones financieras crypto.

Stack del proyecto:
- Next.js 14 con TypeScript strict
- PostgreSQL con soft-delete (is_deleted)
- Jest + @testing-library/react para tests unitarios

Mis preferencias:
- Tests en español (describe/it en español)
- Código TypeScript, nunca JavaScript
- Sin comentarios obvios en el código
- Sin sugerencias de refactor no pedidas
- Si algo está correcto, di explícitamente que está correcto

Cuando generes tests:
- Un describe por función/componente
- Un it por caso
- Nombra los casos como "hace X cuando Y"
- Prioriza edge cases sobre happy path
```

---

## Grounding con Google Search — el superpoder real

Cuando activas el grounding, Gemini busca en Google antes de responder. No es RAG básico — es integración real con el índice de búsqueda de Google.

### Cuándo activarlo

```
✓ Preguntar sobre versiones actuales de dependencias
✓ Verificar si un bug conocido tiene solución en la comunidad
✓ Comparar opciones de librerías con información actualizada
✓ Preguntar sobre breaking changes en APIs recientes
✓ Investigar si un patrón de seguridad tiene vulnerabilidades conocidas

✗ NO activar para: generar código, analizar TU código,
  tareas de razonamiento puro — el grounding agrega latencia
  y tokens innecesarios si no necesitas información externa
```

### Cómo usarlo en la API

```python
from google.generativeai.types import Tool, GoogleSearchRetrieval

model = genai.GenerativeModel(
    model_name="gemini-2.5-pro",
    tools=[Tool(google_search_retrieval=GoogleSearchRetrieval())]
)

response = model.generate_content(
    "¿Cuál es la versión estable actual de @testing-library/react "
    "y hay breaking changes desde la v13?"
)
```

---

## Code Execution — Python nativo en el modelo

Una de las características más exclusivas de Gemini: puede escribir y ejecutar Python directamente, sin setup local.

### Casos de uso reales para QA

**Analizar un CSV de resultados de tests:**
```
[Sube el archivo CSV con resultados]

Usando code execution, analiza este reporte de tests:
1. Calcula el porcentaje de tests que fallaron por módulo
2. Identifica el módulo con más fallos consecutivos
3. Genera una tabla de resumen
Muestra el código Python que usaste.
```

**Transformar fixtures de un formato a otro:**
```
[Sube el archivo JSON con fixtures actuales]

Usando code execution, transforma estos fixtures del formato A al formato B:
[describe el formato B]
Retorna el JSON transformado listo para copiar.
```

**Por qué esto importa para QA:**
No necesitas instalar nada, abrir un notebook ni escribir un script. Gemini ejecuta Python en el momento y te da el resultado. Para transformaciones de datos de test, es una ventaja enorme.

---

# PARTE III — GESTIÓN DE LA VENTANA DE 1M TOKENS

---

## El mito del contexto infinito

Que Gemini tenga 1M tokens no significa que debas usarlos todos. Las investigaciones de Google muestran que el rendimiento de Gemini degrada con contextos extremadamente grandes — especialmente en la parte media del contexto.

### El "lost in the middle" problem

```
Inicio del contexto  →  Alta atención ✓
Mitad del contexto   →  Atención degradada ⚠️
Final del contexto   →  Alta atención ✓
```

Si tienes información crítica, ponla al inicio o al final. Lo que está en el medio de un contexto masivo tiene más probabilidad de ser "olvidado".

### Cuándo SÍ usar el contexto grande

```
✓ Analizar una codebase completa para una refactorización
✓ Revisar el historial completo de un repositorio
✓ Analizar un video largo buscando un momento específico
✓ Procesar un PDF de 500 páginas buscando secciones relevantes
✓ Comparar múltiples documentos de especificación juntos
```

### Estrategia: chunking inteligente vs contexto masivo

```
CONTEXTO MASIVO (cuando la relación entre documentos importa):
→ "Compara la especificación v1 con la v2 y dame los cambios"
→ Necesitas ambos documentos juntos — un solo contexto masivo

CHUNKING (cuando el documento es independiente):
→ "Analiza cada módulo de este sistema por separado"
→ Una llamada por módulo — respuestas más precisas, menor costo
```

---

## Compactación en Gemini — funciona diferente a Claude

Gemini no tiene un sistema de compactación automática como Claude Code. Pero la estrategia manual es la misma:

### Cuándo compactar

```
✓ Terminaste una subtarea y vas a empezar otra
✓ El historial tiene mucho análisis de callejones sin salida
✓ La sesión tiene >50 intercambios y sientes respuestas menos precisas
✓ Cambias de documento o archivo de referencia principal
```

### Cómo compactar en Gemini

```
Antes de continuar, resume el estado actual en este formato:

DECISIONES TOMADAS:
- [lista de decisiones que afectan trabajo futuro]

ESTADO DEL ANÁLISIS:
- Revisado: [qué ya analizamos]
- Pendiente: [qué falta]

HALLAZGOS CLAVE:
- [máximo 5 bullets con lo más importante]

CONTEXTO TÉCNICO RELEVANTE:
- [patrones, restricciones, convenciones encontradas]

Este resumen reemplazará el historial anterior.
```

---

# PARTE IV — MULTIMODALIDAD: EL SUPERPODER REAL

---

## Imágenes — más allá de "describe esta imagen"

El usuario promedio usa las imágenes de Gemini para preguntar qué hay en la foto. El operador maestro las usa para:

### Comparación visual para QA

```
[Sube screenshot del diseño en Figma]
[Sube screenshot de la implementación real]

Compara estos dos screenshots como QA visual:
1. Lista las diferencias de layout, spacing y colores
2. Indica si las diferencias son bugs o variaciones aceptables
3. Prioriza por visibilidad para el usuario final

Formato: tabla con columna Elemento | Diseño | Real | ¿Bug?
```

### Análisis de diagramas y arquitecturas

```
[Sube el diagrama de flujo / ERD / arquitectura]

Analiza este diagrama de arquitectura:
1. ¿Hay puntos únicos de falla?
2. ¿Qué servicios son críticos para el flujo principal?
3. ¿Hay dependencias circulares?
```

### Leer formularios, tablas y documentos escaneados

```
[Sube el documento escaneado]

Extrae todos los datos de este formulario en formato JSON.
Si hay ambigüedad en algún campo, indica "ambiguo: [lo que lees]".
```

---

## PDFs — el caso de uso que más tiempo ahorra a QA

En lugar de copiar y pegar secciones de especificaciones:

```
[Sube el PDF de especificaciones funcionales]

Lee las páginas 15 a 30 de esta especificación.
Extrae todos los criterios de aceptación para el módulo de wallets.
Formatea como lista de criterios testeables:
- Dado [contexto], cuando [acción], entonces [resultado esperado]
```

### Comparar versiones de specs

```
[Sube spec_v1.pdf]
[Sube spec_v2.pdf]

Compara ambas versiones de la especificación.
Lista solo los cambios que requieren modificar tests existentes.
Ignora cambios de redacción sin impacto funcional.
```

---

## Video — el caso de uso que solo Gemini tiene

### Análisis de grabaciones de bugs

```
[Sube el video de la sesión grabada]

Este video muestra un bug reportado por el usuario.
Analiza el video completo y responde:
1. ¿En qué minuto exacto ocurre el comportamiento inesperado?
2. ¿Qué acciones del usuario precedieron el bug?
3. ¿El bug parece reproducible? ¿Cuál sería el paso a paso?
4. ¿Hay otros comportamientos anómalos en el video que no fueron reportados?
```

### Comparación de demos

```
[Sube video demo antes del cambio]
[Sube video demo después del cambio]

Compara los dos videos de demostración:
- ¿Qué flujos cambiaron?
- ¿Hay diferencias de performance visibles?
- ¿Algún flujo del video 1 desaparece en el video 2?
```

---

## Audio — para QA de productos de voz

```
[Sube el audio de la sesión de usuario]

Transcribe este audio de sesión de usuario thinking-aloud.
Identifica:
1. Momentos de confusión ("¿dónde está?", "¿por qué?", "no entiendo")
2. Errores que el usuario cometió y tuvo que corregir
3. Funcionalidades que buscó y no encontró
```

---

# PARTE V — LA API Y EL SDK

---

## Estructura básica — Python

```python
import google.generativeai as genai

genai.configure(api_key="TU_API_KEY")

# Modelo recomendado por caso de uso
modelos = {
    "tareas_complejas": "gemini-2.5-pro",
    "tareas_rapidas": "gemini-2.5-flash",
    "razonamiento_visible": "gemini-2.0-flash-thinking-exp",
}

model = genai.GenerativeModel(
    model_name=modelos["tareas_complejas"],
    system_instruction="""
    Eres un asistente de QA especializado en testing de APIs.
    Responde siempre en español.
    Sin explicaciones no pedidas.
    """
)

response = model.generate_content("Genera 5 casos edge para un endpoint de login")
print(response.text)
```

## Estructura básica — TypeScript/Node

```typescript
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!);

const model = genAI.getGenerativeModel({
  model: "gemini-2.5-flash",
  systemInstruction: "Eres un asistente de QA. Responde en español. Sin explicaciones innecesarias.",
});

const result = await model.generateContent("Genera casos de prueba para validateWalletAddress");
console.log(result.response.text());
```

---

## Multiturno (conversación con historial)

```python
model = genai.GenerativeModel("gemini-2.5-pro")
chat = model.start_chat()

# Primera pregunta
r1 = chat.send_message("Analiza este endpoint: [código]")
print(r1.text)

# Seguimiento — recuerda el contexto anterior
r2 = chat.send_message("Ahora genera los tests para los casos que identificaste")
print(r2.text)
```

---

## Analizar archivos con la File API

```python
import google.generativeai as genai

# Subir el archivo una vez — reutilizable por 48 horas
archivo = genai.upload_file("especificacion.pdf")

model = genai.GenerativeModel("gemini-2.5-pro")

response = model.generate_content([
    archivo,  # el PDF
    "Extrae todos los criterios de aceptación del módulo de wallets"
])
```

### Con múltiples archivos

```python
spec = genai.upload_file("spec_v2.pdf")
tests_actuales = genai.upload_file("wallets.test.ts")
componente = genai.upload_file("WalletManager.tsx")

response = model.generate_content([
    spec,
    tests_actuales,
    componente,
    """
    Dado el spec, los tests existentes y el componente:
    1. ¿Los tests cubren todos los criterios del spec?
    2. ¿El componente implementa todo lo que el spec requiere?
    Lista solo los gaps, no lo que está bien.
    """
])
```

---

## Streaming — para respuestas largas

```python
# Sin streaming: esperas todo antes de ver algo
response = model.generate_content("Analiza este sistema completo...")

# Con streaming: ves la respuesta mientras se genera
for chunk in model.generate_content("Analiza este sistema completo...", stream=True):
    print(chunk.text, end="", flush=True)
```

---

## Structured Output — JSON garantizado

Una de las ventajas de Gemini: puedes forzar el output a seguir un schema JSON.

```python
import typing_extensions as typing

class CasoDePrueba(typing.TypedDict):
    descripcion: str
    input: dict
    expected_output: str
    prioridad: str  # "alta" | "media" | "baja"

response = model.generate_content(
    "Genera 5 casos de prueba para validateWalletAddress(address, network)",
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=list[CasoDePrueba]
    )
)

casos = response.text  # JSON garantizado, sin markdown wrapper
```

**Para QA esto es oro:** generar fixtures, casos de prueba, y datos estructurados sin tener que parsear markdown o JSON anidado en texto.

---

# PARTE VI — GEMS: LOS SKILLS DE GEMINI

---

## ¿Qué son los Gems?

Los Gems son la versión de Gemini de los Skills de Claude Code. Son configuraciones de modelo guardadas con:
- System instructions específicas
- Comportamiento personalizado
- Nombre e ícono

Disponibles en gemini.google.com con Gemini Advanced.

### Limitaciones vs Skills de Claude Code

| | Gems (Gemini) | Skills (Claude Code) |
|---|---|---|
| Dónde viven | Servidor de Google | Archivos en tu repo |
| Versionado con git | ❌ | ✅ |
| Compartible con equipo | ✅ (compartir link) | ✅ (clonar repo) |
| Invocación | Click en la UI | `/nombre-skill` en CLI |
| Integración con filesystem | ❌ | ✅ |
| Complejidad máxima | Media | Alta |

**Conclusión:** Los Gems son útiles para tareas en la interfaz web. Para workflows de desarrollo, los Skills de Claude Code siguen siendo superiores.

### Gems útiles para QA

**Gem: QA Spec Analyzer**
```
System Instructions:
Eres un QA Lead analizando especificaciones funcionales.

Cuando recibas un documento, extrae automáticamente:
1. Lista de criterios de aceptación testeables
2. Casos edge mencionados explícitamente
3. Casos edge que el spec no menciona pero deberías testear
4. Ambigüedades que necesitan clarificación del PO

Formato siempre: secciones separadas, bullets, sin párrafos largos.
Prioriza por riesgo de negocio.
```

**Gem: Visual QA Comparator**
```
System Instructions:
Eres un QA especializado en testing visual.

Cuando recibas dos imágenes (diseño vs implementación):
1. Lista diferencias por categoría: layout, colores, tipografía, spacing, interactividad
2. Clasifica cada diferencia: Bug crítico / Bug menor / Variación aceptable
3. Da una puntuación de similitud del 0 al 100

Sé específico: "el botón tiene 8px menos de padding" no "el botón se ve diferente".
```

---

# PARTE VII — GOOGLE WORKSPACE + GEMINI

---

## La integración que pocos aprovechan

Si tu equipo usa Google Workspace (Drive, Docs, Sheets, Gmail), Gemini tiene acceso directo a tus archivos — sin subirlos manualmente.

### Casos de uso prácticos para QA

**Desde Google Docs:**
- "Resume este documento de spec en criterios de aceptación"
- "Compara este doc con el anterior y lista los cambios funcionales"
- "Convierte esta tabla de casos de prueba a formato Gherkin"

**Desde Google Sheets:**
- "Analiza esta hoja de resultados de tests y genera el reporte"
- "Identifica patrones en los bugs reportados de este sprint"
- "Genera los datos de prueba faltantes según los casos en esta columna"

**Desde Gmail:**
- "Resume los threads de bugs reportados por el cliente esta semana"
- "Lista todos los cambios de requisitos mencionados en emails del último mes"

### Activarlo

1. `gemini.google.com` → activar extensión de Google Workspace
2. En el chat: `@Drive`, `@Docs`, `@Sheets` para referenciar archivos
3. Gemini lee el archivo en tiempo real — siempre la versión más reciente

---

# PARTE VIII — BUENAS Y MALAS PRÁCTICAS

---

## Los 8 anti-patrones específicos de Gemini

### 1. Activar grounding para todo
```
❌ Grounding en ON siempre
→ Latencia alta, tokens extras, respuestas menos precisas en tareas de razonamiento

✅ Grounding en ON solo cuando necesitas información actualizada o verificación externa
```

### 2. Subir documentos masivos cuando basta un fragmento
```
❌ Subir el PDF de 200 páginas completo para una pregunta sobre la página 15

✅ "Lee solo las páginas 14-16 de este documento adjunto"
   O mejor: copiar y pegar solo el fragmento relevante
```

### 3. Confundir contexto grande con mejor comprensión
```
❌ "Le paso todo el código para que entienda mejor"
→ El lost-in-the-middle problem afecta la precisión

✅ Dar el contexto mínimo efectivo + instrucciones precisas
```

### 4. No usar Structured Output para datos estructurados
```
❌ "Genera los casos de prueba en formato JSON"
→ Gemini puede envolver el JSON en markdown o variar la estructura

✅ Usar response_schema para garantizar el formato exacto
```

### 5. No especificar el formato del output
```
❌ "Dame los bugs que encuentras en este código"
→ Gemini puede dar una respuesta muy larga con mucha narrativa

✅ "Dame los bugs. Formato: JSON array. Cada bug: { linea, descripcion, severidad }"
```

### 6. Usar Pro cuando Flash alcanza
```
❌ Pro para generar un mock simple o formatear un JSON

✅ Flash para tareas repetitivas y sencillas
   Pro para análisis complejos, razonamiento profundo, documentos largos
```

### 7. No aprovechar Code Execution
```
❌ Pedirle a Gemini que calcule algo y confiar en el resultado mental
→ Los LLMs fallan en aritmética

✅ "Usa code execution para calcular esto exactamente"
→ Python no se equivoca en números
```

### 8. Tratar a Gemini como si fuera Claude
```
❌ Dar instrucciones de proceso detallado (funciona mejor en Claude)

✅ Dar especificación de resultado detallado
   "El output debe ser X porque Y" en lugar de "primero haz A, luego B, luego C"
```

---

## Los 8 patrones maestros para Gemini

### 1. El archivo como contexto
En lugar de copiar texto, sube el archivo. Gemini lo lee mejor en su formato nativo que como texto plano copiado.

### 2. Structured Output para cualquier dato
Si el resultado va a ser procesado por código, usa `response_schema`. Elimina el parsing manual y los fallos de formato.

### 3. Grounding quirúrgico
Activa el grounding solo para preguntas donde la actualidad importa. Desactívalo para razonamiento y generación de código.

### 4. El modelo correcto para cada tarea

```python
ROUTING = {
    "analisis_documento_largo": "gemini-2.5-pro",
    "generacion_rapida": "gemini-2.5-flash",
    "analisis_imagen": "gemini-2.5-pro",
    "calculo_con_codigo": "gemini-2.5-flash",  # code execution disponible en flash
    "razonamiento_visible": "gemini-2.0-flash-thinking-exp",
}
```

### 5. La conversación multi-archivo
Sube todos los archivos relevantes al inicio de la sesión y refiérelos por nombre durante toda la conversación — no los vuelves a subir.

### 6. Code Execution para transformaciones
Cualquier transformación de datos que implique cálculo exacto → usa Code Execution. No confíes en que Gemini "calcule mentalmente".

### 7. El prompt de verificación
Para análisis críticos, pide que verifique contra la fuente:

```
"Después de tu análisis, cita textualmente del documento adjunto
las frases que respaldan cada punto que afirmes."
```

### 8. Streaming para respuestas largas
Si el análisis va a ser extenso, usa streaming. No esperes 30 segundos mirando una pantalla en blanco — itera mientras Gemini responde.

---

# PARTE IX — APLICACIONES PRÁCTICAS PARA QA

---

## Flujo completo: de spec PDF a test suite

```python
import google.generativeai as genai
import json

genai.configure(api_key="TU_API_KEY")

# 1. Subir la especificación
spec_file = genai.upload_file("spec_wallet_manager.pdf")

# 2. Extraer criterios de aceptación en formato estructurado
model = genai.GenerativeModel(
    model_name="gemini-2.5-pro",
    system_instruction="Eres un QA Lead. Responde en español. Solo JSON."
)

criterios_response = model.generate_content(
    [spec_file, "Extrae todos los criterios de aceptación del módulo de wallets en JSON"],
    generation_config=genai.GenerationConfig(response_mime_type="application/json")
)

criterios = json.loads(criterios_response.text)

# 3. Para cada criterio, generar el test
tests = []
for criterio in criterios:
    test_response = model.generate_content(
        f"""Genera un test Jest para este criterio:
        {json.dumps(criterio, ensure_ascii=False)}
        
        Formato: código TypeScript listo para copiar.
        Sin explicaciones."""
    )
    tests.append(test_response.text)

# 4. Consolidar
with open("generated_tests.ts", "w") as f:
    f.write("\n\n".join(tests))
```

---

## Análisis visual de regresión

```
WORKFLOW:
1. Screenshot del componente en la versión base → guardar
2. Screenshot después del cambio → guardar
3. Subir ambas imágenes a Gemini
4. Prompt:

"Compara estas dos capturas del mismo componente.
Identifica SOLO los cambios visuales que podrían ser regresiones
(elementos que cambiaron sin intención).
Ignora cambios de datos dinámicos (fechas, precios, IDs).
Formato: tabla con Elemento | Antes | Después | ¿Regresión probable?"
```

---

## Análisis de logs masivos

```
[Sube el archivo de log — puede ser de MB]

Analiza este log de aplicación.
Usando code execution:
1. Cuenta errores por tipo y frecuencia
2. Identifica el endpoint con más errores 5xx
3. Detecta patrones temporales (¿hay picos en algún horario?)
4. Lista los 5 errores más críticos con su stack trace completo

Output: informe ejecutivo + tabla de datos.
```

---

## Generación de datos de prueba realistas

```python
import google.generativeai as genai
import json

model = genai.GenerativeModel("gemini-2.5-flash")

# Schema exacto que necesitamos
class WalletFixture(typing.TypedDict):
    id: str
    name: str
    is_deleted: bool
    addresses: list[dict]

response = model.generate_content(
    """Genera 10 wallets de prueba realistas para un sistema crypto.
    Incluye: 6 activas con 1-3 addresses cada una, 2 activas sin addresses,
    2 con soft-delete.
    Usa UUIDs reales (formato correcto), nombres de wallets reales
    (BINANCE, LEDGER, METAMASK, etc.), y addresses crypto válidas
    para las redes BEP20, ETHEREUM y SOLANA.""",
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=list[WalletFixture]
    )
)

fixtures = json.loads(response.text)
# → JSON limpio, tipado, sin markdown
```

---

## Review de accesibilidad con imagen

```
[Sube screenshot de la UI]

Actúa como experto en accesibilidad web (WCAG 2.1).
Analiza este screenshot:
1. ¿Hay problemas de contraste de color? (indica elementos específicos)
2. ¿Los elementos interactivos son suficientemente grandes? (mínimo 44x44px)
3. ¿El orden visual tiene sentido para un lector de pantalla?
4. ¿Hay iconos sin texto alternativo visible?

Clasifica cada issue: Crítico (falla WCAG A) / Mayor (falla AA) / Sugerencia (AAA)
```

---

# PARTE X — REFERENCIA RÁPIDA

---

## Decisión rápida: ¿Gemini o Claude?

```
¿Necesitas analizar archivos grandes (PDFs, videos, imágenes)?  → GEMINI
¿La tarea implica el ecosistema Google (Drive, Docs, Sheets)?   → GEMINI
¿Necesitas ejecutar código Python en el modelo?                 → GEMINI
¿Necesitas info actualizada del mundo real?                     → GEMINI con grounding
¿Necesitas coding workflow con CLI y filesystem?                → CLAUDE
¿La tarea requiere seguir instrucciones complejas multi-paso?   → CLAUDE
¿El output necesita ser muy preciso y consistente?              → CLAUDE
¿Es una tarea general de texto y razonamiento?                  → CUALQUIERA
```

## Checklist del prompt maestro Gemini

```
☐ ¿Subí el archivo relevante en lugar de copiar y pegar?
☐ ¿Especifiqué el formato de output con precisión?
☐ ¿Activé grounding solo si necesito info actualizada?
☐ ¿Usé Structured Output si el resultado es JSON?
☐ ¿Elegí el modelo correcto (Flash vs Pro)?
☐ ¿Las restricciones previenen la sobre-explicación?
☐ ¿Para cálculos, pedí Code Execution?
```

## Los modelos y cuándo usar cada uno

| Modelo | Cuándo usarlo |
|---|---|
| **Gemini 2.5 Pro** | Análisis profundo, documentos complejos, tareas que requieren máxima capacidad |
| **Gemini 2.5 Flash** | Tareas repetitivas, generación rápida, cuando el costo importa |
| **Gemini 2.0 Flash Thinking** | Cuando necesitas ver el razonamiento explícito, problemas matemáticos complejos |
| **Gemini Nano** | On-device, privacidad máxima, sin conexión |

## Glosario del operador maestro Gemini

| Término | Definición operativa |
|---|---|
| **Grounding** | Buscar en Google antes de responder para tener información actualizada |
| **Code Execution** | Sandbox Python en el servidor de Gemini — escribe y ejecuta código real |
| **Multimodal** | Capacidad nativa de procesar texto, imagen, audio y video en el mismo contexto |
| **Gem** | Configuración de modelo guardada (equivalente a Skill en Claude Code) |
| **File API** | Sistema para subir archivos y reutilizarlos en múltiples llamadas (48h de vida) |
| **Structured Output** | Forzar el output a seguir un schema JSON exacto |
| **Vertex AI** | Plataforma enterprise de Google Cloud para Gemini en producción |
| **AI Studio** | Playground gratuito para experimentar con todos los modelos Gemini |
| **Lost in the middle** | Degradación de atención en el centro de contextos muy largos |
| **Flash** | La variante rápida y económica del modelo |
| **Pro** | La variante de máxima capacidad |
| **Thinking mode** | Modo donde el modelo razona explícitamente antes de responder |

---

*Fin del curso — Gemini Uso Maestro*
*Versión 1.0 · Perfil QA · Abril 2026*
