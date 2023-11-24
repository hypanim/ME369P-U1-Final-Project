# imports
from selenium import webdriver
import time
import os
import glob

report_url = "https://iq-analytics.austin.utexas.edu/views/Gradedistributiondashboard/Externaldashboard-Crosstab"

# pass in year_name (ex: 2010_2011) and **direct link** to the grade distribution website
# ex: use the report_url link above and navigate to the respective grade distribution w/ the tableau dashboard
def grade_scrape(year_name, website_url):
    # get /data directory
    curr_directory = os.path.dirname(os.path.realpath(__file__))
    grade_data_path = os.path.join(curr_directory, 'data/')

    # set default download path
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': grade_data_path}
    chrome_options.add_experimental_option('prefs', prefs)

    # create web driver
    driver = webdriver.Chrome(options=chrome_options)

    # grab data
    driver.get(website_url)

    # wait for file to download
    time.sleep(10)

    # cleanup filename - grab most recent file and update it to year_name
    list_of_files = glob.glob(grade_data_path + '*.csv')
    latest_file = max(list_of_files, key=os.path.getctime)
    os.rename(latest_file, grade_data_path + year_name + '.csv')