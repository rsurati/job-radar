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
    driver = webdriver.Chrome()  # Ensure you have the appropriate WebDriver in PATH

    try:
        for i in range(num_job):
            driver.get(url)
            time.sleep(6)  # Let the page load

            job_card_selector = f'.ms-List-cell[data-list-index="{i}"]'
            job_card = driver.find_element(By.CSS_SELECTOR, job_card_selector)
            job_card.click()
            time.sleep(4)

            job_title = driver.find_element(By.CSS_SELECTOR, 'h1').text
            job_number = driver.find_element(By.XPATH, '//div[text()="Job number"]/following-sibling::div').text
            time.sleep(2)

            job_link = driver.current_url
            job_details = {
                "company": "Microsoft",
                "title": job_title,
                "number": job_number,
                "link": job_link
            }
            list_of_jobs.append(job_details)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
    return list_of_jobs

# Asynchronous function to run crawler in thread pool
async def async_run_crawler(executor, url, num_jobs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, run_crawler, url, num_jobs)

async def run_crawler_for_microsoft():
    file_path = "urls/urls.json"
    ensure_company_document("Microsoft")
    with open(file_path, 'r') as file:
        position_urls = json.load(file)

    microsoft_urls = position_urls.get("Microsoft", [])
    all_jobs = []
    num_jobs = 20  # You can adjust this as needed

    with ThreadPoolExecutor() as executor:
        tasks = [async_run_crawler(executor, url, num_jobs) for url in microsoft_urls]
        for task in asyncio.as_completed(tasks):
            jobs = await task
            all_jobs.extend(jobs)
            if jobs:
                added_jobs = add_jobs_if_not_exists(jobs)
                print("Got the folowing new jobs from database")
                print(added_jobs)
                if added_jobs:
                    send_email(added_jobs)

    print(all_jobs)
    return all_jobs

# if __name__ == "__main__":
#     asyncio.run(run_crawler_for_microsoft())
