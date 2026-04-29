# Entrena tu Propia IA en Local: Aprendizaje Autónomo con Recursos Limitados

---

## Prólogo

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

## Capítulo 1 — Fundamentos: Qué está pasando realmente

### 1.1 Tres conceptos que parecen iguales (pero no lo son)

La gente usa indistintamente "entrenar", "fine-tunear", "inferir" como si fueran lo mismo. No lo son. Y esta es la razón por la que muchas personas gastan dinero sin razón.

#### Inferencia

**Qué es:** hacer una pregunta a un modelo que ya está entrenado y listo.

**Analogía:** Es como consultar con un amigo que tiene 10 años de experiencia. Ya sabe todo. Tú solo haces la pregunta. Tu amigo piensa y responde.

**Costo:** Bajo. Mínimo cómputo. Dura segundos (o minutos si el modelo es grande).

**Ejemplo:**
```bash
ollama run llama2 "¿Cuál es la capital de Francia?"
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

1. Mostrarle ejemplos de entrada-salida corrects
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
| **¿Qué pasa si tus datos cambian?** | Actualiza la DB, listo | Debes reentrenar | Debes redestilizar |
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
- **¿Por qué?** Muy veloce. Buena precisión. Excelente arquitectura.
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
ollama pull llama2
```

**Opción B: Hermes (si prefieres instrucciones limpias)**
```bash
ollama pull hermes2-pro
```

**Opción C: Ambos** (si tienes espacio y quieres comparar)
```bash
ollama pull llama2
ollama pull hermes2-pro
```

Esto descarga el modelo. Dependiendo de tu conexión, tomará 5-30 minutos.

⚠️ **Espera a que termine.** No interrumpas. Si se interrumpe, ejecuta el comando de nuevo. Ollama continuará desde donde se quedó.

#### Paso 4: Ejecutar tu primer inference

**Con LLaMA:**
```bash
ollama run llama2 "¿Cuál es la capital de Francia?"
```

**Con Hermes:**
```bash
ollama run hermes2-pro "¿Cuál es la capital de Francia?"
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
ollama show llama2
```

Busca una línea que diga `gpu:` o similar. Si ves números, tu GPU está activa.

❌ Si ves `gpu: 0%`, Ollama está usando solo CPU (lento). Significa que CUDA/Metal no está instalado correctamente. Reinstala tu driver de GPU.

#### Paso 3: Benchmark básico

Ejecuta un modelo pequeño y grande, y mide tiempo:

```bash
time ollama run llama2 "Escribe un poema sobre programación"
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

### 2.5.5 ¿Necesitas más poder? Estrategias de expansión de hardware

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
- Idealpara experimentos rápidos

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

### 2.5.6 Construir un cluster casero: tu plataforma escalable para AIs

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

### 2.6 Instalación de dependencias Python para fine-tuning

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

### 2.7 Primer fine-tuning: verificación de "end-to-end"

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
    model_name="unsloth/llama-2-7b",
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
- ✅ Carga Llama 2 (7B)
- ✅ Aplica QLoRA
- ✅ Fine-túnea con 5 ejemplos
- ✅ Verifica que CUDA funciona

Si ves ✅ al final, todo está correcto. Si ves error, lámoslo, y busca la solución en Capítulo 1.5 "Errores comunes".

### 2.8 Próximo paso

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
    model="hermes2-pro",
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

**¿Continúo con el Capítulo 4 (Fine-tuning con QLoRA)?**
