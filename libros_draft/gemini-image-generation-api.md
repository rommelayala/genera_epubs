# Gemini Image Generation API — Guía Completa de Generación de Imágenes con IA
### Un curso-tutorial exhaustivo · De cero a producción · Con ejemplos en Python, JavaScript, Go, Java y REST

---

> **Este curso cubre TODO lo que necesitas saber para generar, editar y manipular imágenes con la API de Gemini.** Desde tu primera imagen generada hasta flujos de producción con búsqueda en tiempo real, multi-turno, múltiples imágenes de referencia y configuración avanzada de resolución.

---

# PARTE I — FUNDAMENTOS

---

## Capítulo 1: ¿Qué es la Generación de Imágenes de Gemini?

Gemini no solo entiende texto — genera imágenes de forma nativa. A diferencia de sistemas como DALL-E o Midjourney que son modelos separados especializados en imágenes, Gemini integra la generación de imágenes directamente en su modelo de lenguaje multimodal. Esto significa que puedes mezclar texto e imágenes en una misma conversación de forma natural.

### ¿Qué puedes hacer exactamente?

```
CAPACIDADES DE GENERACIÓN DE IMÁGENES
│
├── Text-to-Image          ← Generar imágenes desde descripciones textuales
│   └── "Crea un paisaje futurista de Marte" → imagen generada
│
├── Image Editing           ← Editar imágenes existentes con instrucciones textuales
│   └── Imagen + "Añade un sombrero al gato" → imagen modificada
│
├── Multi-Turn Editing      ← Conversaciones iterativas de edición
│   └── Turno 1: "Crea infografía" → Turno 2: "Ponla en español"
│
├── Multiple References     ← Combinar hasta 14 imágenes de referencia
│   └── 5 fotos de personas → "Foto grupal de oficina"
│
├── Grounding con Search    ← Imágenes basadas en información en tiempo real
│   └── "Pronóstico del clima de hoy en Madrid" → gráfico con datos reales
│
└── Alta Resolución         ← Desde 512px hasta 4K
    └── Control granular de aspecto y tamaño
```

### Los modelos disponibles

Google ofrece tres modelos especializados en generación de imágenes, cada uno optimizado para un caso de uso diferente:

| Modelo | ID del Modelo | Fortaleza | Caso de Uso |
|--------|--------------|-----------|-------------|
| **Gemini 3.1 Flash Image** | `gemini-3.1-flash-image-preview` | Alta eficiencia, velocidad | Prototipado rápido, alto volumen |
| **Gemini 3 Pro Image** | `gemini-3-pro-image-preview` | Calidad profesional | Assets de producción, diseño |
| **Gemini 2.5 Flash Image** | `gemini-2.5-flash-image` | Propósito general | Tareas generales, balance costo/calidad |

**Cuándo usar cada uno:**
- **Flash Image (3.1)**: Cuando necesitas velocidad y volumen. Soporta resolución 512px (los otros no). Ideal para prototipos, iteraciones rápidas, pipelines automatizados.
- **Pro Image (3)**: Cuando la calidad visual es prioritaria. Assets finales, marketing, diseño gráfico profesional.
- **Flash Image (2.5)**: El caballo de batalla diario. Balance entre costo, velocidad y calidad.

### SynthID — La marca de agua invisible

Todas las imágenes generadas por Gemini incluyen una marca de agua digital llamada **SynthID**. Esta marca es imperceptible al ojo humano pero puede ser detectada algorítmicamente. Esto es una medida de seguridad de Google para identificar contenido generado por IA.

**Implicaciones prácticas:**
- No puedes desactivar SynthID
- No afecta la calidad visual de la imagen
- Permite verificar si una imagen fue generada por Gemini
- Es resistente a transformaciones básicas (recorte, compresión, redimensionado)

---

## Capítulo 2: Configuración Inicial

### Prerrequisitos

Antes de generar tu primera imagen, necesitas:

1. **Una cuenta de Google Cloud** o acceso a Google AI Studio
2. **Una API Key de Gemini** (variable de entorno `GEMINI_API_KEY`)
3. **El SDK de tu lenguaje** instalado

### Instalación por lenguaje

**Python:**
```bash
pip install google-genai Pillow
```

**JavaScript (Node.js):**
```bash
npm install @google/genai
```

**Go:**
```bash
go get google.golang.org/genai
```

**Java (Gradle):**
```gradle
implementation 'com.google.genai:google-genai:latest'
```

### Configuración de la API Key

La forma más segura es usar variables de entorno:

```bash
# En tu .bashrc, .zshrc, o .env
export GEMINI_API_KEY="tu-api-key-aquí"
```

**Nunca hardcodees tu API key en el código.** Los SDKs de Google la leen automáticamente de la variable de entorno `GEMINI_API_KEY` o `GOOGLE_API_KEY`.

### Endpoint REST

Para uso directo con curl o HTTP clients, el endpoint base es:

```
https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent
```

Headers requeridos:
```
x-goog-api-key: $GEMINI_API_KEY
Content-Type: application/json
```

---

# PARTE II — GENERACIÓN DE IMÁGENES PASO A PASO

---

## Capítulo 3: Text-to-Image — Tu Primera Imagen Generada

La forma más básica de generar una imagen: describes lo que quieres con texto y Gemini lo genera.

### Ejemplo completo en Python

```python
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()

prompt = ("Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme")
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[prompt],
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        image.save("generated_image.png")
```

**Desglose línea por línea:**
1. `genai.Client()` — crea el cliente. Lee automáticamente `GEMINI_API_KEY` del entorno.
2. `generate_content()` — el método principal. Acepta un modelo y contenido (texto, imágenes, o ambos).
3. `response.parts` — la respuesta puede contener múltiples partes: texto descriptivo Y la imagen generada.
4. `part.text` — texto que el modelo devuelve junto con la imagen (descripciones, comentarios).
5. `part.inline_data` — la imagen generada en formato binario.
6. `part.as_image()` — helper que convierte los bytes a un objeto PIL Image.

### Ejemplo completo en JavaScript

```javascript
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

async function main() {

  const ai = new GoogleGenAI({});

  const prompt =
    "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme";

  const response = await ai.models.generateContent({
    model: "gemini-3.1-flash-image-preview",
    contents: prompt,
  });
  for (const part of response.candidates[0].content.parts) {
    if (part.text) {
      console.log(part.text);
    } else if (part.inlineData) {
      const imageData = part.inlineData.data;
      const buffer = Buffer.from(imageData, "base64");
      fs.writeFileSync("gemini-native-image.png", buffer);
      console.log("Image saved as gemini-native-image.png");
    }
  }
}

main();
```

**Diferencias clave con Python:**
- En JS, la imagen viene como base64 en `part.inlineData.data` — hay que decodificarla a Buffer.
- La estructura de respuesta accede vía `response.candidates[0].content.parts`.
- El SDK usa camelCase (`inlineData`, `generateContent`) mientras Python usa snake_case.

### Ejemplo completo en Go

```go
package main

import (
  "context"
  "fmt"
  "log"
  "os"
  "google.golang.org/genai"
)

func main() {

  ctx := context.Background()
  client, err := genai.NewClient(ctx, nil)
  if err != nil {
      log.Fatal(err)
  }

  result, _ := client.Models.GenerateContent(
      ctx,
      "gemini-3.1-flash-image-preview",
      genai.Text("Create a picture of a nano banana dish in a " +
                 " fancy restaurant with a Gemini theme"),
  )

  for _, part := range result.Candidates[0].Content.Parts {
      if part.Text != "" {
          fmt.Println(part.Text)
      } else if part.InlineData != nil {
          imageBytes := part.InlineData.Data
          outputFilename := "gemini_generated_image.png"
          _ = os.WriteFile(outputFilename, imageBytes, 0644)
      }
  }
}
```

### Ejemplo completo en Java

```java
import com.google.genai.Client;
import com.google.genai.types.GenerateContentConfig;
import com.google.genai.types.GenerateContentResponse;
import com.google.genai.types.Part;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class TextToImage {
  public static void main(String[] args) throws IOException {

    try (Client client = new Client()) {
      GenerateContentConfig config = GenerateContentConfig.builder()
          .responseModalities("TEXT", "IMAGE")
          .build();

      GenerateContentResponse response = client.models.generateContent(
          "gemini-3.1-flash-image-preview",
          "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme",
          config);

      for (Part part : response.parts()) {
        if (part.text().isPresent()) {
          System.out.println(part.text().get());
        } else if (part.inlineData().isPresent()) {
          var blob = part.inlineData().get();
          if (blob.data().isPresent()) {
            Files.write(Paths.get("_01_generated_image.png"), blob.data().get());
          }
        }
      }
    }
  }
}
```

**Nota Java:** Requiere especificar explícitamente `responseModalities("TEXT", "IMAGE")` en la configuración. Sin esto, el modelo solo devolvería texto.

### Ejemplo con REST / curl

```bash
curl -s -X POST \
      "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "contents": [{
          "parts": [
            {"text": "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"}
          ]
        }]
      }'
```

**La respuesta REST** viene en JSON con la imagen en base64:
```json
{
  "candidates": [{
    "content": {
      "parts": [
        {"text": "Descripción opcional del modelo"},
        {
          "inlineData": {
            "mimeType": "image/png",
            "data": "iVBORw0KGgoAAAANSUh..."
          }
        }
      ]
    }
  }]
}
```

Para decodificar la imagen desde la respuesta REST:
```bash
# Extraer y decodificar la imagen del JSON
curl -s -X POST ... | jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' | base64 -d > output.png
```

---

## Capítulo 4: Image Editing — Editar Imágenes Existentes

Uno de los superpoderes de Gemini: no solo genera imágenes desde cero, también puede editar imágenes existentes usando instrucciones en lenguaje natural. Puedes añadir, eliminar o modificar elementos, cambiar estilos, ajustar colores — todo con texto.

### Cómo funciona

El flujo es simple:
1. Envías una imagen existente + un prompt descriptivo
2. Gemini analiza la imagen y aplica los cambios descritos
3. Devuelve una nueva imagen con las modificaciones

```
FLUJO DE EDICIÓN
│
│  Input: imagen.jpg + "Añade un sombrero rojo al gato"
│         ↓
│  [Gemini analiza la imagen original]
│         ↓
│  [Identifica el gato en la imagen]
│         ↓
│  [Genera una versión modificada con el sombrero]
│         ↓
│  Output: imagen_editada.png
```

### Ejemplo completo en Python

```python
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()

prompt = (
    "Create a picture of my cat eating a nano-banana in a "
    "fancy restaurant under the Gemini constellation",
)

image = Image.open("/path/to/cat_image.png")

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[prompt, image],
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        image.save("generated_image.png")
```

**Lo que cambió respecto a text-to-image:**
- `contents` ahora es una lista con DOS elementos: el prompt y la imagen
- La imagen se carga con PIL (`Image.open()`)
- Gemini usa la imagen como referencia visual y aplica las transformaciones descritas en el prompt

### Ejemplo completo en JavaScript

```javascript
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

async function main() {

  const ai = new GoogleGenAI({});

  const imagePath = "path/to/cat_image.png";
  const imageData = fs.readFileSync(imagePath);
  const base64Image = imageData.toString("base64");

  const prompt = [
    { text: "Create a picture of my cat eating a nano-banana in a" +
            "fancy restaurant under the Gemini constellation" },
    {
      inlineData: {
        mimeType: "image/png",
        data: base64Image,
      },
    },
  ];

  const response = await ai.models.generateContent({
    model: "gemini-3.1-flash-image-preview",
    contents: prompt,
  });
  for (const part of response.candidates[0].content.parts) {
    if (part.text) {
      console.log(part.text);
    } else if (part.inlineData) {
      const imageData = part.inlineData.data;
      const buffer = Buffer.from(imageData, "base64");
      fs.writeFileSync("gemini-native-image.png", buffer);
      console.log("Image saved as gemini-native-image.png");
    }
  }
}

main();
```

**En JavaScript, la imagen se envía como base64** dentro de `inlineData`, especificando el `mimeType`. Esto es diferente a Python donde pasas directamente el objeto PIL Image.

### Ejemplo completo en Go

```go
package main

import (
 "context"
 "fmt"
 "log"
 "os"
 "google.golang.org/genai"
)

func main() {

 ctx := context.Background()
 client, err := genai.NewClient(ctx, nil)
 if err != nil {
     log.Fatal(err)
 }

 imagePath := "/path/to/cat_image.png"
 imgData, _ := os.ReadFile(imagePath)

 parts := []*genai.Part{
   genai.NewPartFromText("Create a picture of my cat eating a nano-banana in a fancy restaurant under the Gemini constellation"),
   &genai.Part{
     InlineData: &genai.Blob{
       MIMEType: "image/png",
       Data:     imgData,
     },
   },
 }

 contents := []*genai.Content{
   genai.NewContentFromParts(parts, genai.RoleUser),
 }

 result, _ := client.Models.GenerateContent(
     ctx,
     "gemini-3.1-flash-image-preview",
     contents,
 )

 for _, part := range result.Candidates[0].Content.Parts {
     if part.Text != "" {
         fmt.Println(part.Text)
     } else if part.InlineData != nil {
         imageBytes := part.InlineData.Data
         outputFilename := "gemini_generated_image.png"
         _ = os.WriteFile(outputFilename, imageBytes, 0644)
     }
 }
}
```

### Ejemplo completo en Java

```java
import com.google.genai.Client;
import com.google.genai.types.Content;
import com.google.genai.types.GenerateContentConfig;
import com.google.genai.types.GenerateContentResponse;
import com.google.genai.types.Part;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class TextAndImageToImage {
  public static void main(String[] args) throws IOException {

    try (Client client = new Client()) {
      GenerateContentConfig config = GenerateContentConfig.builder()
          .responseModalities("TEXT", "IMAGE")
          .build();

      GenerateContentResponse response = client.models.generateContent(
          "gemini-3.1-flash-image-preview",
          Content.fromParts(
              Part.fromText("""
                  Create a picture of my cat eating a nano-banana in
                  a fancy restaurant under the Gemini constellation
                  """),
              Part.fromBytes(
                  Files.readAllBytes(
                      Path.of("src/main/resources/cat.jpg")),
                  "image/jpeg")),
          config);

      for (Part part : response.parts()) {
        if (part.text().isPresent()) {
          System.out.println(part.text().get());
        } else if (part.inlineData().isPresent()) {
          var blob = part.inlineData().get();
          if (blob.data().isPresent()) {
            Files.write(Paths.get("gemini_generated_image.png"), blob.data().get());
          }
        }
      }
    }
  }
}
```

### Ejemplo con REST / curl

```bash
curl -s -X POST \
      "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
        -H "x-goog-api-key: $GEMINI_API_KEY" \
        -H 'Content-Type: application/json' \
        -d "{
          \"contents\": [{
            \"parts\":[
                {\"text\": \"Create a picture of my cat eating a nano-banana in a fancy restaurant under the Gemini constellation\"},
                {
                  \"inline_data\": {
                    \"mime_type\":\"image/jpeg\",
                    \"data\": \"<BASE64_IMAGE_DATA>\"
                  }
                }
            ]
          }]
        }"
```

**Para codificar tu imagen en base64 desde bash:**
```bash
BASE64_IMAGE=$(base64 -i tu_imagen.jpg)
```

### Tipos de edición que puedes hacer

| Operación | Ejemplo de prompt |
|-----------|-------------------|
| **Añadir elementos** | "Add a red hat to the person" |
| **Eliminar elementos** | "Remove the background and replace with a beach" |
| **Cambiar estilo** | "Make this look like a watercolor painting" |
| **Ajustar colores** | "Change the color grading to warm sunset tones" |
| **Modificar composición** | "Zoom out to show the full room" |
| **Cambiar texto en imagen** | "Replace the English text with Spanish" |

---

## Capítulo 5: Edición Multi-Turno — Conversaciones Iterativas

La edición multi-turno es donde Gemini realmente brilla. Puedes tener una conversación donde cada mensaje refina la imagen del turno anterior. Esto simula el flujo de trabajo de un diseñador: crear → revisar → ajustar → refinar.

### El concepto

```
FLUJO MULTI-TURNO
│
│  Turno 1 (usuario): "Crea una infografía sobre fotosíntesis"
│  Turno 1 (modelo):  → genera infografía v1
│         ↓
│  Turno 2 (usuario): "Ponla en español"
│  Turno 2 (modelo):  → genera infografía v2 (en español)
│         ↓
│  Turno 3 (usuario): "Cambia el formato a 16:9"
│  Turno 3 (modelo):  → genera infografía v3 (español, 16:9)
│         ↓
│  ... (puedes seguir refinando)
```

### Ejemplo completo en Python — Turno 1: Crear la infografía

```python
from google import genai
from google.genai import types

client = genai.Client()

chat = client.chats.create(
    model="gemini-3.1-flash-image-preview",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        tools=[{"google_search": {}}]
    )
)

message = "Create a vibrant infographic that explains photosynthesis as if it were a recipe for a plant's favorite food. Show the \"ingredients\" (sunlight, water, CO2) and the \"finished dish\" (sugar/energy). The style should be like a page from a colorful kids' cookbook, suitable for a 4th grader."

response = chat.send_message(message)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif image:= part.as_image():
        image.save("photosynthesis.png")
```

**Lo nuevo aquí:**
- `client.chats.create()` — crea una sesión de chat que mantiene el contexto entre turnos
- `response_modalities=['TEXT', 'IMAGE']` — le dice al modelo que puede responder con texto e imágenes
- `tools=[{"google_search": {}}]` — habilita Google Search para que el modelo pueda buscar información real
- `chat.send_message()` — envía un mensaje dentro de la sesión (mantiene historial)

### Ejemplo completo en JavaScript — Turno 1

```javascript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

async function main() {
  const chat = ai.chats.create({
    model: "gemini-3.1-flash-image-preview",
    config: {
      responseModalities: ['TEXT', 'IMAGE'],
      tools: [{googleSearch: {}}],
    },
  });
}

await main();

const message = "Create a vibrant infographic that explains photosynthesis as if it were a recipe for a plant's favorite food. Show the \"ingredients\" (sunlight, water, CO2) and the \"finished dish\" (sugar/energy). The style should be like a page from a colorful kids' cookbook, suitable for a 4th grader."

let response = await chat.sendMessage({message});

for (const part of response.candidates[0].content.parts) {
    if (part.text) {
      console.log(part.text);
    } else if (part.inlineData) {
      const imageData = part.inlineData.data;
      const buffer = Buffer.from(imageData, "base64");
      fs.writeFileSync("photosynthesis.png", buffer);
      console.log("Image saved as photosynthesis.png");
    }
}
```

### Ejemplo completo en Go — Turno 1

```go
package main

import (
    "context"
    "fmt"
    "log"
    "os"

    "google.golang.org/genai"
)

func main() {
    ctx := context.Background()
    client, err := genai.NewClient(ctx, nil)
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()

    model := client.GenerativeModel("gemini-3.1-flash-image-preview")
    model.GenerationConfig = &pb.GenerationConfig{
        ResponseModalities: []pb.ResponseModality{genai.Text, genai.Image},
    }
    chat := model.StartChat()

    message := "Create a vibrant infographic that explains photosynthesis as if it were a recipe for a plant's favorite food. Show the \"ingredients\" (sunlight, water, CO2) and the \"finished dish\" (sugar/energy). The style should be like a page from a colorful kids' cookbook, suitable for a 4th grader."

    resp, err := chat.SendMessage(ctx, genai.Text(message))
    if err != nil {
        log.Fatal(err)
    }

    for _, part := range resp.Candidates[0].Content.Parts {
        if txt, ok := part.(genai.Text); ok {
            fmt.Printf("%s", string(txt))
        } else if img, ok := part.(genai.ImageData); ok {
            err := os.WriteFile("photosynthesis.png", img.Data, 0644)
            if err != nil {
                log.Fatal(err)
            }
        }
    }
}
```

### Ejemplo completo en Java — Turno 1

```java
import com.google.genai.Chat;
import com.google.genai.Client;
import com.google.genai.types.Content;
import com.google.genai.types.GenerateContentConfig;
import com.google.genai.types.GenerateContentResponse;
import com.google.genai.types.GoogleSearch;
import com.google.genai.types.ImageConfig;
import com.google.genai.types.Part;
import com.google.genai.types.RetrievalConfig;
import com.google.genai.types.Tool;
import com.google.genai.types.ToolConfig;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class MultiturnImageEditing {
  public static void main(String[] args) throws IOException {

    try (Client client = new Client()) {

      GenerateContentConfig config = GenerateContentConfig.builder()
          .responseModalities("TEXT", "IMAGE")
          .tools(Tool.builder()
              .googleSearch(GoogleSearch.builder().build())
              .build())
          .build();

      Chat chat = client.chats.create("gemini-3.1-flash-image-preview", config);

      GenerateContentResponse response = chat.sendMessage("""
          Create a vibrant infographic that explains photosynthesis
          as if it were a recipe for a plant's favorite food.
          Show the "ingredients" (sunlight, water, CO2)
          and the "finished dish" (sugar/energy).
          The style should be like a page from a colorful
          kids' cookbook, suitable for a 4th grader.
          """);

      for (Part part : response.parts()) {
        if (part.text().isPresent()) {
          System.out.println(part.text().get());
        } else if (part.inlineData().isPresent()) {
          var blob = part.inlineData().get();
          if (blob.data().isPresent()) {
            Files.write(Paths.get("photosynthesis.png"), blob.data().get());
          }
        }
      }
      // Turno 2 viene a continuación...
    }
  }
}
```

### Ejemplo con REST / curl — Turno 1

```bash
curl -s -X POST \
      "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "contents": [{
          "role": "user",
          "parts": [
            {"text": "Create a vibrant infographic that explains photosynthesis as if it were a recipe for a plants favorite food. Show the \"ingredients\" (sunlight, water, CO2) and the \"finished dish\" (sugar/energy). The style should be like a page from a colorful kids cookbook, suitable for a 4th grader."}
          ]
        }],
        "generationConfig": {
          "responseModalities": ["TEXT", "IMAGE"]
        }
      }'
```

### Turno 2: Actualizar a español con configuración de resolución

Ahora viene lo poderoso — en el segundo turno, modificamos la imagen generada sin tener que reenviarla. El chat mantiene el contexto.

#### Python — Turno 2

```python
message = "Update this infographic to be in Spanish. Do not change any other elements of the image."
aspect_ratio = "16:9" # "1:1","1:4","1:8","2:3","3:2","3:4","4:1","4:3","4:5","5:4","8:1","9:16","16:9","21:9"
resolution = "2K" # "512", "1K", "2K", "4K"

response = chat.send_message(message,
    config=types.GenerateContentConfig(
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=resolution
        ),
    ))

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif image:= part.as_image():
        image.save("photosynthesis_spanish.png")
```

#### JavaScript — Turno 2

```javascript
const message = 'Update this infographic to be in Spanish. Do not change any other elements of the image.';
const aspectRatio = '16:9';
const resolution = '2K';

let response = await chat.sendMessage({
  message,
  config: {
    responseModalities: ['TEXT', 'IMAGE'],
    imageConfig: {
      aspectRatio: aspectRatio,
      imageSize: resolution,
    },
    tools: [{googleSearch: {}}],
  },
});

for (const part of response.candidates[0].content.parts) {
    if (part.text) {
      console.log(part.text);
    } else if (part.inlineData) {
      const imageData = part.inlineData.data;
      const buffer = Buffer.from(imageData, "base64");
      fs.writeFileSync("photosynthesis2.png", buffer);
      console.log("Image saved as photosynthesis2.png");
    }
}
```

#### Go — Turno 2

```go
message = "Update this infographic to be in Spanish. Do not change any other elements of the image."
aspect_ratio = "16:9"
resolution = "2K"

model.GenerationConfig.ImageConfig = &pb.ImageConfig{
    AspectRatio: aspect_ratio,
    ImageSize:   resolution,
}

resp, err = chat.SendMessage(ctx, genai.Text(message))
if err != nil {
    log.Fatal(err)
}

for _, part := range resp.Candidates[0].Content.Parts {
    if txt, ok := part.(genai.Text); ok {
        fmt.Printf("%s", string(txt))
    } else if img, ok := part.(genai.ImageData); ok {
        err := os.WriteFile("photosynthesis_spanish.png", img.Data, 0644)
        if err != nil {
            log.Fatal(err)
        }
    }
}
```

#### Java — Turno 2

```java
String aspectRatio = "16:9";
String resolution = "2K";

config = GenerateContentConfig.builder()
    .responseModalities("TEXT", "IMAGE")
    .imageConfig(ImageConfig.builder()
        .aspectRatio(aspectRatio)
        .imageSize(resolution)
        .build())
    .build();

response = chat.sendMessage(
    "Update this infographic to be in Spanish. " +
    "Do not change any other elements of the image.",
    config);

for (Part part : response.parts()) {
  if (part.text().isPresent()) {
    System.out.println(part.text().get());
  } else if (part.inlineData().isPresent()) {
    var blob = part.inlineData().get();
    if (blob.data().isPresent()) {
      Files.write(Paths.get("photosynthesis_spanish.png"), blob.data().get());
    }
  }
}
```

#### REST — Turno 2 (incluye historial)

```bash
curl -s -X POST \
      "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
        "contents": [
          {
            "role": "user",
            "parts": [{"text": "Create a vibrant infographic that explains photosynthesis..."}]
          },
          {
            "role": "model",
            "parts": [{"inline_data": {"mime_type": "image/png", "data": "<PREVIOUS_IMAGE_DATA>"}}]
          },
          {
            "role": "user",
            "parts": [{"text": "Update this infographic to be in Spanish. Do not change any other elements of the image."}]
          }
        ],
        "tools": [{"google_search": {}}],
        "generationConfig": {
          "responseModalities": ["TEXT", "IMAGE"],
          "imageConfig": {
            "aspectRatio": "16:9",
            "imageSize": "2K"
          }
        }
      }'
```

**Observa en REST:** Debes enviar el historial completo manualmente. Los SDKs manejan esto automáticamente con el objeto `chat`, pero vía REST eres responsable de enviar todos los turnos previos (user → model → user → model → ...).

---

## Capítulo 6: Múltiples Imágenes de Referencia

Gemini puede recibir hasta **14 imágenes de referencia** en una sola solicitud. Esto es enormemente útil para:

- **Fotos grupales**: "Haz una foto grupal de estas personas"
- **Consistencia de personajes**: Mantener la misma apariencia a través de múltiples generaciones
- **Transferencia de estilo**: "Aplica el estilo de esta imagen a esta otra"
- **Composición**: Combinar elementos de varias fuentes

### Ejemplo completo en Python — Foto grupal

```python
from google import genai
from google.genai import types
from PIL import Image

prompt = "An office group photo of these people, they are making funny faces."
aspect_ratio = "5:4"
resolution = "2K"

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[
        prompt,
        Image.open('person1.png'),
        Image.open('person2.png'),
        Image.open('person3.png'),
        Image.open('person4.png'),
        Image.open('person5.png'),
    ],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=resolution
        ),
    )
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif image:= part.as_image():
        image.save("office.png")
```

**Puntos clave:**
- `contents` es una lista que mezcla texto (el prompt) con objetos Image (las referencias)
- El orden importa: el prompt primero, luego las imágenes
- Gemini intenta mantener la fidelidad visual de cada persona referenciada

### Ejemplo completo en JavaScript — Foto grupal

```javascript
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

async function main() {

  const ai = new GoogleGenAI({});

  const prompt =
      'An office group photo of these people, they are making funny faces.';
  const aspectRatio = '5:4';
  const resolution = '2K';

const contents = [
  { text: prompt },
  {
    inlineData: {
      mimeType: "image/jpeg",
      data: base64ImageFile1,
    },
  },
  {
    inlineData: {
      mimeType: "image/jpeg",
      data: base64ImageFile2,
    },
  },
  {
    inlineData: {
      mimeType: "image/jpeg",
      data: base64ImageFile3,
    },
  },
  {
    inlineData: {
      mimeType: "image/jpeg",
      data: base64ImageFile4,
    },
  },
  {
    inlineData: {
      mimeType: "image/jpeg",
      data: base64ImageFile5,
    },
  }
];

const response = await ai.models.generateContent({
    model: 'gemini-3.1-flash-image-preview',
    contents: contents,
    config: {
      responseModalities: ['TEXT', 'IMAGE'],
      imageConfig: {
        aspectRatio: aspectRatio,
        imageSize: resolution,
      },
    },
  });

  for (const part of response.candidates[0].content.parts) {
    if (part.text) {
      console.log(part.text);
    } else if (part.inlineData) {
      const imageData = part.inlineData.data;
      const buffer = Buffer.from(imageData, "base64");
      fs.writeFileSync("image.png", buffer);
      console.log("Image saved as image.png");
    }
  }

}

main();
```

### Ejemplo completo en Go — Foto grupal

```go
package main

import (
    "context"
    "fmt"
    "log"
    "os"

    "google.golang.org/genai"
)

func main() {
    ctx := context.Background()
    client, err := genai.NewClient(ctx, nil)
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()

    model := client.GenerativeModel("gemini-3.1-flash-image-preview")
    model.GenerationConfig = &pb.GenerationConfig{
        ResponseModalities: []pb.ResponseModality{genai.Text, genai.Image},
        ImageConfig: &pb.ImageConfig{
            AspectRatio: "5:4",
            ImageSize:   "2K",
        },
    }

    img1, err := os.ReadFile("person1.png")
    if err != nil { log.Fatal(err) }
    img2, err := os.ReadFile("person2.png")
    if err != nil { log.Fatal(err) }
    img3, err := os.ReadFile("person3.png")
    if err != nil { log.Fatal(err) }
    img4, err := os.ReadFile("person4.png")
    if err != nil { log.Fatal(err) }
    img5, err := os.ReadFile("person5.png")
    if err != nil { log.Fatal(err) }

    parts := []genai.Part{
        genai.Text("An office group photo of these people, they are making funny faces."),
        genai.ImageData{MIMEType: "image/png", Data: img1},
        genai.ImageData{MIMEType: "image/png", Data: img2},
        genai.ImageData{MIMEType: "image/png", Data: img3},
        genai.ImageData{MIMEType: "image/png", Data: img4},
        genai.ImageData{MIMEType: "image/png", Data: img5},
    }

    resp, err := model.GenerateContent(ctx, parts...)
    if err != nil {
        log.Fatal(err)
    }

    for _, part := range resp.Candidates[0].Content.Parts {
        if txt, ok := part.(genai.Text); ok {
            fmt.Printf("%s", string(txt))
        } else if img, ok := part.(genai.ImageData); ok {
            err := os.WriteFile("office.png", img.Data, 0644)
            if err != nil {
                log.Fatal(err)
            }
        }
    }
}
```

### Ejemplo completo en Java — Foto grupal

```java
import com.google.genai.Client;
import com.google.genai.types.Content;
import com.google.genai.types.GenerateContentConfig;
import com.google.genai.types.GenerateContentResponse;
import com.google.genai.types.ImageConfig;
import com.google.genai.types.Part;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class GroupPhoto {
  public static void main(String[] args) throws IOException {

    try (Client client = new Client()) {
      GenerateContentConfig config = GenerateContentConfig.builder()
          .responseModalities("TEXT", "IMAGE")
          .imageConfig(ImageConfig.builder()
              .aspectRatio("5:4")
              .imageSize("2K")
              .build())
          .build();

      GenerateContentResponse response = client.models.generateContent(
          "gemini-3.1-flash-image-preview",
          Content.fromParts(
              Part.fromText("An office group photo of these people, they are making funny faces."),
              Part.fromBytes(Files.readAllBytes(Path.of("person1.png")), "image/png"),
              Part.fromBytes(Files.readAllBytes(Path.of("person2.png")), "image/png"),
              Part.fromBytes(Files.readAllBytes(Path.of("person3.png")), "image/png"),
              Part.fromBytes(Files.readAllBytes(Path.of("person4.png")), "image/png"),
              Part.fromBytes(Files.readAllBytes(Path.of("person5.png")), "image/png")
          ), config);

      for (Part part : response.parts()) {
        if (part.text().isPresent()) {
          System.out.println(part.text().get());
        } else if (part.inlineData().isPresent()) {
          var blob = part.inlineData().get();
          if (blob.data().isPresent()) {
            Files.write(Paths.get("office.png"), blob.data().get());
          }
        }
      }
    }
  }
}
```

### Ejemplo con REST / curl — Foto grupal

```bash
curl -s -X POST \
      "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
        -H "x-goog-api-key: $GEMINI_API_KEY" \
        -H 'Content-Type: application/json' \
        -d "{
          \"contents\": [{
            \"parts\":[
                {\"text\": \"An office group photo of these people, they are making funny faces.\"},
                {\"inline_data\": {\"mime_type\":\"image/png\", \"data\": \"<BASE64_DATA_IMG_1>\"}},
                {\"inline_data\": {\"mime_type\":\"image/png\", \"data\": \"<BASE64_DATA_IMG_2>\"}},
                {\"inline_data\": {\"mime_type\":\"image/png\", \"data\": \"<BASE64_DATA_IMG_3>\"}},
                {\"inline_data\": {\"mime_type\":\"image/png\", \"data\": \"<BASE64_DATA_IMG_4>\"}},
                {\"inline_data\": {\"mime_type\":\"image/png\", \"data\": \"<BASE64_DATA_IMG_5>\"}}
            ]
          }],
          \"generationConfig\": {
            \"responseModalities\": [\"TEXT\", \"IMAGE\"],
            \"imageConfig\": {
              \"aspectRatio\": \"5:4\",
              \"imageSize\": \"2K\"
            }
          }
        }"
```

---

# PARTE III — FUNCIONES AVANZADAS

---

## Capítulo 7: Grounding con Google Search — Imágenes con Datos Reales

Esta es una de las funciones más diferenciadores de Gemini frente a otros generadores de imágenes. Al activar Google Search como herramienta, Gemini puede:

1. **Buscar información actual** en la web antes de generar la imagen
2. **Usar datos en tiempo real** (clima, noticias, estadísticas)
3. **Buscar imágenes de referencia** para especies, objetos o conceptos específicos

```
FLUJO CON GOOGLE SEARCH GROUNDING
│
│  Tu prompt: "Pronóstico del clima de esta semana en Madrid"
│         ↓
│  [Gemini activa Google Search]
│         ↓
│  [Busca datos meteorológicos reales de Madrid]
│         ↓
│  [Genera una visualización con los datos encontrados]
│         ↓
│  Output: imagen con datos reales + metadata de fuentes
```

### Ejemplo: Gráfico del clima con datos reales

#### Python

```python
from google import genai
prompt = "Visualize the current weather forecast for the next 5 days in San Francisco as a clean, modern weather chart. Add a visual on what I should wear each day"
aspect_ratio = "16:9"

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=['Text', 'Image'],
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
        ),
        tools=[{"google_search": {}}]
    )
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif image:= part.as_image():
        image.save("weather.png")
```

#### JavaScript

```javascript
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

async function main() {

  const ai = new GoogleGenAI({});

  const prompt = 'Visualize the current weather forecast for the next 5 days in San Francisco as a clean, modern weather chart. Add a visual on what I should wear each day';
  const aspectRatio = '16:9';
  const resolution = '2K';

const response = await ai.models.generateContent({
    model: 'gemini-3.1-flash-image-preview',
    contents: prompt,
    config: {
      responseModalities: ['TEXT', 'IMAGE'],
      imageConfig: {
        aspectRatio: aspectRatio,
        imageSize: resolution,
      },
    tools: [{ googleSearch: {} }]
    },
  });

  for (const part of response.candidates[0].content.parts) {
    if (part.text) {
      console.log(part.text);
    } else if (part.inlineData) {
      const imageData = part.inlineData.data;
      const buffer = Buffer.from(imageData, "base64");
      fs.writeFileSync("image.png", buffer);
      console.log("Image saved as image.png");
    }
  }

}

main();
```

#### Java

```java
import com.google.genai.Client;
import com.google.genai.types.GenerateContentConfig;
import com.google.genai.types.GenerateContentResponse;
import com.google.genai.types.GoogleSearch;
import com.google.genai.types.ImageConfig;
import com.google.genai.types.Part;
import com.google.genai.types.Tool;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class SearchGrounding {
  public static void main(String[] args) throws IOException {

    try (Client client = new Client()) {
      GenerateContentConfig config = GenerateContentConfig.builder()
          .responseModalities("TEXT", "IMAGE")
          .imageConfig(ImageConfig.builder()
              .aspectRatio("16:9")
              .build())
          .tools(Tool.builder()
              .googleSearch(GoogleSearch.builder().build())
              .build())
          .build();

      GenerateContentResponse response = client.models.generateContent(
          "gemini-3.1-flash-image-preview", """
              Visualize the current weather forecast for the next 5 days
              in San Francisco as a clean, modern weather chart.
              Add a visual on what I should wear each day
              """,
          config);

      for (Part part : response.parts()) {
        if (part.text().isPresent()) {
          System.out.println(part.text().get());
        } else if (part.inlineData().isPresent()) {
          var blob = part.inlineData().get();
          if (blob.data().isPresent()) {
            Files.write(Paths.get("weather.png"), blob.data().get());
          }
        }
      }
    }
  }
}
```

#### REST / curl

```bash
curl -s -X POST \
      "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "contents": [{"parts": [{"text": "Visualize the current weather forecast for the next 5 days in San Francisco as a clean, modern weather chart. Add a visual on what I should wear each day"}]}],
        "tools": [{"google_search": {}}],
        "generationConfig": {
          "responseModalities": ["TEXT", "IMAGE"],
          "imageConfig": {"aspectRatio": "16:9"}
        }
      }'
```

### Grounding con Image Search — Búsqueda de Imágenes de Referencia

Además de buscar texto en la web, Gemini puede buscar imágenes de referencia. Esto es especialmente útil cuando quieres que el modelo genere algo visualmente preciso — por ejemplo, una especie de animal específica.

**Importante:** Image Search solo está disponible en `gemini-3.1-flash-image-preview`.

#### Python — Búsqueda de imagen + generación

```python
from google import genai
prompt = "A detailed painting of a Timareta butterfly resting on a flower"

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        tools=[
            types.Tool(google_search=types.GoogleSearch(
                search_types=types.SearchTypes(
                    web_search=types.WebSearch(),
                    image_search=types.ImageSearch()
                )
            ))
        ]
    )
)

# Mostrar fuentes de grounding si están disponibles
if response.candidates and response.candidates[0].grounding_metadata and response.candidates[0].grounding_metadata.search_entry_point:
    display(HTML(response.candidates[0].grounding_metadata.search_entry_point.rendered_content))
```

#### JavaScript — Búsqueda de imagen + generación

```javascript
import { GoogleGenAI } from "@google/genai";

async function main() {

  const ai = new GoogleGenAI({});

  const prompt = "A detailed painting of a Timareta butterfly resting on a flower";

  const response = await ai.models.generateContent({
    model: "gemini-3.1-flash-image-preview",
    contents: prompt,
    config: {
      responseModalities: ["IMAGE"],
      tools: [
        {
          googleSearch: {
            searchTypes: {
              webSearch: {},
              imageSearch: {}
            }
          }
        }
      ]
    }
  });

  // Mostrar fuentes de grounding si están disponibles
  if (response.candidates && response.candidates[0].groundingMetadata && response.candidates[0].groundingMetadata.searchEntryPoint) {
      console.log(response.candidates[0].groundingMetadata.searchEntryPoint.renderedContent);
  }
}

main();
```

#### Go — Búsqueda de imagen + generación

```go
package main

import (
  "context"
  "fmt"
  "log"

  "google.golang.org/genai"
  pb "google.golang.org/genai/schema"
)

func main() {
  ctx := context.Background()
  client, err := genai.NewClient(ctx, nil)
  if err != nil {
    log.Fatal(err)
  }
  defer client.Close()

  model := client.GenerativeModel("gemini-3.1-flash-image-preview")
  model.Tools = []*pb.Tool{
    {
      GoogleSearch: &pb.GoogleSearch{
        SearchTypes: &pb.SearchTypes{
          WebSearch:   &pb.WebSearch{},
          ImageSearch: &pb.ImageSearch{},
        },
      },
    },
  }
  model.GenerationConfig = &pb.GenerationConfig{
    ResponseModalities: []pb.ResponseModality{genai.Image},
  }

  prompt := "A detailed painting of a Timareta butterfly resting on a flower"
  resp, err := model.GenerateContent(ctx, genai.Text(prompt))
  if err != nil {
    log.Fatal(err)
  }

  if resp.Candidates[0].GroundingMetadata != nil && resp.Candidates[0].GroundingMetadata.SearchEntryPoint != nil {
    fmt.Println(resp.Candidates[0].GroundingMetadata.SearchEntryPoint.RenderedContent)
  }
}
```

#### REST / curl

```bash
curl -s -X POST \
      "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "contents": [{"parts": [{"text": "A detailed painting of a Timareta butterfly resting on a flower"}]}],
        "tools": [{"google_search": {"searchTypes": {"webSearch": {}, "imageSearch": {}}}}],
        "generationConfig": {
          "responseModalities": ["IMAGE"]
        }
      }'
```

### Tipos de búsqueda disponibles

| Tipo | Configuración | Disponibilidad | Uso |
|------|--------------|----------------|-----|
| **Web Search** | `web_search: {}` | Todos los modelos | Buscar datos textuales actuales |
| **Image Search** | `image_search: {}` | Solo `gemini-3.1-flash-image-preview` | Buscar imágenes de referencia visual |
| **Ambos** | `web_search: {} + image_search: {}` | Solo `gemini-3.1-flash-image-preview` | Combinar datos + referencias visuales |

### Grounding Metadata — Las fuentes

Cuando usas Google Search, la respuesta incluye `grounding_metadata` con:
- `search_entry_point` — HTML renderizable con las fuentes citadas
- `grounding_chunks` — las fuentes individuales usadas

**Requisito legal:** Cuando usas Image Search grounding, debes cumplir con los requisitos de atribución y navegación directa de Google.

**Restricción:** Image Search **no puede buscar personas**. Está diseñado para objetos, animales, paisajes, productos, etc.

---

## Capítulo 8: Resolución y Aspect Ratio — Control de Salida

### Opciones de resolución

| Resolución | Tamaño aproximado | Disponibilidad |
|-----------|-------------------|----------------|
| `512` | 512px | Solo `gemini-3.1-flash-image-preview` |
| `1K` | ~1024px | Todos los modelos |
| `2K` | ~2048px | Todos los modelos |
| `4K` | ~4096px | Todos los modelos |

**Nota:** Usa la letra `K` en mayúscula (no `1k`). El valor `512` no lleva sufijo.

### Aspect Ratios disponibles

Gemini soporta una amplia gama de relaciones de aspecto:

| Aspect Ratio | Uso típico |
|-------------|------------|
| `1:1` | Avatares, thumbnails, posts de Instagram |
| `1:4` | Banners verticales estrechos |
| `1:8` | Banners verticales ultra-estrechos |
| `2:3` | Retratos verticales |
| `3:2` | Fotografía clásica horizontal |
| `3:4` | Retratos estándar |
| `4:1` | Banners horizontales |
| `4:3` | Pantallas clásicas, presentaciones |
| `4:5` | Posts de Instagram (retrato) |
| `5:4` | Fotografía medium format |
| `8:1` | Banners panorámicos ultra-anchos |
| `9:16` | Stories de Instagram, TikTok, Reels |
| `16:9` | Widescreen, YouTube, presentaciones |
| `21:9` | Cine ultra-wide |

### Ejemplo de configuración de resolución

```python
# Imagen 4K en formato panorámico para cine
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents="A sweeping landscape of mountains at golden hour",
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="21:9",
            image_size="4K"
        ),
    )
)
```

```javascript
// Story vertical para Instagram
const response = await ai.models.generateContent({
    model: 'gemini-3.1-flash-image-preview',
    contents: 'Minimalist product photo of a coffee cup',
    config: {
      responseModalities: ['IMAGE'],
      imageConfig: {
        aspectRatio: '9:16',
        imageSize: '2K',
      },
    },
});
```

### Ejemplo: Imagen de alta resolución — Sketch estilo Da Vinci

#### Python

```python
from google import genai
from google.genai import types

prompt = "Da Vinci style anatomical sketch of a dissected Monarch butterfly. Detailed drawings of the head, wings, and legs on textured parchment with notes in English."
aspect_ratio = "1:1"
resolution = "1K"

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=resolution
        ),
    )
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif image:= part.as_image():
        image.save("butterfly.png")
```

#### JavaScript

```javascript
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

async function main() {

  const ai = new GoogleGenAI({});

  const prompt =
      'Da Vinci style anatomical sketch of a dissected Monarch butterfly. Detailed drawings of the head, wings, and legs on textured parchment with notes in English.';
  const aspectRatio = '1:1';
  const resolution = '1K';

  const response = await ai.models.generateContent({
    model: 'gemini-3.1-flash-image-preview',
    contents: prompt,
    config: {
      responseModalities: ['TEXT', 'IMAGE'],
      imageConfig: {
        aspectRatio: aspectRatio,
        imageSize: resolution,
      },
    },
  });

  for (const part of response.candidates[0].content.parts) {
    if (part.text) {
      console.log(part.text);
    } else if (part.inlineData) {
      const imageData = part.inlineData.data;
      const buffer = Buffer.from(imageData, "base64");
      fs.writeFileSync("image.png", buffer);
      console.log("Image saved as image.png");
    }
  }

}

main();
```

#### Go

```go
package main

import (
    "context"
    "fmt"
    "log"
    "os"

    "google.golang.org/genai"
)

func main() {
    ctx := context.Background()
    client, err := genai.NewClient(ctx, nil)
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()

    model := client.GenerativeModel("gemini-3.1-flash-image-preview")
    model.GenerationConfig = &pb.GenerationConfig{
        ResponseModalities: []pb.ResponseModality{genai.Text, genai.Image},
        ImageConfig: &pb.ImageConfig{
            AspectRatio: "1:1",
            ImageSize:   "1K",
        },
    }

    prompt := "Da Vinci style anatomical sketch of a dissected Monarch butterfly. Detailed drawings of the head, wings, and legs on textured parchment with notes in English."
    resp, err := model.GenerateContent(ctx, genai.Text(prompt))
    if err != nil {
        log.Fatal(err)
    }

    for _, part := range resp.Candidates[0].Content.Parts {
        if txt, ok := part.(genai.Text); ok {
            fmt.Printf("%s", string(txt))
        } else if img, ok := part.(genai.ImageData); ok {
            err := os.WriteFile("butterfly.png", img.Data, 0644)
            if err != nil {
                log.Fatal(err)
            }
        }
    }
}
```

#### Java

```java
import com.google.genai.Client;
import com.google.genai.types.GenerateContentConfig;
import com.google.genai.types.GenerateContentResponse;
import com.google.genai.types.GoogleSearch;
import com.google.genai.types.ImageConfig;
import com.google.genai.types.Part;
import com.google.genai.types.Tool;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class HiRes {
    public static void main(String[] args) throws IOException {

      try (Client client = new Client()) {
        GenerateContentConfig config = GenerateContentConfig.builder()
            .responseModalities("TEXT", "IMAGE")
            .imageConfig(ImageConfig.builder()
                .aspectRatio("16:9")
                .imageSize("4K")
                .build())
            .build();

        GenerateContentResponse response = client.models.generateContent(
            "gemini-3.1-flash-image-preview", """
              Da Vinci style anatomical sketch of a dissected Monarch butterfly.
              Detailed drawings of the head, wings, and legs on textured
              parchment with notes in English.
              """,
            config);

        for (Part part : response.parts()) {
          if (part.text().isPresent()) {
            System.out.println(part.text().get());
          } else if (part.inlineData().isPresent()) {
            var blob = part.inlineData().get();
            if (blob.data().isPresent()) {
              Files.write(Paths.get("butterfly.png"), blob.data().get());
            }
          }
        }
      }
    }
}
```

#### REST / curl

```bash
curl -s -X POST \
      "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "contents": [{"parts": [{"text": "Da Vinci style anatomical sketch of a dissected Monarch butterfly. Detailed drawings of the head, wings, and legs on textured parchment with notes in English."}]}],
        "generationConfig": {
          "responseModalities": ["TEXT", "IMAGE"],
          "imageConfig": {"aspectRatio": "1:1", "imageSize": "1K"}
        }
      }'
```

---

## Capítulo 9: Control del Proceso de Pensamiento (Thinking)

Los modelos Gemini 3.x usan razonamiento interno para prompts complejos. Puedes controlar este comportamiento para equilibrar entre calidad y latencia.

### Niveles de pensamiento

| Nivel | Comportamiento | Cuándo usar |
|-------|---------------|-------------|
| `minimal` | Razonamiento mínimo, respuesta rápida | Generación de alto volumen, prompts simples |
| `high` | Razonamiento profundo, mayor calidad | Prompts complejos, composiciones detalladas |

**Importante:** Los tokens de pensamiento se facturan independientemente de si configuras `include_thoughts` o no. Activar `include_thoughts=True` solo hace que puedas ver el razonamiento, no cambia el costo.

### Ejemplo completo — Ciudad futurista con pensamiento visible

#### Python

```python
from google import genai

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents="A futuristic city built inside a giant glass bottle floating in space",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        thinking_config=types.ThinkingConfig(
            thinking_level="High",
            include_thoughts=True
        ),
    )
)

for part in response.parts:
    if part.thought: # Saltar los pensamientos en el output
      continue
    if part.text:
      display(Markdown(part.text))
    elif image:= part.as_image():
      image.show()
```

#### JavaScript

```javascript
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

async function main() {

  const ai = new GoogleGenAI({});

  const response = await ai.models.generateContent({
    model: "gemini-3.1-flash-image-preview",
    contents: "A futuristic city built inside a giant glass bottle floating in space",
    config: {
      responseModalities: ["IMAGE"],
      thinkingConfig: {
        thinkingLevel: "High",
        includeThoughts: true
      },
    },
  });

  for (const part of response.candidates[0].content.parts) {
    if (part.thought) { // Saltar los pensamientos
      continue;
    }
    if (part.text) {
      console.log(part.text);
    } else if (part.inlineData) {
      const imageData = part.inlineData.data;
      const buffer = Buffer.from(imageData, "base64");
      fs.writeFileSync("image.png", buffer);
      console.log("Image saved as image.png");
    }
  }
}
main();
```

#### Go

```go
package main

import (
    "context"
    "fmt"
    "log"
    "os"

    "google.golang.org/genai"
    pb "google.golang.org/genai/schema"
)

func main() {
    ctx := context.Background()
    client, err := genai.NewClient(ctx, nil)
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()

    model := client.GenerativeModel("gemini-3.1-flash-image-preview")
    model.GenerationConfig = &pb.GenerationConfig{
        ResponseModalities: []pb.ResponseModality{genai.Image},
        ThinkingConfig: &pb.ThinkingConfig{
            ThinkingLevel:   "High",
            IncludeThoughts: true,
        },
    }

    prompt := "A futuristic city built inside a giant glass bottle floating in space"
    resp, err := model.GenerateContent(ctx, genai.Text(prompt))
    if err != nil {
        log.Fatal(err)
    }

    for _, part := range resp.Candidates[0].Content.Parts {
        if part.Thought { // Saltar pensamientos
            continue
        }
        if txt, ok := part.(genai.Text); ok {
            fmt.Printf("%s", string(txt))
        } else if img, ok := part.(genai.ImageData); ok {
            err := os.WriteFile("image.png", img.Data, 0644)
            if err != nil {
                log.Fatal(err)
            }
        }
    }
}
```

### Thought Signature — Contexto encriptado para multi-turno

Cuando usas thinking en conversaciones multi-turno, la respuesta incluye un `thought_signature` — un contexto encriptado que permite al modelo mantener continuidad de razonamiento entre turnos sin exponer los pensamientos internos.

---

## Capítulo 10: Batch Processing — Generación en Lote

Para escenarios de alto volumen, la Batch API ofrece:

- **Rate limits más altos** que la API estándar
- **Tiempo de respuesta de hasta 24 horas** (no es en tiempo real)
- **Ideal para:** catálogos de productos, generación masiva de variaciones, pipelines de contenido

### Cuándo usar Batch vs Standard

| Escenario | API recomendada |
|-----------|----------------|
| Respuesta inmediata necesaria | Standard API |
| Generación interactiva | Standard API |
| 100+ imágenes de catálogo | Batch API |
| Pipeline nocturno | Batch API |
| Prototipo / exploración | Standard API |

### Ejemplo conceptual de Batch

```python
# Pseudocódigo — consulta la documentación de Batch API para detalles
from google import genai

client = genai.Client()

# Crear batch job con múltiples prompts
prompts = [
    "Product photo: red sneakers on white background",
    "Product photo: blue backpack on white background",
    "Product photo: black sunglasses on white background",
    # ... hasta cientos de prompts
]

# El batch job se procesa de forma asíncrona
# Resultados disponibles en hasta 24 horas
```

---

# PARTE IV — MEJORES PRÁCTICAS Y PATRONES

---

## Capítulo 11: Prompting — El Arte de Describir Imágenes

La calidad de la imagen generada depende directamente de la calidad de tu prompt. Gemini entiende lenguaje natural rico, así que aprovéchalo.

### Principio fundamental: Describe la escena, no listes keywords

```
❌ MALO (lista de keywords):
"cat, sunset, beach, realistic, 4k, professional"

✅ BUENO (descripción narrativa):
"A ginger tabby cat sitting on a sandy beach at golden hour.
The sun is setting behind the ocean, casting warm orange and
pink tones across the sky. The cat is looking directly at the
camera with a content expression. Shot with a shallow depth
of field, the background waves are softly blurred."
```

**¿Por qué?** Gemini es un modelo de lenguaje — entiende contexto, relaciones y narrativa mucho mejor que listas de palabras sueltas.

### Estrategias por tipo de imagen

#### Fotografía realista — Usa terminología fotográfica

```python
# Incluye: ángulo de cámara, tipo de lente, iluminación, detalles finos
prompt = """
A portrait of an elderly craftsman in his workshop.
Shot on a 50mm f/1.4 lens, natural window light from the left.
Shallow depth of field with bokeh in the background.
The craftsman is examining a piece of wood with reading glasses
perched on his nose. Warm color temperature, golden hour feel.
Fine details visible: wood shavings on the workbench,
dust particles caught in the light beam.
"""
```

#### Ilustraciones y stickers — Sé explícito con el estilo

```python
# Especifica estilo visual y fondo
prompt = """
A cute cartoon fox character in kawaii style.
White background. The fox has big sparkly eyes,
a fluffy tail, and is holding a small cup of bubble tea.
Flat colors, clean outlines, sticker-ready design.
No shadows, simple and cheerful.
"""
```

**Nota:** Los fondos transparentes NO están soportados. Si necesitas un fondo limpio, pide explícitamente "fondo blanco" y luego elimínalo en postprocesamiento.

#### Infografías y datos visuales — Estructura el contenido

```python
prompt = """
A clean, modern infographic comparing three renewable energy sources:
solar, wind, and hydroelectric power.

Layout: Three columns side by side.
Each column has:
- An icon at the top (sun, wind turbine, water dam)
- A bar chart showing efficiency percentage
- Three bullet points with key facts

Color scheme: Blue and green palette on white background.
Typography: Sans-serif, clean and readable.
Style: Flat design, minimal, professional.
"""
```

### Tabla de elementos descriptivos efectivos

| Elemento | Para qué sirve | Ejemplo |
|----------|----------------|---------|
| **Ángulo de cámara** | Control de perspectiva | "bird's eye view", "low angle", "close-up macro" |
| **Iluminación** | Mood y atmósfera | "golden hour", "studio lighting", "neon glow" |
| **Lente** | Profundidad de campo | "50mm f/1.4 bokeh", "wide angle 14mm", "telephoto compression" |
| **Estilo artístico** | Look general | "watercolor", "oil painting", "pixel art", "3D render" |
| **Paleta de colores** | Coherencia cromática | "muted earth tones", "vibrant neon", "monochrome blue" |
| **Composición** | Layout visual | "rule of thirds", "centered symmetry", "diagonal leading lines" |
| **Textura** | Detalle de superficies | "rough stone", "smooth glass", "weathered wood" |
| **Ambiente** | Contexto espacial | "cozy indoor", "vast desert", "underwater coral reef" |

### Errores comunes de prompting

| Error | Por qué falla | Solución |
|-------|---------------|----------|
| Prompt demasiado corto | Gemini tiene que inventar demasiados detalles | Añade contexto específico |
| Instrucciones contradictorias | "Fotorrealista con estilo cartoon" | Elige un estilo y sé consistente |
| Demasiados elementos | El modelo no puede componer todo | Simplifica o divide en pasos |
| Pedir texto exacto en imagen | La IA tiene dificultades con texto renderizado | Minimiza texto; añádelo en postprocesamiento |
| Pedir fondo transparente | No está soportado | Pide fondo blanco y recórtalo después |

---

## Capítulo 12: Configuración Completa — Referencia de la API

### Estructura del objeto de configuración

```python
# Python — Configuración completa
config = types.GenerateContentConfig(
    # Qué tipo de respuesta esperas
    response_modalities=['TEXT', 'IMAGE'],  # o solo ['IMAGE']

    # Configuración de imagen
    image_config=types.ImageConfig(
        aspect_ratio="16:9",     # Relación de aspecto
        image_size="2K"          # Resolución
    ),

    # Herramientas (Search, etc.)
    tools=[
        {"google_search": {}},                    # Web search básico
        # O con image search:
        # types.Tool(google_search=types.GoogleSearch(
        #     search_types=types.SearchTypes(
        #         web_search=types.WebSearch(),
        #         image_search=types.ImageSearch()
        #     )
        # ))
    ],

    # Configuración de pensamiento
    thinking_config=types.ThinkingConfig(
        thinking_level="High",      # "minimal" o "High"
        include_thoughts=True       # Ver el razonamiento
    ),
)
```

```javascript
// JavaScript — Configuración completa
const config = {
    responseModalities: ['TEXT', 'IMAGE'],
    imageConfig: {
        aspectRatio: '16:9',
        imageSize: '2K',
    },
    tools: [{ googleSearch: {} }],
    thinkingConfig: {
        thinkingLevel: 'High',
        includeThoughts: true,
    },
};
```

```json
// REST — Configuración completa
{
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "imageConfig": {
      "aspectRatio": "16:9",
      "imageSize": "2K"
    },
    "thinkingConfig": {
      "thinkingLevel": "High",
      "includeThoughts": true
    }
  },
  "tools": [
    {
      "google_search": {
        "searchTypes": {
          "webSearch": {},
          "imageSearch": {}
        }
      }
    }
  ]
}
```

### Response Modalities

| Valor | Comportamiento |
|-------|---------------|
| `["TEXT", "IMAGE"]` | El modelo puede responder con texto, imagen, o ambos |
| `["IMAGE"]` | Solo devuelve imagen (sin texto descriptivo) |
| `["TEXT"]` | Solo texto (sin generación de imagen) |

### Estructura de respuesta

```python
# Estructura de la respuesta
response.candidates[0].content.parts  # Lista de partes
# Cada part puede ser:
#   - text: str               → Texto del modelo
#   - inline_data.data: bytes → Imagen en base64
#   - inline_data.mime_type   → "image/png" o "image/jpeg"
#   - thought: bool           → Si es un pensamiento interno

response.candidates[0].grounding_metadata  # Metadata de search
#   - search_entry_point.rendered_content  → HTML con fuentes
#   - grounding_chunks                     → Fuentes individuales
```

---

## Capítulo 13: Patrones de Uso Comunes

### Patrón 1: Pipeline de generación de producto

```python
from google import genai
from google.genai import types
from pathlib import Path

client = genai.Client()

products = [
    {"name": "Red Running Shoes", "angle": "45-degree side view"},
    {"name": "Blue Backpack", "angle": "front view, slightly angled"},
    {"name": "Black Sunglasses", "angle": "floating, 3/4 view"},
]

for product in products:
    prompt = f"""
    Professional e-commerce product photo of {product['name']}.
    {product['angle']} on a pure white background.
    Studio lighting with soft shadows.
    High detail, commercial quality.
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio="1:1",
                image_size="2K"
            ),
        )
    )

    for part in response.parts:
        if part.inline_data is not None:
            image = part.as_image()
            filename = product['name'].lower().replace(' ', '_')
            image.save(f"products/{filename}.png")
            print(f"Generado: {filename}.png")
```

### Patrón 2: Variaciones de un diseño

```python
styles = [
    "watercolor painting style",
    "pixel art retro game style",
    "minimalist line drawing",
    "photorealistic 3D render",
    "Japanese ukiyo-e woodblock print style",
]

base_subject = "A majestic owl perched on a branch under a full moon"

for i, style in enumerate(styles):
    prompt = f"{base_subject}. Rendered in {style}."

    response = client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio="1:1",
                image_size="1K"
            ),
        )
    )

    for part in response.parts:
        if part.inline_data is not None:
            part.as_image().save(f"owl_variation_{i+1}.png")
```

### Patrón 3: Edición iterativa con validación

```python
chat = client.chats.create(
    model="gemini-3.1-flash-image-preview",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
    )
)

# Paso 1: Generar base
response = chat.send_message(
    "Create a simple logo for a coffee shop called 'Morning Brew'. "
    "Minimalist design, a coffee cup with steam forming the letter M. "
    "Black and white only."
)

# Guardar v1
for part in response.parts:
    if image := part.as_image():
        image.save("logo_v1.png")

# Paso 2: Refinar
response = chat.send_message(
    "The steam should be more prominent and curved. "
    "Make the cup handle more visible. Keep everything else the same."
)

# Guardar v2
for part in response.parts:
    if image := part.as_image():
        image.save("logo_v2.png")

# Paso 3: Colorear
response = chat.send_message(
    "Now add color: the cup should be a deep brown (#4A2C2A), "
    "the steam should be a soft tan (#D4A574). "
    "White background. Do not change the shapes."
)

# Guardar v3
for part in response.parts:
    if image := part.as_image():
        image.save("logo_v3.png")
```

### Patrón 4: Generación con datos en tiempo real

```python
# Generar infografía con datos actuales
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents="""
    Create a beautiful, modern infographic showing the current
    top 5 most valued companies in the world by market cap.

    Use actual current data from Google Search.
    Show each company's logo (simplified), name, and market cap
    in billions. Use a horizontal bar chart layout.

    Style: dark theme, neon accents, futuristic design.
    """,
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
            image_size="2K"
        ),
        tools=[{"google_search": {}}]
    )
)
```

---

# PARTE V — LIMITACIONES Y CONSIDERACIONES

---

## Capítulo 14: Limitaciones Conocidas

### Limitaciones técnicas

| Limitación | Detalle |
|-----------|---------|
| **Fondos transparentes** | No están soportados. Pide fondo blanco y recórtalo en postprocesamiento |
| **Texto en imágenes** | Funciona pero con imprecisiones frecuentes en ortografía y posición |
| **Máximo de imágenes de referencia** | 14 imágenes por solicitud |
| **Image Search para personas** | No puede buscar personas específicas |
| **PDFs escaneados sin texto** | No aplica (esto es generación, no OCR) |
| **Resolución 512** | Solo disponible en `gemini-3.1-flash-image-preview` |

### Limitaciones de contenido

- Debes tener los derechos necesarios sobre cualquier imagen que subas
- No puedes generar contenido que infrinja derechos de terceros
- El contenido no debe engañar, acosar ni dañar
- Todas las imágenes incluyen SynthID (no removible)

### Consideraciones de costo

- Los tokens de pensamiento se facturan aunque no los veas (`include_thoughts=False`)
- Las imágenes de mayor resolución consumen más tokens
- Múltiples imágenes de referencia incrementan el consumo
- El Google Search grounding puede añadir costos adicionales

---

## Capítulo 15: Troubleshooting — Problemas Comunes

### "La imagen no tiene el estilo que pedí"

**Causa probable:** Prompt demasiado genérico.
**Solución:** Sé más específico con el estilo. En vez de "watercolor", usa "traditional watercolor painting with visible brush strokes, wet-on-wet technique, soft bleeding edges, on cold-pressed watercolor paper".

### "El texto en la imagen tiene errores"

**Causa probable:** Limitación inherente de los modelos de generación.
**Solución:** Minimiza el texto en la imagen generada. Genera la imagen sin texto y añade el texto en postprocesamiento con herramientas como Pillow, Canva, o Photoshop.

### "La API devuelve error de rate limiting"

**Causa probable:** Demasiadas solicitudes en poco tiempo.
**Solución:** Implementa retry con exponential backoff, o migra a la Batch API para alto volumen.

### "La imagen no mantiene el aspecto de las referencias"

**Causa probable:** Demasiadas imágenes de referencia o prompt conflictivo.
**Solución:** Reduce el número de referencias. Prioriza 2-3 imágenes clave. Describe explícitamente qué elementos preservar de cada referencia.

### "Google Search no encuentra datos actuales"

**Causa probable:** Datos demasiado específicos o recientes.
**Solución:** Verifica que la información exista en la web. Prueba con queries más amplios primero.

---

# PARTE VI — REFERENCIA RÁPIDA

---

## Cheat Sheet — Todo en una página

### Modelos

```
gemini-3.1-flash-image-preview  ← Rápido, 512-4K, Image Search
gemini-3-pro-image-preview      ← Calidad pro, 1K-4K
gemini-2.5-flash-image          ← General, 1K-4K
```

### Resoluciones

```
"512"  → Solo Flash 3.1
"1K"   → Todos
"2K"   → Todos
"4K"   → Todos
```

### Aspect Ratios

```
1:1  1:4  1:8  2:3  3:2  3:4  4:1  4:3  4:5  5:4  8:1  9:16  16:9  21:9
```

### Response Modalities

```python
['TEXT', 'IMAGE']  # Texto + imagen
['IMAGE']          # Solo imagen
['TEXT']           # Solo texto
```

### Thinking Levels

```python
thinking_level="minimal"  # Rápido, menos razonamiento
thinking_level="High"     # Lento, mejor calidad
```

### Search Types

```python
tools=[{"google_search": {}}]                    # Solo web
tools=[types.Tool(google_search=types.GoogleSearch(
    search_types=types.SearchTypes(
        web_search=types.WebSearch(),
        image_search=types.ImageSearch()          # Web + imágenes
    )
))]
```

### Template mínimo por lenguaje

**Python:**
```python
from google import genai
from google.genai import types

client = genai.Client()
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents="Tu prompt aquí",
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE'],
        image_config=types.ImageConfig(aspect_ratio="1:1", image_size="1K"),
    )
)
for part in response.parts:
    if image := part.as_image():
        image.save("output.png")
```

**JavaScript:**
```javascript
const ai = new GoogleGenAI({});
const response = await ai.models.generateContent({
    model: 'gemini-3.1-flash-image-preview',
    contents: 'Tu prompt aquí',
    config: {
        responseModalities: ['IMAGE'],
        imageConfig: { aspectRatio: '1:1', imageSize: '1K' },
    },
});
for (const part of response.candidates[0].content.parts) {
    if (part.inlineData) {
        fs.writeFileSync("output.png", Buffer.from(part.inlineData.data, "base64"));
    }
}
```

**curl:**
```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "Tu prompt aquí"}]}],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {"aspectRatio": "1:1", "imageSize": "1K"}
    }
  }'
```

---

## Glosario

| Término | Definición |
|---------|-----------|
| **Grounding** | Conectar la generación de imágenes con datos reales de la web |
| **SynthID** | Marca de agua digital invisible de Google en imágenes generadas por IA |
| **Inline Data** | Datos binarios de la imagen codificados en base64 dentro de la respuesta |
| **Response Modalities** | Tipos de salida que el modelo puede devolver (TEXT, IMAGE) |
| **Multi-turn** | Conversación de múltiples turnos que mantiene contexto entre solicitudes |
| **Thinking Config** | Configuración que controla el nivel de razonamiento interno del modelo |
| **Image Config** | Parámetros de configuración de la imagen de salida (aspecto, resolución) |
| **Batch API** | API de procesamiento en lote para alto volumen con menor prioridad |
| **Aspect Ratio** | Relación de aspecto (ancho:alto) de la imagen generada |
| **Part** | Unidad de contenido en una respuesta — puede ser texto, imagen o pensamiento |
| **Grounding Metadata** | Información sobre las fuentes web usadas para generar la imagen |
| **Thought Signature** | Contexto encriptado de razonamiento para continuidad en multi-turno |

---

> **Nota del autor:** Este curso se basa en la documentación oficial de Google AI disponible en ai.google.dev. Los modelos y APIs descritos están en estado "preview" al momento de escritura y pueden cambiar. Consulta siempre la documentación oficial para la información más actualizada.

---

*© Rommel Ayala - All rights reserved*
