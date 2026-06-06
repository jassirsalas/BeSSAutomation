import logging
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoSuchElementException, WebDriverException

# Importaciones locales para POM y configuración
from config import BESS_CONSULT_URL, DOWNLOAD_WAIT_TIME, DEFAULT_BROWSER
from locators import BeSSLocators

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BeSSAutomation:
    """
    Clase para automatizar la interacción con la base de datos BeSS (Be Star Spectra).
    Implementa el patrón Page Object Model (POM) separando selectores y lógica.
    """
    def __init__(self, driver):
        """
        Inicializa la clase con un driver de Selenium.
        
        Args:
            driver: Instancia de WebDriver de Selenium.
        """
        self.driver = driver

    @staticmethod
    def create_driver(download_path, browser=DEFAULT_BROWSER):
        """
        Crea e inicializa una instancia de WebDriver (Chrome o Firefox) con configuraciones optimizadas.
        
        Args:
            download_path (str): Ruta absoluta donde se guardarán las descargas.
            browser (str): El navegador a utilizar ('chrome' o 'firefox').
            
        Returns:
            WebDriver: Instancia configurada del navegador.
        """
        abs_download_path = os.path.abspath(download_path)
        
        # Asegurar que el directorio de descarga existe
        if not os.path.exists(abs_download_path):
            os.makedirs(abs_download_path)
            logger.info(f"Directorio creado: {abs_download_path}")

        if browser.lower() == "chrome":
            logger.info("Iniciando Chrome...")
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )
            # Configurar comportamiento de descarga para Chrome
            params = {'behavior': 'allow', 'downloadPath': abs_download_path}
            driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
            
        elif browser.lower() == "firefox":
            logger.info("Iniciando Firefox...")
            options = FirefoxOptions()
            # Configuración de descargas para Firefox
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.dir", abs_download_path)
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/fits, text/plain")
            
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )
        else:
            raise ValueError(f"Navegador no soportado: {browser}. Usa 'chrome' o 'firefox'.")
            
        return driver

    def get_bess_spectra_url(self, url_bess=BESS_CONSULT_URL):
        """
        Navega a la URL de consulta de BeSS.
        
        Args:
            url_bess (str): URL de la página de consulta. Por defecto usa la constante configurada.
        """
        try:
            logger.info(f"Navegando a la URL: {url_bess}")
            self.driver.get(url_bess)
        except WebDriverException as e:
            logger.error(f"Error al intentar acceder a la URL: {e}")
            raise

    def input_star(self, star_id: str):
        """
        Ingresa el nombre o identificador de la estrella en el campo de búsqueda.
        
        Args:
            star_id (str): Identificador de la estrella (ej: 'Gamma Cas').
        """
        try:
            logger.info(f"Ingresando estrella: {star_id}")
            star_id_input = self.driver.find_element(*BeSSLocators.STAR_ID_INPUT)
            star_id_input.clear()
            star_id_input.send_keys(star_id)
        except NoSuchElementException:
            logger.error("No se encontró el campo de búsqueda de estrellas.")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al ingresar la estrella: {e}")
            raise

    def input_dates(self, from_date: str, to_date: str):
        """
        Configura el rango de fechas para la búsqueda de espectros.
        
        Args:
            from_date (str): Fecha inicial en formato AAAA-MM-DD.
            to_date (str): Fecha final en formato AAAA-MM-DD.
        """
        try:
            logger.info(f"Configurando rango de fechas: {from_date} a {to_date}")
            
            star_ini_date = self.driver.find_element(*BeSSLocators.DATE_FROM_INPUT)
            star_ini_date.clear()
            star_ini_date.send_keys(from_date)

            star_fin_date = self.driver.find_element(*BeSSLocators.DATE_TO_INPUT) 
            star_fin_date.clear()
            star_fin_date.send_keys(to_date)
            
        except NoSuchElementException:
            logger.error("No se encontraron los campos de fecha.")
            raise
        except Exception as e:
            logger.error(f"Error al ingresar las fechas: {e}")
            raise
    
    def submit_star(self):
        """
        Envía el formulario de búsqueda para obtener la lista de espectros.
        """
        try:
            logger.info("Enviando formulario de búsqueda...")
            button_submit = self.driver.find_element(*BeSSLocators.SUBMIT_BUTTON)
            button_submit.click()
        except NoSuchElementException:
            logger.error("No se encontró el botón de enviar (submit).")
            raise
        except Exception as e:
            logger.error(f"Error al enviar el formulario: {e}")
            raise
    
    def sort_dates_oldest_first(self):
        """
        Ordena los resultados de los espectros por fecha, del más antiguo al más reciente.
        """
        try:
            logger.info("Ordenando resultados por fecha (más antiguo primero)...")
            self.driver.find_element(*BeSSLocators.SORT_OLDEST_BTN).click()
        except NoSuchElementException:
            logger.error("No se encontró el elemento para ordenar (más antiguo).")
        except Exception as e:
            logger.error(f"Error al ordenar por fecha antigua: {e}")
    
    def sort_dates_newest_first(self):
        """
        Ordena los resultados de los espectros por fecha, del más reciente al más antiguo.
        """
        try:
            logger.info("Ordenando resultados por fecha (más reciente primero)...")
            self.driver.find_element(*BeSSLocators.SORT_NEWEST_BTN).click()
        except NoSuchElementException:
            logger.error("No se encontró el elemento para ordenar (más reciente).")
        except Exception as e:
            logger.error(f"Error al ordenar por fecha reciente: {e}")
    
    def next_page(self):
        """
        Navega a la siguiente página de resultados (si existe).
        """
        try:
            logger.info("Navegando a la siguiente página...")
            self.driver.find_element(*BeSSLocators.NEXT_PAGE_BUTTON).click()
        except NoSuchElementException:
            logger.warning("No hay más páginas disponibles o no se encontró el botón de siguiente.")
        except Exception as e:
            logger.error(f"Error al navegar a la siguiente página: {e}")

    def select_all_stars(self):
        """
        Marca todos los espectros visibles en la página actual para su descarga.
        """
        try:
            logger.info("Seleccionando todos los espectros disponibles en la página...")
            checkboxes = self.driver.find_elements(*BeSSLocators.SELECT_CHECKBOX)
            
            if not checkboxes:
                logger.warning("No se encontraron espectros para seleccionar en esta página.")
                return

            for cb in checkboxes:
                if not cb.is_selected():
                    cb.click()
        except Exception as e:
            logger.error(f"Error al seleccionar estrellas: {e}")

    def download_selection(self):
        """
        Inicia la descarga de todos los espectros seleccionados.
        """
        try:
            logger.info("Iniciando descarga de selección...")
            download_btn = self.driver.find_element(*BeSSLocators.DOWNLOAD_BUTTON)
            download_btn.click()
            time.sleep(DOWNLOAD_WAIT_TIME) # Usando la constante configurada
        except NoSuchElementException:
            logger.error("No se encontró el botón de descarga.")
        except Exception as e:
            logger.error(f"Error durante la descarga: {e}")

    def process_star(self, star_id, start_date, end_date):
        """
        Flujo completo para procesar una sola estrella: buscar, filtrar, ordenar y descargar.
        
        Args:
            star_id (str): Identificador de la estrella.
            start_date (str): Fecha inicial (AAAA-MM-DD).
            end_date (str): Fecha final (AAAA-MM-DD).
        """
        try:
            logger.info(f"--- Procesando estrella: {star_id} ---")
            self.get_bess_spectra_url()
            self.input_star(star_id)
            self.input_dates(start_date, end_date)
            self.submit_star()
            self.sort_dates_oldest_first()
            self.select_all_stars()
            self.download_selection()
            logger.info(f"--- Finalizado proceso para: {star_id} ---")
        except Exception as e:
            logger.error(f"Error procesando la estrella {star_id}: {e}")
            # No re-lanzamos para permitir que bucles externos continúen si es necesario

    def terminate(self):
        """
        Cierra el navegador y finaliza la sesión del driver.
        """
        try:
            logger.info("Cerrando el navegador...")
            self.driver.close()
            self.driver.quit()
        except Exception as e:
            logger.warning(f"Error al cerrar el navegador: {e}")