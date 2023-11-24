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
import pandas as pd
import pickle
from nltk.sentiment import SentimentIntensityAnalyzer
import os
from pathlib import Path
import threading

class professorScraper:
    def __init__(self):
        #loading config json
        with open("rmp_scraper_config.json") as config_file:
            config_data = json.load(config_file)
            self.universityURL = config_data['universityURL']
            self.multithreading_enabled = config_data['multithreading_enabled']
            self.headless = config_data['headless']
            self.professorURL_file = config_data['professorURL_file']
            self.sentimentAnalysis_enabled = config_data['sentimentAnalysis_enabled']
            self.data_directory = config_data['data_directory']
            self.admin_directory = config_data['admin_directory']
            self.thread_count = config_data['thread_count']
            self.finished_file = config_data['finished_file']
            self.error_file = config_data['error_file']
        
        
        #handling the path
        self.script_dir = os.path.dirname(__file__)
        #making directory for data files
        file = Path(os.path.join(self.script_dir, self.data_directory, 'filler.txt'))
        file.parent.mkdir(parents=True, exist_ok=True)

        self.professorURL_file = os.path.join(self.script_dir, self.admin_directory, self.professorURL_file)
        self.finished_file = os.path.join(self.script_dir, self.admin_directory, self.finished_file)
        self.error_file = os.path.join(self.script_dir, self.admin_directory, self.error_file)

        try:
            #load old finished files
            with open(self.finished_file, 'rb') as fp:
                self.finished_file_list = pickle.load(fp)
            
            #load old error files
            with open(self.error_file, 'rb') as fp:
                self.error_file_list = pickle.load(fp)
        except FileNotFoundError:
            print('finished and read file not yet created')
            self.finished_file_list = []
            self.error_file_list = []

        #load the professor urls pickle file
        with open(self.professorURL_file, 'rb') as fp:
            self.professor_urls = pickle.load(fp)

    def closeCookies(self, driver):
        try:
            close_button = driver.find_element(By.XPATH, "//div[starts-with(@class, 'FullPageModal__')]//button")
            wait = WebDriverWait(driver, timeout = 3)
            wait.until(lambda d : close_button.is_displayed())
            close_button.click()
        except NoSuchElementException:
            pass
        
    def getReviews(self):
        if self.multithreading_enabled:
            self.scrapeReviewsMultithreaded()
        else:
            self.scrapeReviews()

    def scrapeReviewsMultithreaded(self):
        #mutex locks
        professorURL_lock = threading.Lock()
        error_lock = threading.Lock()
        finished_lock = threading.Lock()
        total_num_URL = len(self.professor_urls)

        #creating threads
        print(f'number of scraping threads: {self.thread_count}')
        threads = []
        threads.append(threading.Thread(target=self.continuousPickling, args=(professorURL_lock, error_lock, finished_lock)))
        threads.append(threading.Thread(target=self.multithreadingProgress, args=(total_num_URL, professorURL_lock)))
        for i in range(self.thread_count):
            threads.append(threading.Thread(target=self.scrapeThread, args=(professorURL_lock, error_lock, finished_lock)))
        
        #starting threads
        for thread in threads:
            thread.start()

        #joining threads
        for thread in threads:
            thread.join()

        #pickling the finished and error files
        with open(self.error_file, 'wb') as fp:
            pickle.dump(self.error_file_list, fp)
        with open(self.finished_file, 'wb') as fp:
            pickle.dump(self.finished_file_list, fp)
        
    def multithreadingProgress(self, total_num_URL, professorURL_lock):
        initial_position = 0
        with tqdm.tqdm(total = total_num_URL) as pbar:
            while True:
                with professorURL_lock:
                    remaining_progress = len(self.professor_urls)

                target_position = total_num_URL - remaining_progress
                increment_position = target_position-initial_position
                pbar.update(increment_position)
                initial_position +=increment_position
                #exit condition
                if remaining_progress == 0:
                    return
                time.sleep(1)

    def continuousPickling(self, professorURL_lock, error_lock, finished_lock):
        print('running continuous pickling')
        old_error_file_list = []
        old_finished_file_list = []
        old_professor_urls = []
        while True:
            try:
                #acquire professor URL lock
                with professorURL_lock:
                    temp_professorURL_list = self.professor_urls.copy()
                #acquire finished files lock
                with finished_lock:
                    temp_finished_file_list = self.finished_file_list.copy()
                #acquire error files lock
                with error_lock:
                    temp_error_file_list = self.error_file_list.copy()

                #compare professor url logs
                if len(temp_professorURL_list) != len(old_professor_urls):
                    with open(self.professorURL_file, 'wb') as fp:
                        pickle.dump(temp_professorURL_list, fp)
                        old_professor_urls = temp_professorURL_list.copy()
                #compare finished logs
                if len(temp_finished_file_list) != len(old_finished_file_list):
                    with open(self.finished_file, 'wb') as fp:
                        pickle.dump(temp_finished_file_list, fp)
                        old_finished_file_list = temp_finished_file_list.copy()
                #compare error logs
                if len(temp_error_file_list) != len(old_error_file_list):
                    with open(self.error_file, 'wb') as fp:
                        pickle.dump(temp_error_file_list, fp)
                        old_error_file_list = temp_error_file_list.copy()

                #exit condition
                if len(temp_professorURL_list) == 0:
                    return
                time.sleep(5)
            except Exception as error:
                print(f'an exception occurred: {error}')

    def scrapeThread(self, professorURL_lock, error_lock, finished_lock):
        if self.headless:
            options = Options()
            options.add_argument("-headless")
            driver = webdriver.Firefox(options=options)
        else:
            driver = webdriver.Firefox()

        #grab url
        while True:
            try:
                #acquire professor URL lock
                with professorURL_lock:
                    #check for correct length
                    if len(self.professor_urls)==0:
                        self.driverDestructor(driver)
                        return
                    assigned_url = self.professor_urls[0]
                    del self.professor_urls[0]
                
                driver.get(assigned_url)
                self.closeCookies(driver)
                self.loadReviews(driver)
                professor_data = self.getContent(driver)
                self.pickleProfessor(professor_data)
                
                #acquire finished lock
                with finished_lock:
                    self.finished_file_list.append(assigned_url)
            except Exception as error:
                print(f'an exception occurred: {error}')
                #acquire error lock
                with error_lock:
                    self.error_file_list.append(assigned_url)


            
        

    def scrapeReviews(self):
        #creating driver, local!
        print('scraping with a single thread')
        print("loading driver")
        if self.headless:
            options = Options()
            options.add_argument("-headless")
            driver = webdriver.Firefox(options=options)
        else:
            driver = webdriver.Firefox()
        print("driver loaded")

        #progress bar using tqdm
        progressbar = tqdm.tqdm(range(len(self.professor_urls)), desc="Loading…", ascii=False, ncols=75)

        #iterating each professor
        for i in progressbar:
            try:
                url = self.professor_urls[i]
                driver.get(url)
                self.closeCookies(driver)
                self.loadReviews(driver)
                professor_data = self.getContent(driver)
                self.pickleProfessor(professor_data)
                self.finished_file_list.append(self.professor_urls[i])
            except Exception as error:
                print(f'an exception occurred: {error}')
                self.error_file_list.append(self.professor_urls[i])

        #pickling the finished and error files
        with open(self.error_file, 'wb') as fp:
            pickle.dump(self.error_file_list, fp)
        with open(self.finished_file, 'wb') as fp:
            pickle.dump(self.finished_file_list, fp)

        #clean up driver
        self.driverDestructor(driver)

    def driverDestructor(self, driver):
        driver.quit()

    def pickleProfessor(self, professor_data):
        #check if the professor is valid(having no reviews is invalid)
        if len(professor_data['professor_firstname'])==0:
            return 

        professor_firstname = professor_data['professor_firstname'][0]
        professor_lastname = professor_data['professor_lastname'][0]
        pickle_file_name = professor_firstname+'_'+professor_lastname+'_data.pkl'
        os_pickle_file_name = os.path.join(self.script_dir, self.data_directory, pickle_file_name)
        #writing to pickle file
        with open(os_pickle_file_name, 'wb') as fp:
            pickle.dump(professor_data, fp)
            
    def loadReviews(self, driver):
        #get number of reviews and load all
        review_count_finder = driver.find_element(By.XPATH, "//div[starts-with(@class, 'RatingValue__NumRatings')]").text
        #find the number of ratings
        review_count = 0
        number_checker = re.findall(r'\b\d+\b', review_count_finder)
        if number_checker:
            review_count = int(number_checker[0])

        # print(f'number of reveiws: {review_count}')

        #scroll down if more that 20 reviews
        scroll_count = int(np.ceil((review_count-20)/10))

        if scroll_count >= 1:
            load_more_button = driver.find_element(By.XPATH, "//button[starts-with(@class, 'Buttons__Button-sc')]")
            wait = WebDriverWait(driver, timeout = 3)

            for i in range(scroll_count):
                y_scroll_offset = 80
                wait.until(lambda d : load_more_button.is_displayed())
                button_y_position = load_more_button.rect['y']-y_scroll_offset
                driver.execute_script(f"window.scrollTo(0, {button_y_position})")
                load_more_button.click()

    def getContent(self, driver):
        #get professor name 
        professor_name = driver.find_element(By.XPATH, "//div[starts-with(@class, 'NameTitle__Name')]").text.strip().split()
        professor_firstname = professor_name[0]
        professor_lastname = professor_name[1]

        #get all reviews and all associated elements!
        review_cards = driver.find_elements(By.XPATH, "//div[starts-with(@class, 'Rating__RatingBody')]")
        # print(len(review_cards))
        # print(review_cards)
        professor_firstname_list = []
        professor_lastname_list = []
        time_list = []
        class_list = []
        quality_list = []
        difficulty_list = []
        textbook_list = []
        takeagain_list = []
        comment_list = []
        tags_list = []
        attendance_list = []

        for i in range(len(review_cards)):
            review_card = review_cards[i]
            professor_firstname_list.append(professor_firstname)
            professor_lastname_list.append(professor_lastname)
            class_list.append(review_card.find_element(By.XPATH, "(.//div[starts-with(@class, 'RatingHeader__StyledClass')])[2]").text)
            time_list.append(review_card.find_element(By.XPATH, "(.//div[starts-with(@class, 'TimeStamp__StyledTimeStamp')])[2]").text)
            quality_list.append(review_card.find_element(By.XPATH, "(.//div[starts-with(@class, 'CardNumRating')])[3]").text)
            difficulty_list.append(review_card.find_element(By.XPATH, "(.//div[starts-with(@class, 'CardNumRating')])[6]").text)
            comment_list.append(review_card.find_element(By.XPATH, "(.//div[starts-with(@class, 'Comments__StyledComments')])[1]").text)
            #
            try:
                individual_meta_lists = (review_card.find_elements(By.XPATH, "(.//div[starts-with(@class, 'MetaItem__StyledMetaItem')])"))
                takeagain_flag = False
                textbook_flag = False
                attendance_flag = False
                for meta_item in individual_meta_lists:
                    #scraping for takeagain list in meta items
                    if "Would Take Again:" in meta_item.text:
                        takeagain_list.append(meta_item.text.replace('Would Take Again:','').strip())
                        takeagain_flag = True
                    #scraping for textbook requirement in meta items
                    if "Textbook:" in meta_item.text:
                        textbook_list.append(meta_item.text.replace('Textbook:','').strip())
                        textbook_flag = True
                    #scraping for attendance requirement in meta items
                    if "Attendance:" in meta_item.text:
                        attendance_list.append(meta_item.text.replace('Attendance:','').strip())
                        attendance_flag = True
                if takeagain_flag == False:
                    takeagain_list.append('unknown')
                if textbook_flag == False:
                    textbook_list.append('unknown')
                if attendance_flag == False:
                    attendance_list.append('unknown')
            except NoSuchElementException:
                print('meta tag error')
            #getting the tags in each review
            try:
                individual_tag_list = review_card.find_elements(By.XPATH, "(.//span[starts-with(@class, 'Tag-bs9vf4')])")
                temp_tag_list = []
                for tag in individual_tag_list:
                    temp_tag_list.append(tag.text.strip())
                tags_list.append(temp_tag_list)
            except NoSuchElementException:
                tags_list.append([])
        
        sia_list = self.sentimentAnalysis(comment_list)

        professor_data = {'professor_firstname':professor_firstname_list,
                          'professor_lastname':professor_lastname_list,
                          'class':class_list, 
                          'review_time':time_list, 
                          'comment':comment_list, 
                          'quality':quality_list,
                          'difficulty':difficulty_list, 
                          'textbook':textbook_list,
                          'takeagain':takeagain_list, 
                          'tags':tags_list,
                          'sentimentAnalysis':sia_list}
        return(professor_data)

    def sentimentAnalysis(self, comment_list):
        sia_list = []
        if self.sentimentAnalysis_enabled:
            sia = SentimentIntensityAnalyzer()
            for comment in comment_list:
                sia_list.append(sia.polarity_scores(comment)['compound'])
        else:
            for comment in comment_list:
                sia_list.append('unknown')
        return sia_list

