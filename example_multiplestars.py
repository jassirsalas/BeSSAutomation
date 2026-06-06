import os
import time
import logging
from BessAuto import BeSSAutomation
from config import DEFAULT_BROWSER

# Configuración básica de logging para el script de ejemplo
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DOWNLOAD_PATH = os.path.abspath("downloads")
BESS_FILE = "BeSS_multidownload.zip"
STAR_IDS = ["HD 250163", "HD 36665", "HD 250028"]
BROWSER = DEFAULT_BROWSER

def wait_for_download(download_dir, filename, timeout=30):
    """
    Espera de forma activa a que termine la descarga del archivo especificado,
    asegurando que no existan archivos temporales asociados (.crdownload o .part).
    """
    filepath = os.path.join(download_dir, filename)
    part_filepath_cr = filepath + ".crdownload"
    part_filepath_ff = filepath + ".part"
    
    start_time = time.time()
    logger.info(f"Esperando descarga de {filename}...")
    while time.time() - start_time < timeout:
        if os.path.exists(filepath):
            # Verificar si existen archivos temporales activos de descarga
            if not os.path.exists(part_filepath_cr) and not os.path.exists(part_filepath_ff):
                time.sleep(1)  # Pequeño margen para finalización de escritura en disco
                return True
        time.sleep(1)
    return False

def cleanup_download_file(download_dir, filename):
    """
    Elimina cualquier archivo zip de descarga previa para evitar colisiones de nombres
    o que el navegador lo renombre automáticamente (ej. a BeSS_multidownload(1).zip).
    """
    filepath = os.path.join(download_dir, filename)
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
            logger.info(f"Limpieza: archivo preexistente eliminado: {filepath}")
        except Exception as e:
            logger.warning(f"No se pudo eliminar el archivo preexistente {filepath}: {e}")

def main():
    # 1. Inicializar el driver de Selenium usando la función centralizada
    try:
        driver = BeSSAutomation.create_driver(DOWNLOAD_PATH, browser=BROWSER)
    except Exception as e:
        logger.error(f"Error al inicializar el navegador {BROWSER}: {e}")
        return

    try:
        be_auto = BeSSAutomation(driver=driver)
        
        for idx, star_id in enumerate(STAR_IDS, 1):
            logger.info(f"\n==========================================")
            logger.info(f"Procesando estrella {idx} de {len(STAR_IDS)}: {star_id}")
            logger.info(f"==========================================")
            
            try:
                # 2. Limpiar descargas anteriores del archivo objetivo
                cleanup_download_file(DOWNLOAD_PATH, BESS_FILE)
                
                # 3. Procesar la estrella usando el flujo POM
                # Fechas de ejemplo en este caso de múltiples estrellas
                be_auto.process_star(star_id, "2000-01-01", "2020-12-31")
                
                # 4. Esperar a que la descarga finalice
                if wait_for_download(DOWNLOAD_PATH, BESS_FILE, timeout=45):
                    # 5. Renombrar el archivo descargado
                    rename_bess_file = os.path.join(DOWNLOAD_PATH, BESS_FILE)
                    newname_bess_file = os.path.join(DOWNLOAD_PATH, f"{star_id}.zip")
                    
                    # Si ya existe un archivo con el nombre final de la estrella, lo removemos antes
                    if os.path.exists(newname_bess_file):
                        os.remove(newname_bess_file)
                        
                    os.rename(rename_bess_file, newname_bess_file)
                    logger.info(f"¡Éxito! Archivo renombrado a: {newname_bess_file}")
                else:
                    logger.error(f"Error: La descarga de {star_id} superó el tiempo de espera.")
                    
            except Exception as e:
                logger.error(f"Ocurrió un error al procesar {star_id}: {e}")
                
            # Volver a la URL de consulta antes de la siguiente estrella (por seguridad)
            try:
                be_auto.get_bess_spectra_url()
            except Exception as e:
                logger.warning(f"No se pudo retornar a la URL de consulta: {e}")

    finally:
        # 6. Terminar la sesión del driver
        if 'be_auto' in locals():
            be_auto.terminate()

if __name__ == "__main__":
    main()