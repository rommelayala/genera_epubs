# El Setup Perfecto: Mac/iPad/iPhone + Ubuntu Server

## Por qué trabajar solo en consola

Menos es más. Un servidor Ubuntu sin interfaz gráfica consume 200-400 MB de RAM en idle en lugar de 1-2 GB con entorno de escritorio. Todo el poder de la máquina va a tu código, tus modelos y tus servicios.

La consola te da algo que la GUI nunca puede: **reproducibilidad**. Un script bash o un alias hacen exactamente lo mismo en tu MacBook, en tu iPad y en un servidor en la nube. Sin excepciones.

La curva de aprendizaje es real. Pero el desarrollador que domina la terminal es 5x más rápido que el que depende del ratón. Este libro es ese atajo.

## El stack real de este libro

Este libro asume el siguiente setup:

- **Cliente**: Mac (primario), iPad o iPhone (movilidad)
- **Servidor**: Ubuntu Server 22.04/24.04 LTS sin GUI
- **Conexión**: SSH desde Termius o cliente nativo
- **IA Local**: Ollama con modelos pequeños
- **Servicios**: Hermes corriendo en el servidor

## Clientes SSH: alternativas gratuitas a Termius

Termius es cómodo pero de pago. Hay opciones igual de sólidas sin coste.

### En Mac

**SSH nativo + iTerm2** es la combinación ganadora y completamente gratis:

```bash
# Conectar directamente desde Terminal o iTerm2
ssh usuario@ip-del-servidor

# Con clave privada
ssh -i ~/.ssh/mi_clave usuario@ip-del-servidor

# Guardar configuración en ~/.ssh/config
Host miservidor
    HostName 192.168.1.100
    User rommel
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
```

Después de configurar `~/.ssh/config` solo escribes:

```bash
ssh miservidor
```

**iTerm2** añade pestañas, splits de pantalla, perfiles de color y sincronización de sesiones. Gratuito y open source.

### En iPad / iPhone

| App | Precio | Notas |
|-----|--------|-------|
| **a-Shell** | Gratis | Terminal completa con Python, vim, ssh nativo |
| **iSH Shell** | Gratis | Alpine Linux en iOS, ssh cliente incluido |
| **Prompt 3** | Pago | La mejor UX, vale el precio si lo usas mucho |
| **SSH Files** | Freemium | SSH + SFTP para gestionar archivos |
| **Termius** | Freemium | Plan gratis limitado a 1 host |

**Recomendación para iPad**: a-Shell para uso técnico, iSH para entorno Linux completo. Ambos gratuitos.

```bash
# En a-Shell, conectar con:
ssh -i ~/.ssh/id_ed25519 rommel@192.168.1.100
```

## Generar y copiar claves SSH

Hazlo una sola vez desde tu Mac:

```bash
# Generar clave Ed25519 (más moderna y segura que RSA)
ssh-keygen -t ed25519 -C "rommel@mac"

# Copiar la clave pública al servidor
ssh-copy-id -i ~/.ssh/id_ed25519.pub usuario@ip-servidor

# O manualmente si ssh-copy-id no está disponible
cat ~/.ssh/id_ed25519.pub | ssh usuario@ip "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

---

# Configuración Inicial de Ubuntu Server

## Configurar el teclado en español

Cuando Ubuntu arranca sin GUI el teclado puede estar en inglés. Un teclado en inglés en un teclado español es una pesadilla de símbolos.

```bash
# Método interactivo (recomendado)
sudo dpkg-reconfigure keyboard-configuration
```

Selecciona en orden:
1. **Generic 105-key (Intl) PC**
2. **Spanish** (no la variante latinoamericana salvo que la necesites)
3. **Spanish** (sin variante)
4. **The default for the keyboard layout**
5. **No compose key**

Luego aplica sin reiniciar:

```bash
sudo setupcon
```

Para cambio inmediato en la sesión actual:

```bash
sudo loadkeys es
```

### El problema de Alt Gr en Termius

Si al pulsar `Alt Gr + 2` para escribir `@` aparece `(arg: 2)`, el problema está en Termius, no en Ubuntu.

**Solución en Termius:**

1. Abre la configuración de la sesión SSH
2. Ve a **Terminal → Keyboard**
3. Desactiva **"Use Alt key as Meta key"** o cambia **Alt key behavior** a `Normal`
4. Cambia **Terminal type** a `xterm-256color`

**Mientras tanto, escribir `@` con código ASCII:**

```bash
printf '\x40'
# O simplemente pega desde el portapapeles del Mac
```

## Configuración de red

### Ver interfaces y direcciones IP

```bash
# Ver todas las interfaces
ip addr show

# Solo la IP de la interfaz principal (generalmente eth0 o ens3)
ip addr show eth0

# Forma corta
ip a
```

### Ver rutas y gateway

```bash
ip route show
# La línea "default via X.X.X.X" es tu gateway
```

### Gestión con NetworkManager (nmcli)

```bash
# Estado de conexiones
nmcli connection show

# Ver detalles de una conexión
nmcli connection show "nombre-conexion"

# Activar/desactivar interfaz
nmcli connection up eth0
nmcli connection down eth0

# Ver dispositivos
nmcli device status
```

### Configurar IP estática con Netplan

Ubuntu Server usa Netplan. El archivo de configuración está en `/etc/netplan/`:

```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

```yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: false
      addresses:
        - 192.168.1.100/24
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]
```

```bash
# Aplicar cambios
sudo netplan apply
```

## SSH Hardening básico

Edita `/etc/ssh/sshd_config`:

```bash
sudo nano /etc/ssh/sshd_config
```

Cambios esenciales:

```bash
# Deshabilitar login con contraseña (solo claves)
PasswordAuthentication no

# Deshabilitar login como root
PermitRootLogin no

# Cambiar puerto por defecto (opcional pero reduce bots)
Port 2222

# Solo permitir usuarios específicos
AllowUsers rommel

# Tiempo de espera para conexiones inactivas
ClientAliveInterval 300
ClientAliveCountMax 2
```

Reinicia el servicio:

```bash
sudo systemctl restart sshd
```

**Importante**: antes de cerrar tu sesión actual, abre una segunda conexión SSH para verificar que todo funciona con la nueva configuración.

---

# Navegar por Internet desde la Consola

## curl: la herramienta universal

`curl` es el navaja suiza del desarrollador en consola. Si solo aprendes una herramienta de red, que sea esta.

### Comandos esenciales

```bash
# GET básico
curl https://example.com

# Solo los headers de respuesta
curl -I https://example.com

# Seguir redirecciones (301, 302)
curl -L https://example.com

# Guardar en archivo
curl -o archivo.html https://example.com

# Guardar con el nombre original del servidor
curl -O https://example.com/imagen.jpg

# Modo silencioso (sin barra de progreso)
curl -s https://api.example.com/data
```

### APIs REST con curl

```bash
# GET con header de autenticación
curl -H "Authorization: Bearer TOKEN" https://api.example.com/users

# POST con JSON
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Rommel", "rol": "dev"}' \
  https://api.example.com/users

# PUT
curl -X PUT \
  -H "Content-Type: application/json" \
  -d '{"activo": true}' \
  https://api.example.com/users/42

# DELETE
curl -X DELETE https://api.example.com/users/42

# Ver código de respuesta HTTP
curl -o /dev/null -s -w "%{http_code}" https://example.com
```

### Trabajar con JSON en consola

```bash
# Instalar jq (procesador JSON para terminal)
sudo apt install jq

# Formatear respuesta JSON
curl -s https://api.github.com/users/rommel | jq .

# Extraer campo específico
curl -s https://api.github.com/users/rommel | jq '.name'

# Filtrar array
curl -s https://api.github.com/repos/rommel/proyecto/issues | jq '.[].title'
```

### Autenticación

```bash
# Basic auth
curl -u usuario:contraseña https://api.example.com

# Bearer token
curl -H "Authorization: Bearer $(cat ~/.tokens/api_token)" https://api.example.com

# API key en header
curl -H "X-API-Key: mi_clave" https://api.example.com
```

### curl para depuración

```bash
# Ver request y response completos
curl -v https://example.com

# Solo tiempos de conexión
curl -s -o /dev/null -w "DNS: %{time_namelookup}s\nConexión: %{time_connect}s\nTotal: %{time_total}s\n" https://example.com
```

## wget: descargar archivos

```bash
# Descargar archivo
wget https://example.com/archivo.zip

# En segundo plano
wget -b https://example.com/archivo-grande.iso

# Reanudar descarga interrumpida
wget -c https://example.com/archivo.zip

# Descargar página completa con recursos
wget -r -l1 -p https://example.com

# Mirror completo de un sitio
wget --mirror https://docs.example.com

# Limitar velocidad de descarga
wget --limit-rate=1m https://example.com/archivo.iso

# Descargar lista de URLs desde archivo
wget -i lista_urls.txt
```

## Navegadores de texto

Para sitios simples, documentación o cuando necesitas interactividad básica.

### w3m

```bash
sudo apt install w3m

# Navegar a una URL
w3m https://docs.python.org

# Si aparece error gzip, forzar sin compresión
w3m -o accept_encoding="" https://github.com
```

**Controles w3m:**
- Flechas: navegar
- `Enter`: seguir enlace
- `B`: atrás
- `Tab`: siguiente enlace
- `q`: salir

### lynx

```bash
sudo apt install lynx

lynx https://example.com
```

**Controles lynx:**
- Flechas arriba/abajo: moverse por la página
- Flecha derecha / `Enter`: seguir enlace
- Flecha izquierda: atrás
- `g`: ir a URL
- `q`: salir

### Problemas comunes con navegadores de texto

Los sitios modernos usan JavaScript pesado y compresión agresiva. Los navegadores de texto muestran el HTML crudo sin ejecutar JS.

**Error "gzip: stdin: not in gzip format":**

```bash
# Solución con w3m
w3m -o accept_encoding="" https://sitio.com

# Usar lynx como alternativa
lynx https://sitio.com

# O simplemente usar curl y ver el HTML
curl -s https://sitio.com | less
```

## httpie: curl con mejor UX

```bash
# Instalar
sudo apt install httpie
# O con pip
pip3 install httpie

# GET (salida formateada automáticamente)
http https://api.example.com/users

# POST JSON (sintaxis más limpia que curl)
http POST https://api.example.com/users nombre=Rommel rol=dev

# Con headers
http https://api.example.com/users Authorization:"Bearer TOKEN"
```

httpie colorea la salida, formatea JSON automáticamente y tiene sintaxis más intuitiva que curl. Ideal para desarrollo e inspección rápida.

---

# Monitorizar Recursos del Sistema

Saber qué consume tu servidor es crítico cuando tienes Ollama, Hermes y tus servicios corriendo en paralelo.

## CPU

### top (instalado por defecto)

```bash
top
```

**Atajos dentro de top:**
- `1`: ver cada CPU individualmente
- `M`: ordenar por uso de memoria
- `P`: ordenar por CPU
- `k`: matar proceso (pide PID)
- `q`: salir

### htop (top mejorado)

```bash
sudo apt install htop
htop
```

`htop` muestra barras de progreso para CPU/RAM, permite scroll, y matar procesos con `F9`. Mucho más legible que `top`.

### mpstat (estadísticas por CPU)

```bash
sudo apt install sysstat

# Ver estadísticas cada 2 segundos
mpstat 2

# Por CPU individual
mpstat -P ALL 2
```

## RAM y memoria

```bash
# Uso de memoria (human-readable)
free -h

# Con actualización cada 2 segundos
watch -n 2 free -h

# Estadísticas detalladas
vmstat 2

# Ver qué procesos consumen más RAM
ps aux --sort=-%mem | head -20
```

## Disco

```bash
# Espacio en disco por partición
df -h

# Espacio usado por directorio
du -sh /var/log
du -sh /*

# Encontrar los directorios más grandes
du -h / 2>/dev/null | sort -hr | head -20
```

### ncdu: explorador de disco visual

```bash
sudo apt install ncdu

# Analizar directorio actual
ncdu .

# Analizar desde raíz
sudo ncdu /
```

`ncdu` muestra un explorador interactivo de uso de disco. Perfecto para encontrar qué ocupa espacio.

## Red

```bash
# Ver conexiones activas
ss -tuln

# Ver conexiones establecidas con procesos
ss -tulnp

# Ver estadísticas de interfaz
ip -s link

# Tráfico en tiempo real por interfaz
sudo apt install iftop
sudo iftop -i eth0

# Tráfico en tiempo real por proceso
sudo apt install nethogs
sudo nethogs eth0
```

## Procesos

```bash
# Ver todos los procesos
ps aux

# Buscar proceso por nombre
pgrep -la ollama
pgrep -la hermes

# Ver árbol de procesos
ps auxf

# Matar proceso por PID
kill 1234

# Matar proceso por nombre
pkill ollama

# Forzar matar
kill -9 1234
```

## Logs del sistema

```bash
# Ver logs del sistema (systemd)
journalctl

# Logs en tiempo real
journalctl -f

# Logs de un servicio específico
journalctl -u ollama -f
journalctl -u hermes -f

# Logs desde hace 1 hora
journalctl --since "1 hour ago"

# Últimas 50 líneas de un log
tail -n 50 /var/log/syslog
tail -f /var/log/syslog
```

## btop: dashboard completo

```bash
sudo apt install btop
btop
```

`btop` es el monitor definitivo: CPU, RAM, disco, red y procesos en una sola pantalla con diseño moderno. Reemplaza a `top`, `htop`, `iftop` y `df` a la vez.

### Cheatsheet de monitorización rápida

```bash
# Una línea para ver todo lo importante
echo "=== CPU ===" && mpstat 1 1 | tail -1 && \
echo "=== RAM ===" && free -h && \
echo "=== Disco ===" && df -h / && \
echo "=== Servicios ===" && systemctl is-active ollama hermes
```

---

# Editores de Código en Consola

## nano: el punto de entrada

Si acabas de llegar a la consola, `nano` es tu primer editor. Ya está instalado en Ubuntu.

```bash
nano archivo.py
```

**Atajos esenciales:**
- `Ctrl+O`: guardar
- `Ctrl+X`: salir
- `Ctrl+W`: buscar
- `Ctrl+K`: cortar línea
- `Ctrl+U`: pegar
- `Ctrl+G`: ayuda

Para archivos de configuración rápidos, nano es suficiente. Para desarrollo serio, pasa a los siguientes.

## Vim/Neovim: el estándar de la industria

Vim tiene una curva de aprendizaje empinada pero es omnipresente. Está en absolutamente todos los servidores Linux.

```bash
# Instalar Neovim (versión moderna de Vim)
sudo apt install neovim

nvim archivo.py
```

### Modos de Vim (lo esencial)

- **Normal**: navegar, copiar, pegar. Es el modo por defecto.
- **Insert** (`i`): escribir texto
- **Visual** (`v`): seleccionar texto
- **Command** (`:`): ejecutar comandos

```bash
# Moverse en modo Normal
h j k l    # izquierda, abajo, arriba, derecha
w          # siguiente palabra
b          # palabra anterior
0          # inicio de línea
$          # fin de línea
gg         # inicio del archivo
G          # fin del archivo
Ctrl+d     # bajar media pantalla
Ctrl+u     # subir media pantalla

# Editar
i          # insertar antes del cursor
a          # insertar después del cursor
o          # nueva línea abajo
dd         # cortar línea
yy         # copiar línea
p          # pegar
u          # deshacer
Ctrl+r     # rehacer

# Buscar
/texto     # buscar hacia adelante
n          # siguiente resultado
N          # resultado anterior

# Guardar y salir
:w         # guardar
:q         # salir
:wq        # guardar y salir
:q!        # salir sin guardar
```

### Configuración básica de Neovim

```bash
mkdir -p ~/.config/nvim
nano ~/.config/nvim/init.vim
```

```vim
set number          " números de línea
set relativenumber  " números relativos
set tabstop=4
set shiftwidth=4
set expandtab
set autoindent
set hlsearch        " resaltar búsquedas
set incsearch       " búsqueda incremental
syntax on
```

## Micro: el editor moderno para consola

`micro` tiene atajos familiares (`Ctrl+S`, `Ctrl+Z`, `Ctrl+C`) y no requiere aprender modos.

```bash
# Instalar
sudo apt install micro
# O la última versión
curl https://getmic.ro | bash

micro archivo.py
```

**Atajos:**
- `Ctrl+S`: guardar
- `Ctrl+Q`: salir
- `Ctrl+Z`: deshacer
- `Ctrl+F`: buscar
- `Ctrl+G`: ir a línea
- `Ctrl+E`: ejecutar comando

Ideal para quien viene de VS Code y quiere algo familiar en consola.

## Helix: el editor modal del futuro

`helix` es un editor modal moderno (inspirado en Vim/Kakoune) con LSP integrado desde el primer día.

```bash
sudo apt install helix
# O descargar binario desde releases
hx archivo.py
```

La diferencia clave con Vim: **primero seleccionas, luego actúas** (en Vim es al revés).

```bash
# Moverse
h j k l    # básico
w          # siguiente palabra
b          # palabra anterior

# Seleccionar y editar
v          # modo visual
d          # borrar selección
c          # cambiar selección
y          # copiar

# LSP
Space+d    # diagnósticos
Space+r    # renombrar símbolo
gd         # ir a definición
```

## Comparativa de editores

| Editor | Curva | Potencia | LSP | Ideal para |
|--------|-------|---------|-----|-----------|
| nano | Baja | Baja | No | Editar config rápido |
| micro | Baja | Media | Sí | Migrar desde GUI |
| Vim/Neovim | Alta | Máxima | Con plugins | Desarrollo profesional |
| Helix | Media | Alta | Nativo | Alternativa moderna a Vim |

**Recomendación**: empieza con `micro`, aprende `Vim` en paralelo. A las 4 semanas usarás Vim para todo.

---

# Gestión de Archivos y Navegación

## ranger: explorador de archivos visual

```bash
sudo apt install ranger
ranger
```

Muestra tres columnas: directorio padre, directorio actual, preview del archivo seleccionado. Navegación con flechas, edición con `e`.

**Atajos:**
- Flechas: navegar
- `Enter`: abrir
- `e`: editar en $EDITOR
- `yy`: copiar archivo
- `dd`: cortar archivo
- `pp`: pegar
- `dD`: borrar
- `q`: salir

## tmux: el multiplicador de terminales

`tmux` es **imprescindible** para trabajo en servidor. Mantiene sesiones activas aunque pierdas la conexión SSH. Si se corta tu WiFi, tu trabajo sigue corriendo.

```bash
sudo apt install tmux
```

### Flujo básico de trabajo

```bash
# Crear nueva sesión nombrada
tmux new -s trabajo

# Desconectarse sin cerrar (sesión sigue corriendo)
Ctrl+B, d

# Reconectarse a la sesión
tmux attach -t trabajo

# Listar sesiones
tmux ls
```

### Múltiples ventanas y paneles

```bash
# Dentro de tmux, el prefijo es Ctrl+B

# Ventanas
Ctrl+B, c      # nueva ventana
Ctrl+B, n      # siguiente ventana
Ctrl+B, p      # ventana anterior
Ctrl+B, 0-9    # ir a ventana por número

# Paneles (splits)
Ctrl+B, %      # split vertical
Ctrl+B, "      # split horizontal
Ctrl+B, flechas  # moverse entre paneles
Ctrl+B, z      # zoom en panel actual (toggle)
Ctrl+B, x      # cerrar panel actual
```

### Configuración esencial de tmux

```bash
nano ~/.tmux.conf
```

```bash
# Cambiar prefijo a Ctrl+A (más cómodo)
set -g prefix C-a
unbind C-b
bind C-a send-prefix

# Mouse habilitado
set -g mouse on

# Numeración desde 1
set -g base-index 1

# Colores
set -g default-terminal "screen-256color"

# Reload config
bind r source-file ~/.tmux.conf \; display "Config recargada"
```

## Zsh + Oh My Zsh: un shell de verdad

```bash
# Instalar zsh
sudo apt install zsh

# Instalar Oh My Zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Hacer zsh el shell por defecto
chsh -s $(which zsh)
```

### Plugins esenciales de Oh My Zsh

Edita `~/.zshrc`:

```bash
plugins=(
  git
  sudo
  zsh-autosuggestions
  zsh-syntax-highlighting
  docker
  python
  node
)
```

Instalar plugins de terceros:

```bash
# Autosuggestions (sugiere comandos del historial)
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# Syntax highlighting (colorea comandos válidos/inválidos)
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

## fzf: búsqueda fuzzy

`fzf` transforma cualquier lista en un buscador interactivo.

```bash
sudo apt install fzf
```

```bash
# Buscar archivo y abrirlo
vim $(fzf)

# Buscar en historial de comandos (Ctrl+R con esteroides)
# Se activa automáticamente en Ctrl+R tras instalar fzf

# Buscar proceso y matarlo
kill $(ps aux | fzf | awk '{print $2}')

# Cambiar a directorio con fzf
cd $(find . -type d | fzf)
```

---

# Herramientas de Desarrollo

## Git desde consola

```bash
# Configuración inicial
git config --global user.name "Rommel Ayala"
git config --global user.email "rommel@example.com"
git config --global init.defaultBranch main
git config --global core.editor nvim

# Flujo básico
git init
git clone https://github.com/usuario/repo.git
git status
git add .
git commit -m "mensaje"
git push origin main
git pull

# Ramas
git branch nombre-rama
git checkout -b nombre-rama
git switch nombre-rama
git merge nombre-rama
git branch -d nombre-rama

# Ver historial visual
git log --oneline --graph --all
```

### Aliases de git útiles

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.lg "log --oneline --graph --all --decorate"
```

## Node.js con NVM

Nunca instales Node con `apt`. Usa `nvm` para manejar versiones:

```bash
# Instalar nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Recargar shell
source ~/.bashrc  # o ~/.zshrc

# Instalar Node LTS
nvm install --lts
nvm use --lts

# Listar versiones instaladas
nvm list
```

## Python con pyenv

```bash
# Instalar dependencias
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
  libffi-dev liblzma-dev

# Instalar pyenv
curl https://pyenv.run | bash

# Agregar a .bashrc/.zshrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Instalar Python
pyenv install 3.12
pyenv global 3.12
```

## Docker en modo headless

```bash
# Instalar Docker
curl -fsSL https://get.docker.com | bash
sudo usermod -aG docker $USER

# Reconectarse para que tome efecto el grupo
# (o ejecutar: newgrp docker)

# Comandos esenciales
docker ps                          # contenedores activos
docker ps -a                       # todos los contenedores
docker images                      # imágenes locales
docker run -d -p 3000:3000 app    # correr en background
docker logs -f nombre-contenedor   # ver logs en tiempo real
docker exec -it contenedor bash    # entrar al contenedor
docker stop contenedor
docker rm contenedor
docker system prune                # limpiar todo lo no usado
```

### docker-compose en consola

```bash
# Levantar servicios
docker compose up -d

# Ver estado
docker compose ps

# Ver logs
docker compose logs -f

# Parar todo
docker compose down
```

## Gestión de procesos con systemd

Para que tus servicios arranquen solos y se reinicien si fallan:

```bash
# Crear servicio
sudo nano /etc/systemd/system/mi-app.service
```

```ini
[Unit]
Description=Mi aplicación Node.js
After=network.target

[Service]
Type=simple
User=rommel
WorkingDirectory=/home/rommel/mi-app
ExecStart=/home/rommel/.nvm/versions/node/v20.0.0/bin/node server.js
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable mi-app
sudo systemctl start mi-app
sudo systemctl status mi-app
```

---

# Ollama y IA Local en Consola

## Instalar y gestionar Ollama

```bash
# Instalar
curl -fsSL https://ollama.ai/install.sh | sh

# Verificar que el servicio está activo
systemctl status ollama

# Ver logs de Ollama
journalctl -u ollama -f
```

## Modelos pequeños recomendados

Para un servidor con recursos limitados, estos modelos ofrecen el mejor rendimiento por MB:

| Modelo | Tamaño | RAM mínima | Ideal para |
|--------|--------|-----------|-----------|
| `qwen2.5:1.5b` | 1 GB | 2 GB | Respuestas rápidas, código simple |
| `gemma2:2b` | 1.6 GB | 3 GB | Lenguaje natural, resúmenes |
| `phi3:mini` | 2.3 GB | 4 GB | Código, razonamiento |
| `llama3.2:3b` | 2 GB | 4 GB | Uso general |
| `deepseek-coder:1.3b` | 776 MB | 2 GB | Solo código |

```bash
# Descargar modelo
ollama pull qwen2.5:1.5b

# Listar modelos instalados
ollama list

# Chatear con un modelo
ollama run qwen2.5:1.5b

# Borrar modelo
ollama rm nombre-modelo

# Ver información de un modelo
ollama show qwen2.5:1.5b
```

## Usar Ollama desde la línea de comandos

```bash
# Consulta sin abrir sesión interactiva
ollama run qwen2.5:1.5b "Explica qué es un closure en JavaScript en 2 líneas"

# Pasar stdin al modelo
echo "Resume este texto: $(cat documento.txt)" | ollama run qwen2.5:1.5b

# Revisar código
cat mi_script.py | ollama run phi3:mini "Revisa este código Python y sugiere mejoras"
```

## Ollama via API REST

Ollama expone una API en el puerto 11434:

```bash
# Chat via API
curl http://localhost:11434/api/chat -d '{
  "model": "qwen2.5:1.5b",
  "messages": [{"role": "user", "content": "Hola, ¿cómo estás?"}],
  "stream": false
}' | jq '.message.content'

# Completar texto
curl http://localhost:11434/api/generate -d '{
  "model": "phi3:mini",
  "prompt": "Escribe una función Python que ordene una lista",
  "stream": false
}' | jq '.response'

# Ver modelos disponibles vía API
curl http://localhost:11434/api/tags | jq '.models[].name'
```

## Scripts bash con Ollama

```bash
# Script: asistente de consola
#!/bin/bash
# Guardar como ~/bin/ai y hacer ejecutable: chmod +x ~/bin/ai

MODEL="qwen2.5:1.5b"
PROMPT="$*"

if [ -z "$PROMPT" ]; then
  echo "Uso: ai <pregunta>"
  exit 1
fi

curl -s http://localhost:11434/api/generate -d "{
  \"model\": \"$MODEL\",
  \"prompt\": \"$PROMPT\",
  \"stream\": false
}" | jq -r '.response'
```

```bash
# Usar como:
ai "cómo hago un for loop en bash"
ai "explica qué hace este comando: find / -name '*.log' -mtime +7"
```

## Hermes: gestión y monitorización

Hermes es tu servidor de mensajería/notificaciones. Gestión básica:

```bash
# Ver estado
systemctl status hermes

# Ver logs en tiempo real
journalctl -u hermes -f

# Reiniciar
sudo systemctl restart hermes

# Ver en qué puerto escucha
ss -tlnp | grep hermes

# Ver cuánta RAM consume
ps aux | grep hermes | grep -v grep
```

### Monitorizar todos los servicios de un vistazo

```bash
# Estado de todos tus servicios clave
for svc in ollama hermes; do
  echo -n "$svc: "
  systemctl is-active $svc
done
```

---

# Productividad: Workflows Reales

## Sesión típica de desarrollo

Este es el flujo diario desde Mac con iTerm2 o desde iPad con a-Shell:

```bash
# 1. Conectar al servidor
ssh miservidor

# 2. Retomar sesión tmux existente o crear una nueva
tmux attach -t dev || tmux new -s dev

# 3. Dentro de tmux: organizar el espacio de trabajo
# Ctrl+B, % → split vertical
# Panel izquierdo: editor (nvim)
# Panel derecho arriba: terminal para ejecutar
# Panel derecho abajo: logs del servicio

# 4. Abrir el proyecto
cd ~/proyectos/mi-app
nvim .

# 5. En otro panel, correr el servidor en modo watch
npm run dev

# 6. En otro panel, ver logs
journalctl -u mi-servicio -f

# 7. Al terminar, desconectarse sin matar la sesión
# Ctrl+B, d
```

## Aliases y funciones bash imprescindibles

Agrega esto a tu `~/.bashrc` o `~/.zshrc`:

```bash
# Navegación
alias ..='cd ..'
alias ...='cd ../..'
alias ll='ls -lah'
alias la='ls -lah'

# Git
alias gs='git status'
alias ga='git add .'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline --graph --all'

# Docker
alias dc='docker compose'
alias dps='docker ps'
alias dlogs='docker compose logs -f'

# Sistema
alias ports='ss -tuln'
alias meminfo='free -h'
alias diskinfo='df -h'
alias myip='curl -s ifconfig.me'

# Servicios
alias logs-ollama='journalctl -u ollama -f'
alias logs-hermes='journalctl -u hermes -f'
alias status-all='systemctl status ollama hermes'

# IA rápida
ai() { curl -s http://localhost:11434/api/generate \
  -d "{\"model\":\"qwen2.5:1.5b\",\"prompt\":\"$*\",\"stream\":false}" \
  | jq -r '.response'; }
```

## Port forwarding SSH: acceder a servicios del servidor desde Mac

Si tienes servicios corriendo en el servidor (Ollama en 11434, Hermes en algún puerto), puedes acceder a ellos desde tu Mac sin exponerlos a internet:

```bash
# En ~/.ssh/config del Mac
Host miservidor
    HostName 192.168.1.100
    User rommel
    IdentityFile ~/.ssh/id_ed25519
    # Forward: puerto_local → puerto_remoto
    LocalForward 11434 localhost:11434   # Ollama
    LocalForward 8080 localhost:8080    # Hermes

# Conectar con forwarding activo
ssh miservidor
```

Ahora desde tu Mac puedes acceder a `http://localhost:11434` y hablar con Ollama del servidor.

## rsync: sincronizar archivos entre Mac y servidor

```bash
# Subir directorio local al servidor
rsync -avz --progress ~/proyectos/mi-app/ rommel@miservidor:~/proyectos/mi-app/

# Bajar archivos del servidor al Mac
rsync -avz --progress rommel@miservidor:~/datos/ ~/datos-backup/

# Excluir node_modules y .git
rsync -avz --exclude='node_modules' --exclude='.git' \
  ~/proyectos/mi-app/ rommel@miservidor:~/proyectos/mi-app/

# Sync bidireccional (cuidado: sobrescribe)
rsync -avz --delete ~/proyectos/ rommel@miservidor:~/proyectos/
```

## Alternativas gratuitas a Termius

| Cliente | Plataforma | Precio | Destacado |
|---------|-----------|--------|-----------|
| **SSH nativo + iTerm2** | Mac | Gratis | El mejor para Mac, sin límites |
| **a-Shell** | iPad/iPhone | Gratis | Terminal completa, ssh incluido |
| **iSH Shell** | iPad/iPhone | Gratis | Linux completo emulado |
| **Termius** | Mac/iPad/iPhone | Freemium | Plan gratis: 1 host, sin sync |
| **SSH Files** | iPad/iPhone | Freemium | SFTP + SSH, muy estable |
| **Blink Shell** | iPad/iPhone | Pago anual | El mejor para iPad, mosh incluido |

**Stack recomendado gratuito:**
- Mac: **iTerm2** + SSH config en `~/.ssh/config`
- iPad/iPhone: **a-Shell** o **iSH Shell**

---

# Apéndice

## Cheatsheet de atajos esenciales

### tmux

```
Ctrl+B, d     Desconectarse (sesión sigue activa)
Ctrl+B, c     Nueva ventana
Ctrl+B, n/p   Siguiente/anterior ventana
Ctrl+B, %     Split vertical
Ctrl+B, "     Split horizontal
Ctrl+B, z     Zoom panel actual
Ctrl+B, [     Modo scroll (q para salir)
```

### Vim/Neovim

```
i             Entrar modo insertar
Esc           Volver a modo normal
:w            Guardar
:q!           Salir sin guardar
:wq           Guardar y salir
/texto        Buscar
dd            Cortar línea
yy            Copiar línea
p             Pegar
u             Deshacer
gg / G        Inicio / fin del archivo
```

### nano

```
Ctrl+O        Guardar
Ctrl+X        Salir
Ctrl+W        Buscar
Ctrl+K        Cortar línea
Ctrl+U        Pegar
```

## Comandos de red más usados

```bash
ip addr show                    # Ver IPs
ip route show                   # Ver rutas
ss -tuln                        # Ver puertos abiertos
curl ifconfig.me                # Ver IP pública
ping -c 4 8.8.8.8               # Test conectividad
traceroute google.com           # Ver ruta de paquetes
nslookup google.com             # Resolver DNS
dig google.com                  # DNS detallado
netstat -tlnp                   # Conexiones y procesos
```

## Solución de problemas SSH comunes

**"Connection refused"**
```bash
# Verificar que sshd está corriendo en el servidor
sudo systemctl status sshd
sudo systemctl start sshd
```

**"Permission denied (publickey)"**
```bash
# Verificar permisos en el servidor
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# Verificar que la clave pública está en authorized_keys
cat ~/.ssh/authorized_keys
```

**Sesión SSH se corta sola**
```bash
# En ~/.ssh/config del cliente
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

**"Host key verification failed"**
```bash
# Eliminar la entrada antigua (si reinstalaste el servidor)
ssh-keygen -R ip-del-servidor
```

## Recursos y comunidades

- **man pages**: `man comando` — la documentación oficial siempre disponible offline
- **tldr**: versión resumida de man pages → `sudo apt install tldr && tldr comando`
- **explainshell.com**: pega cualquier comando y lo explica parte por parte
- **archlinux wiki**: la mejor documentación técnica de Linux, aplica a Ubuntu
- **r/linux**: comunidad general
- **r/commandline**: foco en herramientas de consola
- **Hacker News**: noticias y debates sobre herramientas de desarrollo

```bash
# Instalar tldr para consultas rápidas
sudo apt install tldr
tldr curl
tldr rsync
tldr tmux
```
