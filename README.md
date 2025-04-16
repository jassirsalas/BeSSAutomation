# BeSSAutomation
BeSSAutomation is a Python tool that automates the download of FITS spectra from the Be Star Spectra (BeSS) database. It allows users to programmatically input star names, dates, and other parameters to retrieve spectral data efficiently using a single class with helper functions.

This tool was developed in 2023 during my master's studies to help me manage the workload of collecting large amounts of spectral data from the BeSS database more efficiently.

# Files
`BessAuto.py`:
The core of the project. This file contains the BeSSAutomation class, which includes all the necessary methods to launch the browser, perform searches, parse results, and download the spectra.

`example_multiplestars.py`:
A working example script showing how to search and download spectra for multiple Be star using the automation class.

`example_onestars.py`:
Python script showing how to use the BesSSAutomation class to search one star.

# Requirements
- Python 3.10+
- Selenium

# License
MIT License
