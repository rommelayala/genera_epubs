# Playwright + TypeScript: Nivel Intermedio-Avanzado
## El libro del QA que quiere dominar el navegador, no solo usarlo

**Fecha:** Marzo 2026

---

> "No testees lo que el usuario ve. Testea lo que el sistema hace."
> — Mentalidad QA avanzada

---

# ÍNDICE

1. [Setup profesional — configuración sin excusas](#setup)
2. [tsconfig + Node: lo que nadie te explica](#typescript)
3. [globalThis vs window vs global — el triángulo misterioso](#globals)
4. [page.evaluate() — el puente entre Node y el navegador](#evaluate)
5. [jQuery y otras armas en la consola](#jquery)
6. [Manipulación del DOM desde Playwright](#dom)
7. [Network interception — interceptar, modificar, mockear](#network)
8. [Autenticación y seguridad](#seguridad)
9. [Fixtures avanzados — el patrón que lo cambia todo](#fixtures)
10. [Tricks superchulos que no están en la docs](#tricks)
11. [Herramientas del arsenal](#herramientas)
12. [Patrones QA de nivel senior](#patrones)
13. [Integración con Cucumber y Gherkin — BDD con Sentido](#cucumber)
14. [CI/CD a Gran Escala — Sharding y Merge Reports](#sharding)
15. [El Futuro del QA — Self-Healing Locators con IA](#healing)
16. [Glosario de referencia rápida](#glosario)

---

<a name="setup"></a>
# 1. Setup Profesional — Configuración sin Excusas

## Instalación limpia

```bash
# Proyecto nuevo con TypeScript desde cero
npm init -y
npm install -D @playwright/test typescript @types/node

# Instalar navegadores (solo los que necesitas)
npx playwright install chromium
npx playwright install --with-deps chromium  # con dependencias del sistema

# Generar config inicial
npx playwright codegen  # también genera código desde el navegador
```

## `playwright.config.ts` — El archivo que define todo

Este es el archivo más importante del proyecto. La mayoría lo usa al 10% de su capacidad.

```typescript
import { defineConfig, devices } from '@playwright/test';
import * as dotenv from 'dotenv';

// Carga variables de entorno según el entorno activo
dotenv.config({ path: `.env.${process.env.NODE_ENV ?? 'local'}` });

export default defineConfig({
  // ── Directorios ──────────────────────────────────────────
  testDir: './tests',
  outputDir: './test-results',       // screenshots, videos, traces

  // ── Paralelismo ──────────────────────────────────────────
  fullyParallel: true,               // todos los archivos en paralelo
  workers: process.env.CI ? 2 : 4,  // menos workers en CI para no saturar

  // ── Timeouts ─────────────────────────────────────────────
  timeout: 30_000,                   // timeout por test (30s)
  expect: {
    timeout: 5_000,                  // timeout de expect() específicamente
    toHaveScreenshot: {
      maxDiffPixels: 100,            // tolerancia en visual testing
    },
  },

  // ── Reintentos ───────────────────────────────────────────
  retries: process.env.CI ? 2 : 0,  // reintentos solo en CI

  // ── Reporters ────────────────────────────────────────────
  reporter: [
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['line'],  // output en consola
    // ['allure-playwright'],  // si usas Allure
  ],

  // ── Configuración global del browser ─────────────────────
  use: {
    baseURL: process.env.BASE_URL ?? 'http://localhost:3000',

    // Tracing: guarda trace solo cuando falla
    trace: 'retain-on-failure',

    // Screenshots: guarda solo cuando falla
    screenshot: 'only-on-failure',

    // Video: graba solo cuando falla
    video: 'retain-on-failure',

    // Navegador headless o no
    headless: process.env.CI ? true : false,

    // Headers globales
    extraHTTPHeaders: {
      'x-test-run': 'playwright',
    },

    // Viewport por defecto
    viewport: { width: 1280, height: 720 },

    // Locale y timezone
    locale: 'es-ES',
    timezoneId: 'Europe/Madrid',

    // Ignorar errores de certificado SSL en desarrollo
    ignoreHTTPSErrors: process.env.NODE_ENV !== 'production',

    // Inyectar scripts antes de cargar cualquier página
    // (útil para mocks globales, desactivar analytics, etc.)
  },

  // ── Proyectos (perfiles de navegador) ────────────────────
  projects: [
    // Setup global: login una vez, reusar auth
    {
      name: 'setup',
      testMatch: '**/*.setup.ts',
    },

    // Chromium desktop
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
      dependencies: ['setup'],
    },

    // Firefox
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
      dependencies: ['setup'],
    },

    // Mobile Safari (iPhone 14)
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 14'] },
    },

    // API testing (sin navegador)
    {
      name: 'api',
      testMatch: '**/api/**/*.spec.ts',
      use: { baseURL: process.env.API_URL ?? 'http://localhost:3001' },
    },
  ],

  // ── Servidor local (levanta tu app antes de testear) ──────
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
});
```

## Estructura de proyecto profesional

```
proyecto/
├── playwright.config.ts
├── tsconfig.json
├── .env.local
├── .env.staging
├── .env.production
│
├── tests/
│   ├── auth/
│   │   ├── auth.setup.ts        ← login global, genera storageState
│   │   └── login.spec.ts
│   ├── e2e/
│   │   ├── checkout.spec.ts
│   │   └── dashboard.spec.ts
│   └── api/
│       └── users.spec.ts
│
├── fixtures/                    ← fixtures compartidos
│   ├── index.ts                 ← exports de todos los fixtures
│   ├── auth.fixture.ts
│   └── db.fixture.ts
│
├── pages/                       ← Page Object Model
│   ├── BasePage.ts
│   ├── LoginPage.ts
│   └── DashboardPage.ts
│
├── utils/
│   ├── helpers.ts
│   ├── faker-helpers.ts
│   └── api-client.ts
│
└── test-results/                ← generado automáticamente
```

---

<a name="typescript"></a>
# 2. tsconfig + Node: Lo Que Nadie Te Explica

## `tsconfig.json` optimizado para Playwright

```json
{
  "compilerOptions": {
    // ── Target y módulos ──────────────────────────────────
    "target": "ES2022",           // Node 18+ soporta ES2022
    "module": "commonjs",         // Playwright usa CommonJS
    "lib": ["ES2022"],            // librerías estándar

    // ── Paths y resolución ────────────────────────────────
    "baseUrl": ".",
    "paths": {
      "@fixtures/*": ["fixtures/*"],
      "@pages/*": ["pages/*"],
      "@utils/*": ["utils/*"]
    },

    // ── Tipo de salida ────────────────────────────────────
    "outDir": "./dist",
    "rootDir": ".",

    // ── Strict mode — siempre activado ───────────────────
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,        // errores por variables sin usar
    "noUnusedParameters": true,    // errores por params sin usar
    "noImplicitReturns": true,     // toda función debe retornar

    // ── Interop ───────────────────────────────────────────
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "resolveJsonModule": true,     // importar JSON como módulos

    // ── Decoradores (si usas class-based POM) ─────────────
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true,

    // ── Source maps para debugging ────────────────────────
    "sourceMap": true,

    // ── Incremental para velocidad ────────────────────────
    "incremental": true,
    "tsBuildInfoFile": ".tsbuildinfo"
  },
  "include": [
    "tests/**/*.ts",
    "fixtures/**/*.ts",
    "pages/**/*.ts",
    "utils/**/*.ts",
    "playwright.config.ts"
  ],
  "exclude": ["node_modules", "dist"]
}
```

## Tipos personalizados — extiende los de Playwright

```typescript
// types/index.d.ts — tipos globales del proyecto
declare namespace NodeJS {
  interface ProcessEnv {
    NODE_ENV: 'local' | 'staging' | 'production';
    BASE_URL: string;
    API_URL: string;
    TEST_USER_EMAIL: string;
    TEST_USER_PASSWORD: string;
    // Añade todos tus env vars aquí
    // TypeScript te avisará si usas uno que no declaraste
  }
}

// Extender los tipos de Playwright
import { Page } from '@playwright/test';

declare module '@playwright/test' {
  interface Page {
    // Método helper custom disponible en todos los tests
    waitForNetworkIdle(): Promise<void>;
  }
}
```

---

<a name="globals"></a>
# 3. globalThis vs window vs global — El Triángulo Misterioso

Este es uno de los temas más confusos en JavaScript moderno, y en Playwright es crítico porque trabajas en DOS contextos simultáneamente.

## Los tres contextos

```
┌─────────────────────────────────────────────────────────┐
│  CONTEXTO NODE (tu código Playwright)                   │
│                                                         │
│  global       → el objeto global de Node               │
│  globalThis   → alias universal (Node + Browser)        │
│  process      → info del proceso Node                   │
│  __dirname    → directorio del archivo actual           │
│  __filename   → ruta completa del archivo actual        │
│  require()    → importar módulos (CommonJS)             │
└────────────────────────┬────────────────────────────────┘
                         │
                    page.evaluate()
                         │
┌────────────────────────▼────────────────────────────────┐
│  CONTEXTO BROWSER (el navegador)                        │
│                                                         │
│  window       → el objeto global del navegador          │
│  globalThis   → alias universal (apunta a window)       │
│  document     → el DOM                                  │
│  navigator    → info del browser                        │
│  location     → URL actual                              │
└─────────────────────────────────────────────────────────┘
```

## `global` — el objeto global de Node

```typescript
// En Node.js, 'global' es el equivalente de 'window' en el browser
console.log(global === globalThis); // true en Node 12+

// Puedes añadir propiedades globales (úsalo con cuidado)
global.myTestConfig = { baseUrl: 'http://localhost:3000' };

// Accessible desde cualquier archivo del proyecto sin importar
console.log(global.myTestConfig.baseUrl);

// Caso de uso real en QA: variables compartidas entre workers
// ⚠️ OJO: en parallel workers, cada worker tiene su propio 'global'
// Para datos verdaderamente compartidos usa archivos o variables de entorno
```

## `globalThis` — el alias universal

```typescript
// Funciona en CUALQUIER entorno: Node, Browser, Web Workers, Deno
// Es la forma moderna y recomendada de acceder al objeto global

// En Node:
globalThis === global  // true

// En Browser:
globalThis === window  // true

// Útil cuando escribes código que corre en ambos contextos
// (por ejemplo, utilities compartidos entre Playwright y el browser)
function setGlobalValue(key: string, value: unknown) {
  (globalThis as Record<string, unknown>)[key] = value;
}
```

## `window` — el objeto del navegador (solo en browser)

```typescript
// window NO existe en Node — causará error si lo usas directamente
// Solo úsalo dentro de page.evaluate()

const title = await page.evaluate(() => {
  return window.document.title;  // ✅ correcto — estamos en browser context
});

// Acceder a variables globales del sitio web
const analyticsEnabled = await page.evaluate(() => {
  return (window as any).__ANALYTICS_ENABLED__;
});

// Modificar el objeto window para tests
await page.evaluate(() => {
  (window as any).__TEST_MODE__ = true;
  window.localStorage.setItem('debug', 'true');
});
```

## `process.env` — las variables de entorno

```typescript
// Siempre disponible en Node (nunca en browser sin webpack/bundler)

// Acceso tipado con el namespace que declaramos antes
const baseUrl: string = process.env.BASE_URL;  // TypeScript sabe que es string
const env = process.env.NODE_ENV;              // 'local' | 'staging' | 'production'

// Pattern recomendado: validar al inicio del test suite
// tests/global-setup.ts
export default async function globalSetup() {
  const required = ['BASE_URL', 'TEST_USER_EMAIL', 'TEST_USER_PASSWORD'];
  const missing = required.filter(key => !process.env[key]);

  if (missing.length > 0) {
    throw new Error(`Missing required env vars: ${missing.join(', ')}`);
  }
}

// En playwright.config.ts:
// globalSetup: './tests/global-setup.ts'
```

---

<a name="evaluate"></a>
# 4. page.evaluate() — El Puente Entre Node y el Navegador

`page.evaluate()` es la herramienta más poderosa de Playwright. Te permite ejecutar JavaScript directamente en el contexto del navegador.

## La distinción crítica que debes tatuarte

```typescript
// ❌ ESTO NO FUNCIONA — myVariable no existe en el browser
const myVariable = 'test';
await page.evaluate(() => {
  console.log(myVariable); // ReferenceError: myVariable is not defined
});

// ✅ ESTO SÍ — pasas el valor como argumento
const myVariable = 'test';
await page.evaluate((value) => {
  console.log(value); // 'test'
}, myVariable);

// ✅ También puedes pasar objetos
await page.evaluate(({ url, token }) => {
  fetch(url, { headers: { Authorization: `Bearer ${token}` } });
}, { url: '/api/data', token: myToken });
```

## Retornar valores del browser a Node

```typescript
// Retornar primitivos
const title = await page.evaluate(() => document.title);
const count = await page.evaluate(() => document.querySelectorAll('.item').length);

// Retornar objetos (serializados con JSON)
const userInfo = await page.evaluate(() => ({
  name: window.localStorage.getItem('userName'),
  token: window.sessionStorage.getItem('authToken'),
  cookies: document.cookie,
}));

// ⚠️ No puedes retornar funciones, Promises sin resolver, o referencias DOM
// Para referencias DOM usa evaluateHandle()
```

## `evaluateHandle()` — cuando necesitas manipular elementos

```typescript
// evaluateHandle retorna un JSHandle — una referencia a un objeto del browser
// No serializa — mantiene la referencia viva

// Útil para pasar elementos DOM como argumento a otras funciones
const bodyHandle = await page.evaluateHandle(() => document.body);

// Luego puedes pasarlo a otra evaluación
await page.evaluate((body) => {
  body.style.border = '2px solid red'; // útil para debugging visual
}, bodyHandle);

await bodyHandle.dispose(); // limpia la referencia
```

## `addInitScript()` — ejecutar código ANTES de que cargue la página

```typescript
// Se ejecuta en CADA página nueva, antes de cualquier script del sitio
// Perfecto para mocks, spies, y configuración global

// Caso 1: Desactivar analytics para no contaminar datos reales
await page.addInitScript(() => {
  window.ga = () => {};             // Google Analytics no-op
  window.gtag = () => {};           // Google Tag Manager no-op
  window.fbq = () => {};            // Facebook Pixel no-op
  (window as any).analytics = {     // Segment/Mixpanel no-op
    track: () => {},
    page: () => {},
    identify: () => {},
  };
});

// Caso 2: Congelar el tiempo (¡superchulo para tests de fechas!)
await page.addInitScript(() => {
  const fixedDate = new Date('2025-01-15T12:00:00.000Z');
  const originalDate = Date;

  class MockDate extends originalDate {
    constructor(...args: any[]) {
      if (args.length === 0) {
        super(fixedDate.getTime());
      } else {
        super(...args);
      }
    }
    static now() { return fixedDate.getTime(); }
  }

  (window as any).Date = MockDate;
});

// Caso 3: Inyectar feature flags de test
await page.addInitScript(() => {
  (window as any).__FEATURE_FLAGS__ = {
    newCheckout: true,
    betaFeature: false,
  };
});

// Caso 4: Añadir desde archivo (más limpio para scripts largos)
await page.addInitScript({ path: './scripts/mock-analytics.js' });
```

---

<a name="jquery"></a>
# 5. jQuery y Otras Armas en la Consola

## Inyectar jQuery en cualquier página

```typescript
// Método 1: Inyectar jQuery desde CDN
await page.addScriptTag({
  url: 'https://code.jquery.com/jquery-3.7.1.min.js'
});

// Método 2: Desde archivo local (mejor para CI sin internet)
await page.addScriptTag({
  path: './vendor/jquery.min.js'
});

// Método 3: Inline (para jQuery simplificado o custom)
await page.addScriptTag({
  content: `window.$ = window.jQuery = /* tu código */`
});

// Luego úsalo en evaluate
const items = await page.evaluate(() => {
  return $('table tbody tr').map(function() {
    return {
      name: $(this).find('td:first').text().trim(),
      price: $(this).find('td.price').text().trim(),
    };
  }).get();
});
```

## El `$` y `$$` nativo de la consola del DevTools

En la consola del navegador, Chrome ya incluye helpers similares a jQuery:

```javascript
// Estos funcionan en la consola del DevTools (no en Playwright directamente)
$('selector')     // = document.querySelector()
$$('selector')    // = Array.from(document.querySelectorAll())
$x('//xpath')    // = document.evaluate() con XPath

// En Playwright, el equivalente es:
await page.$('selector')        // → ElementHandle | null
await page.$$('selector')       // → ElementHandle[]
await page.$eval('sel', el => el.textContent)  // evalúa sobre el elemento
await page.$$eval('sel', els => els.map(e => e.textContent))
```

## Inyectar helpers custom en la consola

```typescript
// Crea tu librería de helpers para el proyecto
await page.addInitScript(() => {
  // Helper para debug visual — rodea elementos con borde de color
  (window as any).highlight = (selector: string, color = 'red') => {
    document.querySelectorAll(selector).forEach((el: Element) => {
      (el as HTMLElement).style.outline = `3px solid ${color}`;
      (el as HTMLElement).style.outlineOffset = '2px';
    });
  };

  // Helper para inspeccionar el estado de React/Next.js
  (window as any).getReactState = (el: Element) => {
    const fiber = Object.keys(el).find(k => k.startsWith('__reactFiber'));
    if (!fiber) return null;
    return (el as any)[fiber]?.memoizedState;
  };

  // Helper para limpiar todo en localStorage/sessionStorage
  (window as any).clearStorage = () => {
    localStorage.clear();
    sessionStorage.clear();
    console.log('✅ Storage limpiado');
  };

  // Helper para listar todas las cookies
  (window as any).listCookies = () => {
    return document.cookie.split(';').reduce((acc, cookie) => {
      const [key, val] = cookie.trim().split('=');
      acc[key] = decodeURIComponent(val);
      return acc;
    }, {} as Record<string, string>);
  };
});

// Ahora en tus tests puedes hacer:
await page.evaluate(() => (window as any).highlight('.button', 'cyan'));
```

## Locators de Playwright vs selectores clásicos

```typescript
// Playwright tiene su propio sistema de selectores que son más robustos

// Por texto (recomendado — el más legible)
page.getByText('Iniciar sesión')
page.getByText('Iniciar sesión', { exact: true })

// Por rol accesible (recomendado para componentes de UI)
page.getByRole('button', { name: 'Enviar' })
page.getByRole('textbox', { name: 'Email' })
page.getByRole('link', { name: 'Ver detalles' })

// Por label (para formularios)
page.getByLabel('Contraseña')

// Por placeholder
page.getByPlaceholder('Escribe tu email')

// Por test-id (el mejor para QA — no depende de texto visible)
page.getByTestId('submit-button')  // busca data-testid="submit-button"

// Por alt (imágenes)
page.getByAltText('Logo de la empresa')

// CSS clásico (evitar si es posible — frágil)
page.locator('.btn-primary')
page.locator('#submit')

// XPath (potente pero verboso)
page.locator('//button[contains(@class, "primary")]')

// Combinaciones
page.locator('.card').filter({ hasText: 'Producto A' }).getByRole('button')
page.locator('tr').filter({ has: page.locator('td', { hasText: 'Activo' }) })
```

---

<a name="dom"></a>
# 6. Manipulación del DOM desde Playwright

## Leer el estado del DOM

```typescript
// Texto de un elemento
const text = await page.locator('.title').textContent();
const innerHtml = await page.locator('.content').innerHTML();

// Atributos
const href = await page.locator('a.link').getAttribute('href');
const isDisabled = await page.locator('button').getAttribute('disabled') !== null;

// Propiedades CSS computadas
const color = await page.evaluate(() => {
  const el = document.querySelector('.title');
  return window.getComputedStyle(el!).color;
});

// Bounding box (posición y tamaño)
const box = await page.locator('.modal').boundingBox();
console.log(box); // { x, y, width, height }

// Visibilidad
const isVisible = await page.locator('.spinner').isVisible();
const isHidden = await page.locator('.modal').isHidden();

// Estado de inputs
const value = await page.locator('input[name="email"]').inputValue();
const isChecked = await page.locator('input[type="checkbox"]').isChecked();
const isEnabled = await page.locator('button[type="submit"]').isEnabled();
```

## Manipular localStorage y sessionStorage

```typescript
// Leer
const token = await page.evaluate(() => localStorage.getItem('authToken'));
const allKeys = await page.evaluate(() => Object.keys(localStorage));

// Escribir (útil para simular usuario ya logueado)
await page.evaluate(() => {
  localStorage.setItem('authToken', 'fake-token-for-test');
  localStorage.setItem('userId', '12345');
  sessionStorage.setItem('currentStep', '2');
});

// Limpiar
await page.evaluate(() => {
  localStorage.clear();
  sessionStorage.clear();
});

// Pattern pro: guardar storageState con Playwright (más robusto)
// Guarda cookies + localStorage + sessionStorage en un archivo
await page.context().storageState({ path: 'auth/user-state.json' });

// Y reusar en el siguiente test sin hacer login
const context = await browser.newContext({
  storageState: 'auth/user-state.json'
});
```

## Manipular cookies

```typescript
// Leer todas las cookies
const cookies = await page.context().cookies();
const authCookie = cookies.find(c => c.name === 'session_token');

// Añadir cookies (simular sesión activa sin pasar por login)
await page.context().addCookies([
  {
    name: 'session_token',
    value: 'test-session-12345',
    domain: 'localhost',
    path: '/',
    httpOnly: true,
    secure: false,
    expires: Date.now() / 1000 + 3600, // 1 hora
  },
]);

// Eliminar cookies
await page.context().clearCookies();

// Eliminar cookie específica
await page.context().clearCookies({ name: 'session_token' });
```

## Interacciones avanzadas con el teclado y ratón

```typescript
// Teclado — combinaciones
await page.keyboard.press('Control+A');    // seleccionar todo
await page.keyboard.press('Control+C');    // copiar
await page.keyboard.press('Control+V');    // pegar
await page.keyboard.press('Escape');
await page.keyboard.press('Enter');

// Teclas especiales en inputs
await page.locator('input').press('Tab'); // mueve el foco al siguiente campo

// Typing con delay (simula usuario real)
await page.locator('input').type('texto lento', { delay: 100 });

// vs fill (instantáneo, más rápido para tests)
await page.locator('input').fill('texto instantáneo');

// Ratón — control preciso
await page.mouse.move(100, 200);
await page.mouse.down();
await page.mouse.move(300, 200); // arrastra
await page.mouse.up();

// Drag and drop de alto nivel
await page.locator('.draggable').dragTo(page.locator('.dropzone'));

// Hover (para menús desplegables)
await page.locator('.menu-item').hover();
await page.waitForSelector('.dropdown', { state: 'visible' });

// Click con opciones
await page.locator('.button').click({
  button: 'right',         // click derecho
  modifiers: ['Control'],  // Ctrl+Click
  position: { x: 10, y: 5 }, // click en posición específica del elemento
  force: true,             // ignora que el elemento esté cubierto
  delay: 100,              // delay antes del click
});
```

---

<a name="network"></a>
# 7. Network Interception — Interceptar, Modificar, Mockear

Aquí está el oro. La capacidad de interceptar requests de red es lo que separa los tests básicos de los tests avanzados.

## Escuchar requests y responses

```typescript
// Escuchar todas las requests
page.on('request', request => {
  console.log(`→ ${request.method()} ${request.url()}`);
});

// Escuchar responses
page.on('response', response => {
  console.log(`← ${response.status()} ${response.url()}`);
});

// Escuchar fallos de red
page.on('requestfailed', request => {
  console.log(`✗ ${request.url()} - ${request.failure()?.errorText}`);
});

// Esperar una request específica
const [request] = await Promise.all([
  page.waitForRequest('**/api/users'),
  page.click('#load-users'),
]);

// Esperar una response específica
const [response] = await Promise.all([
  page.waitForResponse('**/api/users'),
  page.click('#load-users'),
]);

// Leer el body de la response
const data = await response.json();
const status = response.status();
const headers = response.headers();
```

## `page.route()` — el interceptor más potente

`page.route()` te permite interceptar las peticiones de red a nivel de navegador. Es extremadamente útil no solo para mockear, sino para inspeccionar (loggear) lo que la aplicación realmente envía y recibe.

### Debugging de requests/responses en vivo

Si necesitas ver exactamente qué payload se envía al servidor y qué devuelve, sin romper el flujo real de la prueba, puedes usar este patrón:

```typescript
await page.route('**/api/v1/data', async route => {
  const req = route.request();
  
  // 1. Vemos lo que se envía (El request)
  console.log(`[ENVIANDO] -> ${req.method()} ${req.url()}`, req.postDataJSON());
  
  // 2. Ejecutamos la petición real
  const response = await route.fetch();
  
  // 3. Vemos lo que se recibe (El response)
  console.log(`[RECIBIENDO] <- ${response.status()}`);
  
  // 4. Dejamos que el navegador continúe con la respuesta real
  await route.fulfill({ response });
});
```

```typescript
// Mockear una API completa
await page.route('**/api/products', async route => {
  await route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([
      { id: 1, name: 'Producto A', price: 99.99 },
      { id: 2, name: 'Producto B', price: 149.99 },
    ]),
  });
});

// Simular error de servidor
await page.route('**/api/checkout', async route => {
  await route.fulfill({
    status: 500,
    contentType: 'application/json',
    body: JSON.stringify({ error: 'Internal Server Error' }),
  });
});

// Simular timeout de red (sin respuesta)
await page.route('**/api/slow-endpoint', async route => {
  await new Promise(resolve => setTimeout(resolve, 30_000));
  await route.abort('timedout');
});

// Modificar la request antes de enviarla
await page.route('**/api/**', async route => {
  const request = route.request();

  // Añadir header a todas las requests de la API
  await route.continue({
    headers: {
      ...request.headers(),
      'x-test-mode': 'true',
      'Authorization': `Bearer ${process.env.TEST_API_TOKEN}`,
    },
  });
});

// Modificar la RESPONSE antes de que llegue al browser
await page.route('**/api/user/profile', async route => {
  const response = await route.fetch(); // hacer la request real
  const body = await response.json();

  // Modificar datos
  body.role = 'admin'; // simular usuario admin
  body.features.push('beta_feature');

  await route.fulfill({
    response,
    body: JSON.stringify(body),
  });
});

// Bloquear recursos innecesarios (acelera los tests)
await page.route('**/*.{png,jpg,jpeg,gif,svg,ico,woff,woff2}', route => {
  route.abort();
});
await page.route('**/{analytics,tracking,ads}/**', route => {
  route.abort();
});
```

## Patrón: HAR files — grabar y reproducir

```typescript
// Grabar todas las requests en un archivo HAR
await page.routeFromHAR('./fixtures/api-responses.har', {
  update: false, // false = usa el HAR existente. true = actualiza el HAR
});

// La primera vez (update: true), hace las requests reales y guarda las responses
// Las siguientes veces (update: false), sirve desde el archivo sin red

// Útil para: tests que dependen de APIs externas lentas o inestables
```

## Verificar que se hicieron las requests correctas

```typescript
test('debe enviar datos correctos al hacer checkout', async ({ page }) => {
  let capturedRequest: any = null;

  await page.route('**/api/checkout', async route => {
    const request = route.request();
    capturedRequest = await request.postDataJSON(); // captura el body

    await route.fulfill({
      status: 200,
      body: JSON.stringify({ orderId: 'test-123' }),
    });
  });

  // Realizar la acción
  await page.fill('[name="card"]', '4111111111111111');
  await page.click('#pay-button');

  // Verificar que se envió lo correcto
  expect(capturedRequest).toMatchObject({
    amount: 99.99,
    currency: 'EUR',
    cardLast4: '1111',
  });
});
```

---

<a name="seguridad"></a>
# 8. Autenticación y Seguridad

## Patrón óptimo: login una sola vez

```typescript
// tests/auth/auth.setup.ts
import { test as setup, expect } from '@playwright/test';

const authFile = 'auth/user-state.json';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', process.env.TEST_USER_EMAIL);
  await page.fill('[name="password"]', process.env.TEST_USER_PASSWORD);
  await page.click('[type="submit"]');

  // Esperar a que el login sea exitoso
  await expect(page).toHaveURL('/dashboard');

  // Guardar el estado de autenticación
  await page.context().storageState({ path: authFile });
});

// playwright.config.ts — usa el setup como dependencia
// projects: [{ name: 'chromium', dependencies: ['setup'] }]
// use: { storageState: 'auth/user-state.json' }
```

## Múltiples roles de usuario

```typescript
// tests/auth/admin.setup.ts
setup('authenticate as admin', async ({ page }) => {
  // login con credenciales de admin
  await page.context().storageState({ path: 'auth/admin-state.json' });
});

// En playwright.config.ts — proyecto separado para admin
{
  name: 'admin-tests',
  testMatch: '**/admin/**',
  use: { storageState: 'auth/admin-state.json' },
  dependencies: ['setup-admin'],
}
```

## Testing de seguridad — lo que un QA senior debe conocer

```typescript
// 1. XSS — Cross-Site Scripting
test('no debe ejecutar scripts inyectados en el input', async ({ page }) => {
  const xssPayload = '<script>window.__XSS_EXECUTED__ = true</script>';

  await page.fill('#search-input', xssPayload);
  await page.press('#search-input', 'Enter');

  // Verificar que el script NO se ejecutó
  const xssExecuted = await page.evaluate(() => (window as any).__XSS_EXECUTED__);
  expect(xssExecuted).toBeUndefined();

  // Verificar que el contenido se escapó correctamente
  const searchResult = await page.locator('.search-query').textContent();
  expect(searchResult).toContain(xssPayload); // debe mostrarse como texto, no ejecutarse
});

// 2. Open Redirect
test('no debe redirigir a URLs externas desde parámetros', async ({ page }) => {
  await page.goto('/login?redirect=https://malicious.com');
  await page.fill('[name="email"]', 'user@test.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('[type="submit"]');

  // No debe redirigir fuera del dominio
  await expect(page).toHaveURL(/^http:\/\/localhost/);
});

// 3. CSRF — verificar tokens
test('las requests POST deben incluir CSRF token', async ({ page }) => {
  let csrfFound = false;

  await page.route('**/api/**', async route => {
    const request = route.request();
    if (request.method() === 'POST') {
      const headers = request.headers();
      csrfFound = 'x-csrf-token' in headers || 'x-xsrf-token' in headers;
    }
    await route.continue();
  });

  await page.click('#submit-form');
  expect(csrfFound).toBeTruthy();
});

// 4. Headers de seguridad
test('debe incluir headers de seguridad', async ({ page }) => {
  const response = await page.goto('/');
  const headers = response!.headers();

  expect(headers['x-frame-options']).toBeTruthy();          // clickjacking
  expect(headers['x-content-type-options']).toBe('nosniff'); // MIME sniffing
  expect(headers['content-security-policy']).toBeTruthy();   // CSP
  expect(headers['strict-transport-security']).toBeTruthy(); // HSTS (en HTTPS)
});

// 5. Datos sensibles no deben aparecer en URLs
test('el token no debe aparecer en la URL', async ({ page }) => {
  await page.goto('/dashboard');
  const url = page.url();

  expect(url).not.toContain('token=');
  expect(url).not.toContain('password=');
  expect(url).not.toContain('api_key=');
});

// 6. Rate limiting básico
test('debe aplicar rate limiting en endpoints críticos', async ({ page }) => {
  const responses: number[] = [];

  // Hacer múltiples requests rápidas
  for (let i = 0; i < 20; i++) {
    const response = await page.request.post('/api/auth/login', {
      data: { email: 'test@test.com', password: 'wrong' }
    });
    responses.push(response.status());
  }

  // Esperar que al menos algunas devuelvan 429 (Too Many Requests)
  expect(responses).toContain(429);
});
```

## Bypass de autenticación para tests específicos

```typescript
// A veces necesitas acceder a páginas que requieren auth sin pasar por login
// Si el backend tiene un modo de test, úsalo

// Opción 1: Cookie de bypass (solo en entornos no-producción)
test.beforeEach(async ({ page }) => {
  await page.context().addCookies([{
    name: '__bypass_auth',
    value: process.env.TEST_BYPASS_SECRET!,
    domain: 'localhost',
    path: '/',
  }]);
});

// Opción 2: Header especial
test.beforeEach(async ({ page, context }) => {
  await context.setExtraHTTPHeaders({
    'x-test-user-id': '12345',
    'x-test-role': 'admin',
  });
});
```

---

<a name="fixtures"></a>
# 9. Fixtures Avanzados — El Patrón Que Lo Cambia Todo

Los fixtures son la característica más poderosa de Playwright que menos gente usa bien.

## Fixture básico

```typescript
// fixtures/index.ts
import { test as base, expect } from '@playwright/test';
import { LoginPage } from '@pages/LoginPage';
import { DashboardPage } from '@pages/DashboardPage';

// Define el tipo de tus fixtures
type MyFixtures = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  authenticatedPage: Page; // página ya autenticada
};

// Extiende el test base
export const test = base.extend<MyFixtures>({
  // Fixture simple: Page Object
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage); // 'use' es como yield — da el fixture al test
    // Código aquí = teardown (se ejecuta DESPUÉS del test)
  },

  // Fixture con setup: página autenticada lista para usar
  authenticatedPage: async ({ page }, use) => {
    // Setup
    await page.goto('/login');
    await page.fill('[name="email"]', process.env.TEST_USER_EMAIL!);
    await page.fill('[name="password"]', process.env.TEST_USER_PASSWORD!);
    await page.click('[type="submit"]');
    await page.waitForURL('/dashboard');

    await use(page); // el test recibe la página ya autenticada

    // Teardown (logout)
    await page.goto('/logout');
  },
});

export { expect };
```

## Fixtures con base de datos

```typescript
// fixtures/db.fixture.ts
import { test as base } from '@playwright/test';
import { Pool } from 'pg'; // o tu cliente de BD preferido

type DbFixtures = {
  db: Pool;
  testUser: { id: string; email: string; };
};

export const test = base.extend<DbFixtures>({
  db: async ({}, use) => {
    const pool = new Pool({ connectionString: process.env.DATABASE_URL });
    await use(pool);
    await pool.end(); // teardown: cierra la conexión
  },

  // Fixture que depende de otro fixture (db)
  testUser: async ({ db }, use) => {
    // Crear usuario de test en la BD
    const result = await db.query(
      `INSERT INTO users (email, role) VALUES ($1, $2) RETURNING id, email`,
      [`test-${Date.now()}@playwright.com`, 'user']
    );
    const user = result.rows[0];

    await use(user); // el test recibe el usuario creado

    // Teardown: eliminar el usuario después del test
    await db.query('DELETE FROM users WHERE id = $1', [user.id]);
  },
});
```

## Uso en los tests

```typescript
// tests/e2e/dashboard.spec.ts
import { test, expect } from '../fixtures'; // importa TUS fixtures, no los de Playwright

test('el usuario ve sus datos correctos', async ({ authenticatedPage, testUser }) => {
  // authenticatedPage ya está logueado
  // testUser ya fue creado en BD y se limpiará después

  await expect(authenticatedPage.locator('.user-email')).toHaveText(testUser.email);
});
```

## Worker fixtures — compartidos entre todos los tests del worker

```typescript
// Útil para operaciones costosas que no cambian entre tests
type WorkerFixtures = {
  sharedBrowser: Browser;
  sharedApiToken: string;
};

export const test = base.extend<{}, WorkerFixtures>({
  // scope: 'worker' = se crea una vez por worker, no por test
  sharedApiToken: [async ({}, use) => {
    // Obtener token una sola vez para todos los tests del worker
    const token = await fetchApiToken(process.env.API_KEY!);
    await use(token);
    // Este token es válido para todos los tests del worker
  }, { scope: 'worker' }],
});
```

---

<a name="tricks"></a>
# 10. Tricks Superchulos Que No Están en la Docs

## `test.step()` — Reportes Legibles (Estilo BDD) sin Cucumber

Si quieres que tus reportes HTML nativos de Playwright se lean como si estuvieran escritos en Gherkin por negocio, pero no quieres la complejidad de instalar y mantener Cucumber, **`test.step()`** es la respuesta.

Agrupa acciones lógicas en pasos. En el reporte final, estos pasos aparecerán colapsables y detallados.

```typescript
test('Proceso de checkout completo', async ({ page, cartPage, checkoutPage }) => {
  await test.step('1. Dado que el usuario tiene items en el carrito', async () => {
    await cartPage.navigate();
    await cartPage.addMockItems(2);
    await expect(cartPage.totalItems).toHaveText('2');
  });

  await test.step('2. Cuando procede al pago con tarjeta válida', async () => {
    await cartPage.clickCheckout();
    await checkoutPage.fillCreditCard('4242424242424242');
    await checkoutPage.submitOrder();
  });

  await test.step('3. Entonces ve la pantalla de confirmación', async () => {
    await expect(page.locator('.order-success')).toBeVisible();
  });
});
```
Esto transforma un test monolítico en una estructura auto-documentada.

---



## Truco 1: Soft assertions — no parar al primer error

```typescript
// Por defecto, un expect fallido para el test inmediatamente
// Con soft assertions, continúas y ves TODOS los errores al final

test('verifica múltiples condiciones', async ({ page }) => {
  await page.goto('/product/123');

  // Estos no paran el test aunque fallen
  await expect.soft(page.locator('h1')).toHaveText('Producto 123');
  await expect.soft(page.locator('.price')).toHaveText('99.99€');
  await expect.soft(page.locator('.stock')).toHaveText('En stock');
  await expect.soft(page.locator('.rating')).toHaveText('4.5');

  // Al final, si alguno falló, el test falla con TODOS los errores juntos
  // En vez de tener que correr 4 veces para ver los 4 fallos
});
```

## Truco 2: Interceptar logs de la consola del browser

```typescript
test('no debe haber errores en consola', async ({ page }) => {
  const consoleErrors: string[] = [];

  page.on('console', msg => {
    if (msg.type() === 'error') {
      consoleErrors.push(msg.text());
    }
  });

  // Capturar errores JavaScript no capturados
  page.on('pageerror', error => {
    consoleErrors.push(`JS Error: ${error.message}`);
  });

  await page.goto('/');
  await page.click('#load-data');
  await page.waitForTimeout(1000);

  expect(consoleErrors).toHaveLength(0);
});

// Versión avanzada: verificar que SE llaman ciertos logs
test('debe registrar el evento de compra en analytics', async ({ page }) => {
  const analyticsEvents: string[] = [];

  page.on('console', msg => {
    if (msg.text().includes('[Analytics]')) {
      analyticsEvents.push(msg.text());
    }
  });

  await page.click('#purchase-button');

  expect(analyticsEvents).toContain('[Analytics] purchase_complete');
});
```

## Truco 3: Simular condiciones de red

```typescript
// Simular conexión lenta (3G)
await page.context().setOffline(false);
// ↑ no tiene throttling nativo en Playwright, pero sí via CDP:

const client = await page.context().newCDPSession(page);
await client.send('Network.emulateNetworkConditions', {
  offline: false,
  downloadThroughput: 500 * 1024 / 8,  // 500 kbps
  uploadThroughput: 500 * 1024 / 8,
  latency: 200,                          // 200ms latencia
});

// Simular offline
await page.context().setOffline(true);
await page.click('#save-draft'); // debe funcionar offline si hay service worker
await page.context().setOffline(false);
```

## Truco 4: Geolocalización y permisos

```typescript
// Simular ubicación GPS
await page.context().grantPermissions(['geolocation']);
await page.context().setGeolocation({ latitude: 40.416775, longitude: -3.703790 }); // Madrid

// O por contexto al crearlo
const context = await browser.newContext({
  permissions: ['geolocation', 'notifications', 'clipboard-read', 'clipboard-write'],
  geolocation: { latitude: 40.416775, longitude: -3.703790 },
});

// Denegar permisos (para testar el flujo de "permiso denegado")
await page.context().clearPermissions();
```

## Truco 5: Screenshots creativos para debugging

```typescript
// Screenshot de elemento específico (no toda la página)
await page.locator('.error-modal').screenshot({ path: 'error-modal.png' });

// Screenshot con máscara (oculta datos sensibles)
await page.screenshot({
  path: 'dashboard.png',
  mask: [
    page.locator('.user-email'),
    page.locator('.credit-card'),
  ],
});

// Screenshot de página completa (scrollea)
await page.screenshot({ path: 'full-page.png', fullPage: true });

// Comparación visual (visual regression testing)
await expect(page).toHaveScreenshot('baseline.png', {
  maxDiffPixels: 50,
  threshold: 0.1,  // 10% de diferencia permitida
});
```

## Truco 6: Esperar condiciones custom

```typescript
// waitForFunction — espera hasta que una función en el browser devuelva truthy
await page.waitForFunction(() => {
  return document.querySelectorAll('.item').length > 10;
});

// Con timeout personalizado
await page.waitForFunction(
  (minItems) => document.querySelectorAll('.item').length >= minItems,
  50, // argumento pasado a la función
  { timeout: 10_000 }
);

// Esperar que una variable global cambie
await page.waitForFunction(() => {
  return (window as any).__DATA_LOADED__ === true;
});

// Esperar por URL con regex
await page.waitForURL(/\/dashboard\/.*\/settings/);

// Esperar que el DOM deje de cambiar (útil con animaciones)
await page.waitForLoadState('networkidle'); // ninguna request en 500ms
await page.waitForLoadState('domcontentloaded');
await page.waitForLoadState('load');
```

## Truco 7: CDP (Chrome DevTools Protocol) — acceso de bajo nivel

```typescript
// CDP te da acceso directo a las DevTools del Chrome
const client = await page.context().newCDPSession(page);

// Limpiar la caché del browser
await client.send('Network.clearBrowserCache');

// Interceptar requests a nivel de CDP (más control que page.route)
await client.send('Network.enable');
client.on('Network.responseReceived', (event) => {
  console.log(event.response.url, event.response.status);
});

// Tomar screenshots con calidad controlada
const { data } = await client.send('Page.captureScreenshot', {
  format: 'jpeg',
  quality: 80,
});

// Ejecutar en contextos aislados
await client.send('Runtime.evaluate', {
  expression: 'document.title',
  returnByValue: true,
});
```

## Truco 8: Tests de accesibilidad con Playwright

```typescript
// Instalar: npm install -D @axe-core/playwright
import AxeBuilder from '@axe-core/playwright';

test('página principal debe ser accesible', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .exclude('.third-party-widget') // excluir widgets externos
    .analyze();

  expect(results.violations).toEqual([]);
});

// Ver detalles de las violaciones
if (results.violations.length > 0) {
  console.table(results.violations.map(v => ({
    id: v.id,
    impact: v.impact,
    description: v.description,
    nodes: v.nodes.length,
  })));
}
```

## Truco 9: Testing de iframes

```typescript
// Los iframes son un mundo aparte — tienen su propio contexto de DOM
const frame = page.frameLocator('iframe[name="payment"]');

// Interactuar dentro del iframe exactamente igual que en la página principal
await frame.locator('#card-number').fill('4111111111111111');
await frame.locator('#expiry').fill('12/28');
await frame.locator('#cvc').fill('123');

// Múltiples iframes
const frames = page.frames();
const paymentFrame = frames.find(f => f.name() === 'payment');
```

## Truco 10: Emulación de dispositivos custom

```typescript
// Usar un dispositivo predefinido
const { chromium, devices } = require('@playwright/test');
const iPhone = devices['iPhone 14 Pro'];
const context = await browser.newContext({ ...iPhone });

// Crear tu propio perfil de dispositivo
const context = await browser.newContext({
  viewport: { width: 390, height: 844 },
  deviceScaleFactor: 3,
  isMobile: true,
  hasTouch: true,
  userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)...',
});

// Dark mode
const context = await browser.newContext({
  colorScheme: 'dark', // 'light' | 'dark' | 'no-preference'
  reducedMotion: 'reduce',
  forcedColors: 'active', // high contrast mode
});
```

---

<a name="herramientas"></a>
# 11. Herramientas del Arsenal

## Playwright Inspector — debugging en vivo

```bash
# Lanza el inspector visual
PWDEBUG=1 npx playwright test nombre-del-test.spec.ts

# O en el código
await page.pause(); // pausa el test y abre el inspector
```

El inspector te muestra:
- El DOM en tiempo real
- Los selectores sugeridos
- El log de acciones
- La posibilidad de ejecutar acciones manualmente

## UI Mode — el más chulo

```bash
npx playwright test --ui
```

Interfaz gráfica que muestra:
- Todos los tests con su estado
- Timeline de cada test con screenshots
- Network requests
- Console logs
- Trace integrado
- Re-run individual de tests

## Trace Viewer — post-mortem de fallos

```bash
# Ver un trace guardado
npx playwright show-trace test-results/nombre-test/trace.zip
```

El trace incluye:
- Cada acción con screenshot antes y después
- Network requests y responses
- Console logs
- DOM snapshots
- Timeline completo

## Codegen — el generador de código

```bash
# Genera código grabando tus acciones en el browser
npx playwright codegen http://localhost:3000

# Con opciones
npx playwright codegen --browser firefox --save-trace ./trace.zip http://localhost:3000
npx playwright codegen --save-storage ./auth.json http://localhost:3000  # guarda auth
```

**Tip:** El código generado es un buen punto de partida pero siempre necesita refactor. Úsalo para los selectores, no para la lógica del test.

## Allure Reporter — reportes profesionales

```bash
npm install -D allure-playwright allure-commandline
```

```typescript
// playwright.config.ts
reporter: [
  ['allure-playwright', {
    detail: true,
    outputFolder: 'allure-results',
    suiteTitle: false,
  }],
],
```

```typescript
// En los tests — añadir metadata a Allure
import { allure } from 'allure-playwright';

test('checkout completo', async ({ page }) => {
  allure.label('feature', 'Checkout');
  allure.label('severity', 'critical');
  allure.description('Verifica el flujo completo de compra');

  await allure.step('Añadir producto al carrito', async () => {
    await page.click('#add-to-cart');
  });

  await allure.step('Proceder al pago', async () => {
    await page.click('#checkout');
  });
});
```

```bash
# Generar y abrir el reporte
npx allure generate allure-results --clean -o allure-report
npx allure open allure-report
```

## Playwright Component Testing

```bash
# Para React/Vue/Svelte — monta componentes aislados
npm install -D @playwright/experimental-ct-react
```

```typescript
// tests/Button.spec.tsx
import { test, expect } from '@playwright/experimental-ct-react';
import { Button } from './Button';

test('button muestra el texto correcto', async ({ mount }) => {
  const component = await mount(<Button label="Comprar" disabled={false} />);
  await expect(component).toContainText('Comprar');
  await expect(component).toBeEnabled();
});
```

## Faker.js — datos de test realistas

```bash
npm install -D @faker-js/faker
```

```typescript
import { faker } from '@faker-js/faker';

// Datos de usuario realistas
const user = {
  name: faker.person.fullName(),
  email: faker.internet.email(),
  phone: faker.phone.number('+34 9## ### ###'),
  address: faker.location.streetAddress(),
  creditCard: faker.finance.creditCardNumber('visa'),
};

// Locale específico
faker.locale = 'es'; // nombres y direcciones en español
```

---

<a name="patrones"></a>
# 12. Patrones QA de Nivel Senior

## El Anti-Patrón (Anti-POM)

Antes de ver cómo se hace correctamente el POM, identifiquemos cómo **NO** hacerlo. Un "Anti-POM" típico expone los locators o los define directamente dentro de los métodos (repitiéndolos sin tregua), acopla lógica de configuración que no le pertenece, y mezcla aserciones de forma muy estricta, haciendo la clase rígida y casi imposible de escalar.

❌ **Ejemplo de un Anti-Patrón POM:**
```typescript
// ❌ MAL: Anti-Patrón de POM
import { Page, expect } from '@playwright/test';

export class BadLoginPage {
  page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  // Problema 1: Una función monstruosa que hace de todo
  async loginFlujoCompleto(user: string, pass: string) {
    // Problema 2: Selectores frágiles y hardcodeados "al vuelo" (CSS y XPath malos)
    await this.page.fill('//*[@id="login"]/div[1]/input', user);
    await this.page.fill('.password-field', pass);
    await this.page.click('button[type="submit"]');

    // Problema 3: Hardcodear tiempos (¡Pecado capital!)
    await this.page.waitForTimeout(2000);

    // Problema 4: Aserciones estrictas dentro de la función de acción (reduce la reusabilidad)
    await expect(this.page.locator('.welcome-msg')).toHaveText('Bienvenido');
  }
}
```

## Page Object Model (POM) bien hecho

### Arquitectura del POM en Playwright

El POM no es solo meter selectores en una clase. Su estructura es fundamental para escalar cualquier suite de automatización sin dolor de cabeza.

Una **Arquitectura de POM bien definida** tiene las siguientes capas:
1. **BasePage / Application Framework**: Una clase abstracta en la que centralizamos comportamientos compartidos para interactuar de forma segura con los componentes web y lidiar con flujos persistentes como esperas, clics seguros y evaluación de scripts en DOM. Esto sirve de fachada y nos desliga del driver si fuesen necesarios ciertos hacks globales.
2. **Page Objects Específicos**: Clases que heredan de BasePage. Encapsulan los *locators* de una vista, junto con métodos de interacción con significado de negocio (e.g., `login(user, pass)` en lugar de `fillUser`, `fillPass`, `clickSubmit`).
3. **Flujos / Tareas (Tasks o Assertions separados, opcional)**: En patrones más avanzados (como Screenplay), separamos aserciones e intenciones. Aquí, integramos comprobaciones sencillas pero siempre manteniendo nuestra API limpia.

La clave: **un Test NUNCA debería contener selectores CSS ni locators en los scripts E2E**. Solo debería leer como una receta ("Ir a login, ingresar con X, ver dashboard").

```typescript
// pages/BasePage.ts — clase base con métodos comunes
import { Page, Locator } from '@playwright/test';

export abstract class BasePage {
  protected page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  // Métodos comunes a todas las páginas
  async waitForPageLoad() {
    await this.page.waitForLoadState('networkidle');
  }

  async getTitle(): Promise<string> {
    return this.page.title();
  }

  async scrollToBottom() {
    await this.page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  }

  // Helper para esperar y hacer click de forma segura
  async safeClick(locator: Locator) {
    await locator.waitFor({ state: 'visible' });
    await locator.scrollIntoViewIfNeeded();
    await locator.click();
  }
}

// pages/LoginPage.ts
import { Page, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class LoginPage extends BasePage {
  // Locators como propiedades — definidos una vez, usados siempre
  readonly emailInput = this.page.getByLabel('Email');
  readonly passwordInput = this.page.getByLabel('Contraseña');
  readonly submitButton = this.page.getByRole('button', { name: 'Iniciar sesión' });
  readonly errorMessage = this.page.getByRole('alert');
  readonly forgotPasswordLink = this.page.getByText('¿Olvidaste tu contraseña?');

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async loginAndExpectSuccess(email: string, password: string) {
    await this.login(email, password);
    await expect(this.page).toHaveURL('/dashboard');
  }

  async loginAndExpectError(email: string, password: string, errorText: string) {
    await this.login(email, password);
    await expect(this.errorMessage).toContainText(errorText);
  }

  async isVisible(): Promise<boolean> {
    return this.emailInput.isVisible();
  }
}
```

## Patrón Builder para datos de test

```typescript
// utils/builders/user-builder.ts
import { faker } from '@faker-js/faker';

interface User {
  email: string;
  password: string;
  name: string;
  role: 'admin' | 'user' | 'guest';
  isVerified: boolean;
}

export class UserBuilder {
  private user: User = {
    email: faker.internet.email(),
    password: 'Test1234!',
    name: faker.person.fullName(),
    role: 'user',
    isVerified: true,
  };

  withEmail(email: string): this {
    this.user.email = email;
    return this;
  }

  withRole(role: User['role']): this {
    this.user.role = role;
    return this;
  }

  unverified(): this {
    this.user.isVerified = false;
    return this;
  }

  asAdmin(): this {
    this.user.role = 'admin';
    return this;
  }

  build(): User {
    return { ...this.user };
  }
}

// Uso
const adminUser = new UserBuilder().asAdmin().withEmail('admin@test.com').build();
const unverifiedUser = new UserBuilder().unverified().build();
const regularUser = new UserBuilder().build();
```

## Testing de API con Playwright

```typescript
// Playwright tiene un cliente HTTP integrado — no necesitas axios para tests de API
test('API: crear usuario devuelve 201', async ({ request }) => {
  const response = await request.post('/api/users', {
    data: {
      email: 'nuevo@test.com',
      name: 'Test User',
    },
    headers: {
      'Authorization': `Bearer ${process.env.API_TOKEN}`,
    },
  });

  expect(response.status()).toBe(201);

  const body = await response.json();
  expect(body).toMatchObject({
    email: 'nuevo@test.com',
    id: expect.any(String),
    createdAt: expect.any(String),
  });
});

// Test de API combinado con E2E — verificar que la UI refleja los datos de API
test('los datos de API se muestran en la UI', async ({ page, request }) => {
  // Crear dato via API
  const apiResponse = await request.post('/api/products', {
    data: { name: 'Producto Test', price: 99.99 },
  });
  const { id } = await apiResponse.json();

  // Verificar que aparece en la UI
  await page.goto('/products');
  await expect(page.locator(`[data-product-id="${id}"]`)).toBeVisible();
  await expect(page.locator(`[data-product-id="${id}"] .price`)).toHaveText('99.99€');

  // Cleanup via API
  await request.delete(`/api/products/${id}`);
});
```

## Manejo de condiciones de carrera

```typescript
// Anti-patrón: waitForTimeout (nunca uses esto en producción)
await page.waitForTimeout(2000); // ❌ frágil, lento

// Pro-patrón: esperar condiciones específicas
await page.waitForResponse('**/api/data'); // ✅ espera la response real
await page.waitForSelector('.data-loaded'); // ✅ espera el estado del DOM
await page.waitForFunction(() => document.readyState === 'complete'); // ✅ estado del browser

// Para operaciones asíncronas paralelas
const [_, response] = await Promise.all([
  page.click('#load-button'),           // acción que dispara la request
  page.waitForResponse('**/api/items'), // espera la response
]);

// Retry automático con expect (ya incluido en Playwright)
// Este código reintenta durante el timeout configurado
await expect(page.locator('.items')).toHaveCount(5);
// Si los items tardan en cargar, Playwright reintenta hasta que sean 5
```

## Organización de tests con tags y anotaciones

```typescript
// Anotaciones
test('checkout con tarjeta', {
  tag: ['@critical', '@payment', '@smoke'],
  annotation: [
    { type: 'issue', description: 'JIRA-1234' },
    { type: 'story', description: 'US-567' },
  ],
}, async ({ page }) => {
  // test...
});

// Ejecutar solo tests con cierto tag
// npx playwright test --grep "@smoke"
// npx playwright test --grep-invert "@slow"

// Skip tests en ciertos entornos
test('feature de admin', async ({ page }) => {
  test.skip(process.env.NODE_ENV === 'production', 'No correr en prod');
  // test...
});

// Test solo en cierto navegador
test('feature de webkit', async ({ page, browserName }) => {
  test.skip(browserName !== 'webkit', 'Solo para Safari');
  // test...
});

// Marcar test como fallando (se documenta el bug sin bloquear CI)
test('bug conocido JIRA-999', async ({ page }) => {
  test.fail(true, 'Bug abierto en JIRA-999 - se arregla en sprint 42');
  // el test falla, pero CI lo marca como "expected failure"
});
```

---

<a name="cucumber"></a>
# 13. Integración con Cucumber y Gherkin — BDD con Sentido

Playwright Test runner es brutal, pero a veces nuestro negocio o equipo nos exige hablar en **Gherkin**. Añadir la capa de BDD (Behavior-Driven Development) usando **Cucumber** nos permite que QA, Product Owners y Devs tengan una "fuente de la verdad única" sin sacrificar el poder de Playwright.

## ¿Por qué Cucumber con Sentido?

Gherkin permite documentar y testear que el código no solo cumple con las especificaciones técnicas sino con el modelo de negocio. Hacer BDD "Con Sentido" significa: **no intentes mapear Gherkin 1:1 a acciones manuales o clics en la web**. ¡No hagas sentencias imperativas de bajo nivel!

❌ **Anti-patrón (Imperativo):**
```gherkin
Given I navigate to "/login"
And I fill in "#email" with "admin@empresa.com"
And I fill in "#password" with "123456"
And I click the "Login" button
Then I should see an element with class ".dashboard-title"
```

✅ **Lo correcto (Declarativo basado en comportamiento):**
```gherkin
Given un usuario con rol "Administrador" necesita acceder a la plataforma
When intenta iniciar sesión con credenciales válidas
Then es redirigido a su "Dashboard Principal"
```

## Setup e Instalación

Antes de escribir un solo step necesitas instalar el stack completo. Esta es la combinación probada:

```bash
npm install --save-dev @cucumber/cucumber @playwright/test ts-node
```

Y si quieres reportes HTML nativos de Cucumber:

```bash
npm install --save-dev @cucumber/html-formatter
```

El `package.json` debe tener al menos estos scripts:

```json
{
  "scripts": {
    "test":        "cucumber-js",
    "test:smoke":  "cucumber-js --profile smoke",
    "test:ci":     "cucumber-js --profile ci",
    "test:debug":  "cucumber-js --profile debug"
  }
}
```

### `tsconfig.json` — ajustes para convivir con Cucumber

Cucumber carga los steps con `ts-node`. Añade o ajusta estas opciones:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "strict": true,
    "baseUrl": ".",
    "paths": {
      "@pages/*":  ["pages/*"],
      "@steps/*":  ["steps/*"],
      "@support/*": ["support/*"]
    }
  },
  "ts-node": {
    "transpileOnly": true
  },
  "include": ["**/*.ts"],
  "exclude": ["node_modules"]
}
```

`transpileOnly: true` en `ts-node` es importante: omite el chequeo de tipos en runtime y hace que Cucumber arranque mucho más rápido. Los tipos los sigue verificando tu IDE y tu pipeline de build, no el runner.

## Arquitectura de la Capa Cucumber

Para trabajar correctamente con Playwright y Cucumber, la estructura recomendada separa BDD, step definitions y el modelo de páginas (POM):

```text
proyecto_bdd/
├── features/
│   ├── login.feature              ← Gherkin puro (El QUÉ)
│   └── checkout.feature
├── steps/
│   ├── world.ts                   ← Contexto global tipado (CustomWorld)
│   ├── hooks.ts                   ← Ciclo de vida de Playwright
│   ├── login.steps.ts             ← Steps de autenticación
│   └── checkout.steps.ts
├── pages/                         ← Tu POM (El CÓMO)
│   ├── LoginPage.ts
│   └── CheckoutPage.ts
├── support/
│   └── api.client.ts              ← Cliente HTTP reutilizable
├── cucumber.js                    ← Perfiles y configuración del runner
└── tsconfig.json
```

## 1. El Feature (Gherkin avanzado)

### Scenario básico

```gherkin
Feature: Autenticación de Usuarios

  Scenario: Un usuario administrador inicia sesión
    Given el usuario navega a la página de login
    When ingresa credenciales válidas de "Administrador"
    Then es redirigido correctamente al Dashboard
```

### Background — pasos compartidos en el feature

`Background` se ejecuta antes de cada `Scenario` del mismo feature. Úsalo para el setup que comparten todos los escenarios, no para lógica de negocio compleja.

```gherkin
Feature: Gestión de Carrito

  Background:
    Given el usuario ha iniciado sesión como "Cliente"
    And está en la página de productos

  Scenario: Añadir un producto al carrito
    When selecciona el producto "Zapatillas Pro"
    Then el carrito muestra 1 artículo

  Scenario: Vaciar el carrito
    Given ha añadido 3 productos
    When vacía el carrito
    Then el carrito muestra 0 artículos
```

### Scenario Outline — escenarios parametrizados

Cuando el mismo flujo debe probarse con distintos datos, `Scenario Outline` + `Examples` evita duplicar escenarios. Es el equivalente en Gherkin a los `@DataProvider` de TestNG o los `test.each` de Jest.

```gherkin
Feature: Validación de login

  Scenario Outline: Inicio de sesión con distintos roles
    Given el usuario navega a la página de login
    When ingresa credenciales del rol "<rol>"
    Then es redirigido a "<destino>"
    And el menú lateral muestra la sección "<seccion>"

    Examples:
      | rol           | destino              | seccion         |
      | Administrador | /admin/dashboard     | Gestión usuarios|
      | Cliente       | /home                | Mis pedidos     |
      | Auditor       | /reports             | Informes        |
```

Cucumber instancia un `Scenario` independiente por cada fila de `Examples`. Cada uno corre aislado con su propio `Before`/`After`.

### Data Tables — datos estructurados en un step

Cuando un step recibe una tabla de datos (no un simple valor), usa `DataTable`:

```gherkin
Scenario: Crear un usuario con datos completos
  Given existe un usuario con los siguientes datos:
    | campo     | valor              |
    | nombre    | Ana García         |
    | email     | ana@test.com       |
    | rol       | Editor             |
    | activo    | true               |
  Then el usuario aparece en el listado de administración
```

```typescript
// steps/users.steps.ts
import { Given } from '@cucumber/cucumber';
import { DataTable } from '@cucumber/cucumber';

Given('existe un usuario con los siguientes datos:', async function (table: DataTable) {
  const data = table.rowsHash(); // { campo: valor, ... }
  console.log('[users.steps] Creando usuario:', data);
  // data.nombre → "Ana García", data.email → "ana@test.com"
  await this.page.goto('/admin/users/new');
  await this.page.fill('#nombre', data['nombre']);
  await this.page.fill('#email', data['email']);
  await this.page.selectOption('#rol', data['rol']);
  await this.page.click('[type="submit"]');
});
```

## 2. Los Step Definitions (El Puente)

A diferencia del runner nativo de Playwright (que inyecta `page` como fixture), en Cucumber `page` vive en `this` — el `CustomWorld` que configuramos más adelante.

```typescript
// steps/login.steps.ts
import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import { LoginPage } from '@pages/LoginPage';

Given('el usuario navega a la página de login', async function () {
  const loginPage = new LoginPage(this.page);
  await loginPage.goto();
});

When('ingresa credenciales válidas de {string}', async function (userType: string) {
  const loginPage = new LoginPage(this.page);

  const userMap: Record<string, { email: string; pass: string }> = {
    Administrador: { email: 'admin@test.com', pass: 'Admin123!' },
    Cliente:       { email: 'user@test.com',  pass: 'User123!'  },
    Auditor:       { email: 'audit@test.com', pass: 'Audit123!' },
  };

  const credentials = userMap[userType];
  if (!credentials) throw new Error(`Rol desconocido: ${userType}`);

  await loginPage.login(credentials.email, credentials.pass);
});

Then('es redirigido correctamente al Dashboard', async function () {
  await expect(this.page).toHaveURL(/.*dashboard/);
});
```

## 3. El CustomWorld — Tipado correcto en TypeScript

El `World` es el objeto `this` disponible en todos los steps y hooks de un mismo escenario. El problema con TypeScript: si no lo tipas bien, `this.page` da error de compilación.

La solución es declarar el tipo del World y exportarlo para que los steps lo consuman:

```typescript
// steps/world.ts
import { setWorldConstructor, World, IWorldOptions } from '@cucumber/cucumber';
import { Browser, BrowserContext, Page, APIRequestContext } from '@playwright/test';

export interface ICustomWorld extends World {
  browser:    Browser;
  context:    BrowserContext;
  page:       Page;
  apiRequest: APIRequestContext;
  testData:   Record<string, unknown>;  // bolsillo para datos entre steps
}

class CustomWorld extends World implements ICustomWorld {
  browser!:    Browser;
  context!:    BrowserContext;
  page!:       Page;
  apiRequest!: APIRequestContext;
  testData:    Record<string, unknown> = {};

  constructor(options: IWorldOptions) {
    super(options);
  }
}

setWorldConstructor(CustomWorld);
```

Ahora en cada step file importas la interfaz y tipas `this`:

```typescript
// steps/login.steps.ts
import { Given, When, Then, IWorld } from '@cucumber/cucumber';
import { ICustomWorld } from './world';

Given('el usuario navega a la página de login', async function (this: ICustomWorld) {
  await this.page.goto('/login');
});
```

## 4. Hooks — El ciclo de vida completo

Los hooks de Cucumber gestionan el ciclo de vida de cada escenario. La regla de oro: **todo lo que levanta Playwright va aquí, nunca en los steps**.

```typescript
// steps/hooks.ts
import {
  Before, After,
  BeforeAll, AfterAll,
  BeforeStep, AfterStep,
  Status,
} from '@cucumber/cucumber';
import { chromium, Browser, request } from '@playwright/test';
import { ICustomWorld } from './world';

// ─── BeforeAll: una sola vez por toda la ejecución ────────────────────────────
let browser: Browser;

BeforeAll(async function () {
  browser = await chromium.launch({
    headless: process.env.HEADLESS !== 'false',
  });
  console.log('[hooks] Browser iniciado');
});

// ─── Before: una vez por escenario ───────────────────────────────────────────
Before(async function (this: ICustomWorld) {
  this.context = await browser.newContext({
    baseURL:     process.env.BASE_URL ?? 'http://localhost:3000',
    locale:      'es-ES',
    timezoneId:  'Europe/Madrid',
    recordVideo: { dir: 'test-results/videos' },
  });
  this.page = await this.context.newPage();

  // Cliente de API disponible en todos los steps vía this.apiRequest
  this.apiRequest = await request.newContext({
    baseURL:     process.env.API_URL ?? 'http://localhost:3001',
    extraHTTPHeaders: {
      Authorization: `Bearer ${process.env.API_TOKEN ?? ''}`,
    },
  });
});

// ─── Before con tag: solo para escenarios @auth ───────────────────────────────
Before({ tags: '@auth' }, async function (this: ICustomWorld) {
  // Pre-autentica vía API para no pasar por el flujo de login en cada escenario
  const res = await this.apiRequest.post('/auth/login', {
    data: { email: 'admin@test.com', password: 'Admin123!' },
  });
  const { token } = await res.json();
  await this.context.addCookies([
    { name: 'auth_token', value: token, domain: 'localhost', path: '/' },
  ]);
  console.log('[hooks] @auth — token de sesión inyectado');
});

// ─── BeforeStep: antes de cada step individual ────────────────────────────────
BeforeStep(async function (this: ICustomWorld) {
  // Útil para screenshots o logging por step en modo debug
  // En producción déjalo vacío o elimínalo — añade overhead
});

// ─── AfterStep: después de cada step ─────────────────────────────────────────
AfterStep(async function (this: ICustomWorld, { result }) {
  if (result?.status === Status.FAILED) {
    const screenshot = await this.page.screenshot({ fullPage: true });
    this.attach(screenshot, 'image/png'); // aparece en el reporte HTML
    console.error('[hooks] Step fallido — screenshot adjunto al reporte');
  }
});

// ─── After: al cerrar cada escenario ─────────────────────────────────────────
After(async function (this: ICustomWorld, { result }) {
  if (result?.status === Status.FAILED) {
    // Video ya se guarda solo por recordVideo en el context
    // Adjuntamos también el HTML de la página para post-mortem
    const html = await this.page.content();
    this.attach(html, 'text/html');
  }

  // Ejemplo: Atachar respuestas API al reporte de Cucumber (Estilo Karate)
  // Si en tu test guardaste un payload JSON en this.testData['lastResponse'], 
  // puedes inyectarlo al HTML report así:
  if (this.testData['lastResponse']) {
    this.attach(JSON.stringify(this.testData['lastResponse'], null, 2), 'application/json');
  }

  await this.apiRequest.dispose();
  await this.page.close();
  await this.context.close();
});

// ─── AfterAll: una sola vez al terminar todo ──────────────────────────────────
AfterAll(async function () {
  await browser.close();
  console.log('[hooks] Browser cerrado');
});
```

### Hooks con tags — ejecución condicional

Los hooks pueden filtrarse por tags de Gherkin. Solo se ejecutan si el escenario tiene la etiqueta indicada:

```typescript
// Solo para escenarios marcados con @mobile
Before({ tags: '@mobile' }, async function (this: ICustomWorld) {
  await this.context.close();
  this.context = await browser.newContext({
    ...devices['iPhone 13'],
    baseURL: process.env.BASE_URL,
  });
  this.page = await this.context.newPage();
});

// Solo para escenarios @slow — aumenta timeouts
Before({ tags: '@slow' }, function (this: ICustomWorld) {
  this.page.setDefaultTimeout(60_000);
});
```

## 5. Profiles — `cucumber.js`

Los perfiles son la forma de tener configuraciones distintas para distintos contextos (local, CI, smoke, debug) sin duplicar scripts en `package.json`. Un solo `cucumber.js` lo gestiona todo.

```javascript
// cucumber.js
const common = [
  'features/**/*.feature',
  '--require-module ts-node/register',
  '--require steps/**/*.ts',
  '--format progress-bar',
  '--format @cucumber/pretty-formatter',
].join(' ');

module.exports = {
  // ── default ───────────────────────────────────────────────────────────────
  // Se usa cuando corres `cucumber-js` sin --profile
  default: [
    common,
    '--format html:test-results/cucumber-report.html',
    '--format json:test-results/cucumber-report.json',
  ].join(' '),

  // ── smoke ─────────────────────────────────────────────────────────────────
  // Solo escenarios críticos: `npm run test:smoke`
  smoke: [
    common,
    '--tags @smoke',
    '--format html:test-results/smoke-report.html',
  ].join(' '),

  // ── regression ────────────────────────────────────────────────────────────
  // Todos los escenarios excepto los marcados @wip
  regression: [
    common,
    '--tags "not @wip"',
    '--parallel 4',
    '--format html:test-results/regression-report.html',
    '--format json:test-results/regression-report.json',
  ].join(' '),

  // ── ci ────────────────────────────────────────────────────────────────────
  // Sin colores, sin interactividad, formato JSON para el pipeline
  ci: [
    common,
    '--tags "not @wip"',
    '--parallel 4',
    '--format json:test-results/ci-report.json',
    '--format junit:test-results/junit.xml',
  ].join(' '),

  // ── debug ─────────────────────────────────────────────────────────────────
  // Browser visible, un solo worker, verbose
  debug: [
    common,
    '--tags @debug',
    '--format @cucumber/pretty-formatter',
  ].join(' '),
};
```

Con esto los comandos quedan limpios:

```bash
npm test                  # todos los escenarios, reporte HTML
npm run test:smoke        # solo @smoke
npx cucumber-js --profile regression   # paralelo, sin @wip
npx cucumber-js --profile ci           # para GitHub Actions / Jenkins
npx cucumber-js --profile debug        # un escenario, browser visible
```

### Variables de entorno por perfil

Combina los perfiles con `dotenv` para manejar entornos:

```javascript
// cucumber.js
require('dotenv').config({
  path: `.env.${process.env.TEST_ENV ?? 'local'}`,
});
```

```bash
TEST_ENV=staging npm test          # carga .env.staging
TEST_ENV=production npm test:smoke # carga .env.production
```

## 6. Tags — Organizar y filtrar escenarios

Los tags en Gherkin son la forma de agrupar escenarios por tipo, entorno, prioridad o estado. Se definen con `@` y se pueden aplicar a nivel de `Feature`, `Scenario` o `Scenario Outline`.

```gherkin
@smoke @auth
Feature: Autenticación de Usuarios

  @critical
  Scenario: Login de administrador
    Given ...

  @wip
  Scenario: Login con SSO (en desarrollo)
    Given ...

  @mobile @regression
  Scenario Outline: Login en dispositivos móviles
    Given ...
    Examples:
      | dispositivo |
      | iPhone 13   |
      | Pixel 5     |
```

Filtrar por tags en la línea de comandos:

```bash
# Solo @smoke
npx cucumber-js --tags @smoke

# @smoke Y @auth (ambos obligatorios)
npx cucumber-js --tags "@smoke and @auth"

# @smoke O @critical
npx cucumber-js --tags "@smoke or @critical"

# Todo excepto @wip
npx cucumber-js --tags "not @wip"

# @regression pero no @mobile
npx cucumber-js --tags "@regression and not @mobile"
```

## 7. Debugging de requests API con `console.log`

Cuando un step hace llamadas HTTP (ya sea con `this.apiRequest` o con `fetch` dentro de `page.evaluate`), es crítico poder ver exactamente qué se envía y qué se recibe. El patrón es envolver las llamadas en un helper que loguea request y response:

### Helper de API con logging

```typescript
// support/api.client.ts
import { APIRequestContext } from '@playwright/test';

interface RequestLog {
  method: string;
  url: string;
  body?: unknown;
}

export async function apiPost(
  request: APIRequestContext,
  url: string,
  body: unknown,
): Promise<unknown> {
  const log: RequestLog = { method: 'POST', url, body };
  console.log('[API →]', JSON.stringify(log, null, 2));

  const response = await request.post(url, { data: body });
  const responseBody = await response.json().catch(() => null);

  console.log('[API ←]', JSON.stringify({
    status: response.status(),
    ok:     response.ok(),
    body:   responseBody,
  }, null, 2));

  if (!response.ok()) {
    throw new Error(`API ${log.method} ${url} falló con ${response.status()}`);
  }

  return responseBody;
}

export async function apiGet(
  request: APIRequestContext,
  url: string,
): Promise<unknown> {
  console.log('[API →] GET', url);

  const response = await request.get(url);
  const responseBody = await response.json().catch(() => null);

  console.log('[API ←]', JSON.stringify({
    status: response.status(),
    body:   responseBody,
  }, null, 2));

  return responseBody;
}
```

### Uso en los steps

```typescript
// steps/orders.steps.ts
import { When, Then } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import { ICustomWorld } from './world';
import { apiPost, apiGet } from '@support/api.client';

When('crea un pedido con {int} unidades de {string}',
  async function (this: ICustomWorld, quantity: number, product: string) {
    const payload = { product, quantity, userId: this.testData['userId'] };

    // Consola mostrará la request y la response completas
    const order = await apiPost(this.apiRequest, '/api/orders', payload);
    this.testData['orderId'] = (order as any).id;
  }
);

Then('el pedido aparece en el historial del usuario', async function (this: ICustomWorld) {
  const orders = await apiGet(
    this.apiRequest,
    `/api/users/${this.testData['userId']}/orders`,
  );
  const list = orders as any[];
  expect(list.some(o => o.id === this.testData['orderId'])).toBe(true);
});
```

Output en consola durante la ejecución:

```
[API →] {
  "method": "POST",
  "url": "/api/orders",
  "body": { "product": "Zapatillas Pro", "quantity": 2, "userId": "usr_42" }
}
[API ←] {
  "status": 201,
  "ok": true,
  "body": { "id": "ord_99", "status": "pending", "total": 129.90 }
}
```

### Logging de requests de red del browser

Si necesitas ver las requests que lanza el browser (no las de tu código Node), úsalo en los hooks:

```typescript
// steps/hooks.ts — dentro del Before
Before(async function (this: ICustomWorld) {
  this.context = await browser.newContext({ ... });
  this.page    = await this.context.newPage();

  // Log de cada request que sale del browser
  this.page.on('request', req => {
    if (req.url().includes('/api/')) {
      console.log('[browser →]', req.method(), req.url());
      const body = req.postData();
      if (body) console.log('[browser → body]', body);
    }
  });

  // Log de cada response que recibe el browser
  this.page.on('response', res => {
    if (res.url().includes('/api/')) {
      console.log('[browser ←]', res.status(), res.url());
    }
  });
});
```

## 8. Cómo ejecutar los tests

### Con `npm`

```bash
# Todos los escenarios (perfil default)
npm test

# Perfil específico
npm run test:smoke
npm run test:ci

# Pasando variables de entorno
TEST_ENV=staging npm test
HEADLESS=false npm test        # browser visible
```

### Con `npx cucumber-js` directamente

```bash
# Un feature específico
npx cucumber-js features/login.feature

# Un escenario por nombre (regex)
npx cucumber-js --name "administrador inicia sesión"

# Con tag y perfil
npx cucumber-js --profile regression --tags "@smoke and not @wip"

# Paralelo manual
npx cucumber-js --parallel 4

# Verbose — muestra cada step
npx cucumber-js --format @cucumber/pretty-formatter
```

### ¿Playwright Test runner o Cucumber runner?

Esta es la pregunta que más confunde al integrar ambas herramientas. La respuesta corta: **Depende de tu audiencia y de la fase del proyecto**, pero la mejor práctica en proyectos mixtos es mantenerlos separados y orquestarlos vía `npm scripts`.

| Situación | Usa |
|---|---|
| Tests técnicos, componentes, integración | Playwright Test (`npx playwright test`) |
| Escenarios BDD con stakeholders no técnicos | Cucumber (`npx cucumber-js`) |
| Ambos en el mismo proyecto | Scripts separados en `package.json` |

**No los mezcles en la misma ejecución.** Playwright Test y Cucumber son runners independientes. Playwright puede estar presente como librería (para `chromium`, `Page`, etc.) sin que uses su runner. El `cucumber-js` es el que orquesta los escenarios Gherkin. La mejor opción arquitectónica es centralizar toda la ejecución en comandos de Node estándar:

```json
{
  "scripts": {
    "test:unit":       "npx playwright test tests/unit/",
    "test:integration":"npx playwright test tests/integration/",
    "test:bdd":        "cucumber-js",
    "test:bdd:smoke":  "cucumber-js --profile smoke",
    "test:all":        "npm run test:unit && npm run test:bdd"
  }
}
```

## 9. Buenas prácticas — Cucumber + Playwright + Node

**El mundo está en el World, los clics están en el POM, el negocio está en el Gherkin.**

Cada capa tiene una responsabilidad fija. Cuando un step se vuelve largo, es señal de que algo del POM está filtrándose hacia arriba.

### Lo que va en cada capa

| Capa | Contiene | No contiene |
|---|---|---|
| `.feature` | comportamiento de negocio en lenguaje natural | selectores, URLs, datos técnicos |
| `steps/*.ts` | traducción Gherkin → POM | lógica de UI, waits, clics directos |
| `pages/*.ts` | acciones de UI, locators, waits | assertions de negocio |
| `hooks.ts` | setup/teardown de Playwright | lógica de test |
| `world.ts` | estado compartido entre steps | lógica de negocio |

### Steps reutilizables

Un step bien escrito se puede reutilizar en múltiples features sin modificarlo:

```typescript
// ✅ Genérico y reutilizable
Given('el usuario {string} ha iniciado sesión', async function (role: string) { ... });
When('navega a la sección {string}', async function (section: string) { ... });
Then('ve el mensaje {string}', async function (message: string) { ... });

// ❌ Acoplado a un feature específico
Given('el administrador ha iniciado sesión y está en el panel de control', ...);
```

### Un contexto de browser por escenario

Nunca compartas `page` ni `context` entre escenarios. El `Before`/`After` en `hooks.ts` garantiza que cada escenario empiece limpio — sin cookies, sin storage, sin estado de sesión residual.

### Datos de test en `testData`, no en variables globales

```typescript
// ✅ Estado en el World — aislado por escenario
this.testData['orderId'] = createdOrder.id;

// ❌ Variable módulo — se filtra entre escenarios en ejecución paralela
let orderId: string;
```

### Tags como documentación, no solo como filtros

Los tags bien elegidos documentan la suite:

```gherkin
@smoke          → escenario crítico, debe pasar siempre
@regression     → suite completa
@wip            → en desarrollo, excluido de CI
@slow           → tarda más de 30s, excluido de feedback rápido
@mobile         → requiere emulación de dispositivo
@api            → valida contrato de API, no UI
@destructivo    → modifica datos reales, solo en entorno aislado
```

### Nunca `page.waitForTimeout()` en los steps

Si un step necesita un `waitForTimeout` fijo, es una señal de que el POM no está esperando el estado correcto. Usa `waitForSelector`, `waitForURL` o `waitForResponse` en el POM.

```typescript
// ❌ Anti-patrón — frágil y lento
await this.page.waitForTimeout(2000);

// ✅ Espera el estado real
await this.page.waitForURL(/.*dashboard/);
await this.page.waitForSelector('[data-testid="dashboard-loaded"]');
```

---

<a name="glosario"></a>
# 14. CI/CD a Gran Escala — Sharding y Merge Reports

Correr 100 tests localmente toma 2 minutos. Correr 5,000 tests E2E reales en un pipeline puede tomar horas. La solución profesional no es optimizar selectores, es **escalar horizontalmente**.

Playwright tiene soporte nativo para fragmentar (shard) una suite de tests.

## `--shard` en GitHub Actions

En lugar de correr un job largo, levantas 10 runners paralelos. Cada runner corre un 10% de los tests.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        shardIndex: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        shardTotal: [10]
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
    - run: npm ci
    - run: npx playwright install --with-deps
    
    # Corre solo 1 décima parte de la suite
    - run: npx playwright test --shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }}
    
    # Sube el blob del reporte de este fragmento
    - uses: actions/upload-artifact@v4
      with:
        name: blob-report-${{ matrix.shardIndex }}
        path: blob-report
        retention-days: 1
```

## `merge-reports`

Luego de que los 10 jobs terminen, usas un job final que descarga todos los blobs (fragmentos de reporte) y los unifica en un solo reporte HTML gigante, como si los 5,000 tests hubieran corrido en una sola máquina superpotente.

```bash
npx playwright merge-reports --reporter html ./all-blob-reports
```
Esto reduce el tiempo de pipeline de horas a los minutos que tarde el test más largo.

---

# 15. El Futuro del QA — Self-Healing Locators con IA

Como hemos visto en los libros de *Gemini Uso Maestro* y *Claude*, la IA no viene a reemplazar al tester, viene a darle superpoderes.
El mayor dolor del QA tradicional es el mantenimiento: un desarrollador cambia `<button class="btn-primary">` a `<button class="btn-submit">` y todo el pipeline rojo.

En 2026, construimos **Self-Healing Fixtures**.

En lugar de fallar inmediatamente ante un `TimeoutError`, el fixture captura el error, extrae el DOM de la página, se lo envía a una IA (Gemini, Claude o un modelo local en Ollama) y le pregunta: *"El botón que buscaba con el selector '.btn-primary' ya no existe. Analiza este DOM y dime el nuevo selector CSS."*

### Concepto de Fixture de Auto-Recuperación

```typescript
// Pseudocódigo arquitectónico del futuro
export const test = base.extend({
  smartPage: async ({ page }, use) => {
    const smartClick = async (selector: string) => {
      try {
        await page.click(selector, { timeout: 3000 });
      } catch (error) {
        if (error.name === 'TimeoutError') {
          console.log(`[AI] Selector roto: ${selector}. Pidiendo ayuda a Gemini...`);
          const domSnapshot = await page.evaluate(() => document.body.innerHTML);
          
          // Llamada a la API de tu LLM (gemini-2.5-flash)
          const newSelector = await askAIForNewSelector(domSnapshot, selector);
          
          console.log(`[AI] Nuevo selector encontrado: ${newSelector}. Reintentando...`);
          await page.click(newSelector);
          
          // BONUS: Reportar automáticamente el cambio a Slack/Jira para arreglar el POM
          await reportBrokenLocatorToDevs(selector, newSelector);
        } else {
          throw error;
        }
      }
    };
    
    await use({ ...page, smartClick });
  }
});
```

Este es el santo grial de la automatización. Playwright + TypeScript proporcionan la infraestructura robusta; la IA proporciona la adaptabilidad.

---

<a name="glosario"></a>
# 16. Glosario de Referencia Rápida


| Término | Qué es |
|---------|--------|
| **CDP** | Chrome DevTools Protocol — API de bajo nivel para controlar Chrome |
| **Context** | Contexto de navegador: cookies, storage, permisos aislados. Equivale a un perfil de usuario. |
| **evaluate()** | Ejecuta JS en el browser desde Node |
| **evaluateHandle()** | Como evaluate() pero devuelve una referencia DOM sin serializar |
| **Fixture** | Setup/teardown reutilizable que se inyecta en los tests |
| **Frame** | Iframe — contexto de DOM aislado dentro de la página |
| **globalThis** | Objeto global universal (Node y Browser) |
| **HAR** | HTTP Archive — formato para grabar/reproducir requests de red |
| **Headless** | Browser sin interfaz visual (más rápido, para CI) |
| **Headed** | Browser con interfaz visual (para debugging) |
| **Locator** | Selector "vivo" de Playwright — siempre busca en el DOM actual |
| **Page** | Una pestaña del navegador |
| **POM** | Page Object Model — patrón de diseño para organizar tests |
| **route()** | Intercepta/modifica/mockea requests de red |
| **Soft assertion** | expect.soft() — no para el test si falla |
| **StorageState** | Snapshot de cookies + localStorage/sessionStorage |
| **Trace** | Grabación completa de un test (acciones + screenshots + network) |
| **Worker** | Proceso paralelo que ejecuta tests |
| **addInitScript()** | Inyecta JS que corre antes de cualquier script de la página |
| **waitForFunction()** | Espera hasta que una condición en el browser sea verdadera |

---

# Coda — La Mentalidad del QA con Playwright

Playwright no es una herramienta de "record and playback". Es un framework de automatización de nivel profesional que te da acceso completo al navegador.

**Los tres niveles de madurez con Playwright:**

```
Nivel 1 — Usuario:    Graba acciones, escribe tests básicos, usa locators simples
Nivel 2 — Developer:  POM, fixtures, network mocking, configuración avanzada
Nivel 3 — Arquitecto: Tests de seguridad, estrategia de test, CI/CD integration,
                       observabilidad, métricas de calidad, evaluación de cobertura
```

Tu ventaja como QA con mentalidad AIQ® es que no solo sabes usar la herramienta — sabes qué vale la pena testear, por qué puede fallar, y cómo el fallo afecta al negocio.

Eso no lo genera ningún AI. Eso es criterio.

---

*Libro generado por Claude Sonnet 4.6 para Rommel Ayala · AIQ® · Marzo 2026*
*"Flowing with your vision. Curiosity that could break it."*
