import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from email_config.email_setup import send_email

# Function to run the crawler for a given URL
def run_crawler(url):
    driver = webdriver.Chrome()  # Ensure you have the appropriate WebDriver in PATH
    job_details = {}

    try:
        driver.get(url)
        time.sleep(3)  # Let the page load

        # Step 1: Click on the first job card
        first_job_card = driver.find_element(By.CSS_SELECTOR, '.ms-List-cell[data-list-index="0"]')
        first_job_card.click()
        time.sleep(3)  # Allow time for the new page to load

        # Step 2: Extract the job title and job number
        job_title = driver.find_element(By.CSS_SELECTOR, 'h1').text
        job_number = driver.find_element(By.XPATH, '//div[text()="Job number"]/following-sibling::div').text

        # Step 3: Get the JOB URL
        job_link = driver.current_url
        job_details = {
            "company": "Nvidia",
            "title": job_title,
            "number": job_number,
            "link": job_link
        }
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    return job_details

# Asynchronous function to run crawler in thread pool
async def async_run_crawler(executor, url):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, run_crawler, url)

# Asynchronous function to run the crawler for Nvidia
async def run_crawler_for_nvidia(receiverEmail=None):
    file_path = "urls/urls.json"
    with open(file_path, 'r') as file:
        position_urls = json.load(file)

    nvidia_urls = position_urls.get("Nvidia", [])
    all_jobs = []

    with ThreadPoolExecutor() as executor:
        tasks = [async_run_crawler(executor, url) for url in nvidia_urls]
        for task in asyncio.as_completed(tasks):
            job = await task
            if job:
                all_jobs.append(job)
                send_email(job, receiverEmail)

    print(all_jobs)
    return all_jobs

# Uncomment the following lines to run the Nvidia crawler asynchronously
# if __name__ == "__main__":
#     asyncio.run(run_crawler_for_nvidia())
