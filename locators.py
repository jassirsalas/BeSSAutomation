from selenium.webdriver.common.by import By

class BeSSLocators:
    """
    Clase para centralizar todos los selectores (XPaths, CSS, etc.) de la web de BeSS.
    Sigue el patrón Page Object Model (POM).
    """
    
    # Selectores del formulario de búsqueda
    STAR_ID_INPUT = (By.XPATH, '/html/body/form/div/table/thead/tr[1]/td[2]/input')
    DATE_FROM_INPUT = (By.XPATH, '/html/body/form/div/table/tbody[4]/tr/td[2]/input[1]')
    DATE_TO_INPUT = (By.XPATH, '/html/body/form/div/table/tbody[4]/tr/td[2]/input[2]')
    SUBMIT_BUTTON = (By.XPATH, '/html/body/form/div/input[4]')
    
    # Selectores de ordenamiento
    SORT_OLDEST_BTN = (By.XPATH, "/html/body/form/div/table/tbody/tr[1]/td[9]/table/tbody/tr[1]/td[2]/input")
    SORT_NEWEST_BTN = (By.XPATH, "/html/body/form/div/table/tbody/tr[1]/td[9]/table/tbody/tr[2]/td[2]/input")
    
    # Navegación y Selección
    NEXT_PAGE_BUTTON = (By.XPATH, "/html/body/form/div/table/tbody/tr[102]/td[1]/input[2]")
    SPECTRA_ROWS = (By.CSS_SELECTOR, 'tr.amateur, tr.pro')
    SELECT_CHECKBOX = (By.CSS_SELECTOR, 'td:last-child input')
    
    # Descarga
    DOWNLOAD_BUTTON = (By.CSS_SELECTOR, 'html body form div table tbody tr td input.bouton')
