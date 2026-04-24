# CONTEXT — Rommel Ayala / AIQ®

Usa este archivo para retomar el trabajo en cualquier AI (Claude, Gemini, ChatGPT, etc.).
Al inicio de cada sesión pégalo y di: **"Contexto cargado, continuamos."**

---

## 1. QUIÉN SOY

- **Nombre:** Rommel Ayala
- **Rol:** QA Lead Architect — especialista en automatización con IA
- **Marca:** AIQ® (Ayala Intelligence & Quality) — marca registrada
- **Dominio:** ayala-iq.com | **Email:** rommel@ayala-iq.com
- **GitHub:** github.com/ayala-iq
- **LinkedIn:** linkedin.com/in/rommelayala
- **Eslogan:** *"Flowing with your vision. Curiosity that could break it."*

## 2. FILOSOFÍA DE TRABAJO

- Soluciones simples y directas. Si un script bash resuelve el problema, usar bash.
- No sobreingeniería. No agregar capas de tecnología innecesarias.
- Tono: cercano, riguroso, de tú a tú (nivel CTO/Tech Lead). Sin lenguaje corporativo.
- Escepticismo preventivo: cuestiona mis decisiones si hay una forma mejor.

## 3. LÍNEAS DE NEGOCIO

- **Consultoría QA:** Auditoría y madurez de equipos usando el modelo RMM (Responsive Maturity Model)
- **Soluciones Tech/IA:** Sistemas inteligentes (Webs, Bots, Apps) integrando IA con calidad

## 4. STACK TÉCNICO

- **Frontend:** Next.js (App Router), Tailwind CSS, TypeScript
- **Automatización:** Playwright + TypeScript
- **Hosting:** Vercel | **DNS:** Cloudflare | **Repo:** GitHub
- **Notas/Vault:** Obsidian en `/Users/rommel/Documents/project/Rommel/vaults-Obs/`

---

## 5. PROYECTOS ACTIVOS

### 📚 Pipeline de Libros EPUB
- **Ruta:** `/home/rommel/Documents/project/genera_epubs/`
- **Script actual:** `generate_epub.sh` — convierte `.md` a EPUB con pandoc
- **Uso:**
  - `./generate_epub.sh` → genera todos los libros
  - `./generate_epub.sh nombre-archivo.md` → genera uno específico
  - Archivo inexistente → error + lista los disponibles
- **Borradores en:** `libros_draft/` (✅ EPUB generado 2026-04-10)
  - `fundamentos-ia-libro.md`
  - `playwright-ts-intermedio-avanzado.md`
  - `agentes-ia-libro.md` (con PARTE III — Contexto Persistente)
  - `skills-libro.md`
  - `claude-uso-maestro.md` 🆕
  - `gemini-uso-maestro.md` 🆕
  - `gemini-nano-on-device-ai.md` 🆕
- **Output:** `epubs_generados/` (con timestamp `YYYYMMDD_HHMMSS`); versiones viejas en `Z-old_version/`
- **Portadas:** `generate_minimal_covers.py` + `portadas_draft/`
- **Plan en curso:** migración de `generate_epub.sh` a CLI Python (`Documentacion/planes/plan-migracion-python.md`) — añade metadata YAML sidecar, portadas configurables y soporte de entrada `.pdf` vía `ebook-convert` (Calibre) además de `.md` vía pandoc.
- **Contexto portable:** `context/CONTEXT.md` ← este archivo

### 🌐 Landing Page AIQ®
- **Repo:** github.com/ayala-iq/landing-page
- **Stack:** Next.js + Tailwind CSS + TypeScript → Vercel
- **Secciones construidas:** Navbar, Hero, Grid de Servicios, Manifiesto, Footer
- **Siguiente paso:** pendiente de definir

---

## 6. CÓMO TRABAJAR CONMIGO

- Ve directo al punto, sin rodeos
- Si algo ya está resuelto de forma simple, mejóralo — no lo reemplaces con algo más complejo
- Si propones tecnología nueva, justifica por qué es necesaria
- Pregunta antes de asumir qué quiero construir

---

*Última actualización: 2026-04-11*
