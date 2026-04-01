import os
import uuid
from limpiar import borrar_archivos_viejos
from dotenv import load_dotenv
from flask import Flask, render_template, request, session
from pdf_manager import crear_agenda_pdf
from generador import crear_pictograma 

load_dotenv()
debug_mode= os.getenv('DEBUG', 'False') == 'True'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave_local')
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    # Obtenemos la lista de la sesión para que siempre se vea en el HTML
    lista_pdf = session.get('lista_pdf', [])
    return render_template('index.html', lista=lista_pdf)

@app.route('/generar', methods=['POST'])
def generar():
    borrar_archivos_viejos(['uploads', 'static'], horas=24)
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    texto = request.form.get('texto')
    archivo = request.files['imagen']
    color = request.form.get('color_borde')
    
    if archivo:
        extension = os.path.splitext(archivo.filename)[1]
        nombre_unico = str(uuid.uuid4()) + extension
        
        ruta_subida = os.path.join(app.config['UPLOAD_FOLDER'], nombre_unico)
        archivo.save(ruta_subida)
        
        nombre_resultado = "pictogram_" + nombre_unico
        crear_pictograma(ruta_subida, texto, nombre_resultado, color)
        
        # Enviamos la lista actual también aquí para no perder la vista
        lista_pdf = session.get('lista_pdf', [])
        return render_template('index.html', resultado=nombre_resultado, lista=lista_pdf)
    
@app.route('/agregar_a_pdf', methods=['POST'])
def agregar_a_pdf():
    lista_pdf = session.get('lista_pdf', [])
    nombre_img = request.form.get('nombre_imagen')
    
    if nombre_img and nombre_img not in lista_pdf:
        lista_pdf.append(nombre_img)
        session['lista_pdf'] = lista_pdf
        # Forzamos que la sesión se guarde (buena práctica)
        session.modified = True
    
    return render_template('index.html', lista=lista_pdf)

@app.route('/descargar_pdf')
def descargar_pdf():
    lista = session.get('lista_pdf', [])
    if not lista:
        return "No hay imágenes en la lista", 400
    
    # PDF con nombre único para evitar que se crucen entre usuarios
    nombre_final = f"agenda_{uuid.uuid4().hex[:8]}.pdf"
    crear_agenda_pdf(lista, nombre_final)
    
    return render_template('index.html', pdf_listo=nombre_final, lista=lista)

@app.route('/limpiar_lista')
def limpiar_lista():
    # Nueva ruta útil para que el usuario empiece de cero
    session['lista_pdf'] = []
    return render_template('index.html', lista=[])

if __name__ == "__main__":
    # Render usa el puerto 10000 por defecto
    port = int(os.environ.get("PORT", 10000))
    # '0.0.0.0' es obligatorio para que Render pueda ver la app
    app.run(host='0.0.0.0', port=port, debug=debug_mode)