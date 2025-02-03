from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

# Set up Chrome options
chrome_options = Options()
#chrome_options.add_argument("")  # Run headless Chrome, without opening a window

# Specify the path to chromedriver if it's not in your PATH
service = Service("C:\Webdrivers\chromedriver.exe")

# Initialize the ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the Microsoft careers page for Product Manager jobs
# base_url = "https://jobs.careers.microsoft.com/global/en/search?q=Software%20Engineer&lc=United%20States&l=en_us&pg=1&pgSz=20&o=Recent"
base_url = "https://jobs.careers.microsoft.com/global/en/search?q={}&lc={}&l=en_us&pg=1&pgSz=20&o=Recent"

N = 10

def generate_search_url(job_title, location):
    # Replace spaces in query with '%20' for URL encoding
    formatted_job_title = job_title.replace(" ", "%20")
    # Replace spaces in location with '%20' for URL encoding
    formatted_location = location.replace(" ", "%20")
    return base_url.format(formatted_job_title, formatted_location)

def check_new_jobs(num_job, job_title, location):
    list_of_jobs = []

    # add location and job title in url and return the result url
    url = generate_search_url(job_title,location)

    for i in range(num_job):
        driver.get(url)
        time.sleep(5)  # Let the page load
        
        # list of jobs
        # Step 1: Click on the job card based on the loop index
        job_index = i  # Adjust this if your job indices start from a different number
        job_card_selector = f'.ms-List-cell[data-list-index="{job_index}"]'
        job_card = driver.find_element(By.CSS_SELECTOR, job_card_selector)
        ActionChains(driver).move_to_element(job_card).perform()
        time.sleep(2)  # Give some time for the hover effect (optional)

        job_card.click()
        time.sleep(2) 

        # Step 2: Extract the job title and job number
        job_title = driver.find_element(By.CSS_SELECTOR, 'h1').text
        #job_title.click()
        job_number = driver.find_element(By.XPATH, '//div[text()="Job number"]/following-sibling::div').text

        # Step 3: Click on the "Share Job" button
        # share_button = driver.find_element(By.ID, 'jobsharebuttoncomponentid')
        #share_button.click()
        time.sleep(2)  # Allow time for the share options to appear

        job_link = driver.current_url
        job_details = {
            "title": job_title,
            "number": job_number,
            "link": job_link
        }

        list_of_jobs.append(job_details)
        
    return list_of_jobs

if __name__ == "__main__":
    location = "India"
    title = "Software Engineer"
    job_details = check_new_jobs(N, title, location)
    if not job_details:
        print("No job details found.")
    
    for jobs in job_details:
        print("Job details found:")
        print(f"Title: {jobs['title']}")
        print(f"Number: {jobs['number']}")
        print(f"Link: {jobs['link']}")
    
    driver.quit()
