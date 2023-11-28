# CIS_URL_scrape.py: Serves as one of the primary .py functions of the program
# Mass scrapes URLs from CIS database and saves them into file (filename at line 19)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Initialize browser options
browser_options = Options()
browser_options.add_experimental_option("debuggerAddress", "localhost:9222")
driver = webdriver.Chrome(options=browser_options)

url = "https://utdirect.utexas.edu/ctl/ecis/results/search.WBX"

try:
    driver.get(url)
    with open("output_urls_new.txt", "w") as file:
        while True:
            # Extract links from the current page
            links = driver.find_elements(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div[3]/table/tbody/tr/td[1]")
            for link in links:
                # Process each link as needed (e.g., store in a list, perform actions, etc.)
                href = link.find_element(By.TAG_NAME, "a").get_attribute("href")
                print(href)
                file.write(href + "\n")  # Write the URL to the file with a newline
            # Click the "Next page" button
            try:
                next_page_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@value='Next page']"))
                )
                next_page_button.click()
            except Exception as e:
                print(f"Error clicking the 'Next page' button: {e}")
                break  # Break the loop if there is an error or no more pages
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()