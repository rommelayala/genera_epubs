# Entrena tu Propia IA en Local: Aprendizaje Autónomo con Recursos Limitados

---

# Prólogo

### Para quién es este libro

Este libro es para ti si:

- Tienes una GPU de 8–16 GB (RTX 4060, RTX 4070, A10, M3/M4 Pro/Max, o similar)
- Quieres entrenar y mejorar tu propio modelo sin dependencias de OpenAI, Claude o Gemini
- No quieres gastar $500/mes en APIs de IA, pero sí invertir 2–3 horas en aprender
- Eres ingeniero, científico de datos, desarrollador o simplemente alguien que come IA cruda
- Te aterra la idea de "black boxes" y quieres entender qué está pasando dentro de tu modelo
- Tienes datos propios (códigos, documentos, logs) que quieres que tu modelo entienda mejor

### Para quién NO es este libro

Este libro **no es para ti** si:

- Esperas que tu modelo local compita con GPT-4o mañana por la mañana (no va a pasar)
- Prefieres un botón rojo que "aprenda solo" sin tocar nada (no existen)
- Tu GPU tiene menos de 8 GB de VRAM (te quedarás a mitad del camino)
- Quieres entrenar desde cero un modelo de 70B parámetros (necesitarías 8 GPUs profesionales)
- No tienes paciencia para leer comandos y ejecutarlos en terminal

Si eres de los anteriores, sigue con las APIs comerciales. No hay vergüenza en eso.

### Qué hardware es suficiente (y qué no necesitas)

**Suficiente:**
- GPU: RTX 4060 (8GB), RTX 4070 (12GB), RTX 4090 (24GB), A10 (24GB), M3/M4 Pro/Max (18-36GB)
- RAM: 32 GB mínimo (16 GB extremadamente ajustado)
- Almacenamiento: 500 GB libres (2 TB si vas a experimentar mucho)
- Internet: conexión estándar (no necesitas fibra, pero no puedes estar offline)

**NO necesitas:**
- Un cluster de servidores
- TPUs (las GPUs de consumo son suficientes)
- Una red profesional privada
- Hardware especializado para IA
- Un PhD en machine learning (créeme, el sentido común y la paciencia son más valiosos)

**Si tienes menos:**
- GPU < 8 GB: puedes hacer RAG y un poco de fine-tuning con QLoRA extremadamente ajustado
- RAM < 32 GB: mucho más lento, menos modelos en paralelo, pero viable
- Almacenamiento < 500 GB: descarga modelos bajo demanda (menos conveniente)

### El ciclo que aprenderás

Tu modelo mejora en este orden. Este es el mapa visual de todo el libro:

```
┌─────────────────────────────────────────────────┐
│  1. Elige modelo base (Ollama / Hugging Face)  │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────▼──────────┐
        │  2. Instala locally  │  (Windows/Mac/Linux)
        └──────────┬───────────┘
                   │
    ┌──────────────▼──────────────┐
    │  3. RAG: Tus datos → vectores │  (sin reentrenamiento)
    └──────────────┬───────────────┘
                   │
    ┌──────────────▼──────────────┐
    │  4. Fine-tune con QLoRA      │  (entrenamiento ligero)
    └──────────────┬───────────────┘
                   │
    ┌──────────────▼──────────────┐
    │  5. Destila de modelos grandes │  (comprime conocimiento)
    └──────────────┬───────────────┘
                   │
    ┌──────────────▼──────────────┐
    │  6. Fusiona especialistas    │  (combina fuerzas)
    └──────────────┬───────────────┘
                   │
    ┌──────────────▼──────────────┐
    │  7. Multi-agente autónomo    │  (colaboración local)
    └──────────────┬───────────────┘
                   │
    ┌──────────────▼──────────────┐
    │  8. Ciclo de mejora continua │  (actualización semanal)
    └──────────────────────────────┘
```

Cada flecha representa un paso que ejecutarás con código real. Al final, tienes un sistema que se mejora a sí mismo cada semana sin intervención manual.

---

# Capítulo 1 — Fundamentos: Qué está pasando realmente

### 1.1 Tres conceptos que parecen iguales (pero no lo son)

La gente usa indistintamente "entrenar", "fine-tunear", "inferir" como si fueran lo mismo. No lo son. Y esta es la razón por la que muchas personas gastan dinero sin razón.

#### Inferencia

**Qué es:** hacer una pregunta a un modelo que ya está entrenado y listo.

**Analogía:** Es como consultar con un amigo que tiene 10 años de experiencia. Ya sabe todo. Tú solo haces la pregunta. Tu amigo piensa y responde.

**Costo:** Bajo. Mínimo cómputo. Dura segundos (o minutos si el modelo es grande).

**Ejemplo:**
```bash
ollama run llama3.2 "¿Cuál es la capital de Francia?"
```

El modelo ya existe. Tú lo utilizas. Listo.

#### Entrenamiento desde cero

**Qué es:** crear un modelo completamente nuevo a partir de datos sin procesar.

Es como meter a alguien sin experiencia en una escuela durante 4 años, dándole millones de libros, y esperar que al final sea un experto.

**Costo:** Extremadamente alto. Semanas o meses. Requiere miles de GPUs o una GPU profesional durante días/semanas.

**Ejemplo:**
Entrenar desde cero a LLaMA-3 (70B parámetros) requirió 16,000 GPUs Nvidia H100 durante 7 días.

⚠️ **No vas a entrenar desde cero.** Punto. No es viable con tu hardware.

#### Fine-tuning

**Qué es:** tomar un modelo ya entrenado (tu amigo experimentado) y enseñarle nuevas cosas específicas.

Es como decirle al amigo: "Ya sé que eres experto en muchas cosas, pero ahora voy a enseñarte sobre mi industria específica, mis procesos, mi jerga, mis datos".

**Costo:** Bajo a medio. Horas, no días. Viable en GPU de 8 GB.

**Ejemplo:**
```
Modelo base: LLaMA-3.2-1B (ya entiende español, código, contexto)
Datos nuevos: Tus 10,000 documentos internos sobre procesos de QA
Resultado: Un modelo que entiende QA exactamente como lo hace tu empresa
Tiempo: 4 horas en GPU de 8 GB
```

✅ **Esto sí es viable.** Y es lo central de este libro.

### 1.2 ¿Por qué un modelo local no aprende solo con preguntas?

Aquí viene el concepto que más sorprende a la gente.

**Un modelo NO aprende haciendo inferencia.**

Si haces 1,000 preguntas a un modelo y cada pregunta tiene respuestas correctas, el modelo sigue siendo idéntico. Sus pesos no cambian.

Es como hablarle a tu amigo experto 1,000 veces. Él puede responder mejor cada vez (porque con contexto responde mejor), pero su conocimiento fundamental no cambia. Él no está aprendiendo. Solo está usando mejor lo que ya sabe.

#### ¿Cómo aprende entonces?

Mediante **entrenamiento**. Y entrenar significa:

1. Mostrarle ejemplos de entrada-salida correctos
2. Medir qué tan mal está respondiendo (loss)
3. Ajustar sus pesos internos (gradientes, backpropagation)
4. Repetir con el siguiente lote de ejemplos
5. Después de millones de ejemplos, el modelo es diferente (mejorado)

#### Entonces, ¿RAG no es "aprendizaje"?

No. RAG es un **truco muy inteligente**, pero no es aprendizaje.

RAG = "Búsqueda Aumentada por Generación"

Lo que hace: en lugar de confiar solo en el conocimiento del modelo, **busca información relevante en una base de datos** y se la pasa al modelo para que responda mejor.

**Analogía:**
- Modelo sin RAG: tu amigo de 10 años de experiencia responde de cabeza
- Modelo con RAG: tu amigo tiene Wikipedia abierta. Antes de responder, busca información, la lee, y luego responde

¿Está más acertado? Sí. ¿Aprendió? No. Solo tiene acceso a más información.

**Consecuencia:** RAG es increíblemente útil pero tiene límites. Si tu pregunta es algo que nadie escribió nunca en tu base de datos, RAG no ayuda.

### 1.3 Tabla: RAG vs Fine-tuning vs Destilación

Aquí está la pregunta crucial: **¿Cuándo uso cada uno?**

| Característica | RAG | Fine-tuning | Destilación |
|---|---|---|---|
| **¿Requiere reentrenamiento?** | No | Sí | Sí |
| **¿Dónde va el conocimiento?** | Base de datos externa | Pesos del modelo | Modelo destilado |
| **Tiempo de implementación** | Horas | Horas a días | Días a semanas |
| **GPU necesaria** | Ninguna (solo CPU) | 8+ GB | 12+ GB (para modelo grande) |
| **¿El modelo ocupa menos espacio?** | No | No | Sí (2-10x más pequeño) |
| **¿Qué pasa si tus datos cambian?** | Actualiza la DB, listo | Debes reentrenar | Debes redestilar |
| **¿Funciona sin internet?** | Sí (si la DB está local) | Sí | Sí |
| **Ejemplo de caso de uso** | "Responde preguntas sobre mis 10,000 PDFs" | "Nuestro modelo debe entender nuestra jerga interna" | "Necesito un modelo de 1B que sepa como uno de 70B" |

**La verdad cruda:**

- RAG es la opción fácil y rápida. Úsalo primero.
- Fine-tuning es cuando RAG no es suficiente (porque tu modelo no "piensa" como necesitas).
- Destilación es cuando necesitas un modelo más pequeño y rápido, pero con el conocimiento de uno más grande.

#### Un ejemplo real de la vida

Digamos que eres CEO de una startup de análisis de logs.

**Mes 1:** Necesitas que un modelo responda preguntas sobre logs de tu cliente. RAG + Ollama. Subes PDFs con documentación de logs. Listo en 3 horas.

**Mes 2:** Te das cuenta de que necesitas instrucciones muy específicas al modelo (output en JSON, pasos exactos, etc.). Cambias de LLaMA a Hermes porque es mejor siguiendo instrucciones estructuradas. Hermes produce JSON consistente sin que tengas que hacer prompt engineering complicado.

**Mes 4:** El modelo sigue cometiendo errores en casos de borde. Haces fine-tuning de Hermes con 500 conversaciones reales con clientes. Ahora el modelo "piensa" como un especialista en logs Y sigue instrucciones perfectamente.

**Mes 8:** Necesitas que el modelo sea 10x más rápido para servir a 1,000 usuarios. Destilas de tu modelo Hermes fine-tuneado a uno pequeño. Obtienes 90% de precisión en 1/10 del tiempo.

**Mes 12:** Combinas tu modelo destilado especialista con otro modelo destilado especialista en anomalías. Tienes un super-modelo. Fusión de modelos.

Este es el ciclo que aprenderás en este libro. Y verás que la elección del modelo base (como Hermes) afecta todas las fases posteriores.

### 1.4 ¿Por qué tu GPU de 8 GB es suficiente?

Porque usaremos **QLoRA**.

QLoRA es una técnica que reduce la VRAM necesaria para fine-tuning en un factor de 4-10x.

**Sin QLoRA:** entrenar un modelo de 7B parámetros = 40-60 GB de VRAM necesario

**Con QLoRA:** entrenar un modelo de 7B parámetros = 6-8 GB de VRAM necesario

¿Cómo? No te voy a meter ecuaciones matemáticas ahora. La idea simple es:

- Guardas el modelo en una precisión menor (cuantización a 4 bits)
- Solo entrenas una pequeña parte nueva (adaptadores LoRA)
- El resto del modelo se congela y ocupa menos espacio

Resultado: un modelo fine-tuneado de la misma calidad, pero sin gastarte $10,000 en GPUs.

### 1.5 Errores que comete el 90% cuando empieza

❌ **Error 1:** "Voy a hacer fine-tuning con RAG incluido"

No. Son cosas separadas. Primero haces RAG. Después, si RAG no es suficiente, haces fine-tuning.

❌ **Error 2:** "Voy a entrenar mi modelo desde cero para que sea único"

Eso no es viable. Toma lo que Llama, Phi, Qwen ya entrenaron (años de trabajo + miles de GPUs). Fine-túnealo con TUS datos. Es 100x más efectivo.

❌ **Error 3:** "Más datos = modelo mejor"

Falso. Calidad > Cantidad. 500 ejemplos limpios superan 50,000 ruidosos.

❌ **Error 4:** "Una vez fine-tuneado, el modelo mejora mágicamente"

No. Fine-tuning es una fotografía de un momento. Si cambias tus datos, debes reentrenar.

❌ **Error 5:** "Mi GPU de 6 GB puede hacer todo lo que hace una de 24 GB, solo más lentamente"

Falso. Con 6 GB literalmente no puedes cargar ciertos modelos. No es un problema de velocidad. Es un problema duro.

### 1.6 Qué aprenderás en cada capítulo

**Capítulo 2:** Configurarás tu entorno. Instalarás Ollama, elegirás un modelo base, verificarás que todo funciona.

**Capítulo 3:** Crearás una base de conocimiento RAG. Subirás tus propios documentos, crearás embeddings, harás búsqueda vectorial.

**Capítulo 4:** Fine-tunearás un modelo con tus datos usando QLoRA. Verás exactamente qué cambia en el modelo.

**Capítulo 5:** Destilarás un modelo grande en uno pequeño. Mantendrás 90% de la precisión con 1/10 del tamaño.

**Capítulo 6:** Crearás un sistema multi-agente. Varios modelos trabajando juntos, cada uno especialista en algo.

**Capítulo 7:** Fusionarás dos modelos especializados en uno solo. Mejoras de ambos, tamaño de uno.

**Capítulo 8:** Automatizarás el ciclo completo. Tu modelo mejora cada semana sin que toques nada.

**Capítulo 9:** Proyecto final: una IA que se actualiza sola.

---

## Conclusión del Capítulo 1

No es magia. Es mecánica.

Tu modelo mejora porque:
1. Le das datos nuevos (que no vio durante entrenamiento original)
2. Ajustas sus pesos
3. Verificas que mejoró

Repetir eso 100 veces = un modelo muy bueno.

El hardware que tienes es suficiente. Las técnicas son abiertas (QLoRA, destilación, fusión). El código es gratuito (Hugging Face, transformers, unsloth).

Lo que te falta es el ciclo. Y eso es lo que este libro te enseña.

**Próxima parada:** Capítulo 2. Instalarás todo, elegirás tu modelo, y harás tu primer inference.

---

# Capítulo 2 — Configuración del Entorno: Tu Primer Modelo Funcionando

### 2.1 Modelos base recomendados: la elección correcta

Hay cientos de modelos. Pero no todos son iguales para tu caso de uso.

Aquí están los mejores modelos para fine-tuning y destilación en GPUs de 8–16 GB, en orden de recomendación:

#### Gemma 3

- **Tamaño:** 2B, 7B
- **VRAM mínima:** 2B = 4 GB | 7B = 8 GB
- **¿Por qué?** Diseñado por Google específicamente para ser destilable. Conocimiento de modelos enormes comprimido en parámetros mínimos.
- **Mejor para:** Si quieres destilación futura o un modelo que ocupe poco.
- **Desventaja:** Menos especializado que Phi en código.

#### Phi 4

- **Tamaño:** 4B, 14B
- **VRAM mínima:** 4B = 6 GB | 14B = 12 GB
- **¿Por qué?** Excelente relación tamaño/inteligencia. Microsoft lo entrenó para razonamiento y código. Fine-tuning muy limpio.
- **Mejor para:** Proyectos que requieren lógica y código.
- **Desventaja:** Menos experiencia comunitaria que Llama.

#### LLaMA 3.2

- **Tamaño:** 1B, 3B, 8B, 70B
- **VRAM mínima:** 1B = 2 GB | 3B = 4 GB | 8B = 8 GB
- **¿Por qué?** El estándar de la industria. Más modelos fine-tuneados, más comunidad, más compatibilidad.
- **Mejor para:** Si no sabes qué elegir, elige este.
- **Desventaja:** La versión 1B/3B es básica. La 8B ya requiere 8 GB.

#### Qwen 3.5

- **Tamaño:** 3B, 7B, 32B
- **VRAM mínima:** 3B = 5 GB | 7B = 8 GB | 32B = 20 GB
- **¿Por qué?** Entrenado con enormes cantidades de código chino y inglés. Comprensión de contexto excepcional.
- **Mejor para:** Proyectos complejos, análisis de datos, código.
- **Desventaja:** Comunidad más pequeña en occidente.

#### Mistral 7B

- **Tamaño:** 7B
- **VRAM mínima:** 8 GB
- **¿Por qué?** Muy veloz. Buena precisión. Excelente arquitectura.
- **Mejor para:** Producción, cuando necesitas velocidad.
- **Desventaja:** No es tan destilable como Gemma.

#### Hermes 3

- **Tamaño:** 8B, 70B
- **VRAM mínima:** 8B = 8 GB | 70B = 40 GB
- **¿Por qué?** Entrenado por NousResearch específicamente para seguir instrucciones y razonamiento profundo. Excelente con tareas estructuradas. Fine-tuning limpio y predecible.
- **Mejor para:** Proyectos que requieren exactitud en instrucciones, análisis paso-a-paso, generación estructurada (JSON, código formateado).
- **Desventaja:** Comunidad más pequeña que Llama, pero creciendo rápidamente.
- **Dato interesante:** Hermes 8B frecuentemente supera a Llama 2 13B en benchmarks de razonamiento. Muy subestimado.

**Versiones de Hermes:**
- **Hermes-2-Pro:** La versión anterior, sigue siendo muy buena
- **Hermes-3:** La más reciente, mejoras en razonamiento y matemáticas
- **Hermes-3-Llama-3.1-70B:** Si tu GPU lo permite (40+ GB), es una bestia

**Patrón de uso recomendado:** Usa Hermes si necesitas que el modelo siga instrucciones muy específicas o produzca salidas estructuradas. Es más determinístico que otros modelos.

### 2.2 Matriz de decisión: ¿Cuál elijo?

```
¿Tu GPU tiene 8 GB?
  → Sí → ¿Necesitas instrucciones estructuradas?
        → Sí → Hermes 8B
        → No  → ¿Necesitas código?
                → Sí → Phi 4 (4B)
                → No  → Gemma 3 (7B) o LLaMA 3.2 (8B)
  → No (< 8 GB) → Gemma 3 (2B) o LLaMA 3.2 (1B)

¿Tu GPU tiene 12+ GB?
  → Sí → ¿Necesitas máxima inteligencia?
        → Sí → LLaMA 3.2 (8B) o Phi 4 (14B) o Hermes (8B con espacio)
        → No  → Cualquiera de los anteriores

¿Tu GPU tiene 20+ GB?
  → Sí → Qwen 3.5 (32B) o LLaMA 3.2 (70B) o Hermes-3 (70B)
  → Pero recuerda: para fine-tuning usa el modelo MENOR que sea viable
```

**Mi recomendación personal para empezar:**

Si quieres razonamiento y comunidad grande: **LLaMA 3.2 (8B)**

Si quieres instrucciones limpias y salidas estructuradas: **Hermes 8B**

Si quieres el mejor balance para tu primer proyecto: **Hermes 8B** (es subestimado y funciona mejor que esperarías)

### 2.3 Instalación paso a paso

Voy a cubrir Windows, Mac (Intel y Apple Silicon), y Linux.

#### Paso 1: Descargar Ollama

Ollama es tu gestor local de modelos. Es como Docker pero para modelos de IA.

**Windows:**
1. Ve a https://ollama.ai/download
2. Descarga el instalador para Windows
3. Ejecuta el instalador
4. Reinicia tu computadora

**Mac:**
1. Ve a https://ollama.ai/download
2. Descarga el instalador para macOS
3. Abre el DMG, arrastra Ollama a Applications
4. Abre Ollama desde Applications

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install -y ollama
```

#### Paso 2: Verificar que Ollama instaló correctamente

Abre una terminal y escribe:

```bash
ollama --version
```

Deberías ver algo como:
```
ollama version 0.1.X
```

Si no ves nada, Ollama no se instaló correctamente. Reinstala.

#### Paso 3: Descargar tu primer modelo

**Opción A: LLaMA (la estándar)**
```bash
ollama pull llama3.2
```

**Opción B: Hermes (si prefieres instrucciones limpias)**
```bash
ollama pull hermes3
```

**Opción C: Ambos** (si tienes espacio y quieres comparar)
```bash
ollama pull llama3.2
ollama pull hermes3
```

Esto descarga el modelo. Dependiendo de tu conexión, tomará 5-30 minutos.

⚠️ **Espera a que termine.** No interrumpas. Si se interrumpe, ejecuta el comando de nuevo. Ollama continuará desde donde se quedó.

#### Paso 4: Ejecutar tu primer inference

**Con LLaMA:**
```bash
ollama run llama3.2 "¿Cuál es la capital de Francia?"
```

**Con Hermes:**
```bash
ollama run hermes3 "¿Cuál es la capital de Francia?"
```

Deberías ver (después de 5-10 segundos):

```
La capital de Francia es París.
```

✅ **Felicidades.** Tu entorno está funcional.

### 2.4 Verificación del entorno: diagnóstico completo

Ahora vamos a verificar que todo está optimizado para lo que viene.

#### Paso 1: Verificar tu GPU

**Windows (Nvidia):**
```bash
nvidia-smi
```

Deberías ver algo como:
```
NVIDIA-SMI 535.XX
GPU Memory: XXXX MiB / XXXX MiB
```

**Mac (Apple Silicon):**
```bash
system_profiler SPDisplaysDataType | grep -i vram
```

Deberías ver tu VRAM de GPU.

**Linux (Nvidia):**
```bash
nvidia-smi
```

#### Paso 2: Verificar que Ollama ve tu GPU

```bash
ollama show llama3.2
```

Busca una línea que diga `gpu:` o similar. Si ves números, tu GPU está activa.

❌ Si ves `gpu: 0%`, Ollama está usando solo CPU (lento). Significa que CUDA/Metal no está instalado correctamente. Reinstala tu driver de GPU.

#### Paso 3: Benchmark básico

Ejecuta un modelo pequeño y grande, y mide tiempo:

```bash
time ollama run llama3.2 "Escribe un poema sobre programación"
```

Deberías ver:
- Modelo pequeño (1-3B): respuesta en 5-15 segundos
- Modelo mediano (7B): respuesta en 20-60 segundos
- Modelo grande (70B): respuesta en 2-10 minutos

Si tu modelo demora más de 2 minutos en responder 100 tokens, algo está mal. Probablemente CUDA no está acelerada.

### 2.5 Qué características buscar en un modelo para fine-tuneable y destilable

No todos los modelos son iguales. Para el propósito de este libro, necesitas características específicas.

#### Característica 1: Arquitectura moderna

✅ **Buenas:**
- Transformers con Attention
- GQA (Grouped Query Attention) = más rápido
- Flash Attention = más eficiente

❌ **Malas:**
- Modelos antiguos (GPT-2, BERT sin modificar)
- Arquitecturas experimentales sin soporte en `transformers`

**Cómo verificarlo:** Ve a Hugging Face y busca "Transformer". Si lo ves, está bien.

#### Característica 2: Compatible con LoRA

No todos los modelos pueden fine-tunearse con LoRA. Necesitas que la arquitectura soporte adaptadores.

**Cómo verificarlo:**
```python
from peft import LoraConfig, get_peft_model
# Si esto no tira error, el modelo es LoRA-compatible
```

Todos los modelos que recomendé (Llama, Phi, Gemma, Qwen) lo son.

#### Característica 3: Pequeño pero potente

Para destilación, necesitas que el modelo base sea "destilable". Esto significa que tiene suficiente capacidad para aprender del conocimiento de un modelo más grande.

**Regla simple:**
- Modelo base: 7B o menos
- Modelo a destilar: 70B o menos

Si intentas destilar un modelo de 140B a uno de 1B, los resultados son pobres.

#### Característica 4: Entrenado con datos relevantes

Un modelo entrenado solo con código no es ideal para análisis de textos legales. Y viceversa.

```
Modelo              Mejor para
─────────────────────────────────
LLaMA               Propósito general
Phi                 Código y razonamiento
Qwen                Código y análisis complejos
Gemma               Propósito general (destilable)
Mistral             Velocidad, producción
Hermes              Instrucciones estructuradas, razonamiento
```

### 2.6 ¿Necesitas más poder? Estrategias de expansión de hardware

En algún momento te encontrarás con un problema real:

> "Mi GPU de 8 GB se queda sin memoria cuando intento hacer X"

O quizás:

> "Tardaría 3 semanas en entrenar esto. Necesito hacerlo en 3 días"

Aquí tienes dos caminos: expandir localmente o usar computación externa. Voy a darte ambas estrategias.

#### Opción A: Expansión interna (tu máquina, componentes nuevos)

**Estrategia 1: Actualizar GPU**

Es la más directa pero la más cara.

```
Tu GPU actual     Upgrade recomendado     Costo aprox.    Mejora
─────────────────────────────────────────────────────────────────
RTX 4060 (8GB) → RTX 4070 (12GB)        $600-800        +50% VRAM
RTX 4070 (12GB) → RTX 4080 (16GB)       $1200-1500      +33% VRAM
RTX 4090 (24GB) → A100 (80GB)           $10,000+        10x VRAM
```

⚠️ **Realidad:** Una GPU más grande NO hace todo 10x más rápido. Hace ciertas cosas (como fine-tuning de modelos grandes) viables, pero no es milagro.

✅ **Vale la pena si:**
- Necesitas entrenar modelos de 20B+ parámetros
- Quieres parallelismo (múltiples procesos simultáneos)
- Planeas vender servicios de IA

❌ **No vale la pena si:**
- Solo necesitas hacer RAG e inference
- Tu GPU actual maneja tus tareas actuales
- Dinero es limitado (hay alternativas mejores)

**Estrategia 2: Agregar más RAM del sistema**

Más barata que GPU. A veces crucial.

```bash
# Ver RAM actual
free -h  # Linux
vm_stat  # Mac
```

Si tienes menos de 32 GB, agregar a 64 GB cuesta $100-200 y es muy rentable. Tu sistema puede hacer caché inteligente, operaciones en paralelo, etc.

**Estrategia 3: Múltiples GPUs locales**

Si tienes una GPU, agregar una segunda (o tercera) en la misma máquina multiplica capacidad.

```bash
# Ver todas tus GPUs
nvidia-smi
```

⚠️ **Complicación:** Paralelizar requiere código especial (Distributed Data Parallel, pipeline parallelism). No es tan simple como "compra 2 GPUs y listo".

**Costo-beneficio:** Solo viable si tu máquina soporte múltiples GPUs (motherboard, PSU, espacio físico).

#### Opción B: Expansión externa (computación en cloud)

**Estrategia 1: Google Colab (Gratuito, con limitaciones)**

Pros:
- Gratis (o $10/mes para Colab Pro)
- GPU K80/T4/A100 disponible
- Jupyter notebook integrado
- Ideal para experimentos rápidos

Contras:
- Sesión muere después de 12 horas (pro) o 30 minutos sin usar
- No puedes dejar modelos entrenando overnight
- Ancho de banda limitado para descargar modelos grandes
- No es reproducible (la GPU que obtengas varía)

✅ **Ideal para:** Prototiping, aprendizaje, un fine-tuning único que no necesite ser exacto.

**Estrategia 2: Runpod (GPU rentada, barata)**

Pros:
- $0.30-0.50/hora por A40 (24GB VRAM)
- $0.70-1.00/hora por A100 (80GB)
- Alquilas por minutos, no por suscripción
- Puedes dejar entrenando días
- Acceso a muchos modelos preinstalados

Contras:
- Costos se acumulan rápido (30 horas × $0.40 = $12)
- Necesitas transferir modelos (descarga lenta)
- Interfaz menos pulida que AWS

✅ **Ideal para:** Fine-tuning serio que no puedes hacer en local, destilación de modelos grandes.

**Ejemplo de costo:**
```
Tu modelo: 7B, batch_size=4, 100 horas entrenamiento
- Local en RTX 4060: 100 horas / 0.5 = 200 horas reales = ~$0 (lo pagas con electricidad)
- Runpod A40: 100 horas × $0.40 = $40
- AWS p3.2xlarge: 100 horas × $3.06 = $306

Veredicto: Runpod gana si necesitas velocidad. Local gana si tienes tiempo.
```

**Estrategia 3: Together AI (acceso a modelos remotos)**

No es GPU rentada. Es "usa nuestros modelos ya entrenados".

Pros:
- $0.001-0.01 por millón de tokens (ultra barato)
- No necesitas GPU, solo internet
- Fine-tuning en cloud (ellos entrenan, tú pagas)

Contras:
- Solo funciona para modelos que ellos hospeden
- No es control total (usas su infraestructura)
- Latencia varía (0.5-2s por respuesta típicamente)

✅ **Ideal para:** Producción sin GPU local. Escalabilidad automática.

**Estrategia 4: Kaggle Notebooks (Gratuito, limitado)**

Pros:
- GPU P100 / T4 gratuita
- 30 horas/semana
- Buena integración con Hugging Face

Contras:
- Menos VRAM que Colab
- Interfaz poco intuitiva
- Comunidad más pequeña que Colab

✅ **Ideal para:** Experimentos cuando Colab está saturado.

#### Opción C: Estrategia híbrida (lo mejor de ambos mundos)

Esto es lo que hacen equipos profesionales:

**Fase 1: Desarrollo local**
- Usa tu GPU de 8 GB
- Itera rápido con datasets pequeños
- Prueba código, hiperparámetros

**Fase 2: Entrenamiento en cloud**
- Cuando el código funciona, escala en Runpod
- Entrena con full dataset
- Guarda modelo resultante

**Fase 3: Deployment local**
- Descarga modelo entrenado
- Sirve en tu máquina o en servidor local
- Cero costos de infraestructura recurrente

**Ejemplo de flujo:**
```
Día 1 (Local, gratis):
  - Descargas 10% de datos
  - Fine-túneas 1 hora
  - Ves que funciona

Día 2-3 (Runpod, $40):
  - Subes script validado
  - Entrenas con 100% datos
  - Esperas ~50 horas

Día 4+ (Local, gratis):
  - Descargas modelo
  - Lo usas en Ollama
  - Cero gastos mensuales
```

#### Tabla decisional: ¿Qué opción elegir?

```
¿Necesitas hacerlo hoy?
  → Sí, en 3 horas → Google Colab (gratuito)
  → Sí, en 24 horas → Runpod A40 ($10-15)
  → Sí, es crítico → AWS p3 ($100-300)
  → No urgente → Espera y usa local

¿Es un experimento único?
  → Sí → Runpod (paga por minuto, no suscripción)
  → No, repetido → Considera actualizar tu GPU

¿Presupuesto?
  → $0 → Colab/Kaggle (gratuito, con límites)
  → $100-500/mes → Runpod bajo demanda
  → $500+ → GPU propia (RTX 4090) + dedicado

¿Cuántos GB de VRAM necesitas?
  → 8-12 GB → Local (probablemente suficiente)
  → 12-24 GB → Runpod T4/A40
  → 24-80 GB → Runpod A100 / AWS p3
  → 80+ GB → AWS DGX / cloud profesional
```

**Mi recomendación:**
1. **Comienza con tu GPU actual.** No es limitante para 80% de lo que querrás hacer.
2. **Si necesitas speedup:** Runpod + Colab (híbrido). Costo bajo, no compromiso.
3. **Si escalas a producción:** Actualiza a RTX 4090 o súbete a un VPS con GPU.

### 2.7 Construir un cluster casero: tu plataforma escalable para AIs

Este es el futuro que la mayoría no ve.

No necesitas una empresa con millones. No necesitas comprar servidores nuevos.

**Necesitas:**
1. Una máquina inicial (la que tienes ahora)
2. Máquinas viejas/baratas que agregues poco a poco
3. Un software que las una y coordine

Resultado: una plataforma donde tus modelos viven, se entrenan, se mejoran. Automáticamente.

#### Concepto 1: Paralelismo en una GPU

Primero, entiende qué pasa dentro de UNA GPU.

Una GPU no es 1 procesador. Son miles. Una RTX 4070 tiene ~5,888 "cores" (núcleos).

Cuando ejecutas:
```python
forward_pass = modelo(datos)  # 1 línea de código
```

Internamente, miles de operaciones suceden en paralelo:
```
GPU Core 1 → calcula multiplicación de matriz A
GPU Core 2 → calcula multiplicación de matriz B
GPU Core 3 → calcula multiplicación de matriz C
... × 5,885 más cores
↓
Resultado final en 1ms
```

Sin GPU (en CPU):
```
CPU Core 1 → calcula A (10ms)
CPU Core 1 → calcula B (10ms)
CPU Core 1 → calcula C (10ms)
... = 30ms total
```

**Conclusión:** Una GPU ya es paralela. Pero solo usa 1 GPU.

#### Concepto 2: Múltiples GPUs en la misma máquina

Si tienes 2-3 GPUs en tu ordenador, puedes paralelizar aún más:

**Data Parallelism (lo más fácil):**
```
Dataset: 1,000 ejemplos

GPU 1 → procesa ejemplos 0-499 (en paralelo)
GPU 2 → procesa ejemplos 500-999 (en paralelo)
↓
Combinan resultados
```

Resultado: **2x más rápido** (aproximadamente).

#### Concepto 3: Múltiples máquinas conectadas (clustering)

Ahora viene lo interesante.

Imagina que tienes:
- Máquina 1: RTX 4070 (12GB)
- Máquina 2: RTX 3060 vieja (6GB)
- Máquina 3: Solo CPU pero potente (32 GB RAM)

Las conectas con Ethernet (wifi también funciona, pero es lento).

Software las coordina:
```
Máquina 1 (GPU fuerte) → Entrena modelo grande
Máquina 2 (GPU media)  → Entrena modelo mediano
Máquina 3 (CPU)        → Prepara datos, RAG, vectorización
↓
Todas en paralelo, simultáneamente
```

**Capacidad resultante:** 24GB VRAM efectiva + procesamiento de datos en paralelo.

#### Arquitectura de un cluster casero

Aquí está el diagrama de cómo crece:

```
SEMANA 1 (Fase inicial):
┌─────────────────────┐
│   Máquina Principal │
│  GPU: RTX 4070 (12G)│
│  RAM: 32GB          │
│  CPU: Ryzen 7       │
│  Rol: Entrenamiento │
└─────────────────────┘

SEMANA 4 (Agregar nodo 2):
┌──────────────────────────────────────────┐
│                  CLUSTER                 │
├──────────────┬──────────────────────────┤
│ Máquina 1    │     Máquina 2 (usada)    │
│ RTX 4070     │     GPU: GTX 1080 (8GB)  │
│ Entrena      │     Entrena paralelo     │
│ LLaMA 8B     │     o procesamiento      │
└──────────────┴──────────────────────────┘
         ↑                 ↑
     conectadas por Ethernet / Gigabit

SEMANA 8 (Agregar nodo 3):
┌─────────────────────────────────────────────────────┐
│                     CLUSTER (3 NODOS)               │
├──────────────┬────────────────┬─────────────────────┤
│ Máquina 1    │  Máquina 2     │  Máquina 3          │
│ RTX 4070 12G │  GTX 1080 8GB  │  CPU + 64GB RAM     │
│ Entrena LoRA │  Destila       │  Vectorización RAG  │
│ + Inference  │  + Inference   │  + Cache distribuida│
└──────────────┴────────────────┴─────────────────────┘

SEMANA 16 (Agregar nodo 4):
[Máquina 4: GPU usada barata (4GB), hace procesamiento específico]

Resultado: Plataforma que escala sin límite. Agregas máquinas, ella se adapta.
```

#### Dónde conseguir máquinas baratas para el cluster

No necesitan ser nuevas. De hecho, lo antiguo es mejor (amortizado).

```
Opción          Precio      GPU            Pros                Contras
────────────────────────────────────────────────────────────────────────
Marketplace     $50-200     GTX 1060-1080  Muy barato          Estado desconocido
(usadas)

Refurbished     $150-400    RTX 3060-3070  Garantía            Más caro
(Amazon/eBay)

Tienda local    $100-300    Varía          Inspeccionas antes  Pocas opciones
electrónica

Empresa cierre  $200-500    Varía mucho    Lote completo       Requiere volumen
(auctions)

Donativos       $0          A menudo bueno Gratis              Espacio/tiempo
(universidades,
  empresas)
```

#### Software para coordinar el cluster

Ahora, cómo haces que múltiples máquinas actúen como 1.

**Opción 1: Ray (RECOMENDADO para principiantes)**

Ray es fácil y poderosa.

```python
# En la máquina principal (node manager)
import ray

# Conectar al cluster
ray.init(address="auto")  # Auto-descubre máquinas

# Definir tarea distribuida
@ray.remote
def entrenar_modelo(datos, modelo_nombre):
    # Esta función puede correr en CUALQUIER máquina del cluster
    return entrenar(datos, modelo_nombre)

# Ejecutar en paralelo
futures = [
    entrenar_modelo.remote(datos_1, "llama"),
    entrenar_modelo.remote(datos_2, "hermes"),
    entrenar_modelo.remote(datos_3, "qwen"),
]

# Esperar resultados
resultados = ray.get(futures)
```

Ray automáticamente:
- Busca máquina con GPU disponible
- Envía el código allá
- Ejecuta
- Devuelve resultados

**Opción 2: Kubernetes (profesional, complicado)**

Es lo que usan empresas grandes. Pero es overhead para un cluster casero.

```bash
# Instalación es 50+ pasos. No lo recomiendo para principiantes.
```

**Opción 3: Docker Swarm (simple, no tan poderoso como K8s)**

Más simple que Kubernetes, más poderoso que nada.

```bash
# Máquina 1: manager
docker swarm init

# Máquina 2,3,4: workers
docker swarm join --token XXXX manager-ip:2377
```

Luego defines servicios que corren distribuidos.

**Opción 4: SLURM (para HPC, típico en universidades)**

Si tu cluster crece mucho, SLURM es el estándar.

```bash
# Submeter job a cluster
sbatch entrenar_modelo.slurm
# SLURM distribuye automáticamente entre nodos
```

**Mi recomendación para ti:**
- Comienza con **Ray** (muy simple, escala bien)
- Si crece, considera **Docker Swarm** (un paso arriba)
- Si tienes 10+ máquinas, aprende **SLURM**

#### Configuración paso a paso de un cluster Ray casero

Supongamos tienes 2 máquinas.

**Máquina 1 (Head Node - la principal):**
```bash
# Instalar Ray
pip install ray[default]

# Iniciar Ray en modo cluster
ray start --head --port=6379
# Salida:
# Ray started successfully with node ID xxxxxxx
# Dashboard available at http://127.0.0.1:8265
```

**Máquina 2 (Worker Node):**
```bash
# Instalar Ray
pip install ray[default]

# Conectarse al head node
ray start --address='192.168.1.100:6379'  # IP de Máquina 1
# Salida:
# Successfully connected to Ray head at 192.168.1.100:6379
```

**Verificar cluster:**
```bash
# En Máquina 1
python -c "import ray; ray.init(address='auto'); print(ray.cluster_resources())"
# Salida:
# {'GPU': 2.0, 'CPU': 16.0, 'memory': 68GB}  # Suma de todos los nodos
```

✅ **Cluster funcionando.**

#### Distribución de tareas: ejemplo real

Ahora quieres que 2 modelos se entrenen en paralelo en tu cluster.

```python
import ray
import time

ray.init(address="auto")

@ray.remote(num_gpus=1)  # Esta tarea NECESITA 1 GPU
def entrenar_llama(epochs):
    print(f"Entrenando LLaMA en GPU...")
    # Simular entrenamiento
    time.sleep(10)
    return "LLaMA fine-tuned"

@ray.remote(num_gpus=0.5)  # Puede usar CPU o media GPU
def procesar_datos(archivos):
    print(f"Procesando datos...")
    time.sleep(5)
    return "Datos listos"

# Ejecutar en paralelo
tarea_1 = entrenar_llama.remote(epochs=3)
tarea_2 = procesar_datos.remote(archivos=["doc1.pdf", "doc2.pdf"])

# Esperar que ambas terminen
resultado_1, resultado_2 = ray.get([tarea_1, tarea_2])

print(resultado_1)  # "LLaMA fine-tuned"
print(resultado_2)  # "Datos listos"
```

**Qué pasó:**
1. Ray vio que `entrenar_llama` necesita GPU
2. Lo envió a Máquina 1 (que tiene GPU disponible)
3. Ray vio que `procesar_datos` no necesita GPU
4. Lo envió a Máquina 2 (que está libre)
5. Ambas corren en paralelo
6. Esperas resultados

**Tiempo total:** ~10 segundos (las 2 en paralelo)
**Sin cluster:** ~15 segundos (una después de otra)

#### Escenario real: plataforma de AIs que se mejora sola

Aquí está el ciclo completo en tu cluster:

```
Lunes 8am (automático, Ray scheduler):
  - Máquina 1 (GPU): Fine-tuning de LLaMA con datos nuevos
  - Máquina 2 (CPU+GPU): Destilación de modelo
  - Máquina 3 (CPU): Procesamiento de logs nuevos

Martes 8am:
  - Máquina 1: Evaluación de nuevos modelos
  - Máquina 2: Fusión de especialistas
  - Máquina 3: Vectorización de nuevos datos para RAG

Resultado: Todos tus modelos mejoran cada semana automáticamente.
```

Para esto, usas **APScheduler** + Ray:

```python
from apscheduler.schedulers.background import BackgroundScheduler
import ray

@ray.remote
def ciclo_mejora_semanal():
    """Tarea que corre automáticamente cada lunes"""
    print("Iniciando mejora semanal...")
    
    # Fine-tuning
    nuevo_modelo = entrenar_llama.remote(epochs=5)
    
    # Destilación
    modelo_destilado = destilar.remote(nuevo_modelo)
    
    # Evaluación
    metricas = evaluar.remote(modelo_destilado)
    
    return ray.get([nuevo_modelo, modelo_destilado, metricas])

# Programar
scheduler = BackgroundScheduler()
scheduler.add_job(ciclo_mejora_semanal.remote, 'cron', day_of_week='mon', hour=8)
scheduler.start()
```

**Cada semana, automáticamente:**
- Tu cluster mejora modelos
- Sin que toques nada
- Usando GPUs que de otra forma estarían ociosas

#### Presupuesto realista para un cluster casero

```
Fase 1 (Semana 0): $0
- Ya tienes: 1 máquina con GPU

Fase 2 (Mes 1): $200-300
- Máquina usada con GPU (GTX 1080)
- Switch Ethernet Gigabit: $20
- Cables: $10

Fase 3 (Mes 2): $100-150
- Máquina CPU fuerte (procesamiento de datos)

Fase 4 (Mes 4): $200-400
- Otra GPU usada o máquina más

Total 6 meses: $500-850 inversión
Máquinas operativas: 4
GPUs totales: 3
Capacidad: ~25GB VRAM + CPU procesamiento

Costo mensual: $0 (solo electricidad: ~$50)
ROI vs AWS: Te ahorras $500/mes en GPU hours
Payback: 1-2 meses
```

#### Checklist: construir tu primer cluster

- [ ] Máquina 1 funcionando (tienes)
- [ ] Máquina 2 usada comprada (RTX 3060 / GTX 1080)
- [ ] Switch Ethernet Gigabit (25GB/s es ideal)
- [ ] Cables Ethernet CAT 6 o superior
- [ ] Ray instalado en ambas máquinas
- [ ] Máquinas en la misma red (ping entre ellas)
- [ ] Ray cluster iniciado y verificado
- [ ] Primer script distribuido ejecutado
- [ ] Ray dashboard abierto (http://localhost:8265) para monitoreo

#### Monitoreo y dashboard

Ray tiene dashboard integrado:

```bash
# Abrir en navegador
http://localhost:8265
```

Ves:
- GPUs disponibles en cada nodo
- Tareas en ejecución
- Bottlenecks (cuello de botella)
- Historial de rendimiento

Ahora sabes qué máquina está ociosa y dónde agregar más poder.

### 2.8 Instalación de dependencias Python para fine-tuning

Antes de fine-tunear, necesitas algunas librerías.

#### Paso 1: Crear un entorno virtual

```bash
python3 -m venv venv_ia
source venv_ia/bin/activate  # Mac/Linux
# o en Windows:
venv_ia\Scripts\activate
```

#### Paso 2: Instalar dependencias base

```bash
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers datasets peft trl accelerate bitsandbytes
```

⚠️ **Importante:** El comando `torch` varía según tu GPU:
- **Nvidia (CUDA 11.8):** usa `cu118` (mostrado arriba)
- **Nvidia (CUDA 12.1):** usa `cu121`
- **Mac (Apple Silicon):** usa `--index-url https://download.pytorch.org/whl/nightly/cpu` y luego instala pytorch separado
- **CPU only:** usa `--index-url https://download.pytorch.org/whl/cpu`

Si no sabes cuál tienes, busca en Google "[tu GPU] pytorch install".

#### Paso 3: Instalar unsloth (opcional pero recomendado)

Unsloth acelera el fine-tuning 2-3x. Vale la pena.

```bash
pip install unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git
```

#### Paso 4: Verificar instalación

```python
python -c "import torch; print(f'Torch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"
```

Deberías ver:
```
Torch version: 2.0.X
CUDA available: True
```

Si `CUDA available: False`, tu GPU no está siendo detectada. Reinstala el driver.

### 2.9 Primer fine-tuning: verificación de "end-to-end"

Antes de hacer fine-tuning serio, vamos a hacer uno pequeño, rápido, solo para verificar que todo funciona.

#### El código (script_test_finetuning.py)

```python
from unsloth import FastLanguageModel
import torch
from datasets import Dataset
from transformers import TrainingArguments
from trl import SFTTrainer

# 1. Cargar modelo
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Llama-3.2-3B",
    max_seq_length=512,
    dtype=torch.float16,
    load_in_4bit=True,
)

# 2. Preparar LoRA
model = FastLanguageModel.get_peft_model(
    model,
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    use_gradient_checkpointing="unsloth",
)

# 3. Dataset mínimo (solo 5 ejemplos para test)
datos = {
    "text": [
        "Usuario: ¿Qué es Python? Asistente: Python es un lenguaje de programación versátil.",
        "Usuario: ¿Cómo hago un loop? Asistente: Usa 'for' o 'while' en Python.",
        "Usuario: ¿Qué es una función? Asistente: Es un bloque de código reutilizable.",
        "Usuario: ¿Cómo imprimo algo? Asistente: Usa print() en Python.",
        "Usuario: ¿Qué es una variable? Asistente: Es un contenedor de datos.",
    ]
}
dataset = Dataset.from_dict(datos)

# 4. Configurar entrenamiento
training_args = TrainingArguments(
    output_dir="./test_output",
    num_train_epochs=1,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=2,
    warmup_steps=2,
    weight_decay=0.01,
    learning_rate=5e-4,
    logging_steps=1,
    save_steps=999,  # No guardar durante el test
)

# 5. Entrenar
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=512,
    args=training_args,
)

trainer.train()
print("✅ Fine-tuning test completado exitosamente")
```

#### Ejecutar el test

```bash
python script_test_finetuning.py
```

Este script:
- ✅ Carga Llama 3.2 (3B)
- ✅ Aplica QLoRA
- ✅ Fine-túnea con 5 ejemplos
- ✅ Verifica que CUDA funciona

Si ves ✅ al final, todo está correcto. Si ves error, léelo, y busca la solución en la sección 1.5 "Errores que comete el 90% cuando empieza".

### 2.10 Próximo paso

Ahora tienes:
- ✅ Ollama instalado
- ✅ Un modelo descargado
- ✅ Tu GPU funcional
- ✅ Librerías de fine-tuning instaladas
- ✅ Un test de fine-tuning completado

En el Capítulo 3, crearemos tu primera base de conocimiento RAG. Subirás tus propios documentos y harás consultas sobre ellos.

---

# Capítulo 3 — RAG: Usa Tus Propios Datos Sin Reentrenamiento

### 3.1 ¿Qué es RAG? La ilusión óptica más útil de la IA

RAG = "Retrieval-Augmented Generation"

**Traducción literal:** "Generación aumentada por recuperación"

**Lo que significa:** antes de responder una pregunta, el modelo busca información relevante y se la pasa, para que responda basándose en eso.

#### La analogía: el amigo experto en una biblioteca

Sin RAG:
```
Tú: "¿Cuál es el capital social de mi empresa?"
Amigo de memoria: "Creo que son $50,000... pero no estoy seguro"
```

Con RAG:
```
Tú: "¿Cuál es el capital social de mi empresa?"
Amigo: "Espera, déjame buscar en nuestros documentos"
[Abre carpeta, busca, encuentra PDF de constitución]
Amigo: "Aquí está: son $50,000 exactos, firmado el 2020"
```

**Diferencia crítica:**
- Sin RAG: el modelo solo confía en lo que aprendió durante entrenamiento
- Con RAG: el modelo accede a información NUEVA y ACTUALIZADA

#### Comparación: RAG vs Fine-tuning vs Destilación

Recuerda la tabla del Capítulo 1. Aquí la contextualizamos con ejemplos:

```
Escenario: Tienes 10,000 PDFs de tu empresa que suben 50 nuevos cada día

CON RAG:
  - Día 1: Indexas los 10,000 PDFs
  - Día 2: Suben 50 nuevos, los agregas al índice (5 minutos)
  - Resultado: El modelo sabe del contenido nuevo automáticamente
  - Tiempo: 0 entrenamiento

CON FINE-TUNING:
  - Día 1: Fine-túneas el modelo con 10,000 PDFs (5 horas)
  - Día 2: Suben 50 nuevos, necesitas reentrenar (5 horas más)
  - Resultado: Más "inteligente" pero requiere reentrenamiento
  - Tiempo: 5 horas cada vez que hay datos nuevos

CON DESTILACIÓN:
  - Proceso de semanas
  - Requiere modelo grande como referencia
  - No es para datos que cambian diariamente
```

**Conclusión:** RAG es para cuando tus datos cambian frecuentemente o son muy específicos de tu dominio.

### 3.2 Cómo funciona RAG por dentro (sin matemáticas complicadas)

RAG tiene 3 pasos:

#### Paso 1: Indexar (convertir documentos a vectores)

Un documento NO se almacena como texto.

Se convierte a **vectores** (listas de números).

```
Documento: "Python es un lenguaje de programación versátil"

Convertido a vector (embeddings):
[0.2, -0.5, 0.8, 0.1, -0.3, 0.9, 0.4, -0.1, ...]
↑     ↑     ↑    ↑     ↑     ↑    ↑     ↑
Estos números capturan el "significado" del documento
```

¿Cómo se crea el vector? Usas un modelo de embeddings (usualmente pequeño y rápido):
- Sentence-Transformers
- OpenAI Embeddings
- Ollama (embeddings locales)

**Analogía:** Es como traducir un documento a un idioma secreto que solo la computadora entiende, pero que mantiene el significado.

#### Paso 2: Buscar (encontrar documentos similares)

Cuando haces una pregunta, ocurre:

```
Pregunta: "¿Cómo instalo Python?"

Paso 1: Convierte la pregunta a vector
[0.1, -0.4, 0.7, 0.2, -0.2, 0.8, 0.3, -0.2, ...]

Paso 2: Busca documentos cuyo vector es SIMILAR
  - Doc1 (sobre instalar Python): similitud = 0.95 ✅ MUY similar
  - Doc2 (sobre variables): similitud = 0.3 ❌ poco similar
  - Doc3 (sobre loops): similitud = 0.25 ❌ poco similar

Paso 3: Recupera los top 3 más similares
```

**¿Cómo se mide "similar"?** Usa "cosine similarity" (ángulo entre vectores). Si dos vectores apuntan en la misma dirección, son similares.

#### Paso 3: Aumentar y generar (meter contexto al modelo)

Finalmente, le pasas al modelo:

```
[Contexto recuperado de documentos]
"Python es un lenguaje de programación versátil. Se instala desde python.org..."

[Pregunta original]
"¿Cómo instalo Python?"

[Instrucción especial]
"Responde basándote SOLO en el contexto anterior"
```

El modelo ve el contexto Y la pregunta, y responde con precisión.

### 3.3 Herramientas para RAG: Elige tu camino

Hay 3 caminos, de menor a mayor complejidad:

#### Opción 1: AnythingLLM (la más fácil, interfaz gráfica)

**Pros:**
- No necesitas escribir código
- Interfaz visual, arrastrar y soltar
- Soporta Ollama integrado
- Funciona con cualquier modelo local

**Contras:**
- Menos personalizable
- Rendimiento no optimizado para casos extremos
- Vendor lock-in (dependes de su plataforma)

**Mejor para:** Prototiping rápido, no técnicos, pruebas.

#### Opción 2: LangChain (código, muy popular)

**Pros:**
- Flexible, personalizable
- Excelente documentación
- Integra todo (modelos, vectores, búsqueda)
- Comunidad enorme

**Contras:**
- Requiere escribir código
- Curva de aprendizaje moderada
- A veces overhead innecesario

**Mejor para:** Producción, control fino, desarrolladores.

#### Opción 3: LlamaIndex (código, específico para RAG)

**Pros:**
- Diseñado específicamente para RAG
- Muy rápido
- Excelente manejo de índices

**Contras:**
- Comunidad más pequeña que LangChain
- Documentación a veces incompleta

**Mejor para:** Proyectos RAG puros, alto rendimiento.

**Mi recomendación:** Comienza con AnythingLLM, luego aprende LangChain cuando necesites más control.

### 3.4 Instalación y configuración de AnythingLLM

#### Paso 1: Descargar AnythingLLM

Ve a: https://anythingllm.com/

Descarga la versión desktop (no cloud).

#### Paso 2: Instalar

**Windows:**
1. Ejecuta el instalador `.exe`
2. Sigue los pasos
3. Abre la aplicación

**Mac:**
1. Abre el DMG
2. Arrastra a Applications
3. Abre desde Applications

**Linux:**
```bash
npm install -g @mintplex-labs/anything-llm
anything-llm  # Abre interfaz en http://localhost:3001
```

#### Paso 3: Configuración inicial

Cuando abres AnythingLLM por primera vez:

1. **Elige el modelo LLM:**
   - Opciones → LLM Preference
   - Selecciona "Ollama"
   - Ingresa: `http://localhost:11434`
   - Elige modelo (Hermes, LLaMA, etc.)

2. **Elige el embeddings:**
   - Opciones → Embeddings
   - Selecciona "Ollama embeddings" O "Sentence Transformers" (local)
   - Si usas Ollama: `http://localhost:11434`

3. **Vector store:**
   - Opciones → Vector Database
   - Selecciona "LanceDB" (local, sin servidores externos)

✅ **Listo.** Todo funciona sin internet, sin APIs pagadas.

### 3.5 Crear tu primera base de conocimiento RAG

Scenario: Tienes 5 PDFs sobre procesos internos de tu empresa. Quieres un chatbot que responda preguntas sobre ellos.

#### Paso 1: Preparar documentos

Organiza tus PDFs en una carpeta:
```
documentos_empresa/
  ├── proceso_qa.pdf
  ├── politica_vacaciones.pdf
  ├── manual_seguridad.pdf
  ├── estructura_organizacional.pdf
  └── presupuesto_2024.pdf
```

⚠️ **Importante:** Los PDFs deben tener texto seleccionable, no solo imágenes escaneadas. Si son imágenes, necesitas OCR.

#### Paso 2: Crear "Workspace" en AnythingLLM

Un Workspace es una "colección de documentos + configuración".

1. Abre AnythingLLM
2. Haz clic en "New Workspace"
3. Nombre: "Procesos Internos"
4. Sistema Prompt (cómo comportarse el modelo):
```
Eres un asistente experto en procesos internos de nuestra empresa.
Responde preguntas basándote SOLO en los documentos proporcionados.
Si no encuentras la respuesta, di "No encontré esa información en nuestros documentos".
Sé conciso y profesional.
```

#### Paso 3: Subir documentos

1. Haz clic en el "+" en el Workspace
2. Selecciona "Upload Document"
3. Elige los PDFs de tu carpeta
4. AnythingLLM automáticamente:
   - Extrae texto
   - Crea embeddings
   - Indexa en el vector store

⏳ **Espera:** Depende de tamaño. Para 5 PDFs medianos: 2-5 minutos.

#### Paso 4: Probar RAG

Una vez indexado, haz preguntas:

```
Tú: "¿Cuál es el proceso de vacaciones?"

AnythingLLM internamente:
1. Convierte pregunta a vector
2. Busca documentos similares
3. Encuentra: politica_vacaciones.pdf
4. Lee: "Se otorgan 15 días al año. Solicitud 30 días antes..."
5. Le pasa al modelo con el contexto
6. El modelo responde:

Respuesta: "Según nuestra política, se otorgan 15 días de vacaciones al año.
Las solicitudes deben hacerse con 30 días de anticipación..."
```

✅ **Funciona.**

### 3.6 Usando LangChain para RAG avanzado

Si necesitas más control, aquí está el código equivalente en LangChain:

```python
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOllama
from langchain.chains import RetrievalQA

# 1. Cargar documentos
docs = []
for pdf in ["proceso_qa.pdf", "politica_vacaciones.pdf", "manual_seguridad.pdf"]:
    loader = PyPDFLoader(pdf)
    docs.extend(loader.load())

# 2. Dividir documentos en chunks (partes pequeñas)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # Cada fragmento: 500 caracteres
    chunk_overlap=50,    # Solapamiento para no perder contexto
)
chunks = splitter.split_documents(docs)

# 3. Crear embeddings (vectores)
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",  # Modelo de embeddings
    base_url="http://localhost:11434"
)

# 4. Crear vector store
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 5. Configurar modelo LLM
llm = ChatOllama(
    model="hermes3",
    base_url="http://localhost:11434"
)

# 6. Crear cadena RAG
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # Tipo de cadena
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),  # Top 3 documentos
)

# 7. Hacer preguntas
pregunta = "¿Cuál es el proceso de vacaciones?"
respuesta = qa_chain.run(pregunta)
print(respuesta)
```

**Qué hace este código:**
1. Carga 3 PDFs
2. Los divide en fragmentos pequeños (para precisión)
3. Crea vectores de cada fragmento
4. Guarda en una base de datos local (Chroma)
5. Configura modelo Hermes
6. Crea la cadena RAG
7. Responde preguntas con contexto

**Ventajas sobre AnythingLLM:**
- Control fino sobre chunk_size, embeddings, etc.
- Automatizable (puedes correrlo en un script)
- Integrable en aplicaciones

### 3.7 Evaluación: ¿Tu RAG funciona bien?

No es suficiente "parece que funciona". Debes medir.

#### Métrica 1: Relevancia de documentos recuperados

Después de indexar, haz esta prueba:

```python
pregunta = "¿Cuál es el proceso de vacaciones?"
docs_recuperados = vectorstore.similarity_search(pregunta, k=3)

for doc in docs_recuperados:
    print(f"Documento: {doc.metadata['source']}")
    print(f"Relevancia: [HIGH/MEDIUM/LOW]")
    print(f"Contenido: {doc.page_content[:200]}...")
```

✅ **Esperado:** Los 3 documentos mencionan "vacaciones"

❌ **Problema:** Si recupera documentos irrelevantes, necesitas:
- Mejor modelo de embeddings
- Ajustar chunk_size
- Agregar más contexto

#### Métrica 2: Precisión de respuestas

Crea un pequeño test set:

```python
test_cases = [
    {
        "pregunta": "¿Cuál es el proceso de vacaciones?",
        "respuesta_esperada": "15 días al año",
    },
    {
        "pregunta": "¿Quién es el CEO?",
        "respuesta_esperada": "Juan García",
    },
]

correctas = 0
for test in test_cases:
    respuesta = qa_chain.run(test["pregunta"])
    if test["respuesta_esperada"].lower() in respuesta.lower():
        correctas += 1

precision = (correctas / len(test_cases)) * 100
print(f"Precisión: {precision}%")
```

✅ **Esperado:** 80%+ precisión

❌ **Si es bajo:** Mejora con fine-tuning (Capítulo 4)

#### Métrica 3: Tiempo de respuesta

```python
import time

inicio = time.time()
respuesta = qa_chain.run("Tu pregunta")
fin = time.time()

tiempo_ms = (fin - inicio) * 1000
print(f"Tiempo de respuesta: {tiempo_ms:.0f}ms")
```

✅ **Esperado:** 500-3000ms dependiendo de modelo

❌ **Si es muy lento:** Usa modelo más pequeño o mejor hardware

### 3.8 Mejoras prácticas para RAG

#### Mejora 1: Aumentar documentos relevantes

Si RAG dice "no encontré información", el problema es documentos:

```python
# Opción A: Agregar más documentos
# Sube más PDFs al Workspace

# Opción B: Mejorar extracción de texto
# Si los PDFs tienen imágenes, usa OCR (tesseract + langchain)

from langchain.document_loaders import OCRDocumentLoader
loader = OCRDocumentLoader("documento_escaneado.pdf")
docs = loader.load()
```

#### Mejora 2: Aumentar contexto (chunk_overlap)

Si el modelo pierde contexto entre fragmentos:

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,  # Aumentado de 50 a 100
)
```

#### Mejora 3: Recuperar más documentos

Si necesita más contexto:

```python
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}  # Top 5 en lugar de 3
)
```

⚠️ **Advertencia:** Más documentos = más contexto = respuestas más lentas y a veces confusas.

#### Mejora 4: Usar modelo de embeddings mejor

Si la recuperación es imprecisa:

```python
# Opción A: Sentence-Transformers (mejor calidad, requiere más VRAM)
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Opción B: Ollama con modelo mejor
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",  # Mejor que por defecto
    base_url="http://localhost:11434"
)
```

### 3.9 Caso de uso real: RAG para documentación técnica

Escenario: Eres engineer en una startup. Tienes 200 markdown files de documentación. 5 nuevos cada día.

**Problema sin RAG:**
- Devs buscan en Google: "cómo usar X en nuestro código"
- No encuentran, preguntan en Slack
- Pierden 30 minutos esperando respuesta

**Solución con RAG:**
- Indexas toda la documentación
- Devs preguntan al chatbot en Slack
- Obtienen respuesta en 5 segundos

**Implementación:**

```python
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import UnstructuredMarkdownLoader

# 1. Cargar todos los markdown
loader = DirectoryLoader(
    "docs/",
    glob="**/*.md",
    loader_cls=UnstructuredMarkdownLoader
)
docs = loader.load()

# 2. Crear RAG (resto igual a 3.6)
# ... [código de RAG] ...

# 3. Integrar con Slack (usando webhook)
from slack_sdk import WebClient

def responder_slack(pregunta):
    respuesta = qa_chain.run(pregunta)
    return respuesta

# Cuando alguien usa /pregunta en Slack
# Se ejecuta: responder_slack(pregunta) → devuelve respuesta
```

**Resultado:**
- Documentación siempre actualizada
- Búsqueda semántica (no solo palabras clave)
- Ahorro de tiempo del equipo
- Cero costo de infraestructura

### 3.10 Próximo paso

Ahora tienes:
- ✅ Entiendes qué es RAG y cómo funciona
- ✅ Puedes crear RAG en 10 minutos (AnythingLLM)
- ✅ Sabes programar RAG en Python (LangChain)
- ✅ Puedes evaluar si funciona bien
- ✅ Conoces mejoras prácticas

**El ciclo de mejora:**

RAG es Fase 1 del ciclo. Pero RAG tiene limitaciones:

```
¿El modelo responde bien?
  → Sí → Excelente, usa RAG. Fin.
  → No → ¿El problema es documentos?
           → Sí → Agrega documentos (soluciona)
           → No → El modelo NO "piensa" como necesitas
                   → Necesitas FINE-TUNING (Capítulo 4)
```

Si después de agregar documentos el modelo sigue equivocándose, necesitas entrenarlo.

**En el Capítulo 4:** Aprenderás fine-tuning con QLoRA. Tomarás datos reales (conversaciones, casos de uso) y entrenarás el modelo para que "piense" como especialista en tu dominio.

---

# Capítulo 4 — Fine-tuning con QLoRA: Entrena sin Quebrar tu GPU

### 4.1 El problema: Fine-tuning tradicional necesita demasiada VRAM

Imagina que quieres entrenar un modelo de 7B parámetros.

**Sin optimizaciones:**
- VRAM necesaria: 40-60 GB
- Tu GPU: 8-12 GB
- Resultado: ❌ Out of Memory error

**Con QLoRA:**
- VRAM necesaria: 6-8 GB
- Tu GPU: 8-12 GB
- Resultado: ✅ Funciona

¿Cómo es posible? QLoRA hace 3 cosas:

1. **Cuantización de 4 bits:** El modelo se comprime. Pesa 1/4
2. **Adaptadores LoRA:** Solo entrenas una pequeña parte (2-5% del modelo)
3. **Gradient checkpointing:** Olvidas cálculos intermedios, los recalculas cuando necesitas

Resultado: El modelo "aparentemente entero" pero optimizado para GPU pequeñas.

### 4.2 Conceptos: Cuantización, LoRA, Gradientes

#### Concepto 1: Cuantización (FP32 → INT4)

Un parámetro del modelo normalmente es un número flotante de 32 bits:

```
FP32: 0.123456789012345
      ↓ (divide entre 4)
INT4: 0 (aproximación burda, pero suficiente)
```

Pierdes algo de precisión, pero:
- El modelo es 4x más pequeño
- Las respuestas son casi idénticas (90-95% de calidad)

**Analogía:** Es como comprimir una foto JPEG. Pierdes píxeles, pero se ve casi igual.

#### Concepto 2: LoRA (Low-Rank Adaptation)

En lugar de actualizar todos los pesos del modelo durante entrenamiento:

```
Modelo original (7B parámetros):
┌─────────────────────────────────┐
│ Parámetro 1: 0.5                │
│ Parámetro 2: -0.3               │
│ Parámetro 3: 0.8                │
│ ...                             │
│ Parámetro 7B: 0.2               │
└─────────────────────────────────┘

Durante entrenamiento normal:
Todos los 7B se actualizan. Costos: 60GB VRAM

Con LoRA:
┌─────────────────────────────────┐
│ Modelo congelado (INMUTABLE)    │ ← Sin actualizar
│ + Adaptador pequeño (LoRA)      │ ← Actualiza solo esto
│   (0.1% del modelo)             │   (8GB VRAM)
└─────────────────────────────────┘
```

**¿Qué es el "adaptador"?** Dos matrices pequeñas que se multiplican por los embeddings:

```
Input → [Matriz A (rango 8)] → [Matriz B (rango 8)] → Output
        (mucho más pequeño que el modelo original)
```

**Resultado:** El modelo "aprende" cosas nuevas sin modificar el cerebro (pesos) original. Usa adaptadores como "enchufes" que amplifican el comportamiento existente.

#### Concepto 3: Gradientes y Backpropagation

Durante entrenamiento:

```
Datos de entrada
    ↓
Forward pass (modelo predice)
    ↓
Calcula loss (qué tan mal está)
    ↓
Backward pass (gradientes, cuánto cambiar cada peso)
    ↓
Actualiza pesos
```

El problema: el backward pass requiere guardar todos los cálculos intermedios. Para un modelo de 7B, es MUCHA memoria.

**Gradient checkpointing:** No guardes todo. Recalcula cuando lo necesites:

```
En lugar de guardar 1000 valores intermedios (1GB memoria)
Guarda 100 valores (100MB)
Cuando haces backward, recalculas los 900 faltantes
Costo: +10% tiempo, -90% memoria
```

### 4.3 Preparar tu dataset para fine-tuning

El modelo aprende de ejemplos. Necesitas buenos ejemplos.

#### Formato del dataset

El formato estándar es JSON con estructura instrucción-respuesta:

```json
[
  {
    "instruction": "¿Cuál es el proceso de onboarding?",
    "input": "",
    "output": "El onboarding toma 3 semanas e incluye: 1) Entrenamiento técnico 2) Integración cultural 3) Asignación de mentor"
  },
  {
    "instruction": "¿Cuántos días de vacaciones hay?",
    "input": "",
    "output": "15 días de vacaciones al año. Solicitar 30 días antes."
  },
  {
    "instruction": "¿Cómo reporto un bug?",
    "input": "He encontrado que el login no funciona en Safari",
    "output": "Ve a jira.empresa.com, crea un issue en proyecto 'BUGS', incluye: navegador, OS, pasos para reproducir, captura de pantalla. Nuestro equipo lo revisa en 24h."
  }
]
```

**Estructura:**
- `instruction`: La pregunta o tarea
- `input`: Contexto adicional (opcional)
- `output`: La respuesta correcta

#### Cuántos ejemplos necesitas

```
Calidad de resultados vs Cantidad de ejemplos:

50 ejemplos:     [###] Básico, cambios notables
100 ejemplos:    [######] Bueno, especialidad clara
500 ejemplos:    [#########] Muy bueno, experto evidente
1000+ ejemplos:  [###########] Excelente, casi indistinguible de entrenamiento completo
```

**Regla práctica:**
- Mínimo: 50 ejemplos (para ver si funciona)
- Recomendado: 200-500 ejemplos (para producción)
- Ideal: 1000+ ejemplos (dominio completo)

**Importante:** 100 ejemplos LIMPIOS > 1000 ejemplos RUIDOSOS

#### Limpiar y validar dataset

Antes de entrenar, verifica:

```python
import json

with open("dataset.json") as f:
    datos = json.load(f)

# Validación 1: ¿Todos tienen las 3 claves?
for i, ejemplo in enumerate(datos):
    assert "instruction" in ejemplo, f"Falta 'instruction' en {i}"
    assert "output" in ejemplo, f"Falta 'output' en {i}"

# Validación 2: ¿Ninguno está vacío?
for i, ejemplo in enumerate(datos):
    assert len(ejemplo["instruction"]) > 5, f"Instrucción muy corta en {i}"
    assert len(ejemplo["output"]) > 10, f"Output muy corto en {i}"

# Validación 3: ¿Hay duplicados?
instrucciones = [e["instruction"] for e in datos]
assert len(instrucciones) == len(set(instrucciones)), "Hay instrucciones duplicadas"

print(f"✅ Dataset válido: {len(datos)} ejemplos")
```

### 4.4 Instalación de unsloth (acelera 2-3x)

Unsloth es un fork optimizado de transformers. Hace fine-tuning 2-3x más rápido.

```bash
# Instalar unsloth
pip install unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git

# Verificar instalación
python -c "from unsloth import FastLanguageModel; print('✅ Unsloth instalado')"
```

### 4.5 Script completo: Fine-tuning de un modelo con QLoRA

Aquí está el script que necesitas. Cópialo y adapta:

```python
# fine_tune_model.py

from unsloth import FastLanguageModel
import torch
from datasets import Dataset, load_dataset
from transformers import TrainingArguments
from trl import SFTTrainer
import json

# ===== 1. CARGAR MODELO =====
print("1️⃣ Cargando modelo...")

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Hermes-3-Llama-3.1-8B",  # O cualquier modelo: llama, phi, etc.
    max_seq_length=2048,
    dtype=torch.float16,
    load_in_4bit=True,  # Cuantización 4 bits
)

# ===== 2. APLICAR LORA =====
print("2️⃣ Aplicando LoRA...")

model = FastLanguageModel.get_peft_model(
    model,
    r=16,                          # Rango LoRA (8-64 típico)
    lora_alpha=32,                 # Scaling
    lora_dropout=0.05,             # Regularización
    bias="none",
    use_gradient_checkpointing="unsloth",  # Checkpointing
    random_state=42,
)

# ===== 3. CARGAR DATASET =====
print("3️⃣ Cargando dataset...")

with open("dataset.json") as f:
    datos = json.load(f)

# Convertir a formato de cadena
textos = []
for d in datos:
    # Formato estándar para Hermes
    texto = f"""<|im_start|>user
{d['instruction']}
{d.get('input', '')}<|im_end|>
<|im_start|>assistant
{d['output']}<|im_end|>
"""
    textos.append({"text": texto})

dataset = Dataset.from_dict({"text": textos})

print(f"   Dataset: {len(dataset)} ejemplos")
print(f"   Ejemplo 1: {dataset[0]['text'][:200]}...")

# ===== 4. CONFIGURAR ENTRENAMIENTO =====
print("4️⃣ Configurando entrenamiento...")

training_args = TrainingArguments(
    output_dir="./modelo_fine_tuned",
    num_train_epochs=3,                    # 3 pasadas por datos
    per_device_train_batch_size=4,         # Batch size (ajusta según VRAM)
    gradient_accumulation_steps=2,         # Simula batch 8 con VRAM de 4
    warmup_steps=100,                      # Calentar learning rate
    weight_decay=0.01,                     # Regularización
    learning_rate=5e-4,                    # Learning rate
    logging_steps=10,                      # Log cada 10 pasos
    save_steps=100,                        # Guardar checkpoint cada 100
    save_total_limit=2,                    # Guardar solo 2 últimos checkpoints
    optim="paged_adamw_8bit",              # Optimizer de 8 bits (ahorra VRAM)
    seed=42,
)

# ===== 5. ENTRENAR =====
print("5️⃣ Entrenando...")

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=2048,
    args=training_args,
)

trainer.train()

print("✅ Entrenamiento completado")

# ===== 6. GUARDAR MODELO =====
print("6️⃣ Guardando modelo...")

model.save_pretrained("./mi_modelo_lora")
tokenizer.save_pretrained("./mi_modelo_lora")

print("✅ Modelo guardado en ./mi_modelo_lora")

# ===== 7. PROBAR =====
print("7️⃣ Probando modelo...")

FastLanguageModel.for_inference(model)

inputs = tokenizer(
    ["<|im_start|>user\n¿Cuál es el proceso de vacaciones?\n<|im_end|>\n<|im_start|>assistant\n"],
    return_tensors="pt",
).to("cuda")

outputs = model.generate(**inputs, max_new_tokens=200)
respuesta = tokenizer.decode(outputs[0])

print("RESPUESTA:")
print(respuesta)
```

**Explicación línea por línea:**

1. **Cargar modelo:** `FastLanguageModel.from_pretrained` con 4-bit (cuantización)
2. **LoRA:** `get_peft_model` agrega adaptadores pequeños (r=16 es estándar)
3. **Dataset:** JSON → Dataset de Hugging Face
4. **Configuración:** TrainingArguments (epochs, batch_size, learning_rate)
5. **Entrenamiento:** SFTTrainer es el trainer optimizado
6. **Guardar:** Guarda LoRA (pequeño, ~100MB) + tokenizer
7. **Probar:** Genera respuesta con modelo fine-tuneado

**Ejecución:**

```bash
python fine_tune_model.py

# Output esperado:
# 1️⃣ Cargando modelo...
# 2️⃣ Aplicando LoRA...
# 3️⃣ Cargando dataset...
#    Dataset: 150 ejemplos
# 4️⃣ Configurando entrenamiento...
# 5️⃣ Entrenando...
#    [████████████████████] 100% - Epoch 3/3
# ✅ Entrenamiento completado
# ✅ Modelo guardado en ./mi_modelo_lora
```

### 4.6 Ajustes según tu VRAM

Si se queda sin memoria, ajusta:

```python
# Opción 1: Batch size más pequeño
per_device_train_batch_size=2,  # En lugar de 4

# Opción 2: Secuencia más corta
max_seq_length=1024,  # En lugar de 2048

# Opción 3: LoRA más pequeño
r=8,  # En lugar de 16

# Opción 4: Todas las anteriores
per_device_train_batch_size=2,
max_seq_length=1024,
r=8,
gradient_accumulation_steps=4,  # Simula batch más grande
```

### 4.7 Importar modelo fine-tuneado a Ollama

Una vez entrenado, queremos usarlo en Ollama.

#### Paso 1: Fusionar LoRA con modelo base

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM

# Cargar modelo base
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B",  # Modelo base original
    torch_dtype=torch.float16,
    device_map="auto"
)

# Cargar LoRA
modelo_fusionado = PeftModel.from_pretrained(
    base_model,
    "./mi_modelo_lora"
)

# Fusionar (LoRA + base = un solo modelo)
modelo_fusionado = modelo_fusionado.merge_and_unload()

# Guardar
modelo_fusionado.save_pretrained("./modelo_final_fusionado")
```

#### Paso 2: Convertir a formato GGUF (para Ollama)

```bash
# Instalar llama-cpp-python
pip install llama-cpp-python

# Convertir a GGUF
python -m llama_cpp.convert \
  --model-dir ./modelo_final_fusionado \
  --outfile ./modelo_final.gguf \
  --outtype q4_k_m  # Cuantización para GPU (q4_k_m) o CPU (q5_k_m)
```

#### Paso 3: Agregar a Ollama

```bash
# Crear Modelfile
cat > Modelfile << EOF
FROM ./modelo_final.gguf
PARAMETER temperature 0.7
PARAMETER top_k 40
PARAMETER top_p 0.9
SYSTEM "Eres un asistente experto en nuestra empresa"
EOF

# Crear modelo en Ollama
ollama create mi-modelo-entrenado -f Modelfile

# Probar
ollama run mi-modelo-entrenado "¿Cuál es el proceso de vacaciones?"
```

✅ **Tu modelo fine-tuneado ahora vive en Ollama.**

### 4.8 Evaluación: ¿Mejoró el modelo?

Crea un test set (datos que NO usaste en entrenamiento):

```python
test_cases = [
    {
        "pregunta": "¿Cuántos días de vacaciones?",
        "respuesta_correcta": "15 días al año"
    },
    {
        "pregunta": "¿Cómo reporto un bug?",
        "respuesta_correcta": "Crea un issue en Jira"
    },
]

# Antes del fine-tuning (modelo base)
print("MODELO BASE:")
for test in test_cases:
    respuesta = modelo_base(test["pregunta"])
    match = test["respuesta_correcta"].lower() in respuesta.lower()
    print(f"  {test['pregunta']}: {'✅' if match else '❌'}")

# Después del fine-tuning
print("\nMODELO FINE-TUNEADO:")
for test in test_cases:
    respuesta = modelo_fine_tuned(test["pregunta"])
    match = test["respuesta_correcta"].lower() in respuesta.lower()
    print(f"  {test['pregunta']}: {'✅' if match else '❌'}")
```

✅ **Si ve más ✅ después, el fine-tuning funcionó.**

### 4.9 Próximo paso

Fine-tuning es Fase 2 del ciclo.

```
Fase 1: RAG (datos en contexto)
Fase 2: Fine-tuning ← Aquí estás
Fase 3: Destilación (comprime el modelo entrenado)
Fase 4: Fusión (combina modelos especializados)
Fase 5: Ciclo autónomo (mejora automática)
```

**Cuándo pasar a Fase 3:**

- Fine-tuneaste exitosamente ✅
- El modelo responde bien ✅
- Pero es lento o grande para producción ❌
- → Destila a modelo pequeño (Capítulo 5)

---

# Capítulo 5 — Destilación de Conocimiento: Modelo Grande → Pequeño

### 5.1 El problema: Tu modelo es demasiado grande/lento

Scenario: Fine-tuneaste un modelo de 70B parámetros. Funciona increíblemente bien. Pero:

- Pesa 140 GB
- Responde en 10 segundos (lento para producción)
- No cabe en una GPU de consumo
- Cuesta $1000/mes en inference en cloud

**¿Qué si pudiera ser 10x más pequeño pero tan inteligente?**

Eso es destilación.

### 5.2 Concepto: Un modelo grande enseña a uno pequeño

**Destilación** = transferencia de conocimiento de modelo grande a pequeño.

#### Analogía: El maestro y el aprendiz

```
Maestro (70B):
- Experto absoluto
- Respuestas perfectas
- Muy lento

Aprendiz (7B):
- Novato
- Respuestas incorrectas
- Muy rápido

¿Qué pasa si el maestro enseña?
Aprendiz aprende no solo respuestas, sino CÓMO PENSAR del maestro
Resultado: Aprendiz casi tan bueno como maestro, pero sigue siendo rápido
```

#### ¿Cómo transfiere el conocimiento?

A través de **soft labels** y **logits**.

**Soft labels** = probabilidades, no respuestas binarias.

```
Modelo grande responde: "¿Cuántos días de vacaciones?"
- Opción A (15 días): 95% confianza
- Opción B (20 días): 3% confianza
- Opción C (30 días): 2% confianza

En lugar de solo decir "A", el modelo pequeño aprende esas probabilidades.
Aprende no solo QUÉ responder, sino CUÁN SEGURO estar.
```

### 5.3 Proceso de destilación paso a paso

#### Paso 1: Generar datos sintéticos (modelo grande genera respuestas)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Modelo grande (maestro)
modelo_maestro = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-70B")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-70B")

# Dataset de preguntas (sin respuestas)
preguntas = [
    "¿Cuál es el proceso de onboarding?",
    "¿Cuántos días de vacaciones?",
    "¿Cómo reporto un bug?",
    # ... 1000 preguntas más
]

# Generar respuestas con modelo grande
respuestas_maestro = []
for pregunta in preguntas:
    input_ids = tokenizer(pregunta, return_tensors="pt")
    output_ids = modelo_maestro.generate(input_ids, max_new_tokens=100)
    respuesta = tokenizer.decode(output_ids[0])
    respuestas_maestro.append(respuesta)

# Guardar dataset
dataset_destilacion = [
    {"pregunta": p, "respuesta": r}
    for p, r in zip(preguntas, respuestas_maestro)
]

with open("dataset_destilacion.json", "w") as f:
    json.dump(dataset_destilacion, f)
```

#### Paso 2: Entrenar modelo pequeño con soft labels

El modelo pequeño aprende a "imitar" al grande:

```python
from unsloth import FastLanguageModel
import torch
from transformers import TrainingArguments
from trl import SFTTrainer

# Modelo pequeño (aprendiz)
modelo_aprendiz, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/phi-3-mini-4k-instruct",  # 2.7B parámetros
    max_seq_length=2048,
    dtype=torch.float16,
    load_in_4bit=True,
)

# Aplicar LoRA
modelo_aprendiz = FastLanguageModel.get_peft_model(
    modelo_aprendiz,
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
)

# Cargar dataset destilado
with open("dataset_destilacion.json") as f:
    datos = json.load(f)

# Convertir a Dataset
textos = [f"Q: {d['pregunta']}\nA: {d['respuesta']}" for d in datos]
dataset = Dataset.from_dict({"text": textos})

# Entrenar
training_args = TrainingArguments(
    output_dir="./phi_destilado",
    num_train_epochs=5,              # Más épocas (aprendiz necesita repetición)
    per_device_train_batch_size=4,
    learning_rate=1e-4,              # Learning rate más bajo
    logging_steps=10,
    save_steps=100,
)

trainer = SFTTrainer(
    model=modelo_aprendiz,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=2048,
    args=training_args,
)

trainer.train()
print("✅ Destilación completada")
```

#### Paso 3: Evaluar (¿aprendió bien?)

```python
# Comparar respuestas
test_preguntas = [
    "¿Cuál es el proceso de onboarding?",
    "¿Cuántos días de vacaciones?",
]

for pregunta in test_preguntas:
    print(f"\nPregunta: {pregunta}")
    
    # Modelo maestro (referencia)
    respuesta_maestro = modelo_maestro(pregunta)
    print(f"Maestro: {respuesta_maestro}")
    
    # Modelo aprendiz destilado
    respuesta_aprendiz = modelo_aprendiz(pregunta)
    print(f"Aprendiz: {respuesta_aprendiz}")
    
    # Comparar similitud
    similitud = comparar_similitud(respuesta_maestro, respuesta_aprendiz)
    print(f"Similitud: {similitud:.0%}")
```

### 5.4 Temperatura y logits (los secretos de la destilación)

**Temperatura** controla cómo "suave" o "dura" son las probabilidades.

```
Logits (antes de softmax):     [2.0, 1.0, 0.1]

Temperatura baja (T=0.1):      softmax → [0.99, 0.01, 0.00]  (muy seguro)
Temperatura normal (T=1.0):    softmax → [0.73, 0.27, 0.00]  (seguro)
Temperatura alta (T=5.0):      softmax → [0.50, 0.33, 0.17]  (inseguro)

Durante destilación:
Usa T=5.0 para que el modelo grande sea "menos seguro"
Esto permite que el modelo pequeño aprenda matices
```

### 5.5 Caso real: Destilar Llama 3.1 70B a Phi 3 Mini

```python
# Configuración para destilación inteligente

# Paso 1: Generar dataset con temperatura alta
temperatura_destilacion = 4.0
dataset = generar_respuestas_con_temperatura(
    modelo_maestro=llama_70b,
    preguntas=preguntas_dominio,
    temperatura=temperatura_destilacion,
    num_preguntas=1000,
)

# Paso 2: Entrenar Phi con learning rate bajo
modelo_phi, _ = FastLanguageModel.from_pretrained("unsloth/phi-3-mini-4k-instruct")
modelo_phi = FastLanguageModel.get_peft_model(modelo_phi, r=16)

trainer = SFTTrainer(
    model=modelo_phi,
    train_dataset=dataset,
    args=TrainingArguments(
        learning_rate=5e-5,  # Muy bajo
        num_train_epochs=10,
        per_device_train_batch_size=2,
    )
)

trainer.train()

# Paso 3: Validar que Phi aprendió
validar_destilacion(
    modelo_maestro=llama_70b,
    modelo_aprendiz=phi_destilado,
    test_set=test_preguntas,
    umbral_similitud=0.85,  # 85% de similitud mínimo
)
```

### 5.6 Evaluación de destilación

```python
def evaluar_destilacion(maestro, aprendiz, test_set):
    """
    Compara maestro vs aprendiz
    """
    resultados = {
        "coincidencias_exactas": 0,
        "similitud_promedio": 0,
        "tiempo_maestro_ms": 0,
        "tiempo_aprendiz_ms": 0,
    }
    
    for pregunta in test_set:
        # Maestro
        inicio = time.time()
        resp_maestro = maestro(pregunta)
        tiempo_maestro = (time.time() - inicio) * 1000
        
        # Aprendiz
        inicio = time.time()
        resp_aprendiz = aprendiz(pregunta)
        tiempo_aprendiz = (time.time() - inicio) * 1000
        
        # Comparar
        similitud = calcular_similitud(resp_maestro, resp_aprendiz)
        resultados["similitud_promedio"] += similitud
        resultados["tiempo_maestro_ms"] += tiempo_maestro
        resultados["tiempo_aprendiz_ms"] += tiempo_aprendiz
    
    # Promedios
    n = len(test_set)
    print(f"Similitud promedio: {resultados['similitud_promedio']/n:.0%}")
    print(f"Speedup: {resultados['tiempo_maestro_ms']/(resultados['tiempo_aprendiz_ms']+0.1):.1f}x")
    
    return resultados
```

✅ **Esperado:** 85-95% similitud, 5-10x más rápido

### 5.7 Generación de datasets sintéticos a escala

El secreto de una buena destilación es el dataset. No basta con 100 preguntas: necesitas 5,000–20,000 ejemplos diversos.

#### Estrategia 1: Variaciones de una pregunta semilla

```python
def expandir_preguntas(semillas, modelo_grande, n_variaciones=10):
    """
    A partir de N semillas, genera N*n_variaciones reformulaciones.
    """
    dataset_expandido = []
    for semilla in semillas:
        prompt = (
            f"Genera {n_variaciones} formas distintas de preguntar lo mismo que: "
            f"'{semilla}'. Devuelve solo las preguntas, una por línea."
        )
        respuesta = modelo_grande(prompt)
        variaciones = [v.strip("- 1234567890.") for v in respuesta.split("\n") if v.strip()]
        for v in variaciones[:n_variaciones]:
            dataset_expandido.append(v)
    return dataset_expandido
```

#### Estrategia 2: Destilación cadena-de-pensamiento (CoT)

Pide al maestro que **razone paso a paso**, no solo que responda. El aprendiz copia el razonamiento.

```python
prompt_cot = """
Pregunta: {pregunta}

Razona paso a paso antes de responder. Formato:
PASO 1: ...
PASO 2: ...
RESPUESTA FINAL: ...
"""

respuestas_con_razonamiento = []
for pregunta in preguntas:
    respuesta = modelo_maestro(prompt_cot.format(pregunta=pregunta))
    respuestas_con_razonamiento.append({
        "pregunta": pregunta,
        "respuesta_completa": respuesta,
    })
```

Resultado: el aprendiz no solo responde, **explica su razonamiento**, lo que mejora drásticamente la calidad.

#### Estrategia 3: Filtrado de calidad automatizado

No todas las respuestas del maestro son buenas. Filtra antes de entrenar:

```python
def filtrar_dataset(dataset, modelo_evaluador, umbral=0.7):
    """
    Pide a un segundo modelo que evalúe cada respuesta del maestro.
    Solo conserva las que reciben puntuación > umbral.
    """
    dataset_limpio = []
    for item in dataset:
        prompt_eval = (
            f"Evalúa esta respuesta de 0 a 1. Solo el número.\n\n"
            f"Pregunta: {item['pregunta']}\n"
            f"Respuesta: {item['respuesta']}"
        )
        score = float(modelo_evaluador(prompt_eval).strip())
        if score >= umbral:
            dataset_limpio.append(item)
    print(f"Filtrado: {len(dataset)} → {len(dataset_limpio)} ({len(dataset_limpio)/len(dataset):.0%} sobreviven)")
    return dataset_limpio
```

### 5.8 Caso real: Destilar Hermes 70B → Hermes 3B

Hermes 3 viene en varios tamaños. La meta: comprimir el de 70B en uno de 3B que sigue capturando su estilo.

```python
# Paso 1: Maestro
maestro = AutoModelForCausalLM.from_pretrained(
    "NousResearch/Hermes-3-Llama-3.1-70B",
    torch_dtype=torch.bfloat16,
    device_map="auto",
    load_in_4bit=True,  # Necesario en GPU de consumo
)

# Paso 2: Aprendiz
aprendiz, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Llama-3.2-3B",
    max_seq_length=2048,
    load_in_4bit=True,
)

aprendiz = FastLanguageModel.get_peft_model(
    aprendiz,
    r=32,            # Rank más alto = más capacidad de absorber
    lora_alpha=64,
    lora_dropout=0.05,
)

# Paso 3: Generar dataset (5000 ejemplos con CoT)
dataset = generar_dataset_cot(
    maestro=maestro,
    semillas=cargar_semillas("preguntas_dominio.json"),
    n_variaciones=10,
    temperatura=4.0,  # Soft labels
)

dataset = filtrar_dataset(dataset, modelo_evaluador=maestro, umbral=0.75)

# Paso 4: Entrenar
trainer = SFTTrainer(
    model=aprendiz,
    tokenizer=tokenizer,
    train_dataset=dataset,
    args=TrainingArguments(
        output_dir="./hermes_3b_destilado",
        num_train_epochs=8,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        warmup_steps=100,
        logging_steps=20,
        save_steps=200,
        fp16=True,
    ),
)

trainer.train()
trainer.save_model("./hermes_3b_destilado_final")
```

**Resultado típico** (en RTX 4090):
- Tiempo de entrenamiento: 6–10 horas
- Similitud con maestro: 87–92%
- Speedup en inferencia: 12–18x
- VRAM en producción: 2.5 GB (vs 40 GB del maestro cuantizado)

### 5.9 Errores comunes en destilación

#### Error 1: El aprendiz copia palabra por palabra (overfitting)

**Síntoma:** Respuestas idénticas al maestro, pero falla con cualquier reformulación.

**Solución:**
- Aumenta `lora_dropout` a 0.1
- Reduce `num_train_epochs`
- Aumenta diversidad del dataset (más reformulaciones)

#### Error 2: El aprendiz no converge

**Síntoma:** Loss se queda alta y oscilando.

**Solución:**
- Reduce `learning_rate` (prueba 5e-5)
- Verifica que el dataset tenga buen formato (sin tokens especiales rotos)
- Aumenta `r` de LoRA (más capacidad)

#### Error 3: El aprendiz alucina más que el maestro

**Causa:** El dataset tiene respuestas inventadas del maestro que el aprendiz aprende como verdad.

**Solución:**
- Filtra el dataset con un segundo modelo
- Añade ejemplos negativos: "no sé" cuando no haya información

### 5.10 Próximo paso

Destilación es Fase 3. Ahora tienes:
- Modelo pequeño
- Rápido
- Inteligente (aprendió del grande)
- Datasets sintéticos generados con CoT y filtrado

**Pero:** Cada modelo sigue siendo especialista en su dominio.

**Próximo paso:** Fusiona modelos especializados para obtener lo mejor de ambos (Capítulo 7).

Pero antes, en Capítulo 6: Sistemas multi-agente. Cómo hacer que múltiples modelos colaboren.

---

# Capítulo 6 — Sistemas Multi-Agente con MCP: Modelos Colaborando

### 6.1 El problema: Un modelo solo no es suficiente

Tu modelo es bueno. Pero:

- Para código, necesita ser especialista en programación
- Para análisis de datos, necesita ser matemático
- Para writing, necesita ser redactor

**¿Qué si tuvieras 3 modelos, cada uno especialista, trabajando juntos?**

Eso es multi-agente.

### 6.2 ¿Qué es MCP? (Model Context Protocol)

MCP es un protocolo estándar (creado por Anthropic) para que modelos se comuniquen.

```
Agent 1 (Investigador)    → Busca información
    ↓ (vía MCP)
Agent 2 (Redactor)        → Escribe basado en info
    ↓ (vía MCP)
Agent 3 (Crítico)         → Revisa calidad
    ↓ (resultado final)
Salida final
```

Cada agente es un modelo pequeño con herramientas específicas.

### 6.3 Arquitectura de un sistema multi-agente

```
┌─────────────────────────────────────────────────────────┐
│                    Orquestador (Ray)                    │
│  Coordina tareas, distribuye entre modelos              │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│                     Agent Layer                          │
├──────────────────┬──────────────────┬──────────────────┤
│  Investigador    │    Redactor      │    Crítico       │
│  (LLaMA 8B)      │  (Phi 7B)        │  (Hermes 8B)     │
│  Herramientas:   │  Herramientas:   │  Herramientas:   │
│  - Wikipedia API │  - Grammar check │  - Evaluación    │
│  - SearchAPI     │  - Formatting    │  - Metrics       │
│  - Database      │  - Templates     │  - Test suite    │
└──────────────────┴──────────────────┴──────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│                    Tool Layer (MCP)                      │
│  Provee herramientas que cada agente usa                │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│                    Recursos Externos                     │
│  APIs, DBs, archivos, ejecutables                       │
└─────────────────────────────────────────────────────────┘
```

### 6.4 Ejemplo: Sistema de 3 agentes para análisis

Tarea: Analizar un dataset de logs, escribir reporte, revisarlo.

```python
import ray
from typing import List

# Inicializar Ray (ya configurado en Capítulo 2)
ray.init(address="auto")

# ===== AGENT 1: INVESTIGADOR =====
@ray.remote
def agent_investigador(dataset_path: str) -> dict:
    """
    Busca patrones en los datos
    """
    import pandas as pd
    
    df = pd.read_csv(dataset_path)
    
    analisis = {
        "total_registros": len(df),
        "errores": df[df["nivel"] == "ERROR"].shape[0],
        "patrones_principales": df.groupby("tipo").size().head(5).to_dict(),
    }
    
    return analisis

# ===== AGENT 2: REDACTOR =====
@ray.remote
def agent_redactor(analisis: dict) -> str:
    """
    Escribe el reporte basado en análisis
    """
    reporte = f"""
    REPORTE DE ANÁLISIS DE LOGS
    ============================
    
    Registros procesados: {analisis['total_registros']}
    Errores encontrados: {analisis['errores']}
    
    Patrones principales:
    {chr(10).join(f"  - {k}: {v}" for k, v in analisis['patrones_principales'].items())}
    
    RECOMENDACIONES:
    1. Investigar patrones de error
    2. Implementar alertas para errores frecuentes
    3. Mejorar logging en módulos críticos
    """
    
    return reporte

# ===== AGENT 3: CRÍTICO =====
@ray.remote
def agent_critico(reporte: str) -> dict:
    """
    Revisa calidad del reporte
    """
    metricas = {
        "longitud": len(reporte),
        "tiene_recomendaciones": "RECOMENDACIONES" in reporte,
        "es_legible": len(reporte.split("\n")) > 5,
        "calidad": "BUENO" if "RECOMENDACIONES" in reporte else "MEJORABLE",
    }
    
    return metricas

# ===== ORQUESTADOR =====
def procesar_logs(dataset_path: str):
    """
    Coordina los 3 agentes
    """
    print("🔍 Agent 1: Investigando...")
    analisis_future = agent_investigador.remote(dataset_path)
    
    print("📝 Agent 2: Escribiendo...")
    # Agent 2 espera a Agent 1
    analisis = ray.get(analisis_future)
    reporte_future = agent_redactor.remote(analisis)
    
    print("✅ Agent 3: Revisando...")
    # Agent 3 espera a Agent 2
    reporte = ray.get(reporte_future)
    metricas_future = agent_critico.remote(reporte)
    
    # Resultado final
    metricas = ray.get(metricas_future)
    
    print("\n" + reporte)
    print("\nMÉTRICAS DE CALIDAD:")
    for k, v in metricas.items():
        print(f"  {k}: {v}")

# Ejecutar
procesar_logs("logs.csv")
```

**Flujo:**
1. Agent 1 analiza datos
2. Agent 2 escribe basado en análisis de Agent 1
3. Agent 3 revisa calidad
4. Resultado: reporte validado

### 6.5 Modelos especializados en multi-agente

Cada agente debería ser especialista:

```
Tarea: Desarrollar una API
├─ Agent Planeador (Hermes): Diseña arquitectura
├─ Agent Coder (Phi): Genera código
├─ Agent Tester (LLaMA): Escribe tests
└─ Agent Reviewer (Claude/GPT-4): Revisa todo
```

**¿Cómo asignar modelos?**

```
Tarea tipo         Modelo ideal
─────────────────────────────────
Análisis lógico   Phi (razonamiento)
Código            Phi, Qwen
Writing           Hermes, LLaMA (general)
Matemáticas       Qwen, LLaMA
Creatividad       LLaMA, Gemma
```

### 6.6 Comunicación entre agentes (MCP en detalle)

MCP define cómo agentes comparten información:

```python
# Agent A genera output
resultado_a = {
    "tipo": "analisis_datos",
    "contenido": {"errores": 42, "patrones": [...]},
    "confianza": 0.92,
    "timestamp": "2024-04-29T10:30:00",
}

# Agent B recibe vía MCP
def procesar_resultado_a(mensaje_mcp: dict):
    # Valida formato
    assert "contenido" in mensaje_mcp
    # Procesa
    contenido = mensaje_mcp["contenido"]
    # Continúa tarea
    ...
```

### 6.7 Caso de uso: Sistema de QA automático

Tarea: Generar preguntas de test automáticamente.

```python
@ray.remote
def agent_generador_preguntas(documentacion: str) -> List[str]:
    """Genera preguntas sobre la doc"""
    prompt = f"""Lee esta documentación y genera 5 preguntas de test:
    {documentacion}
    
    Formato: Una pregunta por línea"""
    
    preguntas = modelo.generate(prompt)
    return preguntas.split("\n")

@ray.remote
def agent_generador_respuestas(preguntas: List[str], documentacion: str) -> List[dict]:
    """Responde las preguntas basándose en doc"""
    respuestas = []
    for p in preguntas:
        r = modelo_rag.query(p, documentacion)
        respuestas.append({"pregunta": p, "respuesta": r})
    return respuestas

@ray.remote
def agent_evaluador(qa_pares: List[dict]) -> float:
    """Evalúa calidad de preguntas"""
    puntuacion = 0
    for par in qa_pares:
        # ¿Tiene respuesta clara?
        if len(par["respuesta"]) > 20:
            puntuacion += 1
    return puntuacion / len(qa_pares)

# Orquestar
doc = open("documentacion.md").read()
preguntas_future = agent_generador_preguntas.remote(doc)
preguntas = ray.get(preguntas_future)

respuestas_future = agent_generador_respuestas.remote(preguntas, doc)
respuestas = ray.get(respuestas_future)

score_future = agent_evaluador.remote(respuestas)
score = ray.get(score_future)

print(f"Calidad: {score:.0%}")
for par in respuestas[:3]:
    print(f"\nP: {par['pregunta']}")
    print(f"R: {par['respuesta']}")
```

### 6.8 Escalabilidad multi-agente

Con Ray, agregar agentes es trivial:

```python
@ray.remote
def agent_nuevo():
    # Nuevas capacidades
    pass

# Simplemente agregalo al flujo
resultado1 = agent_a.remote()
resultado2 = agent_b.remote(resultado1)
resultado3 = agent_nuevo.remote(resultado2)  # Nuevo agente
resultado4 = agent_c.remote(resultado3)

final = ray.get([resultado1, resultado2, resultado3, resultado4])
```

Ray automáticamente:
- Lo ejecuta en la máquina más ociosa del cluster
- Lo paraleliza si es posible
- Maneja fallos

---

# Capítulo 7 — Fusión de Modelos: Combina Especialistas

### 7.1 El problema: Cada modelo es especialista en una cosa

- Modelo A: muy bueno en código
- Modelo B: muy bueno en análisis
- Modelo C: muy bueno en writing

**¿Qué si los combinara en UNO?**

Eso es fusión de modelos.

### 7.2 Concepto: Fusión de pesos

Fusión toma los pesos de 2+ modelos y los combina.

```
Modelo A (código):      w_a1, w_a2, w_a3, ...
Modelo B (análisis):    w_b1, w_b2, w_b3, ...

Fusión simple (promedio):
w_fusión = (w_a + w_b) / 2

Fusión ponderada (da peso a uno):
w_fusión = 0.7 * w_a + 0.3 * w_b
```

### 7.3 Herramienta: mergekit

mergekit es la herramienta estándar para fusión.

```bash
# Instalar
pip install git+https://github.com/arcee-ai/mergekit.git

# Crear config de fusión
cat > config_fusión.yaml << EOF
models:
  - model: /camino/a/modelo_codigo
    parameters:
      weight: 0.7
  - model: /camino/a/modelo_análisis
    parameters:
      weight: 0.3

merge_method: linear
EOF

# Ejecutar fusión
mergekit-cli merge config_fusión.yaml ./modelo_fusionado
```

### 7.4 Métodos de fusión disponibles

```
Método        Complejidad    Mejor para              Resultado
─────────────────────────────────────────────────────────────────
linear        Baja          Modelos similares       Promedio ponderado
slerp         Baja          Modelos similares       Interpolación suave
ties          Media         Modelos diferentes      Elimina ruido
DARE          Alta          Fusión experta          Máxima calidad
```

### 7.5 Caso: Fusionar Phi (código) + Hermes (razonamiento)

```yaml
# config_fusión_phi_hermes.yaml
models:
  - model: unsloth/phi-3-mini-4k-instruct
    parameters:
      weight: 0.6
      alpha: 0.5
  - model: NousResearch/Hermes-3-Llama-3.1-8B
    parameters:
      weight: 0.4
      alpha: 0.5

merge_method: slerp
dtype: float16
```

Ejecutar:
```bash
mergekit-cli merge config_fusión_phi_hermes.yaml ./phi_hermes_fusionado

# Resultado: modelo de ~8B que entiende código Y razonamiento
```

### 7.6 Evaluación de fusión

```python
def evaluar_fusión(modelo_a, modelo_b, modelo_fusionado, test_set):
    """
    Compara rendimiento
    """
    
    for test in test_set:
        # Modelo A
        r_a = modelo_a(test["pregunta"])
        
        # Modelo B
        r_b = modelo_b(test["pregunta"])
        
        # Modelo fusionado
        r_fusionado = modelo_fusionado(test["pregunta"])
        
        # ¿Es mejor que cada uno?
        mejora_a = similitud(r_fusionado, test["respuesta_correcta"]) > similitud(r_a, test["respuesta_correcta"])
        mejora_b = similitud(r_fusionado, test["respuesta_correcta"]) > similitud(r_b, test["respuesta_correcta"])
        
        print(f"Mejora vs A: {mejora_a}, vs B: {mejora_b}")
```

### 7.7 Métodos avanzados: TIES y DARE

Cuando los modelos a fusionar son muy diferentes (por ejemplo, uno fine-tuneado en código y otro en español literario), el promedio simple destruye conocimiento. Para esos casos, existen métodos más inteligentes.

#### TIES (TrIm, Elect Sign, & Merge)

TIES funciona en tres pasos:

1. **Trim:** Elimina parámetros poco significativos (ruido).
2. **Elect Sign:** Si dos modelos discrepan en la dirección de un peso, gana el de mayor magnitud.
3. **Merge:** Promedia solo los pesos que sobrevivieron.

```yaml
# config_ties.yaml
models:
  - model: NousResearch/Hermes-3-Llama-3.1-8B
    parameters:
      density: 0.5    # Conserva el 50% más relevante
      weight: 0.6
  - model: meta-llama/CodeLlama-7b
    parameters:
      density: 0.5
      weight: 0.4

merge_method: ties
base_model: meta-llama/Llama-3.1-8B
dtype: float16
```

#### DARE (Drop And REscale)

DARE es similar a TIES pero "deja caer" pesos al azar y reescala los demás. Resultado: fusiones más limpias, menos colisiones.

```yaml
# config_dare.yaml
models:
  - model: NousResearch/Hermes-3-Llama-3.1-8B
    parameters:
      density: 0.7
      weight: 0.5
  - model: meta-llama/CodeLlama-7b
    parameters:
      density: 0.7
      weight: 0.5

merge_method: dare_ties
base_model: meta-llama/Llama-3.1-8B
dtype: float16
```

**Regla práctica:**
- Modelos similares (mismo base, diferente fine-tune) → `linear` o `slerp`
- Modelos diferentes (mismas dimensiones, distinto entrenamiento) → `ties` o `dare_ties`

### 7.8 Errores comunes en fusión

#### Error 1: "Tensor shape mismatch"

```
RuntimeError: Tensor shape mismatch: model A has [4096, 4096], model B has [5120, 5120]
```

**Causa:** Los modelos tienen arquitecturas distintas (Llama 7B vs Llama 13B).

**Solución:** Solo se pueden fusionar modelos del MISMO tamaño y arquitectura. Verifica con:

```bash
python -c "from transformers import AutoConfig; print(AutoConfig.from_pretrained('modelo_a'))"
python -c "from transformers import AutoConfig; print(AutoConfig.from_pretrained('modelo_b'))"
```

#### Error 2: "El modelo fusionado responde mal"

**Síntomas:**
- Respuestas incoherentes
- Mezcla idiomas sin sentido
- Olvida una de las habilidades

**Soluciones (en orden):**

1. Reduce los pesos al promedio (`0.5/0.5`).
2. Cambia de `linear` a `slerp`.
3. Si persiste, usa `ties` con `density: 0.5`.
4. Si nada funciona, los modelos son incompatibles. Vuelve a fine-tunear desde el mismo base.

#### Error 3: "Out of memory" al fusionar

```
torch.cuda.OutOfMemoryError: CUDA out of memory
```

**Causa:** mergekit carga ambos modelos en VRAM por defecto.

**Solución:** Usa `--cuda` solo si tienes GPU grande. En GPU de 8-16 GB, fusiona en CPU:

```bash
mergekit-cli merge config_fusion.yaml ./output --copy-tokenizer --allow-crimes
```

(`--allow-crimes` permite operaciones costosas pero más conservadoras de memoria.)

### 7.9 Cuantizar el modelo fusionado para Ollama

Después de fusionar, querrás usarlo con Ollama. El paso clave es cuantizar a GGUF:

```bash
# 1. Instalar llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make

# 2. Convertir a GGUF F16
python convert.py ../phi_hermes_fusionado --outtype f16 --outfile fusion.f16.gguf

# 3. Cuantizar a Q4_K_M (balance calidad/tamaño)
./quantize fusion.f16.gguf fusion.Q4_K_M.gguf Q4_K_M

# 4. Crear Modelfile para Ollama
cat > Modelfile <<EOF
FROM ./fusion.Q4_K_M.gguf
TEMPLATE """{{ .Prompt }}"""
PARAMETER temperature 0.7
PARAMETER num_ctx 4096
EOF

# 5. Importar en Ollama
ollama create mi-fusion -f Modelfile
ollama run mi-fusion "Escribe una función Python que calcule fibonacci"
```

### 7.10 Caso real: Modelo bilingüe técnico

**Objetivo:** un modelo que entienda código (CodeLlama) y responda en español natural (Hermes 3).

```yaml
# config_bilingue_tecnico.yaml
models:
  - model: NousResearch/Hermes-3-Llama-3.1-8B
    parameters:
      density: 0.6
      weight: 0.55
  - model: meta-llama/CodeLlama-7b-Instruct-hf
    parameters:
      density: 0.6
      weight: 0.45

merge_method: dare_ties
base_model: meta-llama/Llama-3.1-8B
dtype: float16
parameters:
  normalize: true
  int8_mask: true
```

Pruebas esperadas:

| Pregunta | Modelo CodeLlama solo | Modelo Hermes solo | Modelo fusionado |
|---|---|---|---|
| "Explica recursión en español" | Mezcla idiomas | Bien, pero sin código | Bien + código |
| "Refactoriza este Python" | Bien | Texto genérico | Bien |
| "Cuéntame un cuento" | Mediocre | Bien | Bien |

### 7.11 Próximo paso

Ahora tienes:
- ✅ Modelos fine-tuneados
- ✅ Modelos destilados
- ✅ Sistemas multi-agente
- ✅ Modelos fusionados (con TIES, DARE, slerp)
- ✅ Modelos fusionados cuantizados para Ollama

**Próximo:** Automatizar todo (Capítulo 8)

---

# Capítulo 8 — Ciclo Autónomo: Tu IA se Mejora Sola

### 8.1 El sueño: Inteligencia que mejora sin intervención

```
Lunes 8am:
  Robot: "Nuevos datos llegaron"
  Robot: "Fine-tuning iniciado"
  [4 horas de entrenamiento]
  
  Robot: "Modelo mejorado"
  Robot: "Destilando..."
  [2 horas]
  
  Robot: "Fusionando..."
  [1 hora]
  
  Robot: "Evaluando..."
  [30 min]
  
  Robot: "Tú: tu modelo mejoró 8% esta semana. Reporte adjunto."

Tú: "Cool 😎"
```

### 8.2 Arquitectura del ciclo autónomo

```
┌──────────────────────────────────────────────────┐
│         Scheduler (APScheduler / Cron)           │
│         Ejecuta cada semana (lunes 8am)          │
└──────────────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────────────┐
│  1. DETECTOR DE DATOS                            │
│  "¿Hay datos nuevos desde última semana?"        │
└──────────────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────────────┐
│  2. ENTRENADOR (Fine-tuning)                     │
│  Si hay datos: fine-túnea modelo                 │
└──────────────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────────────┐
│  3. DESTILADOR                                   │
│  Comprime modelo grande a pequeño               │
└──────────────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────────────┐
│  4. EVALUADOR                                    │
│  Compara viejo vs nuevo                          │
└──────────────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────────────┐
│  5. PUBLICADOR                                   │
│  Si mejoró: reemplaza versión en producción     │
└──────────────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────────────┐
│  6. REPORTERO                                    │
│  Envía reporte a Slack / email                  │
└──────────────────────────────────────────────────┘
```

### 8.3 Script del ciclo completo

```python
# ciclo_autonomo.py

import ray
import json
import os
from datetime import datetime
from pathlib import Path
import requests

ray.init(address="auto")

# ===== 1. DETECTOR =====
@ray.remote
def detector_datos():
    """Busca datos nuevos en carpeta"""
    datos_path = Path("datos_nuevos")
    archivos = list(datos_path.glob("*.json"))
    
    print(f"📊 Detectados {len(archivos)} archivos nuevos")
    return archivos

# ===== 2. ENTRENADOR =====
@ray.remote
def entrenador(archivos):
    """Fine-túnea modelo con datos nuevos"""
    if not archivos:
        print("⏭️ Sin datos nuevos, saltando fine-tuning")
        return None
    
    print("🔧 Iniciando fine-tuning...")
    
    # Cargar datos
    todos_datos = []
    for archivo in archivos:
        with open(archivo) as f:
            todos_datos.extend(json.load(f))
    
    # Crear dataset
    dataset = crear_dataset(todos_datos)
    
    # Fine-túnea (script del Capítulo 4)
    modelo_finetuned = ejecutar_finetuning(dataset)
    
    print(f"✅ Fine-tuning completado: {len(todos_datos)} ejemplos")
    
    return modelo_finetuned

# ===== 3. DESTILADOR =====
@ray.remote
def destilador(modelo_finetuned):
    """Destila modelo grande a pequeño"""
    if modelo_finetuned is None:
        return None
    
    print("🫗 Destilando modelo...")
    
    # Genera respuestas con modelo grande
    dataset_destilacion = generar_datos_destilacion(modelo_finetuned)
    
    # Entrena modelo pequeño
    modelo_destilado = entrenar_destilacion(dataset_destilacion)
    
    print("✅ Destilación completada")
    
    return modelo_destilado

# ===== 4. EVALUADOR =====
@ray.remote
def evaluador(modelo_viejo, modelo_nuevo):
    """Compara rendimiento"""
    if modelo_nuevo is None:
        return {"mejora": 0, "valido": False}
    
    print("📊 Evaluando modelos...")
    
    # Test set
    test_set = cargar_test_set()
    
    # Evaluar viejo
    score_viejo = evaluar_modelo(modelo_viejo, test_set)
    
    # Evaluar nuevo
    score_nuevo = evaluar_modelo(modelo_nuevo, test_set)
    
    mejora = (score_nuevo - score_viejo) / (score_viejo + 0.001) * 100
    
    print(f"  Viejo: {score_viejo:.2f}")
    print(f"  Nuevo: {score_nuevo:.2f}")
    print(f"  Mejora: {mejora:+.1f}%")
    
    return {
        "mejora": mejora,
        "valido": mejora > 0,  # Valido si mejoró
        "score_viejo": score_viejo,
        "score_nuevo": score_nuevo,
    }

# ===== 5. PUBLICADOR =====
@ray.remote
def publicador(modelo_nuevo, metricas_evaluacion):
    """Reemplaza modelo en producción si mejoró"""
    if not metricas_evaluacion["valido"]:
        print("⏭️ Modelo no mejoró, no publicando")
        return False
    
    print("🚀 Publicando modelo en producción...")
    
    # Guardar modelo nuevo
    modelo_nuevo.save_pretrained("./modelos/produccion/latest")
    
    # Crear versión con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    modelo_nuevo.save_pretrained(f"./modelos/archivo/{timestamp}")
    
    print(f"✅ Publicado: ./modelos/produccion/latest")
    
    return True

# ===== 6. REPORTERO =====
@ray.remote
def reportero(metricas_evaluacion, mejora_publicada):
    """Envía reporte a Slack"""
    timestamp = datetime.now().isoformat()
    
    mensaje = f"""
🤖 CICLO AUTÓNOMO COMPLETADO
Timestamp: {timestamp}

Métricas:
  - Score anterior: {metricas_evaluacion['score_viejo']:.2f}
  - Score nuevo: {metricas_evaluacion['score_nuevo']:.2f}
  - Mejora: {metricas_evaluacion['mejora']:+.1f}%
  - Publicado: {"Sí ✅" if mejora_publicada else "No ⏭️"}

Próximo ciclo: próximo lunes 8am
    """
    
    # Enviar a Slack
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if webhook_url:
        requests.post(webhook_url, json={"text": mensaje})
    
    # Guardar en log
    with open("ciclos_autonomos.log", "a") as f:
        f.write(mensaje + "\n")
    
    print("📧 Reporte enviado")

# ===== ORQUESTADOR =====
@ray.remote
def ciclo_completo():
    """Ejecuta el ciclo entero"""
    print("\n" + "="*50)
    print("🔄 INICIANDO CICLO AUTÓNOMO")
    print("="*50 + "\n")
    
    # 1. Detectar
    archivos = ray.get(detector_datos.remote())
    
    # 2. Entrenar
    modelo_finetuned = ray.get(entrenador.remote(archivos))
    
    # 3. Destilar
    modelo_destilado = ray.get(destilador.remote(modelo_finetuned))
    
    # 4. Evaluar
    modelo_viejo = cargar_modelo_produccion()
    metricas = ray.get(evaluador.remote(modelo_viejo, modelo_destilado))
    
    # 5. Publicar
    publicado = ray.get(publicador.remote(modelo_destilado, metricas))
    
    # 6. Reportar
    ray.get(reportero.remote(metricas, publicado))
    
    print("\n" + "="*50)
    print("✅ CICLO COMPLETADO")
    print("="*50 + "\n")

# ===== SCHEDULER =====
if __name__ == "__main__":
    from apscheduler.schedulers.background import BackgroundScheduler
    import atexit
    
    # Programar para cada lunes a las 8am
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: ray.get(ciclo_completo.remote()),
        trigger="cron",
        day_of_week="mon",
        hour=8,
        minute=0,
    )
    
    scheduler.start()
    print("✅ Scheduler iniciado. Próximo ciclo: próximo lunes 8am")
    
    # Mantener scheduler corriendo
    atexit.register(lambda: scheduler.shutdown())
    
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Detenido manualmente")
```

### 8.4 Monitoreo del ciclo

```python
# dashboard_ciclos.py

def mostrar_dashboard():
    """Visualiza histórico de ciclos"""
    
    with open("ciclos_autonomos.log") as f:
        lineas = f.readlines()
    
    # Parse histórico
    for bloque in " ".join(lineas).split("CICLO AUTÓNOMO"):
        if "Score anterior:" in bloque:
            # Extraer métricas
            score_ant = float(extraer(bloque, "Score anterior: ", "\n"))
            score_nuevo = float(extraer(bloque, "Score nuevo: ", "\n"))
            mejora = float(extraer(bloque, "Mejora: ", "%"))
            
            print(f"{score_ant:.2f} → {score_nuevo:.2f} ({mejora:+.1f}%)")

# Ejecutar dashboard
mostrar_dashboard()
```

### 8.5 Próximo paso

Ahora tienes:
- ✅ Ciclo autónomo que corre cada semana
- ✅ Detecta datos nuevos
- ✅ Entrena automáticamente
- ✅ Destila
- ✅ Evalúa
- ✅ Publica si mejoró
- ✅ Reporta

**El sueño:** Tu IA mejora cada semana sin que hagas nada. Eso es Capítulo 8 completado.

**Próximo:** Capítulo 9. Proyecto integrador que usa TODO esto.

---

# Capítulo 9 — Proyecto Integrador Final: Sistema de IA Autónomo Completo

### 9.1 El proyecto: Chatbot que entrena cada semana

Vas a construir un sistema completo:

```
1. Usuario hace preguntas a un chatbot
2. Cada pregunta + respuesta se guarda
3. Cada lunes, el sistema:
   - Toma conversaciones reales
   - Fine-túnea el modelo
   - Destila
   - Evalúa
   - Si mejoró, publica
4. Semana siguiente: usuario nota que responde mejor
```

### 9.2 Requisitos del proyecto

**Hardware:**
- 1 GPU de 8+ GB (tu máquina principal)
- 1+ máquina de cluster (cluster distribuido)
- 32 GB RAM mínimo

**Software:**
- Ollama (con 2+ modelos)
- LangChain (para RAG)
- Ray (para distribución)
- unsloth (para fine-tuning)
- APScheduler (para automatización)

**Datos:**
- 100-200 conversaciones reales (para fine-tuning)
- 10-20 para test

### 9.3 Arquitectura del sistema

```
┌─────────────────────────────────────────────┐
│         INTERFAZ USUARIO                    │
│    Discord Bot / Telegram / Web              │
└────────────────┬────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────┐
│      API (FastAPI)                          │
│  Recibe preguntas, almacena conversaciones  │
└────────────────┬────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────┐
│     RAG + Inference (LangChain + Ollama)    │
│  Responde preguntas con contexto            │
└────────────────┬────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────┐
│    DATABASE                                 │
│  Conversaciones, modelos, métricas          │
└────────────────┬────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────┐
│  CICLO AUTÓNOMO (Capítulo 8)               │
│  Ejecuta cada lunes automáticamente         │
└─────────────────────────────────────────────┘
```

### 9.4 Código completo del proyecto

#### Parte 1: API (main.py)

```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from langchain.chat_models import ChatOllama
from langchain.vectorstores import Chroma
import sqlite3
import json

app = FastAPI()
db = sqlite3.connect("conversaciones.db", check_same_thread=False)

# Modelo de entrada
class Pregunta(BaseModel):
    texto: str
    usuario_id: str

# Modelo LLM
llm = ChatOllama(model="hermes3", base_url="http://localhost:11434")

# Vector store (RAG)
vectorstore = Chroma(persist_directory="./chroma_db")

# ===== ENDPOINTS =====

@app.post("/preguntar")
def preguntar(pregunta: Pregunta):
    """Responde pregunta con RAG + LLM"""
    
    # 1. RAG: Buscar contexto
    docs_relevantes = vectorstore.similarity_search(pregunta.texto, k=3)
    contexto = "\n".join([d.page_content for d in docs_relevantes])
    
    # 2. Generar respuesta
    prompt = f"""Contexto:
{contexto}

Pregunta: {pregunta.texto}

Responde basándote en el contexto."""
    
    respuesta = llm.predict(prompt)
    
    # 3. Guardar conversación
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO conversaciones (usuario_id, pregunta, respuesta, timestamp)
        VALUES (?, ?, ?, ?)
    """, (pregunta.usuario_id, pregunta.texto, respuesta, datetime.now().isoformat()))
    db.commit()
    
    return {
        "respuesta": respuesta,
        "fuentes": [d.metadata.get("source", "?") for d in docs_relevantes]
    }

@app.get("/metricas")
def metricas():
    """Retorna métricas de entrenamiento"""
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ciclos ORDER BY id DESC LIMIT 1")
    ultimo_ciclo = cursor.fetchone()
    
    return {
        "score_anterior": ultimo_ciclo[1],
        "score_nuevo": ultimo_ciclo[2],
        "mejora": ultimo_ciclo[3],
    }

# ===== INIT =====

def init_db():
    """Crea tablas si no existen"""
    cursor = db.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversaciones (
            id INTEGER PRIMARY KEY,
            usuario_id TEXT,
            pregunta TEXT,
            respuesta TEXT,
            timestamp TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ciclos (
            id INTEGER PRIMARY KEY,
            score_anterior FLOAT,
            score_nuevo FLOAT,
            mejora FLOAT,
            timestamp TEXT
        )
    """)
    
    db.commit()

if __name__ == "__main__":
    init_db()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Ejecutar:
```bash
python main.py
# API en http://localhost:8000
```

#### Parte 2: Entrenamiento automático (auto_train.py)

```python
# auto_train.py
# Este es el ciclo autónomo del Capítulo 8
# Adaptado para nuestro proyecto

import ray
import sqlite3
import json
from datetime import datetime

ray.init(address="auto")

@ray.remote
def ciclo_entrenamiento_proyecto():
    """Ciclo completo para el proyecto"""
    
    # 1. Extraer conversaciones reales
    db = sqlite3.connect("conversaciones.db")
    cursor = db.cursor()
    cursor.execute("""
        SELECT pregunta, respuesta FROM conversaciones 
        WHERE timestamp > datetime('now', '-7 days')
    """)
    conversaciones = cursor.fetchall()
    
    if len(conversaciones) < 10:
        print("⏭️ Menos de 10 conversaciones, saltando")
        return
    
    print(f"📊 Recolectadas {len(conversaciones)} conversaciones")
    
    # 2. Convertir a formato de entrenamiento
    dataset = [
        {
            "instruction": c[0],
            "input": "",
            "output": c[1]
        }
        for c in conversaciones
    ]
    
    # 3. Fine-tuning (código del Capítulo 4)
    modelo_ft = ejecutar_fine_tuning(dataset)
    print("✅ Fine-tuning completado")
    
    # 4. Destilación (código del Capítulo 5)
    modelo_destilado = ejecutar_destilacion(modelo_ft)
    print("✅ Destilación completada")
    
    # 5. Evaluación
    test_set = cargar_test_set()
    score_viejo = evaluar_en_produccion(test_set)
    score_nuevo = evaluar_modelo_nuevo(modelo_destilado, test_set)
    mejora = (score_nuevo - score_viejo) / score_viejo * 100
    
    print(f"📊 Mejora: {mejora:+.1f}%")
    
    # 6. Si mejoró, publicar
    if mejora > 0:
        modelo_destilado.save_pretrained("./modelos/produccion/latest")
        print("🚀 Publicado en producción")
    
    # 7. Registrar en DB
    cursor.execute("""
        INSERT INTO ciclos (score_anterior, score_nuevo, mejora, timestamp)
        VALUES (?, ?, ?, ?)
    """, (score_viejo, score_nuevo, mejora, datetime.now().isoformat()))
    db.commit()
    
    return True

# Programar
if __name__ == "__main__":
    from apscheduler.schedulers.background import BackgroundScheduler
    import atexit
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: ray.get(ciclo_entrenamiento_proyecto.remote()),
        trigger="cron",
        day_of_week="mon",
        hour=8,
    )
    scheduler.start()
    print("✅ Ciclo autónomo programado (lunes 8am)")
    
    atexit.register(lambda: scheduler.shutdown())
    
    # Mantener corriendo
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Detenido")
```

#### Parte 3: Discord Bot (bot.py)

```python
# bot.py
import discord
from discord.ext import commands
import requests

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

API_URL = "http://localhost:8000"

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

@bot.command()
async def ask(ctx, *, pregunta):
    """Haz una pregunta al chatbot"""
    
    # Llamar API
    response = requests.post(f"{API_URL}/preguntar", json={
        "texto": pregunta,
        "usuario_id": str(ctx.author.id)
    })
    
    datos = response.json()
    respuesta = datos["respuesta"]
    
    # Enviar a Discord
    embed = discord.Embed(
        title="🤖 Respuesta",
        description=respuesta[:2000],  # Límite Discord
        color=discord.Color.blue()
    )
    
    await ctx.send(embed=embed)

@bot.command()
async def metricas(ctx):
    """Ver métricas del modelo"""
    
    response = requests.get(f"{API_URL}/metricas")
    datos = response.json()
    
    embed = discord.Embed(
        title="📊 Métricas del Modelo",
        color=discord.Color.green()
    )
    embed.add_field(name="Score Anterior", value=f"{datos['score_anterior']:.2f}")
    embed.add_field(name="Score Nuevo", value=f"{datos['score_nuevo']:.2f}")
    embed.add_field(name="Mejora", value=f"{datos['mejora']:+.1f}%")
    
    await ctx.send(embed=embed)

# Token en variable de entorno
import os
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot.run(TOKEN)
```

Ejecutar:
```bash
export DISCORD_BOT_TOKEN="tu_token"
python bot.py
```

### 9.5 Diagrama de ejecución completa

```
Usuario en Discord:
  !ask ¿Cuál es el proceso de vacaciones?
    ↓
Bot envía a API
    ↓
API:
  1. Busca contexto en RAG
  2. Genera respuesta con LLM
  3. Guarda en DB
    ↓
Bot responde en Discord
  "Según nuestros documentos, son 15 días..."
    ↓
[Cada lunes a las 8am]
    ↓
Ciclo autónomo:
  1. Recolecta conversaciones de la semana
  2. Fine-túnea modelo
  3. Destila
  4. Evalúa
  5. Si mejoró: publica
  6. Reporta en Slack
    ↓
[Próxima semana]
    ↓
Modelo mejorado, usuarios notan respuestas mejores
```

### 9.6 Checklist: Lanzar el sistema

- [ ] Base de datos creada (`conversaciones.db`)
- [ ] Modelos en Ollama descargados
- [ ] RAG indexado (`chroma_db`)
- [ ] API iniciada (`python main.py`)
- [ ] Ciclo autónomo programado (`python auto_train.py`)
- [ ] Bot Discord conectado (`python bot.py`)
- [ ] Cluster Ray funcionando (2+ máquinas)
- [ ] Primeras conversaciones guardadas
- [ ] Primer ciclo lunes ejecutado exitosamente
- [ ] Métricas mejorando semana a semana

### 9.7 Costos y ROI

```
Inversión inicial (hardware):
  - GPU actual: $0 (ya tienes)
  - Máquina cluster: $200
  - Networking: $50
  - Total: $250

Costo mensual:
  - Electricidad: $50
  - Mantenimiento: $0
  Total: $50/mes

Ahorro vs cloud:
  - API Claude: $1000/mes
  - API OpenAI: $500-2000/mes
  - Runpod (backup): $200/mes
  
  Ahorro: $500-2000/mes

ROI: 0.2-0.5 meses (recuperas inversión muy rápido)
```

### 9.8 Próximos pasos avanzados

Una vez el sistema corra:

1. **Agregar más agentes:** Multi-agente del Capítulo 6
2. **Fusionar modelos:** Capítulo 7
3. **Escalar cluster:** Agregar más máquinas
4. **Monetizar:** Vender acceso a la API
5. **Especializarse:** Fine-túnea para dominio específico

---

# Apéndices

## Apéndice A: Comandos Esenciales de Ollama

```bash
# === Gestión de modelos ===
ollama list                       # Modelos descargados
ollama pull llama3.2              # Descargar
ollama pull hermes3               # Descargar Hermes 3
ollama rm nombre_modelo           # Eliminar
ollama show llama3.2              # Ver metadatos del modelo
ollama cp llama3.2 mi-llama       # Clonar (para Modelfile custom)

# === Inferencia ===
ollama run llama3.2                              # Modo interactivo
ollama run llama3.2 "Pregunta puntual"           # Una sola consulta
ollama run llama3.2 --verbose                    # Ver tokens/segundo

# === Servicio ===
ollama serve                      # Arrancar servidor (suele auto-arrancar)
pkill -f ollama                   # Parar el servicio

# === Logs (macOS) ===
tail -f ~/.ollama/logs/server.log

# === Logs (Linux con systemd) ===
journalctl -u ollama -f

# === Importar GGUF custom ===
cat > Modelfile <<EOF
FROM ./mi-modelo.Q4_K_M.gguf
PARAMETER temperature 0.7
PARAMETER num_ctx 4096
EOF
ollama create mi-modelo -f Modelfile

# === API HTTP ===
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Hola",
  "stream": false
}'
```

## Apéndice B: Errores Frecuentes y Soluciones

### GPU / Memoria

| Error | Causa | Solución |
|---|---|---|
| `CUDA out of memory` | VRAM insuficiente | Reduce `batch_size`, `max_seq_length`, o usa `load_in_4bit=True` |
| `RuntimeError: NCCL error` | Múltiples GPUs mal configuradas | `export CUDA_VISIBLE_DEVICES=0` |
| `torch.cuda.is_available()` devuelve `False` | Drivers/CUDA mal instalados | Reinstala drivers NVIDIA + `pip install torch --index-url https://download.pytorch.org/whl/cu121` |
| `MPS backend out of memory` (Mac) | Memoria unificada saturada | `export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0` |

### Ollama

| Error | Causa | Solución |
|---|---|---|
| `connection refused` | Servicio no corriendo | `ollama serve` en otra terminal |
| `model not found` | Modelo no descargado | `ollama pull <nombre>` |
| Respuestas truncadas | `num_ctx` bajo | Aumenta en Modelfile: `PARAMETER num_ctx 8192` |
| Timeout en peticiones largas | Cliente impaciente | Aumenta `timeout` en tu código (300s+) |

### Ray / Cluster

| Error | Causa | Solución |
|---|---|---|
| `ray connection refused` | Head node caído | `ray status` y, si nada, `ray start --head` |
| Workers no se conectan | Firewall | Abre puertos 6379, 8265, 10001-10010 |
| `actors keep dying` | OOM en worker | Reduce `num_gpus` por actor o el batch |

### Hugging Face / Datasets

| Error | Causa | Solución |
|---|---|---|
| `401 Unauthorized` en `from_pretrained` | Modelo gated (Llama, Gemma) | `huggingface-cli login` y aceptar términos en la web |
| `dataset format invalid` | JSON mal formado | `python -m json.tool dataset.json` |
| Tokenizer no encuentra `pad_token` | Modelo sin token de padding | `tokenizer.pad_token = tokenizer.eos_token` |

### QLoRA / Fine-tuning

| Error | Causa | Solución |
|---|---|---|
| Loss se queda en `nan` | Learning rate demasiado alto | Reduce a `1e-4` o `5e-5` |
| Loss no baja | Dataset muy pequeño o mal formato | Verifica formato y usa al menos 100 ejemplos |
| Modelo final no responde como esperabas | Pocas épocas o LoRA `r` bajo | Sube a 3-5 épocas y `r=16` o `r=32` |

## Apéndice C: Fuentes de Modelos y Datasets

### Modelos

- **Hugging Face Hub:** https://huggingface.co/models — el catálogo principal
- **Ollama Library:** https://ollama.com/library — modelos listos para Ollama
- **NousResearch (Hermes):** https://huggingface.co/NousResearch — la familia Hermes
- **unsloth (versiones optimizadas):** https://huggingface.co/unsloth — modelos preparados para QLoRA
- **Replicate:** https://replicate.com/models — modelos hosteados
- **TheBloke (GGUF cuantizados, archivo histórico):** https://huggingface.co/TheBloke

### Datasets para fine-tuning

- **OpenAssistant/oasst1:** conversaciones humanas multi-idioma
- **databricks/databricks-dolly-15k:** instrucciones generales
- **OpenOrca:** dataset masivo derivado de GPT-4
- **HuggingFaceH4/ultrachat_200k:** chats multi-turno
- **glaiveai/glaive-function-calling-v2:** function calling

### Benchmarks

- **lm-eval-harness:** https://github.com/EleutherAI/lm-evaluation-harness
- **HELM:** https://crfm.stanford.edu/helm/
- **Open LLM Leaderboard:** https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard

## Apéndice D: Glosario Extendido

**Embedding** — Vector numérico (típicamente de 384 a 4096 dimensiones) que representa el significado de un texto. Textos similares tienen embeddings cercanos en el espacio vectorial.

**Fine-tuning** — Reentrenamiento de un modelo preentrenado con datos nuevos para adaptarlo a un dominio o tarea específica.

**QLoRA** — Quantized Low-Rank Adaptation. Técnica que permite fine-tunear modelos grandes en GPU de consumo cuantizando los pesos a 4 bits y entrenando solo adaptadores pequeños.

**LoRA** — Low-Rank Adaptation. Inserta matrices pequeñas (`r` filas) en las capas del modelo y solo entrena esas matrices, dejando los pesos originales intactos.

**Destilación** — Transferencia de conocimiento de un modelo grande (maestro) a uno pequeño (aprendiz) mediante imitación de su distribución de salida.

**RAG** — Retrieval-Augmented Generation. El modelo busca información relevante en una base de datos externa antes de responder, sin necesidad de reentrenarse.

**VRAM** — Video RAM. Memoria dedicada de la GPU, donde viven los pesos del modelo durante inferencia y entrenamiento.

**Cuantización** — Reducir la precisión numérica de los pesos (de FP16 a INT8 o INT4) para que ocupen menos memoria, sacrificando un poco de precisión.

**GGUF** — Formato binario optimizado para inferencia eficiente en CPU/GPU de consumo, usado por llama.cpp y Ollama.

**Logits** — Salidas del modelo antes de aplicar softmax. Contienen más información que las probabilidades finales y son clave en destilación.

**Soft labels** — Distribución de probabilidad sobre todas las opciones, en lugar de una respuesta única. Permiten transferir matices al aprendiz.

**Temperatura** — Parámetro que controla la aleatoriedad del modelo. Baja (0.1) = determinista; alta (1.5+) = creativo.

**Top-k / Top-p** — Estrategias de muestreo. Top-k considera solo las `k` opciones más probables; top-p considera las que sumen hasta `p` de probabilidad acumulada.

**Cluster** — Conjunto de máquinas conectadas por red que comparten carga de trabajo (ej. entrenamiento distribuido con Ray).

**MCP (Model Context Protocol)** — Protocolo abierto para que múltiples modelos compartan contexto y herramientas.

**Multi-agente** — Sistema donde varios modelos especializados colaboran, cada uno con un rol distinto (planificador, ejecutor, evaluador).

**Mergekit** — Herramienta para fusionar pesos de varios modelos en uno solo.

**Slerp** — Spherical Linear Interpolation. Método de fusión que preserva mejor la geometría del espacio de pesos.

**TIES / DARE** — Métodos avanzados de fusión que recortan ruido y resuelven conflictos entre modelos.

## Apéndice E: Checklist final del libro

Si has completado todo el libro, deberías tener:

- [ ] Ollama instalado y corriendo localmente
- [ ] Al menos un modelo base descargado (Llama 3.2 o Hermes 3)
- [ ] Entorno Python con `unsloth`, `transformers`, `peft`, `trl` funcionando
- [ ] Una base RAG con tus documentos indexados
- [ ] Un modelo fine-tuneado con QLoRA en tu dominio
- [ ] Un modelo destilado (versión ligera) en producción
- [ ] Un sistema multi-agente con al menos 2 roles colaborando
- [ ] Un modelo fusionado con mergekit
- [ ] Ciclo automatizado (APScheduler/cron) corriendo semanalmente
- [ ] Cluster local con Ray (head + al menos 1 worker)
- [ ] Métricas registradas y dashboard funcionando

Si tienes los 11 puntos: enhorabuena, tienes una IA local autónoma corriendo en tu casa.

---

**FIN DEL LIBRO**

Ahora tienes todo. Desde configuración básica hasta un sistema autónomo completo que mejora cada semana.
