# BeSSAutomation
BeSSAutomation is a Python tool that automates the download of FITS spectra from the Be Star Spectra (BeSS) database. It allows users to programmatically input star names, dates, and other parameters to retrieve spectral data efficiently using a single class with helper functions.

This tool was developed in 2023 during my master's studies to help me manage the workload of collecting large amounts of spectral data from the BeSS database more efficiently.

# Files
`BessAuto.py`:
The core of the project. This file contains the BeSSAutomation class, which includes all the necessary methods to launch the browser, perform searches, parse results, and download the spectra.

`config.py`:
Centralized configuration file for URLs, default browser settings, and timeouts.

`locators.py`:
Centralized locators and selectors using the Page Object Model (POM) to ensure clean separation of HTML selectors from logic.

`example_multiplestars.py`:
A working example script showing how to search and download spectra for multiple Be stars using the automation class.

`example_onestar.py`:
Python script showing how to use the BeSSAutomation class to search one star.

# How to Use

### 1. Installation
Install the required dependencies (Selenium and Webdriver Manager) using pip:
```bash
pip install selenium webdriver-manager
```
*(Or if you are using `uv`, simply run `uv sync` to set up the environment using `pyproject.toml`)*.

### 2. Configuration
You can customize general settings like the default browser (`chrome` or `firefox`), download timeouts, and search URLs in [config.py](file:///d:/jass/BeSSAutomation/config.py):
```python
DEFAULT_BROWSER = "firefox"  # or "chrome"
DOWNLOAD_WAIT_TIME = 4       # time in seconds to wait for download
```

### 3. Running Examples
* **Query a Single Star:**
  Edit the star and date range parameters in [example_onestar.py](file:///d:/jass/BeSSAutomation/example_onestar.py) and run it:
  ```bash
  python example_onestar.py
  ```
  This queries BeSS for the star, sorts and selects all available spectra, downloads them in a zip package, and saves it in the `downloads/` directory.

* **Query Multiple Stars (Sequential Batch):**
  Edit the `STAR_IDS` list in [example_multiplestars.py](file:///d:/jass/BeSSAutomation/example_multiplestars.py) and run it:
  ```bash
  python example_multiplestars.py
  ```
  This handles downloads sequentially, actively waits for each download to complete, and automatically renames the resulting zip files (e.g. `downloads/HD 250163.zip`).

# Requirements
- Python 3.10+
- Selenium 4.0+

# License
MIT License
