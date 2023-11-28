# CIS_load_scrape.py: Serves as one of the primary .py functions of the program
# Mass scrapes information loaded from a .txt file of URLs created via CIS_URL_scrape.py
# URL source location found at line 125, output location found at 121

# selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os

# Function to delete the file if it exists
def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted existing file: {file_path}")

# scrape function
def scrape_page(website_url, output_file):
    # create a dictionary to store all data
    page_data = {
        'InstructorData': [],
        'Table1': {},
        'Table2': {},
        'Table3': {}
    }
    # create browser_options and add user data directory
    browser_options = Options()
    browser_options.add_experimental_option("debuggerAddress", "localhost:9222")
    # create driver
    driver = webdriver.Chrome(options=browser_options)
    driver.get(website_url)
    # wait for the page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_to_be(website_url))
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div[2]/fieldset/div[1]")))
    # create locators
    name_locator = driver.find_elements(By.XPATH, "/html/body/div[4]/div[2]/div[2]/fieldset/div[1]")
    code_locator = driver.find_elements(By.XPATH, "/html/body/div[4]/div[2]/div[2]/fieldset/div[2]")
    semester_locator = driver.find_elements(By.XPATH, "/html/body/div[4]/div[2]/div[2]/fieldset/div[5]")

    # loop through each row and extract data
    for i in range(len(name_locator)):
        # Extracting and splitting names
        full_name = name_locator[i].text.strip().replace("Instructor:", "")
        last_name, first_name = map(str.strip, full_name.split(','))
        # Extracting and splitting course details
        course_details = code_locator[i].text.strip().replace("Course & Unique Number:", "")
        course_number, unique_number = map(str.strip, course_details.split('('))
        # Extracting semester
        semester = semester_locator[i].text.strip().replace("Semester: ", "")
        # create a dictionary for the current instructor
        instructor_data = {
            'Last Name': last_name,
            'First Name': first_name,
            'Course Number': course_number,
            'Unique Number': unique_number.rstrip(')'),
            'Semester': semester,
        }
        # append the instructor dictionary to the list
        page_data['InstructorData'].append(instructor_data)
    # create locators for the first table
    table_locator = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/table[1]/tbody")
    # get the number of rows in the first table
    num_rows = len(table_locator.find_elements(By.TAG_NAME, "tr"))
    # loop through each row and extract data from the first table
    for row_num in range(2, min(11, num_rows + 1)):  # Iterate up to the 10th row or the actual number of rows if less
        # create locators for each question and score in the row of the first table
        question_locator = table_locator.find_element(By.XPATH, f"tr[{row_num}]/td[1]")
        score_locator = table_locator.find_element(By.XPATH, f"tr[{row_num}]/td[8]")
        # add the data to the dictionary for the first table
        page_data['Table1'][f"Question {row_num - 1}"] = question_locator.text
        page_data['Table1'][f"Question {row_num - 1} Score"] = score_locator.text
    # create locators for the second table
    table2_locator = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/table[2]/tbody")
    # get the number of rows in the second table
    num_rows_table2 = len(table2_locator.find_elements(By.TAG_NAME, "tr"))
    # loop through each row and extract data from the second table
    for row_num_table2 in range(2, min(11, num_rows_table2 + 1)):
        # create locators for each question and score in the row of the second table
        question_locator_table2 = table2_locator.find_element(By.XPATH, f"tr[{row_num_table2}]/td[1]")
        score_locator_table2 = table2_locator.find_element(By.XPATH, f"tr[{row_num_table2}]/td[8]")
        # add the data to the dictionary for the second table
        page_data['Table2'][f"T2 Question {row_num_table2 - 1}"] = question_locator_table2.text
        page_data['Table2'][f"T2 Question {row_num_table2 - 1} Score"] = score_locator_table2.text
    # create locators for the third table
    table3_locator = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/table[3]/tbody")
    # locate the divisor value in Table 3
    divisor_locator_table3 = table3_locator.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/table[3]/tbody/tr[2]/td[7]")
    divisor_value = int(divisor_locator_table3.text)
    # loop through each row and extract data from the third table
    for row_num_table3 in range(2, 3):
        # create locator for the question in the row of the third table
        question_locator_table3 = table3_locator.find_element(By.XPATH, f"tr[{row_num_table3}]/td[1]")
        # add the data to the dictionary for the third table
        page_data['Table3']['Workload Question'] = question_locator_table3.text
        # create locators for the scores in Table 3
        score_locators_table3 = [
            table3_locator.find_element(By.XPATH, f"tr[{row_num_table3}]/td[{i}]") for i in range(2, 7)
        ]
        # multiply each score by its corresponding weight (5, 4, 3, 2, 1)
        weighted_scores = [
            int(score_locator.text.split('(')[0].strip()) * weight
            for weight, score_locator in zip(range(5, 0, -1), score_locators_table3)
        ]
        # divide the weighted sum by the divisor value
        average_score = sum(weighted_scores) / divisor_value
        # add the average score to the dictionary for the third table
        page_data['Table3']['Workload Score (5 = Highest, 1 = Lowest)'] = average_score
    # save page_data to a text file
    with open(output_file, 'a') as txt_file:
        txt_file.write(json.dumps(page_data) + '\n')
    # close the driver
    driver.quit()

if __name__ == "__main__":
    # Output file to store the dictionaries
    output_txt_file = 'instructor_data9ba.txt'
    # If file already exists, delete it
    delete_file(output_txt_file)
    # Read URLs from the text file
    with open('output_slices/output_part_9ba.txt', 'r') as url_file:
        urls_to_scrape = url_file.read().splitlines()
    total_urls = len(urls_to_scrape)
    for index, url in enumerate(urls_to_scrape, start=1):
        scrape_page(url, output_txt_file)
        print(f"Scraped CIS {index}/{total_urls}")