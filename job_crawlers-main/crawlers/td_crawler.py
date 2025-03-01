import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from email_config.email_setup import send_email
from database.mongo import ensure_company_document, add_jobs_if_not_exists

# Function to run the crawler for a given URL
def run_crawler(url, num_job):
    list_of_jobs = []
    driver = webdriver.Chrome()   # Ensure you have the appropriate WebDriver in PATH

    try:
        driver.get(url)
        time.sleep(8)  # Let the page load

        # Use the first child element under 'ul' with role='list' as the container for each job listing
        job_elements = driver.find_elements(By.CSS_SELECTOR, 'ul[role="list"] > li')[:num_job]

        for i, job_element in enumerate(job_elements):
            try:
                # Extract job title from the anchor tag within the h3 element
                job_link = job_element.find_element(By.CSS_SELECTOR, 'h3 a.css-19uc56f')
                job_url = job_link.get_attribute("href")
                job_title = job_link.text.strip()

                # Extract job number from the element with class 'css-h2nt8k' (assuming it contains the job number)
                job_number_element = job_element.find_element(By.CSS_SELECTOR, 'ul.css-14a0imc > li')
                job_number = job_number_element.text.strip()

                job_details = {
                    "company": "TD",
                    "title": job_title,
                    "number": job_number,
                    "link": job_url
                }

                list_of_jobs.append(job_details)

            except Exception as e:
                print(f"An error occurred while processing job {i}: {e}")
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

# Asynchronous function to run the crawler for TD
async def run_crawler_for_td(receiverEmail=None):
    file_path = "urls/urls.json"
    ensure_company_document("TD")

    with open(file_path, 'r') as file:
        position_urls = json.load(file)

    td_urls = position_urls.get("TD", [])
    all_jobs = []
    num_jobs = 20  # You can adjust this as needed

    with ThreadPoolExecutor() as executor:
        tasks = [async_run_crawler(executor, url, num_jobs) for url in td_urls]
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

# Uncomment the following lines to run the SWBC crawler asynchronously
# if __name__ == "__main__":
#     asyncio.run(run_crawler_for_td())
