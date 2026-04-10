from PIL import Image, ImageDraw, ImageFont
import os

covers_dir = "portadas_draft"
os.makedirs(covers_dir, exist_ok=True)

books = {
    "agentes-ia-libro": "Agentes IA",
    "claude-uso-maestro": "Claude: Uso Maestro",
    "fundamentos-ia-libro": "Fundamentos IA",
    "gemini-uso-maestro": "Gemini: Uso Maestro",
    "playwright-ts-intermedio-avanzado": "Playwright TS (Intermedio-Avanzado)",
    "skills-libro": "Skills"
}

width, height = 600, 800
bg_color = "#151515" # Gris casi negro, muy sobrio y elegante
text_color = "#EAEAEA" # Blanco hueso suave, no lastima la vista
accent_color = "#4A4A4A" # Gris medio para la línea y copyright
copyright_text = "© Rommel Ayala - All rights reserved"

for filename, title in books.items():
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Intenta cargar fuentes del sistema en macOS
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 42)
        footer_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except IOError:
        title_font = ImageFont.load_default()
        footer_font = ImageFont.load_default()
        
    # Dibujar título principal centrado
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    title_h = title_bbox[3] - title_bbox[1]
    
    # Posición central, ligeramente hacia arriba (regla de los tercios)
    draw.text(((width - title_w) / 2, (height / 2) - 60), title, font=title_font, fill=text_color)
    
    # Dibujar línea horizontal fina (minimalista)
    line_y = height - 100
    # Línea un poco más estrecha que el ancho total para dar margen
    draw.line([(100, line_y), (width - 100, line_y)], fill=accent_color, width=1)
    
    # Dibujar texto de copyright centrado debajo de la línea
    copy_bbox = draw.textbbox((0, 0), copyright_text, font=footer_font)
    copy_w = copy_bbox[2] - copy_bbox[0]
    draw.text(((width - copy_w) / 2, line_y + 25), copyright_text, font=footer_font, fill=accent_color)
    
    # Guardar con alta calidad
    img.save(os.path.join(covers_dir, f"{filename}.jpg"), quality=95)
    print(f"Generada portada minimalista: {filename}.jpg")
