from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from BessAuto import BeSSAutomation

DOWNLOAD_PATH = "/path/to/folder"

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Skip the download alert (optional. You can remove it, 
# but it's annoying for automatizers)
# and set the download path 
params = {'behavior' : 'allow', 'downloadPath': DOWNLOAD_PATH}
driver.execute_cdp_cmd('Page.setDownloadBehavior', params)

# Initialize the object and get the URL
be_auto = BeSSAutomation(driver=driver)
be_auto.get_bess_spectra_url()

# input star id
be_auto.input_star(star_id="59 Cyg")

# Input dates and submit
be_auto.input_dates("2000-01-01", "2002-12-31")
be_auto.submit_star()

# Sort dates and select all
be_auto.sort_dates_oldest_first()
be_auto.select_all_stars()

# Download the selected files
be_auto.download_selection()

be_auto.terminate()