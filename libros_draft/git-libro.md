# Git y SSH: Configuración y Resolución de Problemas

## Configuración y Diagnóstico de SSH

Cuando trabajas con repositorios remotos en GitHub y utilizas claves SSH, es fundamental saber cómo diagnosticar problemas de conexión. Aquí tienes los comandos más útiles:

### 1. Ver la configuración de SSH

Estos comandos te ayudan a ver cómo se está conectando tu computadora a internet y a GitHub.

*   **Ver el archivo principal de reglas SSH:**
    ```bash
    cat ~/.ssh/config
    ```
    *Para qué sirve:* Te muestra qué llaves están asignadas a qué hosts (por ejemplo, para separar tu cuenta personal de la de trabajo en GitHub).

*   **Listar todas las llaves disponibles en tu equipo:**
    ```bash
    ls -la ~/.ssh/
    ```
    *Para qué sirve:* Te enseña qué archivos de llaves tienes guardados. Las que terminan en `.pub` son las públicas (las que se comparten); las que no, son las privadas (nunca se comparten).

*   **Ver qué llaves SSH están cargadas en la memoria (el agente):**
    ```bash
    ssh-add -l
    ```
    *Para qué sirve:* Muestra una lista de las identidades (llaves) que tu computadora tiene listas y "desbloqueadas" para usar.

*   **Ver el contenido de tu llave pública (para copiar a GitHub):**
    ```bash
    cat ~/.ssh/id_ed25519.pub
    ```
    *Para qué sirve:* Imprime en pantalla el texto exacto de la llave que debes registrar en la página de GitHub. Sustituye `id_ed25519.pub` por el nombre real del archivo que viste con `ls -la ~/.ssh/` (por ejemplo, `id_ed25519_personal.pub` o `id_rsa.pub`).

*   **Hacer una prueba de conexión detallada ("Modo Dios"):**
    ```bash
    ssh -vT git@github.com
    ```
    *Para qué sirve:* El `-v` significa *verbose*. Te muestra paso a paso exactamente qué archivos lee SSH, qué llave intenta mandar y por qué GitHub la acepta o la rechaza.

### 2. Ver la configuración de Git

Estos comandos sirven para entender cómo está configurado tu repositorio actual.

*   **Ver hacia dónde apunta tu repositorio (los remotos):**
    ```bash
    git remote -v
    ```
    *Para qué sirve:* Te dice la dirección URL exacta (de GitHub, GitLab, etc.) de donde tu proyecto está intentando hacer `pull` o `push`.

*   **Ver toda la configuración general de Git:**
    ```bash
    git config --list
    ```
    *Para qué sirve:* Muestra cosas como tu nombre de usuario, tu correo electrónico registrado y otras variables globales de Git.

*   **Ver solo tu usuario y correo de Git:**
    ```bash
    git config user.name
    git config user.email
    ```
    *Para qué sirve:* Muy útil para asegurar que los commits que hagas van a salir con tu nombre correcto.

## Resolución de Problemas: Permission denied (publickey)

Si al intentar hacer `git pull` o `git push` te encuentras con el error `Permission denied (publickey)`, sigue estos pasos:

1. **Prueba la conexión SSH:**
   ```bash
   ssh -T git@github.com
   ```
   Si el mensaje de respuesta no es un éxito (algo como `Hi usuario! You've successfully authenticated...`), hay un problema con tu llave.

2. **Verifica si la llave está registrada en GitHub:**
   Incluso si la terminal está mandando la llave correcta, GitHub puede rechazarla si no la has registrado en tu cuenta.
   * Ve a [Settings > SSH and GPG keys](https://github.com/settings/keys) en tu cuenta de GitHub.
   * Agrega tu llave pública usando el botón "New SSH key".

3. **Cuentas múltiples (Trabajo y Personal):**
   Si utilizas varias cuentas en el mismo equipo, asegúrate de tener tu archivo `~/.ssh/config` correctamente configurado para diferenciar el host (por ejemplo, `github.com` vs `github.com-trabajo`), y de iniciar sesión en la cuenta correcta en el navegador cuando agregues la llave.

   Ejemplo mínimo de `~/.ssh/config`:
   ```
   # Cuenta personal
   Host github.com
     HostName github.com
     User git
     IdentityFile ~/.ssh/id_ed25519_personal

   # Cuenta de trabajo (alias)
   Host github.com-trabajo
     HostName github.com
     User git
     IdentityFile ~/.ssh/id_ed25519_trabajo
   ```

   Con esa configuración, los repos de trabajo deben usar la URL `git@github.com-trabajo:org/repo.git` para que SSH elija la llave correcta.
