from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import os
from BessAuto import BeSSAutomation

DOWNLOAD_PATH = "/home/jassir/Projects"
BESS_FILE = "BeSS_multidownload.zip"

# Stars ids 
star_idxs = ["HD 250163", "HD 36665", "HD 250028"]

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
for star_idx in star_idxs:
    be_auto.input_star(star_id=star_idx)

    # Input dates and submit
    be_auto.input_dates("2000-01-01", "2020-12-31")
    be_auto.submit_star()

    # Sort dates and select all
    be_auto.sort_dates_oldest_first()
    be_auto.select_all_stars()

    # Download the selected files
    be_auto.download_selection()

    rename_bess_file = os.path.join(DOWNLOAD_PATH, BESS_FILE)
    newname_bess_file = os.path.join(DOWNLOAD_PATH, star_idx)

    # Rename the file
    if os.path.exists(rename_bess_file):
        os.rename(rename_bess_file, newname_bess_file)
        print(f"File renamed to: {newname_bess_file}")
    else:
        print("File not found. Maybe the download is still in progress?")

    # Get back to the main URL to start the search again
    be_auto.get_bess_spectra_url()


be_auto.terminate()