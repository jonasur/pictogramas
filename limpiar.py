import os
import time

def borrar_archivos_viejos(carpetas, horas=24):
    ahora = time.time()
    limite = ahora - (horas * 3600) # Convertimos horas a segundos
    

    for carpeta in carpetas:
        if not os.path.exists(carpeta):
            continue
            
        for archivo in os.listdir(carpeta):
            ruta_completa = os.path.join(carpeta, archivo)
            
            # Verificamos la fecha de última modificación
            if os.path.getmtime(ruta_completa) < limite:
                try:
                    os.remove(ruta_completa)
                    print(f"🗑️ Borrado por antigüedad: {archivo}")
                except Exception as e:
                    print(f"❌ Error al borrar {archivo}: {e}")

# Prueba manual
if __name__ == "__main__":
    borrar_archivos_viejos(['uploads', 'static'], horas=24)
    