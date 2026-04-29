# Entrena tu Propia IA en Local: Aprendizaje Autónomo con Recursos Limitados
*(Edición Especial Mac M1 Pro / 32GB)*

---

## Prólogo: La IA ya no es solo de las Big Tech

¡Hola! Qué bueno tenerte por aquí. Si has abierto este libro, es porque probablemente estés cansado de depender de una API de pago, de preocuparte por la privacidad de tus datos o, simplemente, porque tienes un Mac potente y quieres ver de qué es capaz realmente.

Este libro nace de una frustración personal: la mayoría de la documentación sobre entrenamiento de IA asume que tienes un clúster de H100s de Nvidia. **Spoiler: no los necesitas.** ### ¿Para quién es este libro?
* **Para ti**, que tienes un Mac M1 Pro con 32GB de memoria unificada y quieres dejar de ser un simple "usuario" para convertirte en "creador".
* Para desarrolladores que quieren integrar modelos privados en sus flujos de trabajo locales.
* Para entusiastas que no se conforman con el "Chat" y quieren entender cómo se destila o se fusiona un modelo.

### ¿Para quién NO es?
* Para quien busca una guía académica llena de fórmulas matemáticas. Aquí vamos a la práctica.
* Para quien cree que va a entrenar un modelo desde cero (Pre-training) que compita con GPT-4 en su casa. Vamos a ser realistas: vamos a hacer **Fine-tuning, Destilación y Fusión**, que es donde reside el verdadero poder.

### El Hardware: La verdad sobre tu Mac
Tienes un Mac M1 Pro con 32GB de RAM. En el mundo de la IA, esto es un superpoder. A diferencia de un PC tradicional, tu CPU y tu GPU comparten esos 32GB. Esto significa que puedes cargar modelos inmensos que en un PC normal requerirían una tarjeta gráfica de 2.000 dólares. El ecosistema nativo de Apple (Metal y MLX) será nuestra arma secreta.

### Mapa Visual del Ciclo de Mejora Continua
Imagina este flujo como un círculo:
1.  **Elegir un modelo base** (Llama 3.2, Phi-4).
2.  **RAG:** Darle contexto inmediato con tus documentos.
3.  **Fine-tuning (MLX LoRA):** Enseñarle un estilo o conocimiento específico.
4.  **Destilación:** Pasar la sabiduría de un modelo gigante a uno pequeño que vuele en tu Mac.
5.  **Fusión (Merge):** Mezclar lo mejor de dos mundos sin gastar un gramo de energía extra.
6.  **Agentes:** Dejar que la IA use herramientas para mejorar su propio dataset.

---

## Capítulo 1 — Fundamentos: Rompiendo mitos

Antes de instalar nada, pongamos los pies en la tierra. Hay mucha confusión allá afuera sobre qué significa "entrenar" una IA.

### Inferencia vs Entrenamiento vs Fine-tuning

A menudo escucho: "Estoy entrenando a mi IA en Ollama porque le hago muchas preguntas". **Falso.**

* **Inferencia:** Es usar el modelo. El modelo lee tu entrada y predice la siguiente palabra. Sus "pesos" (su cerebro) no cambian. Es como leer un libro.
* **Entrenamiento (Pre-training):** Es crear el modelo desde cero. Requiere miles de GPUs y meses. Olvídalo.
* **Fine-tuning (Ajuste fino):** Aquí entramos nosotros. Es tomar el modelo base y darle un curso intensivo. Cambiamos ligeramente sus neuronas para que se especialice.

### ¿Por qué un modelo local no aprende solo con preguntas?

Los LLM son archivos estáticos de solo lectura. Cuando hablas con uno en local, lo guarda en su **contexto** (memoria a corto plazo). En cuanto cierras el programa, se borra. Para que "aprenda" de verdad, necesitamos realizar un proceso donde esos datos modifiquen el archivo del modelo (LoRA).

### RAG vs Fine-tuning vs Destilación

¿Cuándo usar cada uno?

| Característica | RAG (Generación Aumentada) | Fine-tuning | Destilación |
| :--- | :--- | :--- | :--- |
| **Uso principal** | Consultar datos externos frescos (PDFs, Wikis). | Cambiar el comportamiento, tono o formato. | Hacer que un modelo pequeño sea tan listo como uno grande. |
| **Dificultad** | Baja (Base de datos vectorial). | Media-Alta (Limpiar datos y GPU/Metal). | Alta (Scripts de generación de datos). |
| **Costo Computacional**| Muy bajo. | Medio (Tus 32GB son ideales). | Alto. |
| **¿Aprende hechos nuevos?**| Sí, los lee en tiempo real. | Sí, pero puede alucinar si los datos son pocos. | No, copia el razonamiento de otro. |
| **Privacidad** | Totalmente local. | Totalmente local. | Totalmente local. |

---

## Capítulo 2 — Configuración del entorno

Olvidaremos las herramientas exclusivas de Nvidia (como CUDA o Unsloth) y utilizaremos el ecosistema nativo de Apple: **Metal** y **MLX**.

### Modelos recomendados para tu M1 Pro (32GB)
Puedes dedicar unos 20-24GB a la IA sin congelar el Mac.
1.  **Llama 3.1/3.2 (8B):** Tu caballo de batalla. En formato cuantizado, usará 5-8GB.
2.  **Phi-4 (Mini):** Excelente para lógica y código. Ideal como "alumno".
3.  **Mixtral 8x7B (MoE):** Muy pesado (24GB en Q4), casi nivel GPT-3.5. Será nuestro "profesor".

### Instalación paso a paso en macOS

Abre tu **Terminal**.

**1. Instalar Homebrew y Ollama:**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install ollama
```

**2. Instalar Python y MLX (El framework de Apple):**
```bash
brew install python
python3 -m venv ~/ia-local
source ~/ia-local/bin/activate
pip install mlx mlx-lm
```

**3. Verificación:**
```bash
ollama run llama3.2
```
*Escribe "Hola". Para salir, `/bye`.*

❌ **Esto no funciona si:** Ollama te dice "connection refused". Asegúrate de abrir la aplicación Ollama desde tu carpeta de Aplicaciones primero.

---

## Capítulo 3 — RAG: Usa tus propios datos

### ¿Cómo funciona RAG?
Como ir a un examen a libro abierto. No memorizas el libro (eso es Fine-Tuning), pero sabes usar el índice para encontrar la respuesta y redactarla.

### Configurar AnythingLLM
Es una app gráfica que gestiona RAG sin tocar código.
1. Descarga AnythingLLM para Mac (Apple Silicon).
2. Ábrela. En **LLM Provider**, selecciona `Ollama`. URL: `http://127.0.0.1:11434`. Modelo: `llama3.2`.
3. Crea un Workspace, arrastra un PDF y haz clic en "Save and Embed".
4. Pregúntale a tu documento.

### La forma "Hardcore" (LangChain con Python)
Crea `mi_rag.py` e instala: `pip install langchain langchain-community chromadb bs4`

```python
from langchain_community.llms import Ollama
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

loader = WebBaseLoader("https://es.wikipedia.org/wiki/Inteligencia_artificial")
data = loader.load()
splits = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0).split_documents(data)

# vectorstore: ollama run mxbai-embed-large (ejecutar antes)
vectorstore = Chroma.from_documents(documents=splits, embedding=OllamaEmbeddings(model="mxbai-embed-large"))
qa_chain = RetrievalQA.from_chain_type(Ollama(model="llama3.2"), retriever=vectorstore.as_retriever())

print(qa_chain.run("¿Riesgos de la IA?"))
```

---

## Capítulo 4 — Fine-tuning con MLX en Mac

RAG no cambia la personalidad del modelo. El Fine-Tuning sí.
En tu Mac no usaremos QLoRA tradicional (que es para Nvidia), usaremos **MLX LoRA**, que está diseñado para exprimir tu chip M1 Pro.

### Preparar el Dataset (El secreto del éxito)
Necesitas un archivo `.jsonl`. Cada línea es un ejemplo de cómo quieres que hable tu IA.
Crea un archivo `train.jsonl`:

```json
{"text": "Usuario: ¿Qué es MLX? \nAsistente: MLX es el framework de Apple para IA, compadre. Va rapidísimo en los M1."}
{"text": "Usuario: Explica RAG. \nAsistente: RAG es como darle apuntes al modelo para el examen, compadre."}
```
*Nota: Necesitas al menos 100-500 líneas para que el modelo absorba el "tono" (en este caso, añadir "compadre").*

### Entrenar el LoRA con MLX
Abre tu terminal, activa tu entorno (`source ~/ia-local/bin/activate`) y ejecuta:

```bash
mlx_lm.lora   --model mlx-community/Meta-Llama-3-8B-Instruct-4bit   --train   --data ./   --iters 200   --batch-size 2   --lora-layers 16
```
*Qué hace esto:* Descarga un Llama 3 cuantizado a 4-bit (ocupa poca RAM) y lo entrena usando tu archivo `train.jsonl` (asegúrate de que esté en la carpeta actual). 

⚠️ **Cuidado con esto:** Tu Mac se pondrá caliente. Es normal. El chip M1 está haciendo matemáticas pesadas.

### Exportar y fusionar
Al terminar, MLX genera una carpeta `adapters`. Para fusionarlo con el modelo original:
```bash
mlx_lm.fuse --model mlx-community/Meta-Llama-3-8B-Instruct-4bit --adapter-path adapters
```
¡Felicidades! Tienes tu propio modelo ajustado en tu Mac.

---

## Capítulo 5 — Destilación de conocimiento

Aquí vamos a crear un modelo pequeño e inteligente robándole el "razonamiento" a un modelo gigante.

### ¿Cómo funciona la destilación?
Como no tienes 100 GPUs para entrenar desde cero, usas un modelo "Profesor" muy listo pero lento, para que genere miles de respuestas perfectas. Luego, usas ese texto para hacer Fine-Tuning a un modelo "Alumno" pequeño y rápido.

### El Script de Destilación (El Profesor crea los datos)
Usaremos Ollama con un modelo pesado (Profesor) para generar un dataset para nuestro alumno (Phi-4).

```python
import requests
import json

# Lista de preguntas difíciles
preguntas = ["Explica la recursividad", "Diferencia entre RAM y VRAM", "Qué es un puntero en C"]

with open("destilacion_train.jsonl", "w") as f:
    for preg in preguntas:
        # Usamos Mixtral (Profesor) vía Ollama
        res = requests.post('http://localhost:11434/api/generate', 
                            json={"model": "mixtral", "prompt": preg, "stream": False})
        respuesta_profesor = res.json()['response']
        
        # Guardamos en el formato MLX para entrenar luego al alumno
        fila = {"text": f"Usuario: {preg} \nAsistente: {respuesta_profesor}"}
        f.write(json.dumps(fila) + "\n")

print("Dataset de destilación creado.")
```
*Qué hace:* Le hace preguntas difíciles a Mixtral (que razonará bien) y lo guarda en un JSONL.
Luego, solo tienes que volver al Capítulo 4 y usar ese `destilacion_train.jsonl` para entrenar a un modelo pequeñito como `phi4`.

---

## Capítulo 6 — Sistemas Multi-Agente con CrewAI

Tener un modelo está bien. Tener 3 modelos hablando entre ellos y repartiéndose el trabajo, es el futuro.

### Implementación con CrewAI sobre Ollama
Instala: `pip install crewai langchain-community`

Crea `agentes.py`:
```python
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama

# Tu Llama 3.2 corriendo en el Mac
mi_llm = Ollama(model="llama3.2")

# Agente 1: Investigador
investigador = Agent(
    role='Investigador Senior',
    goal='Descubrir tendencias en IA',
    backstory='Eres un analista obsesionado con la tecnología.',
    verbose=True,
    allow_delegation=False,
    llm=mi_llm
)

# Agente 2: Redactor
redactor = Agent(
    role='Escritor Técnico',
    goal='Crear un artículo basado en la investigación',
    backstory='Escribes claro, directo y sin rodeos.',
    verbose=True,
    allow_delegation=False,
    llm=mi_llm
)

# Tareas
tarea1 = Task(description='Investiga sobre los modelos MLX de Apple.', agent=investigador, expected_output='Un resumen con 3 puntos clave sobre MLX de Apple.')
tarea2 = Task(description='Escribe un post de blog con el resumen.', agent=redactor, expected_output='Un post de blog corto y directo sobre MLX de Apple.')

# El Equipo
equipo = Crew(agents=[investigador, redactor], tasks=[tarea1, tarea2], process=Process.sequential)
resultado = equipo.kickoff()

print("######################")
print(resultado)
```
*Qué hace:* El Investigador genera un texto, y cuando termina, el Redactor lo toma y lo mejora. Todo 100% local en tus 32GB de RAM.

---

## Capítulo 7 — Fusión de modelos (Merge)

¿Qué pasa si tienes un modelo muy bueno en código (Coder) y otro muy bueno en español (Spanish)? Los fusionas.
En Mac, usaremos `mergekit`, que funciona perfecto en CPU/RAM.

```bash
pip install mergekit
```

Crea un archivo `merge.yml`:
```yaml
models:
  - model: mlx-community/Meta-Llama-3-8B-Instruct-4bit
    parameters:
      weight: 1.0
  - model: tu-modelo-fine-tuneado-del-cap-4
    parameters:
      weight: 0.5
merge_method: slerp
base_model: mlx-community/Meta-Llama-3-8B-Instruct-4bit
parameters:
  t:
    - value: [0.5, 0.5]
dtype: bfloat16
```
Ejecuta la fusión:
```bash
mergekit-yaml merge.yml modelo_fusionado/
```
❌ **Esto no funciona si:** Intentas fusionar arquitecturas diferentes (ej. Llama 3 con Phi-4). Solo puedes fusionar modelos de la misma "familia".

---

## Capítulo 8 — Ciclo de mejora continua

El secreto de la IA autónoma es cerrar el ciclo. Tu Mac debe hacer esto por la noche mientras duermes:

1. **Recolectar:** Guardar las preguntas que no supo responder bien durante el día.
2. **Profesor (Destilación):** Usar un script que despierte a Mixtral 8x7B para que responda correctamente a esas preguntas fallidas.
3. **Entrenar (Fine-Tuning):** Correr `mlx_lm.lora` usando las respuestas del Profesor.
4. **Fusión:** Aplicar los pesos nuevos al modelo base.
5. **Reinicio:** Levantar el nuevo modelo en Ollama para el día siguiente.

---

## Capítulo 9 — Proyecto Integrador Final

Aquí tienes el orquestador maestro en Bash para tu Mac. Guárdalo como `mejora_nocturna.sh`.

```bash
#!/bin/bash
# 1. Asumimos que tienes un archivo "errores_hoy.txt"
echo "Iniciando ciclo autónomo..."

# 2. Convertir errores en Dataset de Entrenamiento usando Python (Tu script del Cap 5)
python3 destilador_autonomo.py

# 3. Entrenar el LoRA con MLX
echo "Entrenando modelo (esto tardará)..."
mlx_lm.lora --model mlx-community/Meta-Llama-3-8B-Instruct-4bit --train --data ./ --iters 100

# 4. Fusionar el nuevo conocimiento
echo "Fusionando el modelo..."
mlx_lm.fuse --model mlx-community/Meta-Llama-3-8B-Instruct-4bit --adapter-path adapters --save-path modelo_actualizado

# 5. Mover a Ollama (Opcional, usando Modelfile)
echo "FROM ./modelo_actualizado" > Modelfile
ollama create Mi_IA_Mejorada -f Modelfile

echo "¡IA actualizada y lista para trabajar!"
```

---

## Apéndices

### A: Comandos esenciales de Ollama
* `ollama run <modelo>`: Descarga y ejecuta un modelo.
* `ollama list`: Muestra los modelos en tu Mac.
* `ollama rm <modelo>`: Borra un modelo para liberar SSD.

### B: Errores frecuentes en Mac M1
* **Out of Memory (OOM):** Has excedido tus 32GB. Solución: Cierra pestañas de Chrome o usa modelos en versión Q4 (Cuantizados a 4 bits).
* **MLX no detecta la GPU:** Ocurre si instalas el Python equivocado (ej. la versión Intel con Rosetta). Asegúrate de que tu Python es ARM64 nativo.

### C: Fuentes de modelos
* **Hugging Face (`mlx-community`):** Busca esta cuenta. Suben todos los modelos optimizados específicamente para los Mac.
* **Ollama Library:** La vía fácil. `ollama.com/library`.

### D: Glosario Rápido
* **VRAM:** Memoria de video. En tu Mac, es Memoria Unificada.
* **GGUF:** El formato de archivo optimizado para correr IA en local (CPU y Mac).
* **LoRA:** Un "parche" ligero de aprendizaje, en lugar de descargar un juego entero nuevo.

---
**Fin del Documento.** Ya estás listo para exprimir esos 32GB. ¡A programar!
