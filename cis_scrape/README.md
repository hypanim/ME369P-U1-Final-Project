# SeleniumCISScrape
Makes use of Selenium to scrape information from The University of Texas' database of Course Instructor Surveys (CIS) from Fall 2005 to Summer 2022.

## Key Files:
CIS_URL_scrape.py: Mass scrapes URLs from CIS database and saves them into file. Said file is found at output_urls.txt and a copy is saved at output_urls-orig.txt.

CIS_load_scrape.py: Mass scrapes information loaded from a .txt file of URLs created via CIS_URL_scrape.py, originally found at output_urls.txt. In practice, the program can be modified to run smaller chunks of URLs found in the output_slices folder.

output_urls.txt: The entire list of URLs for CIS pages within the UT database. Needs a UT EID to access. There's 191,054 surveys in total. In case something happens to the output_urls.txt file, a copy is saved as output_urls-orig.txt.

instructor_data.txt files: Files containing dictionaries of data extracted from the URLs found in the output_urls.txt. The current dataset makes use of 85% of URLs. All processed data will be in this form; use it to help build the GUI around.

## Running the Programs

See the following video and website as a reference for setting up the programs: 

https://www.youtube.com/watch?v=Zrx8FSEo9lk

https://chromedevtools.github.io/devtools-protocol/

In order to run the program and extract data from the surveys, there's four primary steps that must be done first:
1. Install Selenium and Webdriver (https://googlechromelabs.github.io/chrome-for-testing/). Download Python (https://www.python.org/downloads/) if needed and run 'pip install selenium'. Run Webdriver when installed.
2. In your terminal window, change your directory to the Google Chrome application itself. (For me, this is "cd /Applications/Google\ Chrome.app").
3. In your terminal window, run your Chrome application, followed by the remote debugging port information, and then the user data directory you've created for this new debugging window, which can just be an empty folder that Chrome will fill in itself. (For me, this is ""/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222 --user-data-dir=/Users/CadeWetherill/Desktop/dev/ChromeData"). Upon completing this step, a new Google Chrome window should open.
4. Open any UT page and log-in with your UT EID and passcode. You'll need to go through Duo as well. This should keep your log-in cookies saved to this debugging window, allowing you access to the UT database pages with Selenium. Once logged in, the code should be able to be ran based on changing the input values in the CIS_load_scrape.py file. DO NOT CLOSE THIS WINDOW! Both CIS_load_scrape.py and CIS_URL_scrape.py should be run while this window remains open.
