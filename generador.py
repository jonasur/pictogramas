from PIL import Image, ImageDraw, ImageFont, ExifTags
import os

def corregir_orientacion(img):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation': break
        exif = dict(img._getexif().items())
        if exif[orientation] == 3: img = img.rotate(180, expand=True)
        elif exif[orientation] == 6: img = img.rotate(270, expand=True)
        elif exif[orientation] == 8: img = img.rotate(90, expand=True)
    except: pass
    return img

def crear_pictograma(ruta_imagen, texto, nombre_salida, color_borde="black"):
    # 1. Cargar y corregir rotación
    img_orig = Image.open(ruta_imagen)
    img_orig = corregir_orientacion(img_orig)

    # 2. DIMENSIONES FIJAS EN PÍXELES (Para asegurar proporción 6:6.8)
    # Usamos 600px de ancho y 680px de alto.
    ancho_px = 600
    alto_px = 680
    alto_foto_px = 600 # La foto será un cuadrado perfecto de 600x600

    # 3. Preparar la foto (Center Crop a 600x600)
    w, h = img_orig.size
    min_dim = min(w, h)
    img_cuadrada = img_orig.crop(((w-min_dim)/2, (h-min_dim)/2, (w+min_dim)/2, (h+min_dim)/2))
    img_redimensionada = img_cuadrada.resize((ancho_px, alto_foto_px), Image.Resampling.LANCZOS)
    
    # 4. Crear Lienzo Final
    lienzo = Image.new('RGB', (ancho_px, alto_px), 'white')
    lienzo.paste(img_redimensionada, (0, 0))
    
    # 5. Dibujar MARCO ÚNICO
    dibujo = ImageDraw.Draw(lienzo)
    # Grosor de 15px (equivale a unos 1.5mm - 2mm en el papel)
    grosor = 15 
    
    # Rectángulo exterior
    dibujo.rectangle([0, 0, ancho_px - 1, alto_px - 1], outline=color_borde, width=grosor)
    # Línea divisoria entre foto y texto
    dibujo.line([(0, alto_foto_px), (ancho_px, alto_foto_px)], fill=color_borde, width=grosor)

    # 6. Texto Dinámico
    espacio_texto = alto_px - alto_foto_px
    tamanio_fuente = int(espacio_texto * 0.5)
    try:
        fuente = ImageFont.truetype("fuente.ttf", tamanio_fuente)
    except:
        fuente = ImageFont.load_default()

    texto = texto.upper()
    ancho_max_texto = ancho_px * 0.85

    while True:
        bbox = dibujo.textbbox((0, 0), texto, font=fuente)
        w_t = bbox[2] - bbox[0]
        if w_t <= ancho_max_texto or tamanio_fuente <= 12:
            break
        tamanio_fuente -= 2
        try: fuente = ImageFont.truetype("fuente.ttf", tamanio_fuente)
        except: break

    # 7. Centrar Texto
    h_t = bbox[3] - bbox[1]
    x_t = (ancho_px - w_t) / 2
    y_t = alto_foto_px + (espacio_texto - h_t) / 2 - 5
    
    dibujo.text((x_t, y_t), texto, fill="black", font=fuente)

    # Guardar
    ruta_final = os.path.join('static', nombre_salida)
    lienzo.save(ruta_final)
    return nombre_salida