#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DRAFTS_DIR="$SCRIPT_DIR/libros_draft"
FONTS_DIR="$SCRIPT_DIR/fonts"
VENV_DIR="$SCRIPT_DIR/.venv"
PYTHON="$VENV_DIR/bin/python"
REQUIREMENTS="$SCRIPT_DIR/requirements.txt"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

detect_install_cmd() {
  local pkg="$1"
  case "$(uname -s)" in
    Darwin)
      if command -v brew &>/dev/null; then
        echo "brew install $pkg"
      else
        echo "Instala Homebrew desde https://brew.sh y luego: brew install $pkg"
      fi
      ;;
    Linux)
      if command -v apt-get &>/dev/null; then
        echo "sudo apt-get install -y $pkg"
      elif command -v dnf &>/dev/null; then
        echo "sudo dnf install -y $pkg"
      elif command -v pacman &>/dev/null; then
        echo "sudo pacman -S --noconfirm $pkg"
      elif command -v zypper &>/dev/null; then
        echo "sudo zypper install -y $pkg"
      elif command -v apk &>/dev/null; then
        echo "sudo apk add $pkg"
      else
        echo "Instala '$pkg' con el gestor de paquetes de tu distro"
      fi
      ;;
    MINGW*|MSYS*|CYGWIN*)
      echo "winget install $pkg  (o choco install $pkg)"
      ;;
    *)
      echo "Instala '$pkg' manualmente."
      ;;
  esac
}

# ---------------------------------------------------------------------------
# 1. check pandoc
# ---------------------------------------------------------------------------
if ! command -v pandoc &>/dev/null; then
  echo "❌ pandoc no está instalado."
  echo "   Instálalo con: $(detect_install_cmd pandoc)"
  exit 1
fi

# ---------------------------------------------------------------------------
# 2. check ebook-convert (solo si hay .pdf en el batch)
# ---------------------------------------------------------------------------
if ls "$DRAFTS_DIR"/*.pdf &>/dev/null 2>&1; then
  if ! command -v ebook-convert &>/dev/null; then
    echo "❌ ebook-convert (Calibre) no está instalado. Se requiere para procesar PDFs."
    echo "   Instálalo con: $(detect_install_cmd calibre)"
    echo "   O ejecuta sin los .pdf para procesar solo los .md."
    exit 1
  fi
fi

# ---------------------------------------------------------------------------
# 3. check ffmpeg (requerido para formato audio)
# ---------------------------------------------------------------------------
if ! command -v ffmpeg &>/dev/null || ! command -v ffprobe &>/dev/null; then
  echo "⚠️  ffmpeg/ffprobe no están instalados. Se requieren para generar audiolibros."
  echo "   Instálalo con: $(detect_install_cmd ffmpeg)"
  echo "   (Se omite si solo generas EPUBs.)"
fi

# ---------------------------------------------------------------------------
# 4. check_fonts — descarga Inter si faltan
# ---------------------------------------------------------------------------
check_fonts() {
  if [ ! -f "$FONTS_DIR/Inter-Regular.ttf" ] || [ ! -f "$FONTS_DIR/Inter-Bold.ttf" ]; then
    echo "🔧 Descargando fuentes Inter..."
    if ! command -v curl &>/dev/null; then
      echo "❌ curl no está disponible. Instala curl e inténtalo de nuevo."
      exit 1
    fi
    mkdir -p "$FONTS_DIR"
    local TMP
    TMP=$(mktemp -d)
    curl -fsSL "https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip" \
      -o "$TMP/inter.zip" || { echo "❌ No se pudo descargar Inter. Verifica tu conexión."; exit 1; }
    unzip -q "$TMP/inter.zip" -d "$TMP"
    cp "$(find "$TMP" -name "Inter-Regular.ttf" | head -1)" "$FONTS_DIR/"
    cp "$(find "$TMP" -name "Inter-Bold.ttf" | head -1)" "$FONTS_DIR/"
    rm -rf "$TMP"
    echo "✅ Fuentes instaladas en fonts/"
  fi
}

check_fonts

# ---------------------------------------------------------------------------
# 5. check venv + pip install
# ---------------------------------------------------------------------------
if [ ! -d "$VENV_DIR" ]; then
  echo "🔧 Creando venv en .venv/..."
  python3 -m venv "$VENV_DIR"
fi

if [ ! -f "$PYTHON" ]; then
  echo "❌ No se encontró Python en $VENV_DIR. Recrea el venv manualmente."
  exit 1
fi

echo "🔧 Instalando dependencias Python..."
"$PYTHON" -m pip install --quiet -r "$REQUIREMENTS"

# ---------------------------------------------------------------------------
# 6. delegate to generate_epub.py
# ---------------------------------------------------------------------------
echo "🚀 Ejecutando generate_epub.py..."
cd "$SCRIPT_DIR"
"$PYTHON" generate_epub.py "$@"
