#!/bin/bash

# dirname "$0"-> recupera el directorio desde donde se esta ejecutnado el script
DRAFTS_DIR="$(dirname "$0")/libros_draft"
COVERS_DIR="$(dirname "$0")/portadas_draft"
OUTPUT_DIR="$(dirname "$0")/epubs_generados"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Validar pandoc
if ! command -v pandoc &> /dev/null; then
  echo "❌ Error: pandoc no está instalado. Ejecuta: brew install pandoc"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"
mkdir -p "$COVERS_DIR"

generate() {
  local MD_FILE="$1"
  local COVER_NAME="$2"
  local BASE_NAME
  BASE_NAME=$(basename "$MD_FILE" .md)
  local OUTPUT_PATH="$OUTPUT_DIR/${BASE_NAME}_${TIMESTAMP}.epub"

  echo "🔄 Convirtiendo: $(basename "$MD_FILE")..."

  local PANDOC_ARGS=(
    --output="$OUTPUT_PATH"
    --to=epub3
    --toc
    --toc-depth=2
    --metadata title="$BASE_NAME"
    --metadata author="Rommel Ayala - QA Lead"
    --metadata language="es-ES"
    --syntax-highlighting=espresso
  )

  # Si el usuario no pasó un parámetro de portada explícito, buscamos uno automático
  if [ -z "$COVER_NAME" ]; then
    if [ -f "$COVERS_DIR/${BASE_NAME}.jpg" ]; then
      COVER_NAME="${BASE_NAME}.jpg"
    elif [ -f "$COVERS_DIR/${BASE_NAME}.png" ]; then
      COVER_NAME="${BASE_NAME}.png"
    fi
  fi

  # Validamos y aplicamos la portada si se encontró o fue especificada
  if [ -n "$COVER_NAME" ]; then
    if [ -f "$COVERS_DIR/$COVER_NAME" ]; then
      PANDOC_ARGS+=(--epub-cover-image="$COVERS_DIR/$COVER_NAME")
      echo "🖼️  Usando portada: portadas_draft/$COVER_NAME"
    else
      echo "⚠️  Advertencia: No se encontró '$COVER_NAME' en portadas_draft/. Usando portada por defecto."
    fi
  else
    echo "ℹ️  Sin portada en portadas_draft/ (usando formato por defecto)"
  fi

  pandoc "$MD_FILE" "${PANDOC_ARGS[@]}"

  if [ $? -eq 0 ]; then
    echo "✅ Generado: $OUTPUT_PATH"
  else
    echo "❌ Falló: $(basename "$MD_FILE")"
  fi
}

# Sin argumentos → todos los .md en libros_draft/
if [ -z "$1" ]; then
  FILES=("$DRAFTS_DIR"/*.md)
  if [ ! -e "${FILES[0]}" ]; then
    echo "❌ No hay archivos .md en $DRAFTS_DIR"
    exit 1
  fi
  echo "📚 Procesando todos los borradores..."
  echo ""
  for f in "${FILES[@]}"; do
    generate "$f" ""
    echo ""
  done

# Con argumento → solo ese archivo
else
  MD_FILE="$DRAFTS_DIR/$1"
  COVER_ARG="$2" # El segundo parámetro es la portada
  
  if [ ! -f "$MD_FILE" ]; then
    echo "❌ Error: '$1' no existe en $DRAFTS_DIR"
    echo "📄 Archivos disponibles:"
    ls "$DRAFTS_DIR"/*.md | xargs -I{} basename {}
    exit 1
  fi
  generate "$MD_FILE" "$COVER_ARG"
fi
