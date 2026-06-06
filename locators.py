from selenium.webdriver.common.by import By

class BeSSLocators:
    """
    Clase para centralizar todos los selectores (XPaths, CSS, etc.) de la web de BeSS.
    Sigue el patrón Page Object Model (POM).
    """
    
    # Selectores del formulario de búsqueda
    STAR_ID_INPUT = (By.NAME, 'req_objet')
    DATE_FROM_INPUT = (By.NAME, 'req_date§min')
    DATE_TO_INPUT = (By.NAME, 'req_date§max')
    SUBMIT_BUTTON = (By.NAME, 'submit')
    
    # Selectores de ordenamiento (hjdp = oldest first, hjdm = newest first)
    SORT_OLDEST_BTN = (By.NAME, 'req_tri_hjdp')
    SORT_NEWEST_BTN = (By.NAME, 'req_tri_hjdm')
    
    # Navegación y Selección
    NEXT_PAGE_BUTTON = (By.NAME, 'next')
    SPECTRA_ROWS = (By.CSS_SELECTOR, 'tr.amateur, tr.pro')
    SELECT_CHECKBOX = (By.NAME, 'check[]')
    
    # Descarga
    DOWNLOAD_BUTTON = (By.NAME, 'multidownload')
