from selenium import webdriver
from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import numpy as np
import re
import json
import tqdm
import pickle
import os
from pathlib import Path

class universityScraper:
    def __init__(self):
        #loading config json
        with open("rmp_scraper_config.json") as config_file:
            config_data = json.load(config_file)
            self.universityURL = config_data['universityURL']
            self.multithreading_enabled = config_data['multithreading_enabled']
            self.headless = config_data['headless']
            self.professorURL_file = config_data['professorURL_file']
            self.data_directory = config_data['data_directory']
            self.admin_directory = config_data['admin_directory']
            self.finished_file = config_data['finished_file']
            self.error_file = config_data['error_file']
        
        #handling the path
        self.script_dir = os.path.dirname(__file__)
        #making directory for administration files
        file = Path(os.path.join(self.script_dir, self.admin_directory, 'filler.txt'))
        file.parent.mkdir(parents=True, exist_ok=True)

        self.professorURL_file = os.path.join(self.script_dir, self.admin_directory, self.professorURL_file)

        #creating driver
        print("loading driver")
        if self.headless:
            options = Options()
            options.add_argument("-headless")
            self.driver = webdriver.Firefox(options=options)
        else:
            self.driver = webdriver.Firefox()
        print("driver loaded")

    def __del__(self):
        #destructor for quitting the driver
        self.driver.quit()
    
    def getProfessors(self):
        #getting the url of the university using the driver
        self.driver.get(self.universityURL)
        #close cookies, if any
        self.closeCookies()

        #get professor count
        professor_count = self.driver.find_element(By.XPATH, "//h1[starts-with(@data-testid, 'pagination-header')]")
        professor_number = int(professor_count.text.split()[0])
        print(f'professor count is {professor_number}') #delete later

        #determining the number of reloads needed
        if professor_number >8:
            reloads_needed = int(np.ceil((professor_number-8)/8))
        else:
            reloads_needed = 0
        print(f'reloads needed: {reloads_needed}')

        #load all expected professors
        try:
            #objects needed
            load_more_button = self.driver.find_element(By.XPATH, "//button[starts-with(@class, 'Buttons__Button-sc')]")
            wait = WebDriverWait(self.driver, timeout = 3)

            #progress bar using tqdm
            progressbar = tqdm.tqdm(range(reloads_needed), desc="Loading…", ascii=False, ncols=75)

            for i in progressbar:
                #scrolling offset found manually
                y_scroll_offset = 80
                wait.until(lambda d : load_more_button.is_displayed())
                button_y_position = load_more_button.rect['y']-y_scroll_offset
                self.driver.execute_script(f"window.scrollTo(0, {button_y_position})")
                load_more_button.click()
        except NoSuchElementException:
            print('no more loads available')

        #scrape all professor urls
        teacher_cards = self.driver.find_elements(By.XPATH, "//a[starts-with(@class, 'TeacherCard__StyledTeacherCard')]")
        self.professor_urls=[]
        for i in teacher_cards:
            self.professor_urls.append(i.get_attribute("href"))

        #save to csv
        self.saveProfessors()

        #testing outputs
        print(f'the number of professor urls is {len(self.professor_urls)}')
        print(f'professor urls: {self.professor_urls}') #delete later

    def saveProfessors(self):
        #writing to pickle file
        with open(self.professorURL_file, 'wb') as fp:
            pickle.dump(self.professor_urls, fp)

    def closeCookies(self):
        try:
            self.driver.find_element(By.XPATH, "//div[starts-with(@class, 'FullPageModal__')]//button").click()
        except NoSuchElementException:
            print('no popup found')

