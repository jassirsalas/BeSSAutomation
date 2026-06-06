import os
from BessAuto import BeSSAutomation
from config import DEFAULT_BROWSER

# --- CONFIGURACIÓN ---
DOWNLOAD_PATH = os.path.abspath("downloads")
STAR_ID = "59 Cyg"
FROM_DATE = "2000-01-01"
TO_DATE = "2002-12-31"

# Puedes cambiar 'DEFAULT_BROWSER' por 'chrome' o 'firefox' aquí directamente
BROWSER = DEFAULT_BROWSER 

def main():
    # 1. Crear el driver centralizado con la ruta de descarga y navegador elegido
    try:
        driver = BeSSAutomation.create_driver(DOWNLOAD_PATH, browser=BROWSER)
    except Exception as e:
        print(f"Error al inicializar el navegador {BROWSER}: {e}")
        return
    
    try:
        # 2. Inicializar la automatización
        be_auto = BeSSAutomation(driver=driver)
        
        # 3. Procesar la estrella
        be_auto.process_star(STAR_ID, FROM_DATE, TO_DATE)
        
    finally:
        # 4. Cerrar siempre el navegador al finalizar
        if 'be_auto' in locals():
            be_auto.terminate()

if __name__ == "__main__":
    main()