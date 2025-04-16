from selenium.webdriver.common.by import By
from dateutil.relativedelta import relativedelta
import time

class BeSSAutomation:
    def __init__(self, driver):
        self.driver = driver

    def get_bess_spectra_url(self, url_bess="http://basebe.obspm.fr/basebe/BeSS/Consul.php"):
        self.driver.get(url_bess)
    
    def input_star(self, star_id: str):
        # Date format: (AAAA-MM-DD)
        star_id_input = self.driver.find_element(By.XPATH, '/html/body/form/div/table/thead/tr[1]/td[2]/input')
        star_id_input.clear()
        star_id_input.send_keys(star_id)

    def input_dates(self, from_date: str, to_date: str):
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
    
    def submit_star(self):
        button_submit = self.driver.find_element(By.XPATH, '/html/body/form/div/input[4]')
        button_submit.click()
    
    def sort_dates_oldest_first(self):
        td_date = self.driver.find_element(By.XPATH, "/html/body/form/div/table/tbody/tr[1]/td[9]/table/tbody/tr[1]/td[2]")
        td_date.find_element(By.XPATH, "/html/body/form/div/table/tbody/tr[1]/td[9]/table/tbody/tr[1]/td[2]/input").click()
    
    def sort_dates_newest_first(self):
        td_date = self.driver.find_element(By.XPATH, "/html/body/form/div/table/tbody/tr[1]/td[9]/table/tbody/tr[2]/td[2]")
        td_date.find_element(By.XPATH, "/html/body/form/div/table/tbody/tr[1]/td[9]/table/tbody/tr[2]/td[2]/input").click()
    
    def next_page(self):
        td_nextpage = self.driver.find_element(By.XPATH, "/html/body/form/div/table/tbody/tr[102]/td[1]")

        td_nextpage.find_element(By.XPATH, "/html/body/form/div/table/tbody/tr[102]/td[1]/input[2]").click()

    def select_all_stars(self):
        tr_download = self.driver.find_elements(By.CSS_SELECTOR, 'tr.amateur, tr.pro')
        
        for tablerow_i in tr_download:
            tablerow_i.find_element(By.CSS_SELECTOR, 'td:last-child').find_element(By.TAG_NAME, 'input').click()

    def download_selection(self):
        download_btn = self.driver.find_element(By.CSS_SELECTOR, 'html body form div table tbody tr td input.bouton')
        download_btn.click()
        time.sleep(4) # Sleep for 4 second. Waiting for the download action

    def terminate(self):
        self.driver.close()
        self.driver.quit()