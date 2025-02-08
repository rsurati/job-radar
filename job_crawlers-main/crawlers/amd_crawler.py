import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from email_config.email_setup import send_email
from database.mongo import ensure_company_document, add_jobs_if_not_exists

# Function to run the crawler for a given URL
def run_crawler(url, num_job):
    driver = webdriver.Chrome()  # Ensure you have the appropriate WebDriver in PATH
    list_of_jobs = []

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)  # 10 seconds wait time
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

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    return list_of_jobs

# Asynchronous function to run crawler in thread pool
async def async_run_crawler(executor, url, num_jobs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, run_crawler, url, num_jobs)

# Asynchronous function to run the crawler for AMD
async def run_crawler_for_amd(receiverEmail=None):
    file_path = "urls/urls.json"
    ensure_company_document("Amd")

    with open(file_path, 'r') as file:
        position_urls = json.load(file)

    amd_urls = position_urls.get("Amd", [])
    all_jobs = []
    num_jobs = 100  # You can adjust this as needed

    with ThreadPoolExecutor() as executor:
        tasks = [async_run_crawler(executor, url, num_jobs) for url in amd_urls]
        for task in asyncio.as_completed(tasks):
            jobs = await task
            if jobs:
                all_jobs.extend(jobs)
                added_jobs = add_jobs_if_not_exists(jobs)
                print("Got the following new jobs from database")
                print(added_jobs)
                if added_jobs:
                    send_email(added_jobs, receiverEmail)

    print(all_jobs)
    return all_jobs

