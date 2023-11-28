# CIS_single_roam.py: Scrapes the first page of URLs from the CIS database
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Initialize browser options
browser_options = Options()
browser_options.add_experimental_option("debuggerAddress", "localhost:9222")

# Create the WebDriver with the specified options
driver = webdriver.Chrome(options=browser_options)

url = "https://utdirect.utexas.edu/ctl/ecis/results/search.WBX"

try:
    driver.get(url)
    # Extract links from the current page
    links = driver.find_elements(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div[3]/table/tbody/tr/td[1]")
    for link in links:
        # Process each link as needed (e.g., store in a list, perform actions, etc.)
        href = link.find_element(By.TAG_NAME, "a").get_attribute("href")
        print(href)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the WebDriver after scraping
    driver.quit()