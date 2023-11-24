from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver =webdriver.Firefox()

driver.get("https://www.ratemyprofessors.com/search/")

#waits for web page to load, replace with something more efficient
time.sleep(5)

#accepts cookies basically, write code to test for this!
try:
    driver.find_element(By.XPATH, '/html/body/div[5]/div/div/button').click() 
except:
    pass

school_name = 'University of Texas at Austin'
#inputs professor name
# search_input = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div/header/div[2]/div[3]/div[1]/div[2]/div/div[1]/div[2]/input')
search_input = driver.find_element(By.XPATH, '//input[starts-with(@class, "Search__DebouncedSearchInput")][2]')

# search_input.send_keys(school_name)
# search_input.send_keys(Keys.RETURN)

# search_results = driver.find_elements(By.XPATH, "//div[starts-with(@class, 'SchoolCardHeader')]")
# print(f'search results length: {len(search_results)}')
# print(search_results)
# driver.quit()