# ME369P-U1-Final-Project
**Selenium Final Project for ME369P**

**Required Libraries (non-native):**
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
    - Pip install \<library name>

**Instructions for Running GUI:**
- Open the user_interface.py file and click run
- Be patient as the scraped data is loaded before the GUI is displayed

**Instructions for updating the database:**
- professor_sentiment (Rate My Professor):
  - Edit the rmp_scraper_config.json file to change scraping settings, locations, and urls
      - universityURL: This is where the scraper looks for the professors from. Each university has their unique number.
      - multithreading_enabled: Set to true to enable multithreading. Spawns the number of threads that thread_count is set to.
      - headless: Runs the scraper in a headless manner.
      - professorURL_file: The name of the file for the list of all professor urls for a given university to be stored. Does not need to be changed.
      - sentimentAnalysis_enabled: Setting to true uses the Vader model to perfrom sentiment analysis on the comments.
      - data_directory: The name of the directory for saving scraped professor data. Does not need to be changed.
      - admin_directory: The name of hte directory for saving the error_file, finished_file, and professorURL_file. Does not need to be changed.
      - thread_count: The number of threads that you want spawned if multithreading_enabled is true. Be careful not to make this number too high or crashing may occur.
      - error_file: name of the file to store any professor urls that the scraper had an issue scraping. Can be due to a variety of reasons. Does not need to be changed.
      - finished_file: name of the file to store all professor urls that are successfully stored. Does not need to be changed.
  - Run the test_rmpScraper.py file, this will take a long time. Progress is displayed in the terminal via progress bars.
- grade_distribution:
  - Open the UT Reports website and collect the URLs for the .csv files for school years you would like to collect data for.
    - UT Reports website url: https://reports.utexas.edu/spotlight-data/ut-course-grade-distributions
  - Run the grade_scrape.py file with the URL and filename as function parameters
- course_evaluation:
  - TBD

