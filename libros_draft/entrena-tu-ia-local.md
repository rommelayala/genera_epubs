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

**Mes 4:** El modelo sigue diciendo "tonterías" en ciertos contextos. No capta la jerga de tu dominio. Haces fine-tuning con 500 conversaciones reales con clientes. Ahora el modelo "piensa" como un especialista en logs.

**Mes 8:** Necesitas que el modelo sea 10x más rápido para servir a 1,000 usuarios. Destilas de tu modelo fine-tuneado (que es grande) a uno pequeño. Obtienes 90% de precisión en 1/10 del tiempo.

**Mes 12:** Combinas tu modelo destilado especialista con otro modelo destilado especialista en anomalías. Tienes un super-modelo. Fusión de modelos.

Este es el ciclo que aprenderás en este libro.

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

### 2.2 Matriz de decisión: ¿Cuál elijo?

```
¿Tu GPU tiene 8 GB?
  → Sí → ¿Necesitas código?
        → Sí → Phi 4 (4B)
        → No  → Gemma 3 (7B)
  → No (< 8 GB) → Gemma 3 (2B)

¿Tu GPU tiene 12+ GB?
  → Sí → ¿Necesitas máxima inteligencia?
        → Sí → LLaMA 3.2 (8B) o Phi 4 (14B)
        → No  → Cualquiera de los anteriores

¿Tu GPU tiene 20+ GB?
  → Sí → Qwen 3.5 (32B) o LLaMA 3.2 (70B)
  → Pero recuerda: para fine-tuning usa el modelo MENOR que sea viable
```

**Mi recomendación personal para empezar:** LLaMA 3.2 (8B). No es porque sea el mejor. Es porque es el más documentado, tiene más ejemplos comunitarios, y los errores que encontres ya están resueltos en StackOverflow.

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

```bash
ollama pull llama2
```

Esto descarga el modelo. Dependiendo de tu conexión, tomará 5-30 minutos.

⚠️ **Espera a que termine.** No interrumpas. Si se interrumpe, ejecuta el comando de nuevo. Ollama continuará desde donde se quedó.

#### Paso 4: Ejecutar tu primer inference

```bash
ollama run llama2 "¿Cuál es la capital de Francia?"
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
```

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

**¿Continúo con el Capítulo 3 (RAG), o prefieres que revise/mejore algo de estos primeros dos capítulos?**
