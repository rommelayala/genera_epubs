# Skills de IA — De la Teoría al Poder Real
### Un libro-curso-tutorial · Framework 5W1H

---

# PARTE I — CONTEXTO AMPLIO

---

## WHAT — ¿Qué es un skill?

Un skill es una **instrucción especializada y reutilizable** que le dices a una IA cómo comportarse ante una tarea concreta.

No es un agente — no actúa solo. No es un prompt casual — tiene estructura, proceso y restricciones. Es el punto medio entre los dos.

```
Prompt casual     →  "revisa este código"
Skill             →  /dev  (proceso definido, criterios claros, output predecible)
Agente autónomo   →  revisa, corrige, testea y hace commit sin que lo pidas
```

**La diferencia que importa:**

| | Prompt casual | Skill | Agente |
|---|---|---|---|
| Resultado | Variable | Predecible | Autónomo |
| Activación | Siempre manual | Manual bajo demanda | Puede ser automático |
| Proceso | Implícito | Explícito y definido | Decide solo |
| Reusabilidad | Ninguna | Alta | Alta |

Un skill es básicamente **empaquetar tu criterio experto** en una instrucción que cualquiera puede invocar con un comando.

---

## WHO — ¿Quién los crea y quién los usa?

### Creadores
- **Desarrolladores individuales** — automatizan sus propias revisiones y workflows
- **Equipos de ingeniería** — estandarizan procesos en el repositorio (`.claude/commands/`)
- **Empresas** — empaquetan conocimiento institucional (cómo hacer un PR, cómo revisar seguridad)
- **La comunidad open source** — comparten skills públicos (como recetas)

### Usuarios
- **El mismo que lo creó** — para no repetir el mismo prompt cada vez
- **Compañeros de equipo** — el skill vive en el repo y todos lo comparten
- **Colaboradores nuevos** — onboarding: el skill ya sabe cómo trabaja el equipo

### El actor más valioso
Un senior que empaqueta su criterio en un skill. Sus 10 años de experiencia revisando código se convierten en un comando `/review` que cualquier junior puede invocar.

---

## WHY — ¿Por qué existen?

### El problema que resuelven
El conocimiento experto es difícil de transferir. Los seniors dan feedback inconsistente según el día. Los procesos se documentan pero nadie los lee. Los prompts buenos se pierden en el historial del chat.

Un skill resuelve los tres problemas:
- **Consistencia** — el mismo criterio siempre, sin importar quién lo invoca
- **Transferibilidad** — el conocimiento vive en un archivo, no en la cabeza de alguien
- **Velocidad** — un comando reemplaza 5 minutos de explicación

### La visión de largo plazo
Los skills son la forma en que los equipos van a **institucionalizar el trabajo con IA**. En lugar de que cada persona tenga sus propios prompts privados, el equipo construye una librería compartida de skills que representa cómo ese equipo trabaja.

Es el equivalente a tener un `Makefile` pero para criterio intelectual, no para comandos de terminal.

---

## WHEN — ¿Cuándo aparecieron? ¿Cuándo usarlos?

### Historia rápida

| Año | Hito |
|-----|------|
| 2020–2022 | "Prompt engineering" — la gente descubre que el cómo preguntas importa |
| 2023 | Repositorios públicos de prompts (AwesomePrompts, FlowGPT) — primera sistematización |
| 2023 | OpenAI introduce GPTs personalizados — skills con interfaz gráfica |
| 2024 | Claude introduce `/commands` en Claude Code — skills como archivos en el repo |
| 2024 | Cursor, Windsurf, Copilot añaden sistemas similares de instrucciones persistentes |
| 2025 | Los skills se versionan con git, se revisan en PRs, se comparten como paquetes |

### ¿Cuándo crear un skill vs escribir un prompt directo?

**Escribe un prompt directo cuando:**
- Es una tarea que harás una sola vez
- El contexto es único e irrepetible
- La variación es parte del valor

**Crea un skill cuando:**
- Repites el mismo tipo de tarea más de 3 veces
- Otras personas necesitan hacer lo mismo
- Quieres que el resultado sea predecible y auditble
- El proceso tiene pasos que se pueden olvidar

**Regla del pulgar:** si has escrito el mismo prompt dos veces, la tercera vez debería ser un skill.

---

## WHERE — ¿Dónde viven?

### En Claude Code — 3 niveles de scope

```
~/.claude/commands/          → Global: disponible en TODOS tus proyectos
.claude/commands/            → Proyecto: disponible para todo el equipo que clone el repo
.claude/commands/subdir/     → Subdirectorio: disponible solo en esa carpeta
```

El scope más específico siempre gana. Si tienes `/review` global y `/review` en el proyecto, el del proyecto sobrescribe al global.

### En otros sistemas

| Plataforma | Dónde viven los skills |
|---|---|
| **OpenAI GPTs** | Interfaz web, configuración del GPT personalizado |
| **Cursor** | `.cursorrules` + `@rules` en el chat |
| **Copilot** | `.github/copilot-instructions.md` |
| **Gemini** | Gems (versión de Google de los GPTs personalizados) |
| **LangChain** | Chains y Runnables — skills como código Python |

### El skill como artefacto de equipo
Cuando el skill vive en `.claude/commands/` dentro del repositorio, ocurre algo importante: **se versiona con git**. Eso significa:

- Se revisa en pull requests como cualquier otro código
- Tiene historial de cambios
- Se puede revertir si algo sale mal
- Nuevos miembros del equipo lo tienen automáticamente al clonar

---

## HOW — ¿Cómo funcionan?

### Anatomía de un skill en Claude Code

Un skill es un archivo `.md` con un prompt estructurado. Nada más. No hay código especial, no hay API, no hay configuración extra.

```markdown
# Nombre del skill

Descripción de qué hace y cuándo usarlo.

## Proceso
1. Paso uno
2. Paso dos
3. Paso tres

## Criterios
- Criterio A
- Criterio B

## Restricciones
- No hagas X
- Siempre verifica Y
```

Cuando escribes `/nombre-del-skill`, Claude Code:
1. Busca el archivo `.claude/commands/nombre-del-skill.md`
2. Lo carga como instrucción del sistema
3. Ejecuta el proceso definido sobre el contexto actual

### Variables disponibles en el prompt
Puedes referenciar contexto dinámico dentro del skill:

```markdown
Analiza el archivo $ARGUMENTS
Contexto del proyecto: $PROJECT
```

`$ARGUMENTS` captura lo que escribas después del comando:
```
/review components/Hero.tsx   →  $ARGUMENTS = "components/Hero.tsx"
```

### Patrones de diseño para skills

**Patrón 1 — El Checklist**
El skill es una lista de verificación que Claude aplica sistemáticamente.
```markdown
## Checklist de seguridad
- [ ] ¿Hay variables de entorno expuestas?
- [ ] ¿Las queries SQL están parametrizadas?
- [ ] ¿Los endpoints tienen autenticación?
```

**Patrón 2 — El Proceso**
El skill define un flujo de trabajo paso a paso.
```markdown
## Proceso de code review
1. Lee el diff completo antes de comentar
2. Identifica problemas de lógica primero
3. Luego estilo y convenciones
4. Sugiere tests para casos no cubiertos
```

**Patrón 3 — El Personaje**
El skill define un rol con perspectiva específica.
```markdown
Actúa como un auditor de seguridad con mentalidad de atacante.
Tu objetivo es encontrar vulnerabilidades, no validar el código.
```

**Patrón 4 — El Transformador**
El skill toma un input y produce un output específico.
```markdown
Dado el código en $ARGUMENTS:
1. Extrae todos los endpoints de la API
2. Genera la documentación OpenAPI 3.0
3. Identifica endpoints sin documentar
```

---

# PARTE II — CASOS ESPECÍFICOS

---

## Skills en Claude Code — El sistema más maduro

### Estructura completa

```
.claude/
  commands/
    dev.md          →  /dev   (revisión DRY + SOLID)
    review.md       →  /review (code review con criterios del equipo)
    commit.md       →  /commit (genera mensajes de commit estructurados)
    deploy.md       →  /deploy (checklist pre-deploy)
    security.md     →  /security (auditoría de seguridad)
```

### El skill `/commit` — ejemplo real de valor inmediato

El problema: los mensajes de commit son inconsistentes. "fix", "update", "changes", "asdfg".

El skill:
```markdown
# Commit Message Generator

Lee el diff staged con `git diff --staged`.
Genera un mensaje de commit siguiendo Conventional Commits:

Formato: type(scope): description

Types: feat, fix, refactor, docs, test, chore, style
- feat: nueva funcionalidad
- fix: corrección de bug
- refactor: refactorización sin cambio de comportamiento

Reglas:
- Máximo 72 caracteres en la primera línea
- Imperativo presente: "add" no "added", "fix" no "fixed"
- Si el cambio no es obvio, añade cuerpo explicando el POR QUÉ
```

Resultado: cada commit del equipo sigue el mismo estándar. El historial de git se vuelve legible. Los changelogs se pueden generar automáticamente.

### El skill como documentación viva

A diferencia de un `CONTRIBUTING.md` que nadie lee, un skill se invoca activamente. El proceso de revisión de código no está en una wiki — está en `/review` y Claude lo aplica cada vez.

---

## GPTs de OpenAI — Skills con interfaz gráfica

### Qué son
Los GPTs personalizados de OpenAI son skills con una capa de producto encima. Tienen nombre, descripción, icono, y se pueden publicar en el GPT Store.

### Cómo se definen
```
Nombre: "Senior Code Reviewer"
Descripción: "Reviews code with the perspective of a senior engineer"
Instrucciones: [el equivalente al .md del skill]
Capacidades: ✓ Web browsing  ✓ Code interpreter  ✗ Image generation
Acciones: [APIs externas que puede llamar]
```

### Lo que los diferencia de un skill en Claude Code
- **Distribución:** un GPT se puede compartir con millones de usuarios vía URL
- **Monetización:** OpenAI paga a creadores populares (GPT Store)
- **Sin acceso al repo:** el GPT no puede leer tu código directamente
- **Interfaz propia:** cada GPT tiene su propia URL y puede tener un flujo de conversación guiado

### Caso interesante — GPT "Consensus"
Un GPT especializado en buscar papers científicos y sintetizar el consenso académico sobre cualquier pregunta. Conecta con bases de datos de papers reales. Es un skill de investigación académica empaquetado para cualquier usuario sin conocimientos técnicos.

---

## Cursor Rules — Skills embebidos en el editor

### Qué son
Cursor (editor de código basado en VS Code con IA) tiene un sistema de reglas que funciona como skills siempre activos para el contexto de código.

```
.cursor/rules/
  general.mdc       →  reglas generales del proyecto
  react.mdc         →  reglas específicas para componentes React
  api.mdc           →  reglas para endpoints de API
```

### La diferencia clave
En Claude Code, `/dev` es bajo demanda — lo invocas cuando quieres. En Cursor, las rules son **siempre activas** — se aplican automáticamente a cada sugerencia de código.

```
Claude Code:  skill = on-demand
Cursor rules: skill = always-on
```

### Ejemplo de .cursorrules para un equipo

```markdown
# Reglas del proyecto

## TypeScript
- Siempre usar tipos explícitos, nunca `any`
- Interfaces para objetos de dominio, types para uniones

## React
- Componentes funcionales únicamente
- useState solo para estado local, Zustand para estado global
- No usar useEffect para lógica de negocio

## Testing
- Cada función de utilidad debe tener tests unitarios
- Los componentes se testean con React Testing Library
- No mockear módulos internos, solo dependencias externas
```

Cada vez que Copilot o el AI de Cursor sugiere código, lo hace respetando estas reglas automáticamente.

---

## El Skill Raro — "Rubber Duck" con criterio

### El concepto
El "rubber duck debugging" es una técnica clásica: explicarle tu problema a un pato de goma (o cualquier objeto inanimado) te fuerza a articularlo claramente, y en ese proceso encuentras la solución.

Un skill de rubber duck con IA lo lleva al siguiente nivel:

```markdown
# Rubber Duck Debug

No resuelvas el problema directamente.
Haz preguntas socráticas que fuercen al usuario a pensar:

1. "¿Qué esperabas que pasara exactamente?"
2. "¿En qué paso específico diverge el comportamiento?"
3. "¿Has verificado que los datos de entrada son los que crees?"
4. "¿Qué cambiarías si tuvieras que empezar de cero?"

Nunca des la respuesta. Guía hacia ella con preguntas.
Si el usuario insiste en que le des la solución, recuérdale
que el objetivo es que la encuentre él mismo.
```

**Por qué es raro:** va contra el instinto de la IA (y del usuario) de resolver el problema directamente. Pero los estudios muestran que encontrar la solución uno mismo produce un aprendizaje 10x más profundo.

---

## El Skill que se Salta las Reglas — El "Modo Sin Filtros"

### Contexto
En Claude Code, puedes crear skills que cambien el comportamiento por defecto del asistente dentro del contexto del proyecto.

### Lo que algunos equipos hacen

**Skill de feedback brutal:**
```markdown
# Brutal Honesty Review

Actúa como el CTO más exigente que existe.
No suavices el feedback. No uses frases como:
- "Podrías considerar..."
- "Una posible mejora sería..."
- "Está bastante bien pero..."

Dí exactamente lo que está mal y por qué es un problema.
Si el código es malo, dí que es malo.
Si la arquitectura no escala, dí que no escala.
El objetivo es encontrar todos los problemas antes de producción.
```

**Por qué funciona:** en revisiones de código normales, la gente suaviza el feedback para no herir sensibilidades. Esto permite que problemas reales lleguen a producción. Un skill de feedback brutal (con consentimiento del equipo) elimina ese filtro.

### El límite ético — Skills de manipulación

Aquí es donde los skills se vuelven problemáticos. Existen en la comunidad skills diseñados para:

- **Generar contenido persuasivo sin revelar que es IA** — "Escribe este artículo de tal forma que parezca escrito por un humano experto"
- **Eludir restricciones del modelo** — skills que usan framing de roleplay o ficción para obtener información que el modelo normalmente rechazaría
- **Simular personalidades falsas** — "Actúa como un experto médico certificado" cuando no lo eres

El problema no es el skill en sí — es la intención y el contexto. El mismo skill de "escribe de forma persuasiva" puede ser legítimo (marketing honesto) o manipulador (desinformación).

**La regla de oro:** si el skill oculta información relevante al usuario final o lo induce a creer algo falso, es un problema ético, no una cuestión técnica.

---

# PARTE III — SÍNTESIS

## Cómo diseñar un skill que realmente funcione

**1. Define el output antes que el proceso**
Empieza por el final: ¿cómo es el resultado perfecto? Trabaja hacia atrás para definir los pasos.

**2. Sé específico sobre el scope**
"Revisa el código" es vago. "Identifica violaciones de principio de responsabilidad única en componentes React y sugiere cómo separarlos" es un skill.

**3. Define las restricciones explícitamente**
Lo que el skill NO debe hacer es tan importante como lo que sí debe hacer. Sin restricciones, la IA tiende a hacer demasiado.

**4. Incluye ejemplos del output esperado**
Un ejemplo de buen resultado dentro del skill guía al modelo mejor que cualquier descripción abstracta.

**5. Versiona y trata el skill como código**
- Ponlo en control de versiones
- Revísalo cuando el proceso cambia
- Documenta por qué se tomaron ciertas decisiones de diseño

---

## Los 4 anti-patrones de skills

**Anti-patrón 1 — El skill todo-en-uno**
Un skill que hace revisión de código, genera documentación, Y crea tests. Viola Single Responsibility. Crea tres skills separados.

**Anti-patrón 2 — El skill sin proceso**
```markdown
# Code Review
Revisa el código que te dé.
```
Sin proceso definido, el resultado es tan variable como un prompt casual.

**Anti-patrón 3 — El skill sin restricciones**
Sin definir qué NO hacer, la IA improvisa. Y la improvisación en procesos críticos es riesgo.

**Anti-patrón 4 — El skill que nunca se actualiza**
Un skill escrito hace 6 meses puede estar desalineado con cómo trabaja el equipo hoy. Los skills necesitan mantenimiento como el código.

---

## Glosario rápido

| Término | Definición |
|---|---|
| **Skill** | Instrucción especializada y reutilizable empaquetada como comando |
| **Slash command** | La forma de invocar un skill (`/nombre`) |
| **Scope** | Nivel de disponibilidad del skill (global, proyecto, subdirectorio) |
| **Prompt engineering** | Arte de diseñar instrucciones efectivas para modelos de lenguaje |
| **System prompt** | Instrucciones base que definen el comportamiento del modelo en una sesión |
| **Few-shot** | Técnica de incluir ejemplos dentro del prompt para guiar el output |
| **Chain of thought** | Técnica de pedir al modelo que razone paso a paso antes de responder |
| **Conventional Commits** | Estándar de mensajes de commit: `type(scope): description` |
| **Rubber duck debugging** | Técnica de articular un problema en voz alta para encontrar la solución |
| **CLAUDE.md** | Archivo de contexto persistente cargado automáticamente en cada sesión |

---

*Documento generado como material de estudio personal · AIQ® 2026*
