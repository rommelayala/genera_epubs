# Claude Uso Maestro — De Usuario Promedio a Operador de Élite
### Un libro-curso-tutorial · Framework 5W1H · Perfil QA

---

> **Este curso asume que ya usas Claude.** El objetivo no es explicar qué es una IA — es que aprendas a operar Claude como si fueras el ingeniero que lo construyó.

---

# PARTE I — CONTEXTO AMPLIO

---

## WHAT — ¿Qué es Claude realmente?

La mayoría de usuarios ven a Claude como un chatbot sofisticado. Eso es como ver a un compilador como "un programa que escribe texto".

Claude es un **modelo de lenguaje autorregresivo** que predice el siguiente token más probable dado un contexto. Eso suena técnico pero tiene implicaciones prácticas directas en cómo debes usarlo.

### La arquitectura que te importa saber

```
┌─────────────────────────────────────────────────────┐
│                  VENTANA DE CONTEXTO                │
│                                                     │
│  System Prompt │ Historial │ Tu mensaje │ Respuesta │
│                                                     │
│  ← todo esto se "lee" en cada llamada →             │
└─────────────────────────────────────────────────────┘
```

**Lo que esto significa para ti:**
- Claude no tiene memoria real entre conversaciones — tiene contexto dentro de una sesión
- Cada token en el contexto tiene un costo (dinero si usas API, velocidad si usas el cliente)
- Claude lee TODO el contexto cada vez que responde — no "recuerda", relee
- Lo que pones al principio del contexto pesa más que lo que pones al final

### Tokens: la moneda real

Un token ≈ 0.75 palabras en español. Pero lo que importa no es el número — es entender **qué consume tokens y por qué**.

| Lo que escribes | Tokens aproximados |
|---|---|
| "hola" | 1 |
| Un párrafo de 100 palabras | ~130 |
| Un archivo de código de 50 líneas | ~400–600 |
| Un stack trace completo | ~300–800 |
| Un README largo | ~2,000–5,000 |
| Una conversación larga sin compactar | 10,000–50,000+ |

**El error del usuario promedio:** pegar contexto innecesario pensando que "más contexto = mejores respuestas". A veces es cierto. Muchas veces, el contexto extra satura el modelo y degrada la respuesta.

### Claude vs GPT-4 vs Gemini — la diferencia real

No es una guerra de marcas. Es entender las fortalezas:

| | Claude | GPT-4 | Gemini |
|---|---|---|---|
| Razonamiento largo | ★★★★★ | ★★★★☆ | ★★★☆☆ |
| Seguir instrucciones complejas | ★★★★★ | ★★★★☆ | ★★★☆☆ |
| Código | ★★★★★ | ★★★★★ | ★★★★☆ |
| Honestidad sobre incertidumbre | ★★★★★ | ★★★☆☆ | ★★★☆☆ |
| Ventana de contexto | 200K tokens | 128K tokens | 1M tokens |
| Integración con herramientas (CLI) | Claude Code ★★★★★ | Codex ★★★☆☆ | — |

**Para un perfil QA:** Claude es superior en razonamiento sobre comportamiento esperado vs real, generación de casos edge, y seguir especificaciones precisas sin inventar.

---

## WHO — El usuario promedio vs el operador maestro

### El usuario promedio
- Escribe un mensaje largo en lenguaje natural
- Espera que Claude "adivine" la intención
- Copia y pega contexto masivo "por si acaso"
- No reutiliza prompts exitosos
- Reinicia conversaciones sin estrategia
- Ignora los errores de Claude en lugar de corregirlos en el momento

### El operador maestro
- Da instrucciones estructuradas con rol + tarea + formato + restricciones
- Provee exactamente el contexto necesario, ni más ni menos
- Tiene prompts reutilizables para tareas recurrentes (skills)
- Sabe cuándo compactar una conversación y cuándo empezar una nueva
- Corrige el rumbo de Claude antes de que el error se propague
- Delega tareas complejas a sub-agentes para proteger su contexto principal

### Tu perfil QA — ventajas que ya tienes
Como QA ya tienes el mindset correcto:
- Piensas en casos edge y comportamiento esperado vs real → exactamente lo que necesitas para escribir buenos prompts
- Sabes especificar criterios de aceptación → un prompt maestro es una especificación
- Entiendes el valor de los test cases reproducibles → un skill es un test case para Claude
- Tienes tolerancia cero al comportamiento no determinista → sabes cuándo Claude está inventando

---

## WHY — Por qué el uso eficiente importa más de lo que crees

### El desperdicio invisible

En una conversación de trabajo típica de 2 horas con Claude, el usuario promedio desperdicia:
- ~40% de tokens en contexto repetido que Claude ya "sabe"
- ~20% en correcciones de malentendidos que una mejor especificación hubiera evitado
- ~15% en respuestas que pidió mal y tuvo que repedir
- ~10% en formato que no necesitaba

**El 85% del tiempo y costo se podría eliminar con mejor operación.**

### La ventaja compuesta

Un operador maestro no es 2x más productivo. Con Claude Code y agentes bien configurados, la diferencia real es 10x–50x en tareas de desarrollo y testing. No es hipérbole — es consecuencia de la paralelización.

Mientras el usuario promedio hace una tarea a la vez, el operador maestro lanza 5 sub-agentes en paralelo, protege su contexto principal, y recibe los resultados consolidados.

---

## WHEN — Cuándo usar Claude (y cuándo NO)

### Úsalo para:
- Tareas donde el criterio es definible pero la ejecución es repetitiva
- Generación de variantes (casos de prueba, mocks, fixtures)
- Análisis de código donde el patrón importa más que el conocimiento de negocio
- Transformaciones de formato (JSON → SQL, spec → test cases)
- Revisión de código con criterios explícitos
- Documentación de lo que ya existe

### NO lo uses para:
- Decisiones de arquitectura que requieren contexto de negocio que Claude no tiene
- Validar si algo "es correcto" sin darle el estándar contra el que comparar
- Tareas donde la aleatoriedad del modelo es un problema real (ej: valores exactos en tests)
- Reemplazar una conversación con un colega humano cuando el problema es político, no técnico

### La regla del QA:
> Si puedes escribir los criterios de aceptación, Claude puede ejecutar contra ellos. Si no puedes escribirlos, primero resuélvelos tú.

---

## WHERE — Los entornos de poder

### Claude.ai (web)
Para conversaciones exploratorias, análisis de documentos, brainstorming. No para trabajo repetitivo — no tiene skills ni hooks.

### Claude Code (CLI) ← Tu entorno principal
El entorno donde Claude pasa de ser un chatbot a ser un colaborador de ingeniería real. Tiene:
- Sistema de skills (comandos reutilizables)
- Hooks (acciones automáticas antes/después de eventos)
- Sub-agentes con aislamiento real
- Memoria persistente entre sesiones
- Integración directa con el filesystem y git

### API directa
Para cuando construyes tus propias herramientas. Máximo control, máxima responsabilidad. Si llegas a este nivel, ya eres operador maestro.

---

## HOW — El framework mental del operador maestro

### Los 4 niveles de operación

```
Nivel 1: Prompt casual        → "oye, revisa este código"
Nivel 2: Prompt estructurado  → [rol][contexto][tarea][formato][restricciones]
Nivel 3: Skill               → /review (encapsula el nivel 2 en un comando)
Nivel 4: Agente              → Claude ejecuta autónomamente con herramientas
```

La progresión no es lineal — usarás los 4 niveles según la tarea.

---

# PARTE II — ARQUITECTURA DEL PROMPT PERFECTO

---

## La anatomía del prompt maestro

Un prompt perfecto tiene 5 componentes. Ninguno es opcional cuando la tarea importa:

```
[ROL]          ← Quién es Claude en esta tarea
[CONTEXTO]     ← Lo mínimo necesario para entender el problema
[TAREA]        ← Qué debe hacer exactamente
[FORMATO]      ← Cómo debe entregar el resultado
[RESTRICCIONES]← Qué NO debe hacer
```

### Ejemplo: usuario promedio vs operador maestro

**Promedio:**
```
revisa este componente de React y dime si está bien
```

**Maestro:**
```
Actúa como senior frontend engineer especializado en React con criterio de code review.

CONTEXTO: Este componente es parte de un wallet manager. Los wallets tienen soft-delete
(is_deleted). El componente recibe handlers async desde el padre.

TAREA: Revisa el componente adjunto y reporta:
1. Bugs reales (no teóricos)
2. Problemas de UX (estados de carga, errores no manejados)
3. Problemas de accesibilidad críticos

FORMATO: Lista numerada por severidad (crítico/mayor/menor). Para cada issue:
- Línea exacta del problema
- Por qué es un problema
- Fix concreto (código, no descripción)

RESTRICCIONES:
- No menciones mejoras de style/naming que no afecten funcionamiento
- No sugieras refactors no pedidos
- Si algo está bien, di explícitamente "sin issues en X"
```

La diferencia en calidad de respuesta es abismal. Y el segundo prompt solo tiene ~100 tokens más.

---

## El poder de los XML tags

Claude fue entrenado con XML. Cuando usas tags, no es "decoración" — es una señal estructural que Claude procesa de forma diferente al texto plano.

```xml
<context>
  El sistema procesa transacciones crypto. Un "spread" es la diferencia entre
  precio de compra y venta. Las wallets tienen soft-delete.
</context>

<task>
  Genera 10 casos de prueba para la función calculateSpread(buy, sell).
  Incluye casos edge: valores negativos, cero, iguales, decimales de alta precisión.
</task>

<format>
  Array de objetos TypeScript:
  { description: string, input: { buy: number, sell: number }, expected: number | Error }
</format>
```

### Tags más útiles en práctica

| Tag | Uso |
|---|---|
| `<context>` | Información de fondo que Claude necesita pero no debe mezclar con la tarea |
| `<task>` | La instrucción principal |
| `<format>` | Especificación del output |
| `<example>` | Ejemplos few-shot |
| `<constraints>` | Lo que NO debe hacer |
| `<thinking>` | Para pedirle que razone antes de responder (en prompts de análisis) |
| `<code>` | Código que debe analizar o modificar |

---

## Few-shot: enseñar con ejemplos

Cuando quieres un formato o estilo específico, mostrar es más efectivo que describir:

```
Genera casos de prueba en este formato exacto:

<example>
it("calcula spread positivo", () => {
  expect(calculateSpread(100, 95)).toBe(5);
});
</example>

<example>
it("lanza error si buy es menor que sell", () => {
  expect(() => calculateSpread(90, 100)).toThrow("Spread negativo");
});
</example>

Ahora genera 8 casos más para la función validateWalletAddress(address, network).
```

Claude capturará el patrón exacto: naming convention, estructura del test, tipo de assertions.

---

## Chain of Thought: cuándo pedirlo y cuándo no

Chain of thought (CoT) = pedirle a Claude que razone paso a paso antes de responder.

**Úsalo cuando:**
- El problema tiene múltiples pasos dependientes (análisis de bug complejo)
- Quieres auditar el razonamiento (especialmente en decisiones de arquitectura)
- La tarea tiene alta probabilidad de error sin razonamiento explícito

**NO lo uses cuando:**
- La tarea es straightforward (genera un mock, formatea este JSON)
- Tienes límite de tokens — CoT consume 2x–5x más tokens
- Solo necesitas el resultado, no el proceso

**Cómo activarlo:**
```
Analiza este stack trace. Antes de responder, razona paso a paso:
1. ¿Qué operación falló?
2. ¿En qué condición ocurrió?
3. ¿Cuál es la causa raíz más probable?
Luego da tu diagnóstico final.
```

---

## Personas y roles: el truco del experto invisible

Asignar un rol específico no es "magia de prompt" — cambia la distribución de probabilidad sobre qué respuesta es apropiada. Claude entrenado con código de senior engineers responderá diferente si le dices que ES un senior engineer.

```
Actúa como QA Lead con 10 años en fintech, obsesionado con los edge cases
de manejo de dinero (decimales, overflow, concurrencia). Eres conocido por
encontrar bugs que otros QAs pierden porque "nadie haría eso".
```

**Para tu perfil QA, roles útiles:**
- `QA Lead con experiencia en APIs financieras`
- `Senior SDET especializado en testing de React con TypeScript`
- `Security tester enfocado en input validation y OWASP Top 10`
- `Arquitecto de testing que diseña suites mantenibles, no tests frágiles`

---

# PARTE III — GESTIÓN MAESTRA DE TOKENS

---

## El presupuesto de contexto

Piensa en la ventana de contexto como RAM. Tienes 200K tokens (Claude 3.5+). Cuando se llena:
- En la API: error o truncamiento
- En Claude Code: compactación automática o degradación de respuestas

**El principio de mínimo contexto efectivo:**
> Incluye exactamente lo que Claude necesita para la tarea. Nada más.

### Qué incluir vs qué omitir

| Incluir | Omitir |
|---|---|
| El archivo relevante, no el proyecto completo | node_modules, lock files |
| El stack trace exacto, no el log completo | Logs de éxito irrelevantes |
| La función con el bug, no el módulo entero | Funciones no relacionadas |
| El schema de la tabla afectada | Todo el schema de la DB |
| 3 ejemplos representativos | 50 ejemplos "por si acaso" |

---

## Compactación de conversaciones — el skill crítico

### ¿Qué es la compactación?

Cuando una conversación crece, el contexto se llena de historial que ya no aporta. La compactación es resumir ese historial para liberar tokens sin perder el estado de trabajo.

Claude Code hace esto automáticamente cuando se acerca al límite. Pero el operador maestro lo hace manualmente y estratégicamente.

### Cuándo compactar manualmente

**Compacta cuando:**
- Terminaste una subtarea y vas a empezar otra relacionada
- El historial tiene mucho debugging ya resuelto que no necesitas recordar
- Sientes que Claude "olvidó" decisiones de hace 20 mensajes (contexto saturado)
- Cambiaste de tema significativamente dentro de la misma sesión

**NO compactes cuando:**
- Estás en medio de un problema complejo con contexto entrelazado
- El historial contiene decisiones de diseño que Claude necesita para ser consistente
- Vas a continuar exactamente la misma tarea

### Cómo compactar bien (manual)

```
Antes de continuar, necesito compactar el contexto.
Resume en formato estructurado:

1. DECISIONES TOMADAS: (las que afectan trabajo futuro)
2. ESTADO ACTUAL: (qué está hecho, qué falta)
3. PROBLEMAS CONOCIDOS: (bugs identificados, deuda técnica)
4. CONTEXTO CRÍTICO: (restricciones, patrones elegidos)

Sé conciso — este resumen reemplazará el historial anterior.
```

Después de obtener el resumen, puedes iniciar una nueva conversación pegando solo ese resumen como contexto inicial.

### Cuándo empezar una nueva conversación en lugar de compactar

**Nueva conversación cuando:**
- La tarea es completamente independiente
- Quieres "mente fresca" — sin sesgos del historial anterior
- El contexto anterior podría contaminar la nueva tarea (ej: debuggeaste un enfoque incorrecto y ahora quieres uno nuevo)
- La sesión anterior terminó con Claude en un estado confundido o inconsistente

**Regla práctica:**
```
¿El historial ayuda o estorba para la próxima tarea?
→ Ayuda: compacta y continúa
→ Estorba: nueva conversación con contexto limpio
```

---

## Prompt Caching — para uso con la API

Si usas la API directamente, el prompt caching te permite marcar partes del prompt como "cachéables". Claude no las re-procesa en llamadas repetidas — reduces latencia y costo hasta 90%.

```python
# Patrón con cache_control
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": system_prompt_largo,  # esto se cachéa
                "cache_control": {"type": "ephemeral"}
            },
            {
                "type": "text",
                "text": "ahora analiza este caso específico..."  # esto varía
            }
        ]
    }
]
```

**Regla:** todo lo que no cambia entre llamadas (instrucciones del sistema, documentación de referencia, ejemplos) va con `cache_control`. Lo que varía (la pregunta concreta) va sin él.

---

# PARTE IV — CLAUDE CODE: EL ENTORNO DE ÉLITE

---

## La arquitectura de Claude Code

```
Claude Code CLI
│
├── Conversación principal (tu contexto de trabajo)
│   ├── Herramientas: Read, Write, Edit, Grep, Glob, Bash
│   ├── Sistema de memoria: ~/.claude/projects/[repo]/memory/
│   └── CLAUDE.md: instrucciones persistentes del proyecto
│
├── Skills (comandos reutilizables)
│   ├── Global: ~/.claude/commands/
│   └── Proyecto: .claude/commands/
│
├── Hooks (automatización de eventos)
│   └── settings.json
│
└── Sub-agentes (Agent tool)
    ├── general-purpose
    ├── Explore
    ├── Plan
    └── claude-code-guide
```

---

## CLAUDE.md — El sistema prompt del proyecto

El archivo `CLAUDE.md` en la raíz de tu repo es el system prompt persistente de Claude Code para ese proyecto. Se carga automáticamente en cada sesión.

**Qué poner:**
```markdown
# Proyecto: cripto-spread-js

## Stack
- Next.js 14 App Router
- PostgreSQL (pool de conexiones, transacciones explícitas)
- TypeScript strict

## Convenciones
- Soft-delete en lugar de hard-delete (columna is_deleted)
- Queries en /src/lib/queries/[entidad]/[accionEntidadDB].ts
- API routes en /src/app/api/[entidad]/route.ts

## Testing
- Tests unitarios en /test/unit/
- Framework: Jest + @testing-library/react
- Cobertura mínima: lógica de negocio y componentes con interacción

## Lo que NO hacemos
- No usar any en TypeScript
- No hacer hard-delete de wallets o addresses
- No crear helpers genéricos para uso único
```

**Regla de oro:** CLAUDE.md debe contener las decisiones que, si Claude las ignora, produce código incorrecto para tu proyecto específico.

---

## Skills: comandos que encapsulan criterio

Un skill es un archivo `.md` en `.claude/commands/`. Se invoca con `/nombre-del-skill`.

### Anatomía de un skill efectivo

```markdown
# /review-qa — Revisión de código con criterio QA

Actúa como QA Lead senior revisando un cambio de código.

## Proceso
1. Lee el código o diff proporcionado
2. Identifica problemas en este orden de prioridad:
   - Bugs que causarán fallos en producción
   - Casos edge no manejados (null, empty, concurrent)
   - Validaciones de input faltantes
   - Estados de error no cubiertos
3. Para cada problema: línea exacta + impacto + fix concreto

## Formato de salida
### 🔴 Crítico (rompe producción)
### 🟡 Mayor (comportamiento incorrecto en edge cases)  
### 🟢 Menor (mejora de robustez)
### ✅ Sin issues en: [lista de áreas revisadas y limpias]

## Restricciones
- No menciones style o naming que no afecte comportamiento
- No sugieras refactors no pedidos
- Si no hay issues en una categoría, omítela
```

### Skills esenciales para un perfil QA

**`/test-gen`** — Genera casos de prueba
```markdown
Genera tests unitarios para el código o función proporcionada.
Cubre: happy path, edge cases (null/undefined/empty/boundary values),
casos de error esperados.
Formato: Jest + @testing-library/react si es componente React.
Un describe por función/componente, un it por caso.
Nombra los its en español: "hace X cuando Y".
```

**`/bug-hunt`** — Análisis de bug
```markdown
Analiza el bug reportado siguiendo este proceso:
1. Reproduce mentalmente el flujo hasta el error
2. Identifica la causa raíz (no el síntoma)
3. Verifica si hay bugs similares en código relacionado
4. Propón el fix mínimo que resuelve sin romper nada más
Muestra el diff exacto del cambio.
```

**`/spec-to-tests`** — De especificación a tests
```markdown
Dado una especificación de funcionalidad, genera:
1. Lista de escenarios de prueba (BDD style: Given/When/Then)
2. Implementación en Jest de cada escenario
Prioriza los escenarios más críticos para el negocio.
```

---

## Hooks — Automatización sin intervención

Los hooks ejecutan comandos de shell automáticamente en respuesta a eventos de Claude Code. Se configuran en `settings.json`.

### Hooks disponibles

| Hook | Cuándo se ejecuta |
|---|---|
| `PreToolUse` | Antes de que Claude use una herramienta |
| `PostToolUse` | Después de que Claude usa una herramienta |
| `Notification` | Cuando Claude envía una notificación |
| `Stop` | Cuando Claude termina de responder |

### Casos de uso para QA

**Auto-lint después de cada edición:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx eslint --fix $CLAUDE_FILE_PATH 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

**Notificación sonora cuando termina una tarea larga:**
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Glass.aiff 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

**Verificar que los tests pasan antes de continuar:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Comando a ejecutar: $CLAUDE_TOOL_INPUT'"
          }
        ]
      }
    ]
  }
}
```

---

# PARTE V — AGENTES Y SUB-AGENTES

---

## Cuándo usar un sub-agente

La regla fundamental:

> Usa un sub-agente cuando la tarea es lo suficientemente independiente para no necesitar tu contexto, Y cuando el resultado de esa tarea contaminaría tu contexto principal con demasiado ruido.

### El problema que resuelven

```
SIN sub-agentes:
Tu contexto principal (200K tokens)
├── Tu conversación de trabajo
├── Exploración de archivo A (1,000 tokens de resultados)
├── Exploración de archivo B (800 tokens)
├── Grep de 50 matches (2,000 tokens)
└── → Contexto saturado, Claude "olvida" las decisiones del inicio

CON sub-agentes:
Tu contexto principal
├── Tu conversación de trabajo (limpia)
└── → "Explora el codebase y dame solo el resumen de cómo funciona X"
    └── Sub-agente hace el trabajo sucio y devuelve solo el resumen
```

### Los sub-agentes disponibles en Claude Code

**`general-purpose`** — Para cualquier tarea multi-herramienta
```
Úsalo para: investigación de codebase, tareas de escritura compleja,
análisis que requieren múltiples búsquedas
```

**`Explore`** — Especializado en exploración de código
```
Úsalo para: "¿cómo funciona X en este repo?", "encuentra todos los archivos que usan Y",
"dame un mapa del módulo Z"
Niveles: "quick" | "medium" | "very thorough"
```

**`Plan`** — Arquitecto de implementación
```
Úsalo para: "¿cómo debería implementar esta feature?",
diseño antes de escribir código
```

### Paralelo vs Secuencial

**Paralelo** — cuando las tareas son independientes:
```
"Necesito que simultáneamente:
- Sub-agente A: revise todos los API routes por vulnerabilidades de validación
- Sub-agente B: genere los tests faltantes para el módulo de wallets
- Sub-agente C: busque todas las queries SQL sin transacción explícita"
```
Los 3 corren al mismo tiempo. Resultado en 1/3 del tiempo.

**Secuencial** — cuando el resultado de uno alimenta al siguiente:
```
1. Sub-agente: analiza el bug y diagnostica la causa raíz
2. (Recibes el diagnóstico)
3. Sub-agente: implementa el fix basado en el diagnóstico anterior
```

### Worktrees — aislamiento real

Para tareas que modifican archivos y podrían romper tu trabajo actual:

```
Agent({
  isolation: "worktree",  // ← crea una copia aislada del repo
  prompt: "Refactoriza el módulo de wallets para usar el nuevo patrón X.
           Si no hay cambios, el worktree se limpia automáticamente."
})
```

El sub-agente trabaja en una rama separada. Si lo apruebas, mergeas. Si no, descartas sin afectar tu main.

---

## El anti-patrón del agente innecesario

**No uses sub-agentes para:**
- Búsquedas simples donde Grep o Glob son suficientes
- Tareas que necesitan tu contexto (el agente empieza de cero)
- Respuestas rápidas — lanzar un agente tiene overhead

```
❌ Mal:
Agent({ prompt: "¿qué hace la función calculateSpread?" })
→ Overhead innecesario, Grep es instantáneo

✅ Bien:
Grep({ pattern: "calculateSpread", output_mode: "content" })
```

---

# PARTE VI — MEMORIA PERSISTENTE

---

## El sistema de memoria de Claude Code

Claude Code tiene un sistema de memoria basado en archivos en:
```
~/.claude/projects/[repo-hash]/memory/
├── MEMORY.md          ← índice (se carga automáticamente)
├── user_role.md       ← quién eres, cómo aprendes
├── feedback_*.md      ← correcciones y preferencias
├── project_*.md       ← decisiones y estado del proyecto
└── reference_*.md     ← dónde encontrar información externa
```

**MEMORY.md se carga en CADA conversación.** Lo que está ahí, Claude lo "sabe" desde el primer mensaje.

### Los 4 tipos de memoria

**`user`** — Tu perfil como colaborador
```markdown
---
type: user
---
Rommel es QA con experiencia en testing de APIs y componentes React.
Aprende mejor con ejemplos de código concretos antes de la teoría.
Prefiere tests en español (describe/it en español).
```

**`feedback`** — Correcciones y preferencias
```markdown
---
type: feedback
---
No agregar docstrings ni comentarios a código que no se tocó.
**Why:** el usuario considera que el código debe ser autoexplicativo
y los comentarios innecesarios son ruido.
**How to apply:** solo comentar cuando la lógica no es obvia.
```

**`project`** — Estado del proyecto
```markdown
---
type: project
---
Implementando soft-delete en wallets y addresses.
**Why:** las wallets con operaciones asociadas no se pueden eliminar
por integridad referencial — el soft-delete lo resuelve.
**How to apply:** siempre verificar is_deleted en queries, nunca hard-delete.
```

**`reference`** — Dónde encontrar cosas
```markdown
---
type: reference
---
La migración de soft-delete está en:
scriptDB/migrations/20-03-26-PROD/005_soft_delete_wallets_addresses.sql
```

### Qué NO guardar en memoria

- Código o patrones que Claude puede leer del repo
- Historial de git (usa `git log`)
- Estado temporal de la sesión actual
- Soluciones a bugs (el fix está en el código; el commit message tiene el contexto)

---

# PARTE VII — BUENAS Y MALAS PRÁCTICAS

---

## Los 10 anti-patrones más comunes

### 1. El contexto masivo innecesario
```
❌ "Aquí está todo el proyecto para que entiendas el contexto..."
✅ "Aquí está solo el archivo relevante y el schema de la tabla afectada."
```

### 2. La pregunta abierta para tarea precisa
```
❌ "¿Qué piensas de este código?"
✅ "Revisa este código específicamente para: manejo de errores async,
    validación de inputs, y casos edge con valores nulos."
```

### 3. Corregir en lugar de especificar bien
```
❌ [Claude genera código incorrecto] → "No, así no. Vuelve a intentarlo."
✅ [Claude genera código incorrecto] → "El problema es X. Necesito que
   el output sea Y porque Z. Vuelve a generar."
```

### 4. Pedir múltiples cosas sin prioridad
```
❌ "Revisa el código, genera tests, actualiza la documentación y
    refactoriza la función principal."
✅ Tarea separada por tarea. O: "Prioridad 1: revisa bugs críticos.
   Solo si no hay bugs, continúa con los tests."
```

### 5. Confiar sin verificar en código crítico
```
❌ Copiar el código de Claude directamente a producción
✅ Revisar el output especialmente en: manejo de dinero, validaciones
   de seguridad, queries SQL, concurrencia
```

### 6. Ignorar cuando Claude dice que no sabe
```
❌ "Seguro sabes, inténtalo."
✅ Aceptar la incertidumbre y verificar por tu cuenta.
   Claude que dice "no sé" es más confiable que uno que inventa.
```

### 7. El prompt sin restricciones
```
❌ "Genera tests para esta función."
✅ "Genera tests para esta función. No generes tests para comportamiento
   no especificado en los comentarios. No uses mocks a menos que sea
   estrictamente necesario."
```

### 8. Dejar que la conversación crezca sin estrategia
```
❌ Misma conversación para debugging + feature nueva + refactor
✅ Conversación separada por contexto. Compacta cuando cambias de tarea.
```

### 9. No usar el modo de planificación para cambios grandes
```
❌ "Refactoriza el módulo de autenticación."
✅ Primero: "¿Cómo deberías refactorizar el módulo de autenticación?
   Dame el plan antes de escribir código."
   Segundo: revisar y aprobar el plan.
   Tercero: ejecutar.
```

### 10. Usar Claude como motor de búsqueda
```
❌ "¿Cuál es la sintaxis de useEffect en React?"
✅ Usa la documentación oficial para sintaxis conocida.
   Usa Claude para: "¿Cómo debería usar useEffect en este componente
   específico dado que tenemos estas restricciones?"
```

---

## Los 10 patrones maestros

### 1. El prompt de especificación
Antes de cualquier tarea compleja, pide a Claude que reformule lo que entendió:
```
"Antes de hacer nada, dime en tus propias palabras qué entiendes que debo hacer,
qué asunciones estás haciendo, y qué preguntas tienes."
```

### 2. El checksum de output
Para tareas donde el formato importa:
```
"Al final de tu respuesta, incluye una sección 'Verificación' donde listes
explícitamente los criterios que tu output cumple y cuáles NO cumple."
```

### 3. La corrección quirúrgica
Cuando Claude se equivoca, corrige solo lo específico:
```
"La lógica del cálculo es correcta. El único problema es el manejo del caso
null en la línea X. Corrígelo sin tocar nada más."
```

### 4. El contexto incremental
Para proyectos grandes, no des todo el contexto al inicio:
```
Sesión 1: "Lee solo el archivo de queries y dime cómo está estructurado."
Sesión 2: (con el resumen de sesión 1) "Ahora implementa la nueva query
          siguiendo exactamente el mismo patrón."
```

### 5. El revisor adversarial
Para validar tu propio trabajo:
```
"Actúa como un QA que busca activamente fallos en este test suite.
Tu objetivo es encontrar casos que los tests no cubren y que podrían
romper en producción."
```

### 6. El traductor de especificaciones
Para convertir lenguaje de negocio a criterios técnicos:
```
"El product manager dice: 'El usuario no debería poder tener dos wallets
con el mismo nombre.' Traduce esto a:
1. Constraint de base de datos
2. Validación en API
3. Casos de prueba"
```

### 7. El contexto colapsado
Para reusar resultados de agentes sin contaminar el contexto:
```
Agent({ prompt: "Analiza X y dame solo: [lista de 5 bullets máximo]" })
// El agente hace el trabajo, tú recibes solo el resumen limpio
```

### 8. La sesión de diagnóstico
Para bugs complejos, una sesión dedicada solo al diagnóstico:
```
Sesión de diagnóstico: solo leer, analizar, hipotetizar.
Sin escribir código.
Output: causa raíz con confianza (alta/media/baja) + evidencia.

Sesión de fix: contexto limpio + diagnóstico como input → implementar.
```

### 9. El invariante explícito
Para código crítico, declara las invariantes:
```
"Esta función debe cumplir estas invariantes siempre:
1. Si retorna un valor, nunca es null
2. Si buy > sell, lanza Error
3. El resultado siempre tiene exactamente 2 decimales
Genera el código y verifica explícitamente cada invariante."
```

### 10. La memoria como documentación viva
Guarda en memoria las decisiones que te costó tomar, no las obvias:
```
"Guarda en memoria: elegimos soft-delete sobre hard-delete porque
las wallets con operaciones asociadas no se pueden eliminar —
la FK constraint lo impide y el negocio necesita el historial."
```

---

# PARTE VIII — APLICACIONES PRÁCTICAS PARA QA

---

## Testing de APIs con Claude

### De endpoint a suite de tests completa

```
<context>
Este endpoint maneja soft-delete de wallets:
DELETE /api/wallets/[id]
- Si la wallet tiene operaciones → 409 Conflict
- Si la wallet no existe → 404
- Si existe y no tiene operaciones → soft-delete (is_deleted = true) + 200
</context>

<task>
Genera una suite de tests de integración para este endpoint.
Cubre todos los casos del contrato.
</task>

<format>
describe("DELETE /api/wallets/[id]", () => {
  // setup con beforeEach/afterEach
  // un it por caso
})
Usa supertest para las requests HTTP.
</format>

<constraints>
No mockees la DB — estos son tests de integración.
Limpia los datos de prueba en afterEach.
</constraints>
```

### Encontrar gaps en cobertura

```
Tengo estos tests para el componente WalletManager: [pega los tests]
Tengo este componente: [pega el componente]

Identifica qué casos de uso NO están cubiertos por los tests.
Prioriza por probabilidad de encontrar un bug real.
No me digas que cubra cosas obvias como "el componente renderiza".
```

---

## Análisis de bugs complejos

### El protocolo de diagnóstico QA

```
ROL: Eres un QA senior especializado en debugging de aplicaciones React/Next.js.

BUG: [descripción del comportamiento inesperado]

CONTEXTO:
- Cuándo ocurre: [pasos para reproducir]
- Cuándo NO ocurre: [lo que sí funciona]
- Stack trace si existe: [pegar]

CÓDIGO RELEVANTE: [solo las partes relacionadas]

TAREA:
1. Formula las 3 hipótesis más probables sobre la causa raíz
2. Para cada hipótesis: qué evidencia la confirmaría o refutaría
3. Indica tu hipótesis más probable con nivel de confianza

NO implementes el fix todavía — solo el diagnóstico.
```

---

## Generación de datos de prueba

```
Genera fixtures TypeScript para tests del módulo de wallets.
Necesito:

1. Una wallet activa con 3 direcciones en redes distintas (BEP20, SOLANA, POLYGON)
2. Una wallet activa sin direcciones
3. Una wallet con soft-delete (is_deleted: true)
4. Una wallet con operaciones asociadas (para testear que no se puede eliminar)

Sigue exactamente este tipo:
type WalletWithAddresses = {
  id: string
  name: string
  is_deleted: boolean
  addresses: WalletAddress[]
}

Usa UUIDs realistas pero ficticios. Usa direcciones crypto válidas según el formato de cada red.
```

---

## Review de PRs con criterio QA

Skill recomendado para tu workflow:

```markdown
# /qa-review — Revisión de PR con ojos de QA

Revisa el diff proporcionado con el siguiente criterio prioritario:

## 1. Correctitud funcional
- ¿El código hace lo que la descripción del PR dice que hace?
- ¿Hay casos donde el comportamiento difiere de lo esperado?

## 2. Manejo de errores
- ¿Todos los async/await tienen try-catch apropiado?
- ¿Los errores de la DB se propagan correctamente al cliente?
- ¿Los status codes HTTP son correctos para cada caso?

## 3. Validación de inputs
- ¿Se valida todo input externo antes de usarlo?
- ¿Qué pasa con valores null/undefined/vacíos?
- ¿Hay validación tanto en frontend como en backend?

## 4. Tests
- ¿Los tests nuevos cubren los casos edge del código nuevo?
- ¿Algún test existente debería actualizarse?
- ¿Hay código nuevo sin tests?

## Formato
Para cada issue: CATEGORÍA | ARCHIVO:LÍNEA | Problema | Fix sugerido
Al final: "✅ Aprobado con X issues críticos, Y menores"
```

---

# PARTE IX — REFERENCIA RÁPIDA

---

## Atajos mentales del operador maestro

```
¿Tarea repetitiva?          → Crea un skill
¿Contexto saturado?         → Compacta o nueva sesión
¿Tarea independiente?       → Sub-agente
¿Código podría romper?      → Worktree aislado
¿Output crítico?            → Pide verificación explícita
¿Claude se confundió?       → Corrección quirúrgica, no "inténtalo de nuevo"
¿Cambias de tarea?          → Nueva conversación o compacta
¿Regla importante?          → Guarda en CLAUDE.md o memoria
```

## Checklist del prompt maestro

```
☐ ¿Asigné un rol específico?
☐ ¿El contexto es el mínimo necesario?
☐ ¿La tarea es una sola cosa clara?
☐ ¿Especifiqué el formato de output?
☐ ¿Incluí restricciones de lo que NO hacer?
☐ ¿Hay ambigüedad que Claude podría resolver mal?
```

## Los comandos de Claude Code que más se usan

| Comando | Qué hace |
|---|---|
| `/[nombre-skill]` | Ejecuta un skill |
| `/compact` | Compacta el contexto actual |
| `/clear` | Limpia el contexto |
| `/cost` | Muestra el costo de la sesión |
| `/memory` | Abre el sistema de memoria |
| `#texto` | Añade texto al contexto sin pedir respuesta |
| `@archivo` | Referencia un archivo específico |

---

## Glosario del operador maestro

| Término | Definición operativa |
|---|---|
| **Token** | Unidad mínima de texto que Claude procesa. ~0.75 palabras. |
| **Contexto** | Todo lo que Claude puede "leer" en una sesión. |
| **Compactación** | Resumir el historial para liberar tokens. |
| **Skill** | Prompt encapsulado en un archivo `.md` invocable con `/comando`. |
| **Hook** | Comando que se ejecuta automáticamente en respuesta a eventos de Claude Code. |
| **Sub-agente** | Instancia separada de Claude que trabaja en aislamiento. |
| **Worktree** | Copia aislada del repo donde trabaja un sub-agente. |
| **CLAUDE.md** | System prompt persistente del proyecto. |
| **Memoria** | Archivos que se cargan en cada sesión para dar contexto sobre el usuario y el proyecto. |
| **ReAct loop** | Reason + Act: el ciclo que siguen los agentes autónomos. |
| **Prompt caching** | Mecanismo de la API para cachear partes del prompt y reducir costo. |
| **Few-shot** | Técnica de dar ejemplos en el prompt para que Claude imite el patrón. |
| **CoT** | Chain of Thought: razonamiento paso a paso antes de la respuesta. |

---

*Fin del curso — Claude Uso Maestro*
*Versión 1.0 · Perfil QA · Abril 2026*
