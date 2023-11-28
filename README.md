# ME369P-U1-Final-Project
Selenium Final Project for ME369P

Required Libraries (non-native):
- Selenium
  - Install the library via pip:
    - Pip install selenium
- Install Mozilla Firefox:
  - Go to https://www.mozilla.org/en-US/firefox/new/ and install the latest browser for your operating system
- Install the webdriver for Firefox: 
  - Go to https://github.com/mozilla/geckodriver/releases and install the latest version of the driver compatible with the     installed Firefox browser
- NLTK
  - Install via pip:
    - pip install nltk
  - In a python terminal run: 
    - Import nltk
    - nltk.download()
- Numpy, Pandas, PySimpleGUI, Matplotlib, Tqdm
  - Install via pip::
    - Pip install <library name>

Instructions for Running GUI:
- Open the user_interface.py file and click run
- Be patient as the scraped data is loaded before the GUI is displayed

Instructions for updating the database:
- professor_sentiment (Rate My Professor):
  - Edit the rmp_scraper_config.json file to change scraping settings, locations, and urls
  - Run the test_rmpScraper.py file, this will take a long time. Progress is displayed in the terminal via progress bars.
- grade_distribution:
  - Open the UT Reports website and collect the URLs for the .csv files for school years you would like to collect data for.
    - UT Reports website url: https://reports.utexas.edu/spotlight-data/ut-course-grade-distributions
  - Run the grade_scrape.py file with the URL and filename as function parameters
- course_evaluation:
  - TBD

