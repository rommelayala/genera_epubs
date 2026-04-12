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

El archivo `CLAUDE.md` en la raíz de tu repo es el system prompt persistente de Claude Code para ese proyecto. Se carga automáticamente en cada sesión y se antepone a todo lo que Claude razona.

### Dónde puede vivir CLAUDE.md — jerarquía de carga

Claude Code busca `CLAUDE.md` en varios lugares y los concatena en este orden:

```
1. ~/.claude/CLAUDE.md            ← global del usuario (aplica a TODOS tus repos)
2. [repo]/CLAUDE.md               ← proyecto (commiteado, compartido con el equipo)
3. [repo]/.claude/CLAUDE.md       ← proyecto local (gitignored, personal)
4. [subdir]/CLAUDE.md             ← por directorio (se carga si trabajas dentro)
```

**Estrategia:**
- **Global (`~/.claude/CLAUDE.md`):** tus preferencias personales que se aplican a todo — "responde en español", "no generes docstrings innecesarios", "siempre explica el razonamiento antes de escribir código".
- **Proyecto (`[repo]/CLAUDE.md`):** convenciones del equipo, stack, reglas de negocio. Se commitea.
- **Local (`[repo]/.claude/CLAUDE.md`):** notas temporales tuyas sobre el proyecto que no quieres commitear (experimentos, ramas en curso).
- **Por subdirectorio:** útil en monorepos — el frontend y el backend pueden tener reglas distintas.

### Anatomía de un CLAUDE.md completo

```markdown
# Proyecto: cripto-spread-js

## Stack
- Next.js 14 App Router
- PostgreSQL (pool de conexiones, transacciones explícitas)
- TypeScript strict

## Arquitectura de carpetas
```
src/
├── app/api/[entidad]/route.ts    ← API routes
├── lib/queries/[entidad]/         ← queries SQL (una función = una query)
├── lib/services/                  ← lógica de negocio
└── components/[feature]/          ← componentes agrupados por feature
```

## Convenciones
- Soft-delete en lugar de hard-delete (columna is_deleted)
- Queries en /src/lib/queries/[entidad]/[accionEntidadDB].ts
- API routes en /src/app/api/[entidad]/route.ts
- Errores custom: extienden `AppError` en /src/lib/errors.ts

## Testing
- Tests unitarios en /test/unit/
- Framework: Jest + @testing-library/react
- Cobertura mínima: lógica de negocio y componentes con interacción
- Tests en español: `describe("calcula spread", () => { it("retorna 0 cuando...") })`

## Comandos frecuentes
- `npm run dev` — servidor de desarrollo
- `npm test` — tests unitarios
- `npm run test:e2e` — Playwright
- `npm run db:reset` — resetea DB local con seeds

## Lo que NO hacemos
- No usar `any` en TypeScript (error de compilación, no warning)
- No hacer hard-delete de wallets o addresses
- No crear helpers genéricos para uso único
- No commitear con tests rotos (CI los bloquea de todos modos)

## Contexto de negocio crítico
- Un "spread" es la diferencia entre precio de compra y venta de un activo crypto
- Todos los montos se almacenan en la menor unidad (satoshis, wei) y se formatean en UI
- Las wallets con operaciones asociadas NUNCA se eliminan (FK constraint + regla de negocio)
```

### Reglas de oro de CLAUDE.md

> **Regla 1:** CLAUDE.md debe contener las decisiones que, si Claude las ignora, produce código **incorrecto** para tu proyecto específico.

> **Regla 2:** No repitas lo que el código ya dice. Si el tsconfig ya prohíbe `any`, no hace falta ponerlo. Si hay convenciones que el código grita solo, no las dupliques.

> **Regla 3:** CLAUDE.md compite por tokens con tu trabajo real. Cada línea debe justificar su existencia. Un CLAUDE.md de 500 líneas es un CLAUDE.md que nadie va a mantener.

> **Regla 4:** Si le dices a Claude "no hagas X" tres veces en una sesión, ese "X" pertenece a CLAUDE.md. No corrijas el mismo error dos veces sin persistirlo.

### Cómo Claude Code gestiona CLAUDE.md

- El archivo se carga como **system prompt adicional** — no como contexto de usuario
- Claude lo "lee" antes de responder tu primer mensaje
- Cambios en `CLAUDE.md` se aplican al iniciar una nueva sesión o con `/memory` / `/config` según versión
- Puedes forzar recarga con `#` para añadir texto al contexto actual sin reiniciar

### Usando `#` para actualizar CLAUDE.md en vivo

En Claude Code, escribir un mensaje que empieza con `#` no pide respuesta — lo persiste como instrucción. Ejemplo:

```
# Cuando generes tests de React, usa siempre `screen.getByRole` antes que `getByTestId`.
```

Claude Code te pregunta dónde guardarlo: en `CLAUDE.md` del proyecto, en el global, o solo en memoria de la sesión. Es la forma rápida de "enseñarle" sin abrir el editor.

---

## `context/` y archivos auxiliares — cuando CLAUDE.md no alcanza

`CLAUDE.md` es para reglas que se aplican **siempre**. Pero a veces tienes contexto que solo necesitas cargar puntualmente:
- Notas de diseño de una feature en curso
- Research sobre un bug que no has terminado de entender
- Un spec grande que no quieres re-copiar cada sesión
- Decisiones arquitectónicas que aún no se consolidaron en CLAUDE.md

### El patrón `context/`

Crea un directorio `context/` en la raíz del repo (o donde prefieras) con archivos markdown temáticos:

```
context/
├── CONTEXT.md                    ← índice: qué hay aquí y cuándo usarlo
├── desarrolla_refactoriza.md     ← tu filosofía de refactor (reutilizable)
├── arquitectura_wallets.md       ← diseño actual del módulo wallets
├── bug_soft_delete_race.md       ← notas de un bug en investigación
└── migracion_python.md           ← plan en curso
```

**Cómo invocarlos:**

```
@context/arquitectura_wallets.md   ← carga el archivo al contexto de la sesión
```

El prefijo `@` en Claude Code inyecta el contenido del archivo como contexto sin que tengas que pegarlo. Puedes referenciar múltiples archivos en un solo mensaje.

### `CONTEXT.md` como índice

Un truco útil: mantén un `context/CONTEXT.md` que liste qué archivos hay y para qué sirve cada uno. Cuando empiezas una sesión nueva:

```
Lee @context/CONTEXT.md y dime cuál de los archivos listados es relevante
para lo que voy a hacer hoy: implementar el endpoint de export de wallets.
```

Claude decide por ti qué contexto cargar, y tú evitas saturar tokens con archivos irrelevantes.

### `context/` vs `CLAUDE.md` — cuándo va cada cosa

| Va en `CLAUDE.md` | Va en `context/` |
|---|---|
| Convenciones permanentes del proyecto | Notas de una feature específica en curso |
| Stack, comandos, estructura de carpetas | Research de un bug sin resolver |
| Reglas de estilo y "lo que no hacemos" | Plan temporal de migración |
| Contexto de negocio estable | Decisiones aún no consolidadas |
| Se aplica a **todas** las sesiones | Se carga **cuando lo necesitas** |

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

## Triggers de skills — cómo Claude decide invocar un skill automáticamente

Un skill no solo se invoca escribiendo `/nombre`. Claude Code lo puede **auto-invocar** cuando detecta que el contexto de la conversación coincide con el propósito del skill. Esto es lo que distingue un skill "decorativo" de un skill que realmente te libera trabajo.

### Cómo funciona el trigger

Cada skill tiene una sección de **descripción** en su frontmatter o encabezado. Claude lee todas las descripciones al cargar la sesión. Cuando tu mensaje coincide semánticamente con la descripción, Claude propone (o invoca) el skill automáticamente.

```markdown
---
name: commit
description: Use this skill when the user asks to create a git commit, commit changes, or save their work to git history. Handles staging, message generation, and pre-commit hooks.
---

# /commit — Crear commit estructurado
...
```

**Claves de una buena descripción-trigger:**
- Empezar con "Use this skill when..." le dice al modelo que es un trigger
- Enumerar los fraseos reales que un usuario usaría: "commit changes", "save to git", "create commit"
- Ser específico — una descripción genérica tipo "handles git" hace que Claude dude si invocar
- Listar el contexto en el que NO aplica, si hay ambigüedad

### Ejemplo de skill bien triggerizado

```markdown
---
name: test-gen
description: Use when the user asks to generate unit tests, add test coverage, write tests for a function/component, or mentions "I need tests for X". Applies to Jest and React Testing Library in TypeScript projects.
---

Genera tests unitarios para el código proporcionado...
```

Con esta descripción, mensajes como:
- "genérame tests para `calculateSpread`"
- "añade cobertura al componente WalletManager"
- "necesito tests para este hook"

...harán que Claude sugiera o invoque `/test-gen` solo, sin que tú recuerdes el nombre del comando.

### Evita el anti-trigger

```markdown
❌ description: "Herramienta útil para testing"
    → demasiado genérico, Claude no se atreve a invocarlo

✅ description: "Use this skill when the user asks to generate Jest
    unit tests for a specific function or React component in a
    TypeScript project. Do NOT use for e2e or integration tests."
    → específico, con casos de uso claros y un "no" explícito
```

### Skills globales vs skills del proyecto

```
~/.claude/skills/              ← globales, disponibles en todos los repos
[repo]/.claude/skills/         ← del proyecto, compartidos con el equipo via git
```

Regla práctica:
- **Global:** skills que dependen de **tu forma de trabajar** (`/commit`, `/review-qa`, `/explain-diff`)
- **Proyecto:** skills que dependen de **este repo** (`/run-db-migration`, `/gen-api-route`, `/test-wallet-module`)

---

## skill-creator — el meta-skill para crear skills

Escribir un buen skill es un arte. La descripción tiene que ser específica, el cuerpo tiene que ser claro, y los ejemplos tienen que ser representativos. Por eso existe **skill-creator**: un skill que te ayuda a crear otros skills.

### Qué hace skill-creator

Cuando lo invocas, skill-creator:
1. Te pregunta qué tarea quieres encapsular
2. Te entrevista para refinar el scope (¿siempre aplica? ¿qué inputs?)
3. Genera la descripción-trigger con el patrón "Use this skill when..."
4. Genera el cuerpo del skill con rol, contexto, tarea, formato, restricciones
5. Te propone ejemplos de few-shot si aplican
6. Escribe el archivo `.md` directamente en `.claude/skills/`

### Ejemplo real

```
Tú: /skill-creator

Claude: ¿Qué tarea quieres encapsular como skill?

Tú: Quiero un skill que revise PRs con criterio QA, priorizando bugs
    reales sobre style, y que reporte en formato crítico/mayor/menor.

Claude: Entendido. Algunas preguntas:
  1. ¿Se aplica a cualquier lenguaje o solo a TypeScript/React?
  2. ¿Debería ignorar cambios de tests, o también revisarlos?
  3. ¿Quieres que use algún skill o comando existente (ej: gh pr view)?

Tú: TypeScript/React. Tests sí, también los revisa. Que use `gh pr diff`.

Claude: [genera el archivo .claude/skills/qa-review.md con estructura
        completa y descripción-trigger optimizada]
```

### Por qué es imprescindible

Sin skill-creator, la mayoría de skills que escribes son mediocres: descripciones genéricas, sin trigger semántico claro, sin restricciones, con instrucciones ambiguas. Con skill-creator, tu biblioteca de skills crece con calidad consistente porque el que los escribe (Claude) ya entiende qué hace un buen skill.

**Regla:** la primera vez que vas a crear un skill nuevo, invoca skill-creator. Cuando ya tengas 5+ skills con el mismo patrón, puedes escribir directamente.

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

## Comandos slash — la caja de herramientas diaria

Claude Code viene con un set de comandos slash built-in. Conocerlos es la diferencia entre pelear con el entorno y volar con él. A continuación los más útiles, agrupados por propósito.

### Gestión del contexto y la sesión

| Comando | Qué hace |
|---|---|
| `/clear` | Borra todo el contexto de la conversación actual (reset limpio) |
| `/compact` | Compacta el historial actual — Claude resume y libera tokens sin perder estado |
| `/cost` | Muestra el costo acumulado de la sesión (tokens input/output y USD estimado) |
| `/resume` | Reabre una sesión anterior por ID — recupera contexto de días atrás |
| `/status` | Muestra info de la sesión: modelo, tokens usados, directorio, permisos |

**Cuándo usar cada uno:**
- `/compact` → sigues con la misma tarea pero el historial pesa mucho
- `/clear` → cambias radicalmente de tarea y el historial solo estorba
- `/resume` → retomas trabajo de ayer sin volver a cargar contexto a mano
- `/cost` → al final del día, para saber cuánto consumiste

### Configuración y modelo

| Comando | Qué hace |
|---|---|
| `/model` | Cambia el modelo en uso (Opus, Sonnet, Haiku) sin salir de Claude Code |
| `/config` | Abre el archivo `settings.json` del usuario o proyecto |
| `/permissions` | Gestiona qué herramientas Claude puede usar sin preguntar |
| `/fast` | Alterna modo rápido (respuestas más rápidas del mismo modelo) |
| `/add-dir` | Añade otro directorio al alcance de Claude (útil en monorepos) |

**Ejemplo:** cambiar a Haiku para tareas triviales y ahorrar:
```
/model
> Haiku 4.5
```

### Memoria y conocimiento del proyecto

| Comando | Qué hace |
|---|---|
| `/memory` | Abre el sistema de memoria persistente |
| `#<texto>` | Añade texto a `CLAUDE.md` o memoria sin pedir respuesta |
| `@<archivo>` | Inyecta el contenido de un archivo como contexto |

**Ejemplo combinado:**
```
# Cuando generes queries SQL, siempre usa transacciones explícitas.
@src/lib/queries/wallets/getWalletById.ts
Genera una nueva query `getWalletByName` siguiendo el mismo patrón.
```

Una sola línea `#` actualiza tu CLAUDE.md; `@` te ahorra copiar-pegar el archivo.

### Plugins, skills y agentes

| Comando | Qué hace |
|---|---|
| `/plugin` | Instala, lista o desinstala plugins del marketplace |
| `/agents` | Lista los sub-agentes disponibles y sus capacidades |
| `/hooks` | Inspecciona los hooks configurados actualmente |
| `/mcp` | Gestiona servidores MCP conectados |
| `/help` | Muestra todos los comandos disponibles |

### Comandos que deberías aprender YA

Los 5 que transforman tu flujo desde el primer día:

```
/compact    → libera tokens sin perder contexto
/clear      → reset limpio entre tareas
/model      → alterna Opus/Sonnet/Haiku según coste/calidad
/plugin     → expande Claude Code con plugins
/resume     → retoma sesiones de días anteriores
```

### El flujo diario del operador maestro

```
Lunes 9:00
├── claude               ← abre Claude Code en el repo
├── /resume              ← retoma la sesión del viernes si existe
├── (trabajas una feature completa)
├── /cost                ← revisas cuánto consumiste
├── /compact             ← compactas antes de cambiar de tarea
├── (nueva tarea: revisar PR)
├── /model → Haiku       ← cambias a modelo más barato para la revisión
├── /clear               ← reset al terminar la revisión
└── exit
```

---

## Dictado por voz — Wispr Flow y el prompt hablado

El teclado es el cuello de botella del operador promedio. Un prompt maestro bien estructurado son 200–400 palabras. Tecleando a 60 wpm eso es 4–7 minutos por prompt. Hablando a 150 wpm (tu velocidad natural al pensar en voz alta), son menos de 2 minutos — y el prompt suele salir mejor porque piensas con más contexto.

**Wispr Flow** es la herramienta que hace esto posible sin fricción. Es un dictador por voz para macOS y Windows que convierte tu habla en texto limpio, corrige gramática y puntuación sobre la marcha, y pega el resultado donde tengas el cursor. Funciona en cualquier app — incluida la terminal de Claude Code.

### Por qué funciona tan bien con Claude

Claude prospera con **contexto rico**. El problema es que teclear contexto rico es agotador — por eso la gente manda prompts anémicos tipo "arregla este bug". Cuando dictas, no te cuesta nada decir:

> *"Tengo un bug en el componente WalletManager. Cuando el usuario hace click en eliminar dos veces seguidas muy rápido, a veces se borran dos wallets en vez de una. Creo que es una race condition porque el botón no se deshabilita hasta que vuelve la respuesta del servidor. Quiero que lo investigues, confirmes la hipótesis, y si es correcta me propongas el fix mínimo sin tocar más cosas."*

Ese prompt tecleado lo habrías escrito como "bug en WalletManager, se borran 2 wallets al hacer doble click, arréglalo". Claude, con el prompt corto, responde con algo genérico. Con el prompt hablado, va directo al fix correcto.

### El atajo único

Wispr Flow se invoca con una tecla global (por defecto `Fn` o la que configures). Mantienes pulsada, hablas, sueltas, y el texto aparece donde estaba tu cursor:

```
┌──────────────────────────────────────────────┐
│ 1. Cursor en la terminal de Claude Code      │
│ 2. Mantienes Fn pulsada                      │
│ 3. Hablas tu prompt (con toda la verborrea)  │
│ 4. Sueltas Fn                                │
│ 5. Wispr limpia, pega el texto formateado    │
│ 6. Enter                                     │
└──────────────────────────────────────────────┘
```

No hay ventana emergente, no cambias de app, no copias-pegas. La latencia es casi imperceptible.

### Lo que Wispr corrige automáticamente

Cuando hablas, sale basura verbal que no quieres en el prompt. Wispr la filtra:

```
Hablas:  "eh... arréglame este, o sea, mira, el tema es que este
          componente no, no funciona cuando, eh, el usuario le da
          dos veces al botón"

Wispr:   "Arréglame este componente: no funciona cuando el usuario
          hace click dos veces en el botón."
```

- Elimina muletillas ("eh", "mira", "o sea")
- Une frases rotas
- Añade puntuación
- Capitaliza nombres técnicos si se usan mucho (Claude, React, PostgreSQL)
- Respeta el idioma — puedes mezclar español e inglés técnico en la misma frase

### Configuración recomendada para Claude Code

1. **Tecla global:** algo accesible con el meñique sin soltar el teclado (`Fn`, `Right Alt`, o una tecla en un mouse programable).
2. **Idioma principal:** español, pero activa el modo multilingüe para que reconozca términos técnicos en inglés.
3. **Diccionario personalizado:** añade términos que uses mucho y que el modelo base no reconoce bien — nombres de tu repo, librerías internas, nombres de compañeros, acrónimos del negocio.
4. **Modo "prompt":** algunas versiones permiten un modo que deja el texto tal cual, sin reformateo agresivo. Úsalo cuando dictas código o comandos shell.

### Workflow típico de prompt hablado

```
[Fn pulsada]
"Actúa como un QA senior. Contexto: tengo este archivo abierto,
src/lib/wallets/delete.ts. Quiero que lo revises buscando
específicamente race conditions y validación de input que
falte. No me menciones estilo ni naming. Formato: lista con
archivo dos puntos línea, el problema, y el fix concreto.
Máximo cinco issues priorizados por impacto."
[Fn soltada]

→ El texto aparece en la terminal ya formateado
→ Enter → Claude arranca con un prompt completo
```

El operador promedio nunca habría tecleado ese prompt completo. Lo habría abreviado a "revisa este archivo por bugs". La diferencia en calidad de respuesta es la diferencia entre operar a nivel 2 y a nivel 4.

### Cuándo NO dictar

- **Código literal:** los identificadores con guiones bajos, comillas, paréntesis — tecléalos
- **Nombres de rutas/archivos:** dictar `src/lib/wallets/delete.ts` es frágil; cópialo
- **Secretos o credenciales:** nunca dictes nada sensible, punto
- **Espacios ruidosos:** el reconocimiento degrada con ruido de fondo

### Alternativas si no tienes Wispr Flow

- **macOS dictation:** built-in, peor calidad pero gratis (`Fn Fn` por defecto)
- **SuperWhisper:** otra app Mac con calidad alta, más configurable
- **Whisper + script propio:** el modelo Whisper de OpenAI es open-source; con un script de 30 líneas puedes montar tu propio flujo
- **Talon Voice:** para quien quiere control total por voz (no solo dictado)

### El multiplicador real

La regla que descubrirás a los 3 días de empezar a dictar:

> El mejor prompt es el prompt que **escribirías si no te costara escribirlo**. Cuando dictar es gratis, escribes el prompt correcto. Y el prompt correcto es el que Claude responde bien.

Dictar no te hace 2x más rápido tecleando. Te hace 2x más probable que escribas el prompt completo en lugar del prompt mutilado. Esa es la ganancia real.

---

## Instalación y gestión de plugins

Un **plugin** en Claude Code es un paquete que puede contener:
- **Skills** (comandos slash reutilizables)
- **Sub-agentes** personalizados
- **Hooks** preconfigurados
- **Servidores MCP** (herramientas externas)
- **Reglas de CLAUDE.md** que se inyectan en el proyecto

Los plugins se instalan desde un **marketplace** (repositorio de plugins) o directamente desde una URL/git repo.

### Estructura de un plugin

```
mi-plugin/
├── plugin.json              ← metadata (nombre, versión, descripción)
├── skills/
│   ├── comando-uno.md
│   └── comando-dos.md
├── agents/
│   └── mi-agente.md
├── hooks/
│   └── post-edit.sh
└── README.md
```

### Comandos de gestión

```bash
# Listar plugins instalados
/plugin list

# Buscar en el marketplace
/plugin search <término>

# Instalar un plugin por nombre (desde el marketplace oficial)
/plugin install <nombre-plugin>

# Instalar desde un repositorio git
/plugin install https://github.com/usuario/mi-plugin

# Desinstalar
/plugin remove <nombre-plugin>

# Actualizar todos los plugins
/plugin update
```

### Dónde viven los plugins instalados

```
~/.claude/plugins/              ← globales (disponibles en todos tus repos)
[repo]/.claude/plugins/         ← específicos del proyecto
```

**Regla práctica:** instala global lo que usas en varios proyectos (un skill de commit, un agente de code review). Instala en el proyecto los plugins que solo tienen sentido en ese repo.

### Anti-patrón: el plugin mágico

```
❌ "Instalé 15 plugins y ahora Claude Code hace X, Y y Z automáticamente."
✅ "Instalé estos 3 plugins específicos porque resuelven problemas concretos
   que tenía: un skill-creator, un commit estructurado, y un MCP server para
   acceder a mi Linear."
```

Más plugins = más ruido en el contexto, más triggers compitiendo entre sí, más mantenimiento. Cada plugin que instalas debe ganarse su lugar.

---

## Ejecución automática: modo headless y CLI no interactivo

Claude Code no tiene que ser interactivo. Puedes invocarlo desde un script, un pipeline de CI, un cron o un bucle de shell. Esto desbloquea automatización pesada — desde "regenera el CHANGELOG en cada push" hasta "deja a Claude trabajando toda la noche en un bug difícil".

### El flag `-p` / `--print` — modo print

```bash
# Ejecuta Claude Code una vez, imprime la respuesta a stdout y sale
claude -p "Resume los commits del último día y extrae las decisiones relevantes"

# Con input desde archivo
cat PROMPT.md | claude -p

# Con input desde heredoc
claude -p <<'EOF'
Revisa el diff de git staged y dime si hay problemas críticos
antes de permitir el commit.
EOF
```

En modo `-p`, Claude no abre la REPL interactiva. Lee el prompt, ejecuta las herramientas necesarias (respetando los permisos), imprime la respuesta y termina.

### Flags clave para ejecución no interactiva

| Flag | Efecto |
|---|---|
| `-p` / `--print` | Modo no interactivo: ejecuta y sale |
| `--output-format json` | Salida estructurada (ideal para scripts) |
| `--output-format stream-json` | Streaming JSON — eventos a medida que ocurren |
| `--max-turns N` | Limita el número de ciclos de razonamiento |
| `--model <id>` | Fija el modelo (ej: `claude-haiku-4-5-20251001`) |
| `--append-system-prompt` | Añade instrucciones al system prompt del momento |
| `--allowedTools` | Whitelist de herramientas permitidas |
| `--disallowedTools` | Blacklist de herramientas prohibidas |
| `--dangerously-skip-permissions` | Omite prompts de permiso (¡úsalo con conciencia!) |
| `--resume <session-id>` | Retoma una sesión previa desde un script |

### Ejemplo: script de code review automatizado

```bash
#!/usr/bin/env bash
# review-pr.sh — ejecuta code review con Claude en modo headless

set -euo pipefail

PR_NUMBER=$1

# Obtiene el diff del PR
DIFF=$(gh pr diff "$PR_NUMBER")

# Pide a Claude una revisión estructurada en JSON
RESULT=$(claude -p \
  --output-format json \
  --model claude-sonnet-4-6 \
  --allowedTools "Read,Grep" \
  <<EOF
Revisa este diff con criterio QA. Reporta en JSON con este schema:
{ "critical": [...], "major": [...], "minor": [...] }

Diff:
$DIFF
EOF
)

# Parsea y publica como comentario en el PR
CRITICAL=$(echo "$RESULT" | jq '.critical | length')
if [ "$CRITICAL" -gt 0 ]; then
  echo "⚠️ $CRITICAL issues críticos encontrados"
  echo "$RESULT" | jq '.' | gh pr comment "$PR_NUMBER" --body-file -
else
  echo "✅ Sin issues críticos"
fi
```

Este script lo pones en tu CI y cada PR recibe una revisión automática antes de que un humano la vea.

### Ejemplo: hook de pre-commit con Claude

```bash
#!/usr/bin/env bash
# .git/hooks/pre-commit

STAGED=$(git diff --cached)
[ -z "$STAGED" ] && exit 0

VERDICT=$(claude -p \
  --output-format json \
  --max-turns 3 \
  --model claude-haiku-4-5-20251001 \
  <<EOF
Este es el diff staged. Responde SOLO con JSON:
{ "ok": true/false, "reason": "..." }

Criterio: bloquea solo si hay bugs evidentes o secretos hardcodeados.
No bloquees por estilo o naming.

Diff:
$STAGED
EOF
)

OK=$(echo "$VERDICT" | jq -r '.ok')
if [ "$OK" = "false" ]; then
  echo "❌ Claude bloqueó el commit:"
  echo "$VERDICT" | jq -r '.reason'
  exit 1
fi
```

Haiku es rápido y barato — perfecto para validaciones de pre-commit.

### Ejemplo: cron de salud del repo

```bash
# crontab -e
# Cada mañana a las 8:00, Claude analiza el estado del repo y envía un resumen
0 8 * * * cd ~/proyectos/cripto-spread-js && claude -p "Analiza git log de las últimas 24h, los issues abiertos y los tests en rojo. Dame un resumen en 5 bullets." | mail -s "Daily repo status" yo@ejemplo.com
```

### Cuándo usar modo headless vs interactivo

| Usa headless cuando... | Usa interactivo cuando... |
|---|---|
| La tarea se puede especificar completa de una vez | Necesitas iterar y ajustar sobre la marcha |
| Quieres automatizar en CI/cron/git hooks | Estás explorando o debuggeando |
| El output va a otro programa (jq, mail, gh) | El output es para ti leerlo |
| Conoces el coste y quieres repetibilidad | Estás aprendiendo cómo Claude aborda el problema |

---

## El patrón Ralph — bucles autónomos

"Ralph" es un patrón (más que un plugin formal) popularizado por Geoffrey Huntley que explota el modo headless para poner a Claude a trabajar en bucle hasta que una tarea esté hecha. El nombre viene de la actitud: **incansable, sin recordar lo anterior, siempre empezando de cero, pero con un objetivo claro en un archivo.**

### La esencia del patrón

```bash
#!/usr/bin/env bash
# ralph.sh — el bucle más simple del mundo
while :; do
  cat PROMPT.md | claude -p --dangerously-skip-permissions
  sleep 2
done
```

Es literalmente eso: un `while` infinito que ejecuta Claude Code en modo headless con un prompt leído desde un archivo. Cada iteración empieza con contexto limpio, lee el prompt y avanza un paso.

### Por qué funciona

La clave está en el `PROMPT.md`. Debe estar escrito de forma que Claude, al leerlo, pueda **descubrir por sí mismo** en qué punto está el trabajo y qué es lo siguiente. Algo como:

```markdown
# PROMPT.md — Migración del módulo Wallets a la nueva arquitectura

## Objetivo final
Migrar todos los archivos de src/lib/wallets/ al nuevo patrón hexagonal
documentado en docs/HEXAGONAL.md.

## Estado de progreso
Lee `docs/PROGRESS.md` para saber qué está hecho y qué falta.
Actualiza ese archivo al terminar cada paso.

## Instrucciones
1. Lee docs/PROGRESS.md
2. Identifica el siguiente archivo a migrar
3. Migra solo ese archivo
4. Actualiza docs/PROGRESS.md marcándolo como hecho
5. Si todo está marcado como hecho, escribe "DONE" en docs/PROGRESS.md y termina

## Reglas
- No migres más de un archivo por iteración
- No toques archivos que ya estén marcados como migrados
- Si te encuentras con un bloqueador, documéntalo en docs/BLOCKERS.md y continúa con el siguiente
```

Claude, en cada ciclo, lee el progreso, hace un paso incremental, lo persiste en disco, y termina. El siguiente ciclo empieza con contexto limpio pero con el estado actualizado en archivos. El trabajo converge sin que tú estés delante.

### Ralph mejorado: con condición de parada

```bash
#!/usr/bin/env bash
# ralph.sh — con parada explícita
MAX_ITER=50
i=0

while [ $i -lt $MAX_ITER ]; do
  OUTPUT=$(cat PROMPT.md | claude -p --dangerously-skip-permissions)
  echo "=== Iteración $i ==="
  echo "$OUTPUT"

  # Condición de parada: DONE en el archivo de progreso
  if grep -q "^DONE$" docs/PROGRESS.md 2>/dev/null; then
    echo "✅ Trabajo completado en $i iteraciones"
    break
  fi

  i=$((i+1))
  sleep 5
done

[ $i -ge $MAX_ITER ] && echo "⚠️ Límite alcanzado sin DONE"
```

### Cuándo es útil

- **Migraciones masivas:** refactorizar 100 archivos siguiendo el mismo patrón
- **Generación de tests:** crear suites de test para todos los módulos de un paquete
- **Limpieza iterativa:** eliminar `any` de un proyecto TypeScript archivo por archivo
- **Trabajo nocturno:** dejas Ralph corriendo, te vas a dormir, revisas por la mañana

### Cuándo NO es útil

- Tareas donde el contexto entrelazado importa (Ralph lo pierde en cada ciclo)
- Tareas donde un error se propaga (sin supervisión, Ralph puede multiplicar el desastre)
- Código crítico sin tests (Ralph puede romper cosas sin darse cuenta)

### Las 3 reglas de Ralph

> **Regla 1:** El estado vive en archivos, no en el contexto. Si el estado no se persiste entre ciclos, no funciona.

> **Regla 2:** Cada iteración debe hacer un paso pequeño y verificable. Pasos grandes = errores grandes.

> **Regla 3:** Siempre hay una condición de parada explícita. Ralph sin parada es un servicio, no una tarea.

### El pariente supervisado: `/loop`

Claude Code tiene un comando/skill nativo llamado `/loop` (en versiones recientes) que ejecuta un prompt en bucle con supervisión del modelo (decide cuándo parar). Es una versión más inteligente de Ralph:

```
/loop "Revisa los errores de TypeScript, corrige uno por iteración, y para cuando npm run typecheck pase sin errores"
```

El modelo decide la cadencia y la parada — tú solo defines el objetivo. `/loop` dinámico (sin intervalo fijo) es lo más cercano a "dejar a Claude trabajando por ti" con garantías de que va a parar solo.

---

## Otros plugins y skills imprescindibles

Un starter pack mínimo para empezar con un entorno potente:

### `commit` — commits estructurados
Skill que analiza tus cambios staged, propone un mensaje siguiendo convenciones del repo y crea el commit. Respeta los hooks pre-commit.

```
/commit
→ analiza el diff, propone "fix(wallets): corrige race condition en soft-delete"
→ pregunta si aceptas, crea el commit
```

### `review-pr` — revisión de PRs
Skill que toma un número de PR, obtiene el diff con `gh pr view`, ejecuta una revisión estructurada y publica los comentarios directamente en el PR.

```
/review-pr 342
```

### `schedule` — tareas programadas
Permite crear agentes que se ejecutan en cron. Útil para health checks, resúmenes diarios, releases nocturnos.

```
/schedule "Cada día a las 9am, analiza los issues nuevos de GitHub y clasifícalos por prioridad"
```

### `update-config` — configura hooks y settings
Skill que te ayuda a modificar `settings.json` sin memorizar la sintaxis. Especialmente útil para configurar hooks (`PreToolUse`, `PostToolUse`) con matchers correctos.

```
/update-config "Quiero que después de cada edición de archivos .ts se ejecute `npm run lint -- --fix` sobre ese archivo"
```

### MCP servers imprescindibles

Los servidores MCP (Model Context Protocol) añaden herramientas externas a Claude Code. Los más útiles:

| MCP server | Qué añade |
|---|---|
| **filesystem** | Acceso a directorios fuera del repo actual |
| **git** | Operaciones git avanzadas con semántica |
| **github** | Issues, PRs, releases directamente desde Claude |
| **postgres** / **sqlite** | Queries SQL a tu DB local |
| **puppeteer** / **playwright** | Browser automation para testing E2E |
| **slack** | Postear resúmenes o leer canales |
| **linear** / **jira** | Gestión de tickets |

**Instalación típica:**
```bash
claude mcp add postgres -- npx -y @modelcontextprotocol/server-postgres "postgresql://localhost/midb"
```

Después, desde Claude Code:
```
Consulta la tabla wallets y dime cuántas están con is_deleted=true en los últimos 30 días.
```

Claude usará el MCP server de postgres para ejecutar la query sin salir de la sesión.

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

## Agentes paralelos — el multiplicador real

La diferencia de productividad entre usuario promedio y operador maestro viene, en gran parte, de saber lanzar agentes en paralelo. No es una optimización menor: es pasar de trabajar en serie a trabajar en abanico.

### Patrón fan-out / fan-in

```
               ┌──► Agent A: investiga X
Tu contexto ───┼──► Agent B: investiga Y
               └──► Agent C: investiga Z

(los tres corren a la vez)

Tu contexto ◄── Resumen consolidado A+B+C
```

Mientras tú esperas, los tres trabajan. Recibes tres resúmenes limpios en lugar de tres investigaciones saturando tu contexto.

### Ejemplo 1 — auditoría de seguridad de un módulo

En un único turno, lanzas tres agentes independientes:

```
Tarea: auditar el módulo de wallets antes del release.

Lanzo estos 3 agentes en paralelo:

Agent A (Explore, "very thorough"):
"Busca en src/lib/wallets/ todos los puntos donde entra input externo
(params de request, body, query) y lista los que NO tienen validación
explícita con Zod. Reporta archivo:línea y el tipo de input."

Agent B (general-purpose):
"Revisa src/lib/queries/wallets/ y lista todas las queries SQL que
NO están envueltas en transacción explícita. Para cada una, indica
si debería estarlo (hay múltiples writes) o si es seguro así."

Agent C (Plan):
"Propón un plan para añadir rate limiting al endpoint
DELETE /api/wallets/[id]. Considera: restricciones actuales del
framework, patrones usados en otros endpoints del repo, impacto en
tests existentes."
```

Los tres corren a la vez. Vuelven con resúmenes concisos. Tú los lees, decides, y actúas. En serie tardarías 3x.

### Ejemplo 2 — generación de tests por módulo

```
Lanzo 4 agentes en paralelo para generar tests de 4 módulos
independientes:

Agent 1: "Genera tests unitarios para src/lib/services/spread.ts
         siguiendo las convenciones de test/unit/services/"
Agent 2: "Genera tests unitarios para src/lib/services/wallet.ts"
Agent 3: "Genera tests unitarios para src/lib/services/transaction.ts"
Agent 4: "Genera tests unitarios para src/lib/services/exchange.ts"
```

Cada uno produce su archivo `*.test.ts`. Tú los revisas en conjunto al final.

### Ejemplo 3 — exploración fan-out

Cuando no sabes qué enfoque elegir, lanzas agentes con enfoques distintos y comparas:

```
No estoy seguro de cómo abordar la migración del módulo auth.
Lanzo 3 agentes Plan en paralelo con enfoques distintos:

Agent A: "Plan para migrar auth usando NextAuth v5 manteniendo la DB actual"
Agent B: "Plan para migrar auth a Clerk (SaaS) migrando los datos existentes"
Agent C: "Plan para reescribir el módulo auth desde cero con JWT + refresh token propio"
```

Tres planes independientes, sin que los agentes se contaminen entre sí. Tú comparas y eliges.

### Cómo se lanzan en paralelo en Claude Code

La clave mecánica: **todas las llamadas a `Agent` que quieras en paralelo tienen que ir en el mismo turno del asistente**. Si las pides secuencialmente, Claude las ejecutará secuencialmente. Un único mensaje con múltiples tool calls `Agent` → corren a la vez.

```
# Prompt al operador de Claude Code:
"Lanza en paralelo estos 3 agentes: [A, B, C]"

# El modelo emite un turno con 3 Agent tool calls simultáneos
→ los 3 corren al mismo tiempo
```

### Protocolo de prompt para un agente

Cada sub-agente arranca con contexto frío. Tu prompt tiene que ser **autocontenido**:

```
❌ "Sigue revisando lo que estábamos viendo"
   (el agente no sabe qué estabas viendo)

✅ "Revisa el archivo src/lib/wallets/delete.ts (líneas 45-80).
    Objetivo: encontrar una posible race condition cuando dos requests
    llegan simultáneamente con el mismo wallet_id.
    Ya descarté problemas de validación de input — ese no es el enfoque.
    Reporta en máximo 150 palabras: existe/no existe, evidencia, fix
    sugerido."
```

El prompt perfecto para un agente incluye:
- **Qué:** el objetivo específico
- **Dónde:** archivos o módulos relevantes
- **Qué ya descartaste:** para no desperdiciar ciclos
- **Formato de respuesta:** longitud y estructura

### Paralelo + worktree = refactor seguro

La combinación letal para cambios grandes:

```
Agent A (worktree): "Refactoriza el módulo wallets al nuevo patrón"
Agent B (worktree): "Refactoriza el módulo addresses al nuevo patrón"
Agent C (worktree): "Refactoriza el módulo transactions al nuevo patrón"
```

Cada agente trabaja en una rama aislada. Si los tres terminan bien, mergeas. Si uno falla, descartas solo ese. Tu main nunca se rompe.

### Cuándo NO paralelizar

- **Dependencias entre tareas:** si B necesita el resultado de A, no las lances a la vez
- **Coste sensible:** N agentes = N veces el coste. Paraleliza con conciencia
- **Tareas ambiguas:** lanzar 5 agentes para una tarea mal definida es 5x el desperdicio

### Secuencial con memoria en archivos — el híbrido

Cuando hay dependencia pero quieres evitar que tu contexto se sature, usa el patrón "secuencial con estado en archivos":

```
1. Agent A: "Analiza el bug y escribe el diagnóstico en docs/diagnosis.md"
   (tú no recibes el diagnóstico completo, solo un OK)

2. Agent B: "Lee docs/diagnosis.md e implementa el fix"
   (B carga el contexto de A desde disco, no desde tu conversación)
```

Tu contexto principal no se contamina. Los agentes se pasan información via archivos, como pipes entre procesos.

---

## Sub-agentes personalizados

Además de los built-in (`general-purpose`, `Explore`, `Plan`, `claude-code-guide`), puedes definir tus propios sub-agentes. Viven en:

```
~/.claude/agents/         ← globales
[repo]/.claude/agents/    ← del proyecto
```

### Anatomía de un sub-agente personalizado

```markdown
---
name: qa-auditor
description: Use when the user needs an independent QA audit of a module or feature before release. Runs structured checks on validation, error handling, edge cases, and test coverage. Produces a report in critical/major/minor format.
tools: Read, Grep, Glob, Bash
---

# QA Auditor

Eres un QA Lead senior con 10 años en fintech. Tu trabajo es auditar
el código proporcionado como si estuvieras bloqueando un release.

## Proceso obligatorio

1. Lee todos los archivos relevantes al módulo indicado
2. Para cada archivo, evalúa:
   - Validación de inputs externos
   - Manejo de errores async
   - Edge cases (null, empty, concurrent)
   - Cobertura de tests existentes vs código real

3. Prioriza issues por impacto en producción

## Formato de salida obligatorio

### 🔴 Crítico
[Lista con: archivo:línea | problema | fix]

### 🟡 Mayor
[Lista con: archivo:línea | problema | fix]

### 🟢 Menor
[Lista con: archivo:línea | problema | fix]

### ✅ Verificado sin issues
[Áreas que revisaste y están limpias]

## Restricciones
- No reportes issues de estilo o naming
- No propongas refactors no pedidos
- Si no puedes determinar si algo es un bug, dilo explícitamente
```

Ahora puedes invocarlo con:

```
Agent({
  subagent_type: "qa-auditor",
  description: "Auditoría módulo wallets",
  prompt: "Audita src/lib/wallets/ antes del release v2.4.0"
})
```

### Por qué definir agentes propios

- **Reproducibilidad:** el mismo agente, con los mismos criterios, cada vez
- **Disciplina:** el formato de salida obligatorio evita divagaciones
- **Composición:** puedes tener `qa-auditor`, `security-auditor`, `perf-auditor` y lanzarlos en paralelo

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

# PARTE IX — CONCEPTOS AVANZADOS

---

## MCP — el protocolo que conecta Claude con todo lo demás

MCP (Model Context Protocol) es la forma estándar en que Claude Code añade herramientas externas a su toolbox. Un servidor MCP expone tools, resources y prompts que Claude puede invocar igual que sus herramientas built-in (Read, Edit, etc.).

### Arquitectura mental

```
┌──────────────┐     stdio/HTTP      ┌────────────────────┐
│ Claude Code  │ ◄─────MCP─────────► │ MCP Server         │
│              │                     │ (Python/Node/Rust) │
└──────────────┘                     └────────────────────┘
                                             │
                                             ▼
                                     ┌──────────────────┐
                                     │ Sistema externo  │
                                     │ (DB, API, FS...) │
                                     └──────────────────┘
```

Claude no habla directamente con tu DB. Habla con un MCP server que traduce las peticiones de Claude a operaciones sobre la DB.

### Instalar un MCP server

```bash
# Añadir un MCP server globalmente
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# Con variables de entorno
claude mcp add github -e GITHUB_TOKEN=$GH_TOKEN -- npx -y @modelcontextprotocol/server-github

# Listar MCPs instalados
claude mcp list

# Remover
claude mcp remove github
```

### Ejemplo: MCP de postgres en acción

```
Tú: ¿Cuántas wallets con is_deleted=true tengo en los últimos 30 días?

Claude: [usa la tool `query` del MCP de postgres]
  SELECT COUNT(*) FROM wallets WHERE is_deleted=true AND updated_at > now() - interval '30 days';

  Resultado: 47 wallets

Tú: De esas, ¿cuántas tenían operaciones asociadas?

Claude: [otra query al MCP]
  SELECT COUNT(DISTINCT w.id) FROM wallets w JOIN operations o ON o.wallet_id=w.id WHERE w.is_deleted=true;

  Resultado: 12 wallets
```

Claude usa el MCP como lo haría un humano con `psql`, pero sin salir de la sesión.

### MCP servers que cambian el juego

| MCP | Para qué |
|---|---|
| `filesystem` | Sandbox controlado de acceso a archivos fuera del repo |
| `git` | Git semántico (commits por significado, no por comando) |
| `github` / `gitlab` | Issues, PRs, releases desde la conversación |
| `postgres` / `sqlite` / `mysql` | SQL directo sobre tus DBs |
| `puppeteer` / `playwright` | Navegación web y scraping |
| `slack` | Leer canales, postear mensajes |
| `linear` / `jira` / `notion` | Gestión de tickets y docs |
| `memory` | Memoria persistente gestionada por el MCP |
| `fetch` | HTTP genérico (APIs externas) |

### Cuándo escribir tu propio MCP

Escribe un MCP cuando:
- Tienes un sistema interno único (CRM propio, API privada, DB específica)
- Necesitas lógica custom entre Claude y una API (transformaciones, auth compleja)
- Quieres exponer las mismas tools a varios proyectos con una sola fuente de verdad

No escribas uno cuando:
- Ya existe uno oficial (busca primero en el registry de MCP)
- Solo necesitas una cosa puntual — un script Bash + `Bash` tool es más simple
- La integración es throwaway — no vale la mantención

### Esqueleto mínimo de un MCP server (Python)

```python
# mi_mcp.py
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("mi-sistema-interno")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_wallet_info",
            description="Obtiene info de una wallet por ID interno",
            inputSchema={
                "type": "object",
                "properties": {
                    "wallet_id": {"type": "string"}
                },
                "required": ["wallet_id"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name, args):
    if name == "get_wallet_info":
        wallet = mi_db.find_wallet(args["wallet_id"])
        return [TextContent(type="text", text=str(wallet))]

if __name__ == "__main__":
    server.run_stdio()
```

Después:
```bash
claude mcp add mi-sistema -- python /ruta/a/mi_mcp.py
```

---

## Hooks avanzados — el sistema nervioso del entorno

Los hooks no son solo "corre un comando después de editar". Con matchers y variables de entorno puedes construir un sistema reactivo completo.

### Variables disponibles en hooks

```
$CLAUDE_TOOL_NAME       ← nombre de la tool que Claude usó (Edit, Bash, ...)
$CLAUDE_FILE_PATH       ← archivo afectado (si aplica)
$CLAUDE_TOOL_INPUT      ← input completo del tool call
$CLAUDE_TOOL_OUTPUT     ← output del tool call (en PostToolUse)
$CLAUDE_SESSION_ID      ← ID de la sesión actual
```

### Patrón: matcher por tipo de archivo

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "case \"$CLAUDE_FILE_PATH\" in *.ts|*.tsx) npx eslint --fix \"$CLAUDE_FILE_PATH\" ;; *.py) ruff check --fix \"$CLAUDE_FILE_PATH\" ;; esac"
          }
        ]
      }
    ]
  }
}
```

Un único hook que aplica linters diferentes según el lenguaje del archivo editado.

### Patrón: bloquear operaciones peligrosas

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$CLAUDE_TOOL_INPUT\" | grep -qE 'rm -rf|DROP TABLE|git push.*--force' && { echo 'BLOQUEADO: comando peligroso'; exit 1; } || exit 0"
          }
        ]
      }
    ]
  }
}
```

Un pre-hook que retorna exit != 0 bloquea la ejecución del tool. Úsalo como red de seguridad contra comandos destructivos.

### Patrón: auto-commit tras editar

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cd $(pwd) && git diff --quiet || git add -A && git commit -m 'claude: cambios automáticos sesión $CLAUDE_SESSION_ID' --no-verify 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

(Úsalo con cuidado — solo en repos experimentales donde cada sesión debe quedar trazada.)

### Patrón: notificaciones a tu terminal externa

```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Necesita tu atención' 2>/dev/null || terminal-notifier -title 'Claude' -message 'Atención' 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

---

## Composición de workflows — cuando skills, agentes y hooks se orquestan juntos

El operador maestro no piensa en "skill" o "agente" o "hook" por separado. Piensa en **workflows** — combinaciones que resuelven un problema de principio a fin.

### Workflow: release check completo

```
┌─────────────────────────────────────────────────────────┐
│ Skill: /release-check                                    │
│                                                          │
│  1. Lee CHANGELOG.md y extrae la versión a releasear     │
│                                                          │
│  2. Lanza en paralelo:                                   │
│     ├── Agent qa-auditor: audita src/                    │
│     ├── Agent security-scan: busca secretos hardcodeados │
│     └── Agent test-runner: ejecuta suite completa        │
│                                                          │
│  3. Consolida los 3 reportes en un informe único         │
│                                                          │
│  4. Si todo OK → genera el git tag                       │
│     Si hay issues → imprime reporte y no tagea           │
│                                                          │
│  Hook Stop: envía el resultado a Slack vía MCP           │
└─────────────────────────────────────────────────────────┘
```

Ejecución real:
```
/release-check 2.4.0
```
Y Claude orquesta todo. Tú lees el resultado en Slack desde tu móvil.

### Workflow: debugging de producción

```
┌──────────────────────────────────────────────────────┐
│ 1. Sesión nueva con contexto limpio                   │
│ 2. @logs/error-2026-04-11.log   (carga el log)        │
│ 3. Agent Plan: "propón 3 hipótesis sobre la causa"    │
│ 4. (apruebas una hipótesis)                           │
│ 5. Agent general-purpose (worktree): "implementa el    │
│    fix para la hipótesis N, con tests de regresión"   │
│ 6. /review-pr (sobre el worktree)                     │
│ 7. Merge si pasa el review                            │
└──────────────────────────────────────────────────────┘
```

Cada paso está encapsulado en una herramienta. Tú diriges, Claude ejecuta.

---

## Prompt caching avanzado — técnicas de uso

Si usas la API directamente o un MCP que lo soporte, el prompt caching puede reducir costes entre 50% y 90% cuando reutilizas contexto grande.

### Estrategia: prefix estable

Estructura tu prompt para que todo lo que NO cambia esté al principio, y lo que cambia al final:

```python
messages = [{
    "role": "user",
    "content": [
        # ← todo esto se cachéa (1 cache write, N-1 cache reads)
        {
            "type": "text",
            "text": SYSTEM_INSTRUCTIONS,            # no cambia
            "cache_control": {"type": "ephemeral"}
        },
        {
            "type": "text",
            "text": KNOWLEDGE_BASE_GRANDE,          # no cambia
            "cache_control": {"type": "ephemeral"}
        },
        # ← esto es lo único que varía entre llamadas
        {
            "type": "text",
            "text": pregunta_del_usuario
        }
    ]
}]
```

El TTL del cache es ~5 minutos. Si llamas >1 vez dentro de esa ventana, la segunda llamada paga ~10% del coste del contexto cacheado.

### Anti-patrón: invalidar el cache por orden

Si mueves una línea del prefix, el cache se invalida. Mantén el orden estable entre llamadas.

```
❌ Llamada 1: [A, B, C, pregunta]
❌ Llamada 2: [A, C, B, pregunta]   ← cache miss porque B y C cambiaron de posición

✅ Llamada 1: [A, B, C, pregunta_1]
✅ Llamada 2: [A, B, C, pregunta_2]   ← cache hit
```

---

## ReAct, Tool Use y el loop del agente

Para entender a fondo cómo funcionan los agentes (y por qué a veces fallan), necesitas entender el loop **ReAct**:

```
Reason → Act → Observe → Reason → Act → ...

1. Reason: Claude piensa qué tool llamar y por qué
2. Act: invoca la tool (Edit, Bash, MCP...)
3. Observe: recibe el resultado
4. Loop: con el nuevo observation, vuelve a razonar
```

### Cómo se traduce esto a tu experiencia

Cuando le pides a Claude "arregla el bug", por dentro:
1. Razona que necesita leer el archivo → invoca Read
2. Recibe el contenido → razona que el error está en la línea X
3. Invoca Edit para corregir
4. Razona que debería correr los tests → invoca Bash
5. Recibe el output → si pasan, termina; si fallan, razona de nuevo

### Por qué a veces falla

- **Contexto saturado:** el loop pierde coherencia porque el historial es demasiado largo
- **Tool no disponible:** Claude razona que necesita algo que no tiene (ej: acceso a internet sin fetch MCP)
- **Observation mal formada:** el resultado del tool es demasiado grande o ambiguo
- **Objetivo ambiguo:** Claude no sabe cuándo parar porque no definiste la condición de éxito

### Diagnóstico de loops rotos

```
Síntoma: Claude repite la misma acción varias veces.
Causa: el observation no le da nueva información. Rompe el loop manualmente
       y reformula el objetivo.

Síntoma: Claude "se va por las ramas" y llama tools no pedidas.
Causa: prompt con objetivo impreciso. Añade restricciones claras.

Síntoma: Claude se detiene antes de terminar.
Causa: alcanzó el max_turns o decidió que el objetivo estaba cumplido
       cuando no lo estaba. Da un criterio de éxito verificable
       ("termina cuando `npm test` pase en verde").
```

---

## El operador como arquitecto de sistemas

La última etapa de la maestría es dejar de pensar en Claude como "un asistente al que le mandas tareas" y empezar a diseñarlo como **un sistema que ejecuta políticas que tú defines**.

### La metáfora correcta

```
Antes (usuario promedio):       Claude como teclado mágico
                                 "le escribo, él escribe"

Después (operador maestro):     Claude como sistema operativo
                                 "defino políticas, hooks, skills,
                                  agentes y MCPs. El sistema opera.
                                  Yo superviso excepciones."
```

### Las 5 preguntas del arquitecto

Antes de empezar una tarea compleja, pregúntate:

1. **¿Es repetible?** → Si sí, merece un skill.
2. **¿Es paralelizable?** → Si sí, merece agentes en paralelo.
3. **¿Necesita aislamiento?** → Si sí, merece un worktree.
4. **¿Depende de sistemas externos?** → Si sí, merece un MCP.
5. **¿Debe pasar sin supervisión?** → Si sí, merece un hook o un cron.

Cada "sí" te mueve hacia arriba en la escala de sofisticación del operador.

### El objetivo final

Tu trabajo no es teclear prompts. Tu trabajo es construir el entorno donde Claude opera con mínima fricción y máxima capacidad. Cuando lo hagas bien, notarás que pasas más tiempo **configurando el sistema** que **usándolo**, y que tu productividad sube no porque trabajes más rápido, sino porque el sistema trabaja por ti mientras duermes.

---

# PARTE X — REFERENCIA RÁPIDA

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
| `/model` | Alterna modelo (Opus / Sonnet / Haiku) |
| `/resume` | Retoma una sesión anterior |
| `/status` | Info de la sesión actual |
| `/plugin` | Instalar, listar, actualizar plugins |
| `/mcp` | Gestionar servidores MCP |
| `/agents` | Listar sub-agentes disponibles |
| `/hooks` | Ver hooks configurados |
| `/permissions` | Gestionar permisos de tools |
| `/help` | Lista todos los comandos |
| `#texto` | Añade texto a CLAUDE.md / memoria |
| `@archivo` | Inyecta un archivo como contexto |

---

## Flags de Claude Code en modo headless

| Flag | Uso |
|---|---|
| `-p "prompt"` | Ejecución no interactiva (print mode) |
| `--output-format json` | Salida estructurada |
| `--output-format stream-json` | Streaming de eventos |
| `--max-turns N` | Limita ciclos de razonamiento |
| `--model <id>` | Fija el modelo a usar |
| `--append-system-prompt "..."` | Añade instrucciones al system prompt |
| `--allowedTools "Read,Grep"` | Whitelist de herramientas |
| `--disallowedTools "Bash"` | Blacklist de herramientas |
| `--dangerously-skip-permissions` | Omite confirmaciones (CI/automation) |
| `--resume <id>` | Retoma sesión por ID |

---

## Glosario del operador maestro

| Término | Definición operativa |
|---|---|
| **Token** | Unidad mínima de texto que Claude procesa. ~0.75 palabras. |
| **Contexto** | Todo lo que Claude puede "leer" en una sesión. |
| **Compactación** | Resumir el historial para liberar tokens. |
| **Skill** | Prompt encapsulado en un archivo `.md` invocable con `/comando`. |
| **Trigger de skill** | Descripción-semántica que hace que Claude auto-invoque un skill cuando detecta un contexto coincidente. |
| **skill-creator** | Meta-skill que te ayuda a diseñar y escribir nuevos skills. |
| **Hook** | Comando que se ejecuta automáticamente en respuesta a eventos de Claude Code. |
| **Sub-agente** | Instancia separada de Claude que trabaja en aislamiento. |
| **Agentes paralelos** | Varios sub-agentes lanzados en el mismo turno, corriendo simultáneamente. |
| **Worktree** | Copia aislada del repo donde trabaja un sub-agente. |
| **Plugin** | Paquete que agrupa skills, agentes, hooks y/o MCP servers. |
| **MCP** | Model Context Protocol: estándar para conectar Claude con sistemas externos. |
| **Modo headless** | Ejecución no interactiva de Claude Code con `-p` / `--print`. |
| **Ralph** | Patrón de bucle autónomo que ejecuta Claude Code en modo headless hasta completar una tarea. |
| **Fan-out / fan-in** | Patrón de lanzar N agentes en paralelo y consolidar sus resultados. |
| **CLAUDE.md** | System prompt persistente del proyecto. |
| **context/** | Directorio con archivos markdown auxiliares cargables con `@`. |
| **Memoria** | Archivos que se cargan en cada sesión para dar contexto sobre el usuario y el proyecto. |
| **ReAct loop** | Reason + Act: el ciclo que siguen los agentes autónomos. |
| **Prompt caching** | Mecanismo de la API para cachear partes del prompt y reducir costo. |
| **Few-shot** | Técnica de dar ejemplos en el prompt para que Claude imite el patrón. |
| **CoT** | Chain of Thought: razonamiento paso a paso antes de la respuesta. |

---

*Fin del curso — Claude Uso Maestro*
*Versión 1.0 · Perfil QA · Abril 2026*
