import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BeSSAutomation:
    """
    Clase para automatizar la interacción con la base de datos BeSS (Be Star Spectra).
    Permite buscar espectros por estrella, filtrar por fechas y descargar resultados.
    """
    def __init__(self, driver):
        """
        Inicializa la clase con un driver de Selenium.
        
        Args:
            driver: Instancia de WebDriver de Selenium.
        """
        self.driver = driver

    def get_bess_spectra_url(self, url_bess="http://basebe.obspm.fr/basebe/BeSS/Consul.php"):
        """
        Navega a la URL de consulta de BeSS.
        
        Args:
            url_bess (str): URL de la página de consulta. Por defecto la de Spectra.
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
            star_id_input = self.driver.find_element(By.XPATH, '/html/body/form/div/table/thead/tr[1]/td[2]/input')
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
            # Input star initial date
            star_ini_date = self.driver.find_element(By.XPATH, 
                                                     '/html/body/form/div/table/tbody[4]/tr/td[2]/input[1]')
            star_ini_date.clear()
            star_ini_date.send_keys(from_date)

            # Input star final date
            star_fin_date = self.driver.find_element(By.XPATH, 
                                                     '/html/body/form/div/table/tbody[4]/tr/td[2]/input[2]') 
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
            button_submit = self.driver.find_element(By.XPATH, '/html/body/form/div/input[4]')
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
            td_date = self.driver.find_element(By.XPATH, "/html/body/form/div/table/tbody/tr[1]/td[9]/table/tbody/tr[1]/td[2]")
            td_date.find_element(By.XPATH, "/html/body/form/div/table/tbody/tr[1]/td[9]/table/tbody/tr[1]/td[2]/input").click()
        except NoSuchElementException:
            logger.error("No se encontró el elemento para ordenar (más antiguo).")
            # En este caso podríamos solo avisar y no lanzar excepción si no es crítico
        except Exception as e:
            logger.error(f"Error al ordenar por fecha antigua: {e}")
    
    def sort_dates_newest_first(self):
        """
        Ordena los resultados de los espectros por fecha, del más reciente al más antiguo.
        """
        try:
            logger.info("Ordenando resultados por fecha (más reciente primero)...")
            td_date = self.driver.find_element(By.XPATH, "/html/body/form/div/table/tbody/tr[1]/td[9]/table/tbody/tr[2]/td[2]")
            td_date.find_element(By.XPATH, "/html/body/form/div/table/tbody/tr[1]/td[9]/table/tbody/tr[2]/td[2]/input").click()
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
            td_nextpage = self.driver.find_element(By.XPATH, "/html/body/form/div/table/tbody/tr[102]/td[1]")
            td_nextpage.find_element(By.XPATH, "/html/body/form/div/table/tbody/tr[102]/td[1]/input[2]").click()
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
            tr_download = self.driver.find_elements(By.CSS_SELECTOR, 'tr.amateur, tr.pro')
            
            if not tr_download:
                logger.warning("No se encontraron espectros para seleccionar en esta página.")
                return

            for tablerow_i in tr_download:
                tablerow_i.find_element(By.CSS_SELECTOR, 'td:last-child').find_element(By.TAG_NAME, 'input').click()
        except Exception as e:
            logger.error(f"Error al seleccionar estrellas: {e}")

    def download_selection(self):
        """
        Inicia la descarga de todos los espectros seleccionados.
        """
        try:
            logger.info("Iniciando descarga de selección...")
            download_btn = self.driver.find_element(By.CSS_SELECTOR, 'html body form div table tbody tr td input.bouton')
            download_btn.click()
            time.sleep(4) # Espera 4 segundos para que se complete la descarga
        except NoSuchElementException:
            logger.error("No se encontró el botón de descarga.")
        except Exception as e:
            logger.error(f"Error durante la descarga: {e}")

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