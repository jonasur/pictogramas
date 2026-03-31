from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import os

def crear_agenda_pdf(lista_imagenes, nombre_pdf):
    ruta_final = os.path.join('static', nombre_pdf)
    c = canvas.Canvas(ruta_final, pagesize=A4)
    ancho_hoja, alto_hoja = A4 # A4 es 21cm x 29.7cm

    # MEDIDAS OBJETIVO
    ancho_p = 6.0 * cm
    alto_p = 6.8 * cm
    separacion = 0.3 * cm # Espacio entre cuadros

    # CÁLCULO PARA CENTRADO PERFECTO
    # El ancho total de los 3 cuadros + sus 2 espacios es:
    ancho_total_contenido = (3 * ancho_p) + (2 * separacion)
    # El margen izquierdo debe ser la mitad de lo que sobra en la hoja
    margen_x = (ancho_hoja - ancho_total_contenido) / 2
    
    # Centrado vertical
    alto_total_contenido = (4 * alto_p) + (3 * separacion)
    margen_y = (alto_hoja - alto_total_contenido) / 2

    x_inicial = margen_x
    y_inicial = alto_hoja - margen_y - alto_p

    for i, img_nombre in enumerate(lista_imagenes):
        ruta_img = os.path.join('static', img_nombre)
        if os.path.exists(ruta_img):
            col = i % 3
            fila = (i // 3) % 4
            
            x = x_inicial + (col * (ancho_p + separacion))
            y = y_inicial - (fila * (alto_p + separacion))

            c.drawImage(ruta_img, x, y, width=ancho_p, height=alto_p)
        
        if (i + 1) % 12 == 0 and (i + 1) < len(lista_imagenes):
            c.showPage()
            y_inicial = alto_hoja - margen_y - alto_p

    c.save()
    return nombre_pdf