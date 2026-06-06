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

# Requirements
- Python 3.10+
- Selenium 4.0+

# License
MIT License
