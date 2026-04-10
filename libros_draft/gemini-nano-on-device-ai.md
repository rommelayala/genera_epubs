# Gemini Nano — IA on-device desde cero hasta producción
### Curso práctico · AIQ® 2026

---

# PARTE I — EL CONTEXTO QUE IMPORTA

---

## ¿Qué es Gemini Nano?

Gemini Nano es el modelo de IA más pequeño de la familia Gemini de Google. Su propósito es uno solo: **correr directamente en el dispositivo**, sin llamadas a servidores, sin necesidad de internet, sin costos por API.

No es un modelo reducido que hace cosas a medias. Es un modelo diseñado desde cero para operar en hardware embebido — el NPU (Neural Processing Unit) de tu teléfono o tablet Android.

```
Modelo         ¿Dónde corre?         ¿Para qué?
────────────────────────────────────────────────────────
Gemini Ultra   Cloud (data centers)   Tareas complejas, razonamiento profundo
Gemini Pro     Cloud                  Balance poder/costo, API general
Gemini Flash   Cloud / Edge           Respuestas rápidas, alto volumen
Gemini Nano    En el dispositivo      Sin internet, privacidad, baja latencia
```

**La diferencia que define todo:**

| Característica        | Cloud AI         | Gemini Nano (On-device)     |
|-----------------------|------------------|-----------------------------|
| Latencia              | 200–2000 ms      | < 50 ms                     |
| Conexión a internet   | Obligatoria      | No requerida                |
| Privacidad            | Datos viajan     | Datos nunca salen           |
| Costo por request     | Facturado        | Cero                        |
| Disponibilidad        | Depende del CDN  | Siempre disponible          |

---

## ¿Por qué existe? — El problema que resuelve

Tres problemas reales que Cloud AI no puede resolver:

**1. Latencia inaceptable para UX en tiempo real**
Transcribir audio, sugerir texto o resumir contenido mientras el usuario escribe no tolera 500ms de round-trip. Con Nano es local, inmediato.

**2. Privacidad by design**
Hacer IA en el dispositivo significa que los datos del usuario (mensajes, fotos, audio) **nunca salen del teléfono**. Es privacidad real, no política de privacidad.

**3. Funcionamiento offline**
El 45% del tráfico móvil global ocurre en condiciones de conectividad degradada. Nano funciona en el metro, en el avión, en zonas rurales.

---

## El ecosistema — dónde encaja Nano

```
┌─────────────────────────────────────────────────────┐
│                     Tu App Android                  │
│                                                     │
│  ┌──────────────────┐    ┌────────────────────────┐ │
│  │ ML Kit GenAI API │    │ Google AI Edge SDK     │ │
│  │ (alto nivel)     │    │ (control total)        │ │
│  └────────┬─────────┘    └──────────┬─────────────┘ │
│           │                         │               │
│           └──────────┬──────────────┘               │
│                      ▼                              │
│              ┌───────────────┐                      │
│              │  AICore       │  ← servicio del SO   │
│              │  (Android OS) │                      │
│              └───────┬───────┘                      │
│                      ▼                              │
│              ┌───────────────┐                      │
│              │ Gemini Nano   │  ← modelo en el NPU  │
│              └───────────────┘                      │
└─────────────────────────────────────────────────────┘
```

- **AICore** es el servicio del sistema operativo que gestiona el modelo. Tú no lo tocas directamente.
- **ML Kit GenAI APIs** son el camino recomendado para tareas estándar (resumir, corregir, reescribir, describir imágenes).
- **Google AI Edge SDK** es para casos donde necesitas control fino o experimentación.
- **MediaPipe / LiteRT** es para modelos completamente custom — cuando Nano no es suficiente o necesitas tu propio fine-tune.

---

## Gemini Nano 4 — El estado actual (2026)

En abril de 2026 Google anunció la preview de **Gemini Nano 4**:

- **Multimodal nativo:** entiende texto, imágenes y audio en el mismo prompt
- **Razonamiento mejorado:** chain-of-thought, lógica compleja y matemáticas
- **4x más rápido** que versiones anteriores
- **Más eficiente energéticamente** — crítico para batería en móviles
- **Basado en Gemma 4:** el código escrito para Gemma 4 es compatible con Nano 4

**Hardware requerido:**
NPUs de Google (Tensor), Qualcomm (Snapdragon 8 Gen 2+) y MediaTek (Dimensity 9000+).

---

# PARTE II — HANDS ON

---

## Setup del entorno de desarrollo

### Lo que necesitas

- Android Studio Hedgehog (2023.1.1) o superior
- Android SDK 34+
- Dispositivo físico o emulador AVD con API 34+ y Google Play Services habilitados
- Cuenta Google con acceso a [Google AI Studio](https://aistudio.google.com)

### Dependencias en build.gradle (app)

```kotlin
// ML Kit GenAI APIs — camino recomendado
dependencies {
    implementation("com.google.android.gms:play-services-mlkit-text-recognition:19.0.0")
    
    // GenAI: resumir, reescribir, corregir, describir
    implementation("com.google.mlkit:genai-summarization:1.0.0-beta1")
    implementation("com.google.mlkit:genai-proofreading:1.0.0-beta1")
    implementation("com.google.mlkit:genai-rewriting:1.0.0-beta1")
    implementation("com.google.mlkit:genai-image-captioning:1.0.0-beta1")
}
```

```kotlin
// Google AI Edge SDK — para control total o experimentación
dependencies {
    implementation("com.google.ai.edge.aicore:aicore:0.0.1-exp01")
}
```

---

## ML Kit GenAI — Las 4 APIs que usarás el 80% del tiempo

### 1. Summarization — Resumir texto largo

**Cuándo usarlo:** artículos de noticias, emails largos, documentos, chats.

```kotlin
import com.google.mlkit.genai.summarization.Summarization
import com.google.mlkit.genai.summarization.SummarizationRequest

// 1. Verificar que el feature está disponible
val summarizer = Summarization.getClient()

summarizer.checkFeatureStatus().addOnSuccessListener { status ->
    when (status) {
        FeatureStatus.AVAILABLE -> {
            // Listo para usar
        }
        FeatureStatus.DOWNLOADABLE -> {
            // Trigger descarga del modelo
            summarizer.downloadFeature()
        }
        FeatureStatus.UNAVAILABLE -> {
            // Fallback a cloud o mostrar mensaje
        }
    }
}

// 2. Ejecutar summarización
val request = SummarizationRequest.builder(inputText)
    .setOutputLanguage(OutputLanguage.SAME_AS_INPUT)
    .build()

summarizer.runInference(request).addOnSuccessListener { result ->
    val summary = result.summary
    // Actualizar UI con el resumen
}
```

**Patrón crítico — siempre verificar disponibilidad:**
```kotlin
// NUNCA hagas esto:
summarizer.runInference(request) // puede fallar silenciosamente

// SIEMPRE haz esto:
summarizer.checkFeatureStatus().addOnSuccessListener { status ->
    if (status == FeatureStatus.AVAILABLE) {
        summarizer.runInference(request)
    }
}
```

---

### 2. Proofreading — Corrección gramatical

**Cuándo usarlo:** editores de texto, apps de email, campos de entrada libre.

```kotlin
import com.google.mlkit.genai.proofreading.Proofreading
import com.google.mlkit.genai.proofreading.ProofreadingRequest

val proofreader = Proofreading.getClient()

val request = ProofreadingRequest.builder(userText).build()

proofreader.runInference(request).addOnSuccessListener { result ->
    val correctedText = result.correctedText
    val suggestions = result.suggestions // lista de cambios específicos
}
```

---

### 3. Rewriting — Reescribir con tono/estilo

**Cuándo usarlo:** apps de escritura, editores, herramientas de comunicación profesional.

```kotlin
import com.google.mlkit.genai.rewriting.Rewriting
import com.google.mlkit.genai.rewriting.RewritingRequest
import com.google.mlkit.genai.rewriting.RewritingOption

val rewriter = Rewriting.getClient()

val request = RewritingRequest.builder(userText)
    .setRewritingOption(RewritingOption.ELABORATE)   // ELABORATE, SHORTEN, REPHRASE, FORMALIZE
    .build()

rewriter.runInference(request).addOnSuccessListener { result ->
    val rewrittenText = result.rewrittenText
}
```

**Opciones disponibles:**

| Opción       | Qué hace                            |
|--------------|-------------------------------------|
| `ELABORATE`  | Amplía y añade detalle              |
| `SHORTEN`    | Condensa manteniendo lo esencial    |
| `REPHRASE`   | Reescribe con palabras distintas    |
| `FORMALIZE`  | Convierte al tono formal/profesional|

---

### 4. Image Captioning — Describir imágenes

**Cuándo usarlo:** apps de accesibilidad, herramientas de catalogación, apps de cámara.

```kotlin
import com.google.mlkit.genai.imagecaptioning.ImageCaptioning
import com.google.mlkit.genai.imagecaptioning.ImageCaptioningRequest
import android.graphics.Bitmap

val captioner = ImageCaptioning.getClient()

val bitmap: Bitmap = // tu imagen
val request = ImageCaptioningRequest.builder(bitmap).build()

captioner.runInference(request).addOnSuccessListener { result ->
    val description = result.caption
}
```

---

## Google AI Edge SDK — Cuando necesitas más control

Para prompts libres, flujos conversacionales o configuración avanzada:

```kotlin
import com.google.ai.edge.aicore.GenerativeModel
import com.google.ai.edge.aicore.generationConfig

// Inicializar el modelo
val model = GenerativeModel(
    generationConfig = generationConfig {
        context = applicationContext
        temperature = 0.7f
        topK = 40
        maxOutputTokens = 500
    }
)

// Generar respuesta (streaming)
val response = model.generateContent("Resume este texto en 3 puntos clave: $text")
println(response.text)

// Con streaming para UX en tiempo real
model.generateContentStream("Explica este error de código: $errorLog")
    .collect { chunk ->
        // Actualizar UI en tiempo real con cada token
        appendToTextView(chunk.text)
    }
```

---

## Defensive Programming — El patrón que separa apps robustas de las frágiles

Gemini Nano **no está garantizado** en todos los dispositivos. AICore es un servicio opcional. Una app que no lo maneja explota en producción.

### El patrón completo con fallback a cloud:

```kotlin
class SummaryRepository(
    private val context: Context,
    private val cloudApi: YourCloudApi
) {
    
    suspend fun summarize(text: String): String {
        return when (checkNanoAvailability()) {
            FeatureStatus.AVAILABLE -> summarizeOnDevice(text)
            FeatureStatus.DOWNLOADABLE -> {
                triggerModelDownload()
                // Mientras descarga, usa cloud
                cloudApi.summarize(text)
            }
            FeatureStatus.UNAVAILABLE -> cloudApi.summarize(text)
        }
    }
    
    private suspend fun checkNanoAvailability(): FeatureStatus {
        return suspendCancellableCoroutine { continuation ->
            Summarization.getClient()
                .checkFeatureStatus()
                .addOnSuccessListener { status -> continuation.resume(status) }
                .addOnFailureListener { continuation.resume(FeatureStatus.UNAVAILABLE) }
        }
    }
    
    private suspend fun summarizeOnDevice(text: String): String {
        // implementación con ML Kit
    }
    
    private fun triggerModelDownload() {
        Summarization.getClient().downloadFeature()
        // Notificar al usuario que el modelo está descargando
    }
}
```

---

## Manejo del ciclo de vida del modelo

Los clientes de ML Kit no son baratos de crear. Siguiendo el patrón correcto:

```kotlin
class MyViewModel : ViewModel() {
    
    private val summarizer = Summarization.getClient()
    
    override fun onCleared() {
        super.onCleared()
        summarizer.close() // Liberar recursos cuando el ViewModel se destruye
    }
}
```

**Regla:** un cliente por ViewModel, ciérralo en `onCleared()`.

---

# PARTE III — CASOS DE USO REALES

---

## Caso 1 — Smart Reply en mensajería

```
Input:  "Oye, ¿puedes revisar el PR antes del deploy de hoy?"
Output: ["Claro, lo veo ahora", "Dame 10 min", "Ya lo revisé, listo para merge"]
```

Implementación con Edge SDK:

```kotlin
suspend fun generateReplySuggestions(message: String): List<String> {
    val prompt = """
        Genera exactamente 3 respuestas cortas (máx 8 palabras cada una) para este mensaje:
        "$message"
        
        Formato de salida: una respuesta por línea, sin numeración.
    """.trimIndent()
    
    val response = model.generateContent(prompt)
    return response.text?.lines()?.filter { it.isNotBlank() } ?: emptyList()
}
```

---

## Caso 2 — Transcripción + Resumen de reuniones (offline)

```
Flujo:
Audio → Speech-to-Text (ML Kit) → Texto → Gemini Nano Summarization → Resumen ejecutivo
```

```kotlin
class MeetingProcessor {
    
    private val speechRecognizer = // ML Kit Speech Recognition
    private val summarizer = Summarization.getClient()
    
    suspend fun processMeetingAudio(audioFile: Uri): MeetingResult {
        val transcript = speechRecognizer.transcribe(audioFile)
        
        val summaryRequest = SummarizationRequest.builder(transcript)
            .setOutputLanguage(OutputLanguage.SAME_AS_INPUT)
            .build()
        
        val summary = summarizer.runInference(summaryRequest).await()
        
        return MeetingResult(
            transcript = transcript,
            summary = summary.summary,
            processedAt = System.currentTimeMillis()
        )
    }
}
```

**Ventaja real:** toda esta pipeline ocurre sin internet. El audio nunca sale del dispositivo.

---

## Caso 3 — Asistente de escritura contextual

```
El usuario escribe un email → Nano detecta el tono → Sugiere mejoras en tiempo real
```

```kotlin
// Debounce para no llamar al modelo en cada keystroke
viewModelScope.launch {
    snapshotFlow { emailText.value }
        .debounce(800L)
        .filter { it.length > 50 }
        .collect { text ->
            val suggestions = getWritingSuggestions(text)
            _uiState.update { it.copy(suggestions = suggestions) }
        }
}
```

---

## Caso 4 — Accesibilidad — Descripción de imágenes en tiempo real

```kotlin
class AccessibilityService {
    
    private val captioner = ImageCaptioning.getClient()
    
    fun describeImageForUser(bitmap: Bitmap, onResult: (String) -> Unit) {
        captioner.checkFeatureStatus().addOnSuccessListener { status ->
            if (status == FeatureStatus.AVAILABLE) {
                val request = ImageCaptioningRequest.builder(bitmap).build()
                captioner.runInference(request).addOnSuccessListener { result ->
                    onResult(result.caption)
                    // TTS → reproducir descripción al usuario
                    textToSpeech.speak(result.caption, TextToSpeech.QUEUE_FLUSH, null, null)
                }
            }
        }
    }
}
```

---

# PARTE IV — ARQUITECTURA Y DECISIONES DE DISEÑO

---

## ¿Cuándo usar Nano vs Cloud AI?

```
Usa Gemini Nano cuando:          Usa Cloud AI (Gemini Pro/Flash) cuando:
─────────────────────────────    ──────────────────────────────────────────
✓ Privacidad es crítica          ✓ Necesitas razonamiento complejo
✓ App funciona offline           ✓ El contexto supera 4K tokens
✓ Latencia < 100ms es requerida  ✓ Necesitas multimodalidad avanzada
✓ Cero costo operacional         ✓ El dispositivo no tiene NPU capaz
✓ Tareas repetitivas simples     ✓ Resultados inconsistentes con Nano
```

**La respuesta honesta:** en la mayoría de apps de producción, usarás **ambos**. Nano para la experiencia inmediata, Cloud para la potencia cuando hace falta.

---

## Patrón de arquitectura recomendado

```
┌─────────────────────────────────────────────┐
│                  UI Layer                   │
│          (Composable / Fragment)            │
└────────────────────┬────────────────────────┘
                     │
┌────────────────────▼────────────────────────┐
│               ViewModel                     │
│         (gestiona estado + corrutinas)      │
└────────────────────┬────────────────────────┘
                     │
┌────────────────────▼────────────────────────┐
│            AI Repository                   │
│   ┌──────────────┐    ┌──────────────────┐  │
│   │ NanoStrategy │    │  CloudStrategy   │  │
│   │ (ML Kit)     │    │  (Gemini API)    │  │
│   └──────────────┘    └──────────────────┘  │
│        Selección automática por disponibilidad│
└─────────────────────────────────────────────┘
```

Implementación del Repository con Strategy pattern:

```kotlin
interface AIStrategy {
    suspend fun summarize(text: String): String
    suspend fun isAvailable(): Boolean
}

class AIRepository(
    private val nanoStrategy: NanoStrategy,
    private val cloudStrategy: CloudStrategy
) {
    suspend fun summarize(text: String): String {
        val strategy = if (nanoStrategy.isAvailable()) nanoStrategy else cloudStrategy
        return strategy.summarize(text)
    }
}
```

---

## Testing de funcionalidades Nano

El mayor reto: el emulador no siempre tiene AICore activo.

```kotlin
// Abstrae la dependencia para hacer mocking en tests
interface SummarizationProvider {
    suspend fun summarize(text: String): String
}

class GeminiNanoProvider : SummarizationProvider {
    override suspend fun summarize(text: String): String {
        // Implementación real con ML Kit
    }
}

class FakeSummarizationProvider : SummarizationProvider {
    override suspend fun summarize(text: String): String {
        return "Summary: ${text.take(50)}..." // Fake para tests
    }
}

// En tests:
val viewModel = MyViewModel(summarizationProvider = FakeSummarizationProvider())
```

---

## Privacidad y consentimiento

Aunque los datos no salen del dispositivo con Nano, sigue siendo buena práctica:

- **Documenta en tu política de privacidad** qué procesa Nano localmente.
- **No uses Nano para procesar datos de terceros** sin consentimiento.
- **Si mezclas con Cloud AI**, notifica al usuario qué datos se envían a servidores.
- **El modelo se descarga una vez** y vive en el sistema. No descarga datos del usuario.

---

# PARTE V — REFERENCIA RÁPIDA

---

## Cheatsheet de APIs

| Tarea               | API                              | Input          | Output            |
|---------------------|----------------------------------|----------------|-------------------|
| Resumir texto       | `Summarization.getClient()`      | `String`       | `String` (resumen)|
| Corregir gramática  | `Proofreading.getClient()`       | `String`       | `String` + diffs  |
| Reescribir texto    | `Rewriting.getClient()`          | `String`       | `String`          |
| Describir imagen    | `ImageCaptioning.getClient()`    | `Bitmap`       | `String`          |
| Prompt libre        | `GenerativeModel` (Edge SDK)     | `String`       | `String`          |
| Streaming           | `generateContentStream()`        | `String`       | `Flow<String>`    |

---

## Checklist pre-producción

```
Antes de hacer release, verifica:

[ ] checkFeatureStatus() implementado en todos los puntos de entrada a Nano
[ ] Fallback a cloud (o degradación elegante) cuando Nano no está disponible
[ ] Flujo de descarga del modelo con UX informativa para el usuario
[ ] Clientes de ML Kit cerrados en onCleared() / onDestroy()
[ ] Tests con FakeProvider para cubrir lógica sin depender del hardware
[ ] Política de privacidad actualizada mencionando procesamiento local
[ ] Probado en dispositivo físico con NPU compatible (no solo emulador)
```

---

## Dispositivos compatibles con Gemini Nano (2026)

| Fabricante    | Modelo                        | Chip              |
|---------------|-------------------------------|-------------------|
| Google        | Pixel 8 / 8 Pro / 8a          | Tensor G3         |
| Google        | Pixel 9 / 9 Pro / 9 Pro Fold  | Tensor G4         |
| Samsung       | Galaxy S24 series             | Snapdragon 8 Gen 3|
| Samsung       | Galaxy S25 series             | Snapdragon 8 Elite|
| OnePlus       | 12 / 12R                      | Snapdragon 8 Gen 3|
| Motorola      | Edge 50 Ultra                 | Snapdragon 8s Gen 3|

*Lista no exhaustiva. Verificar en [developer.android.com/ai/gemini-nano](https://developer.android.com/ai/gemini-nano)*

---

## Recursos

| Recurso                             | URL                                                                |
|-------------------------------------|------------------------------------------------------------------- |
| Documentación oficial ML Kit GenAI  | developer.android.com/ml-kit/genai                                 |
| Google AI Edge SDK                  | ai.google.dev/edge                                                 |
| Gemma 4 (base open source de Nano)  | ai.google.dev/gemma                                                |
| Codelabs Android AI                 | codelabs.developers.google.com/android-ai                          |
| AI Core Reference                   | developer.android.com/ml/aicore                                    |

---

*Generado con el skill AIQ® `generar-curso-skill.md` · Rommel Ayala · 2026*
