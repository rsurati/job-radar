import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from email_config.email_setup import send_email
from database.mongo import ensure_company_document, add_jobs_if_not_exists

# Function to run the crawler for a given URL
def run_crawler(url, num_jobs):
    list_of_jobs = []
    driver = webdriver.Chrome()  # Ensure you have the appropriate WebDriver in PATH

    try:
        driver.get(url)
        time.sleep(5)  # Let the page load

        job_elements = driver.find_elements(By.CSS_SELECTOR, 'mat-expansion-panel[data-index]')[:num_jobs]

        for job_element in job_elements:
            try:
                job_link_element = job_element.find_element(By.CSS_SELECTOR, 'a.job-title-link')
                job_url = job_link_element.get_attribute("href")
                job_title = job_element.find_element(By.CSS_SELECTOR, 'span[itemprop="title"]').text
                job_number = job_link_element.get_attribute("href").split('/')[-1]

                job_details = {
                    "company": "DocuSign",
                    "title": job_title,
                    "number": job_number,
                    "link": job_url
                }

                list_of_jobs.append(job_details)

            except Exception as e:
                print(f"An error occurred while processing job: {e}")
                continue

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    return list_of_jobs

# Asynchronous function to run crawler in thread pool
async def async_run_crawler(executor, url, num_jobs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, run_crawler, url, num_jobs)

# Asynchronous function to run the crawler for DocuSign
async def run_crawler_for_docusign( receiverEmail = None):

    file_path = "urls/urls.json"
    ensure_company_document("DocuSign")
    with open(file_path, 'r') as file:
        position_urls = json.load(file)

    docusign_urls = position_urls.get("DocuSign", [])
    all_jobs = []
    num_jobs = 20  # You can adjust this as needed

    with ThreadPoolExecutor() as executor:
        tasks = [async_run_crawler(executor, url, num_jobs) for url in docusign_urls]
        for task in asyncio.as_completed(tasks):
            jobs = await task
            all_jobs.extend(jobs)
            if jobs:
                added_jobs = add_jobs_if_not_exists(jobs)
                print("Got the following new jobs from database")
                print(added_jobs)
                if added_jobs:
                    send_email(added_jobs, receiverEmail)

    print(all_jobs)
    return all_jobs

# Uncomment the following lines to run the DocuSign crawler asynchronously
# if __name__ == "__main__":
#     asyncio.run(run_crawler_for_docusign())
