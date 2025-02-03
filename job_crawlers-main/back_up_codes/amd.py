from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Uncomment this line to run headless Chrome

# Specify the path to chromedriver if it's not in your PATH
service = Service('/opt/homebrew/bin/chromedriver')

# Initialize the ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Base URL for AMD careers page
url = "https://careers.amd.com/careers-home/jobs?keywords=project%20manager&stretchUnits=MILES&stretch=10&location=United%20States&lat=39.76&lng=-98.5&woe=12&sortBy=posted_date&descending=true&page=1&country=United%20States&categories=Engineering&limit=100"

N = 100  # Number of jobs to scrape

def check_new_jobs():
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    list_of_jobs = []

    # Check for the presence of job cards and load them
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.search-result-item')))

    while True:
        job_cards = driver.find_elements(By.CSS_SELECTOR, '.search-result-item')
        
        for job_card in job_cards:
            job_title_elem = job_card.find_element(By.CSS_SELECTOR, '.job-title-link')
            job_title_text = job_title_elem.text
            job_link = job_title_elem.get_attribute('href')
            job_number_elem = job_card.find_element(By.CSS_SELECTOR, '.req-id span')
            job_number_text = job_number_elem.text
            
            job_details = {
                "company": "Amd",
                "title": job_title_text,
                "number": job_number_text,
                "link": job_link
            }

            list_of_jobs.append(job_details)

        # Attempt to find and click the next button
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.next')))
            next_button.click()
            wait.until(EC.staleness_of(job_cards[0]))  # Wait for the page to refresh
        except Exception as e:
            print(f"End of pages or an error occurred: {e}")
            break

    return list_of_jobs

if __name__ == "__main__":
    job_details = check_new_jobs()
    if not job_details:
        print("No job details found.")
    else:
        for job in job_details:
            print("Job details found:")
            print(f"Title: {job['title']}")
            print(f"Number: {job['number']}")
            print(f"Link: {job['link']}")
    
    driver.quit()