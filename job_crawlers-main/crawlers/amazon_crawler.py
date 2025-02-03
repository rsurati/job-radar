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
    list_of_jobs = []
    driver = webdriver.Chrome()  # Ensure you have the appropriate WebDriver in PATH
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)  # 10 seconds wait time
        # Collect all job tiles within the specified container up to 20 listings
        jobs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.job-tile')))

        for job in jobs[:num_job]:  
            job_title = job.find_element(By.CSS_SELECTOR, 'h3.job-title a').text
            job_link = job.find_element(By.CSS_SELECTOR, 'h3.job-title a').get_attribute('href')
            job_id = job.find_element(By.XPATH, './/li[contains(text(), "Job ID:")]').text.split(': ')[1].strip()

            job_details = {
                "company": "Amazon",
                "title": job_title,
                "number": job_id,
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

# Asynchronous function to run the crawler for Amazon
async def run_crawler_for_amazon():
    file_path = "urls/urls.json"
    ensure_company_document("Amazon")
    with open(file_path, 'r') as file:
        position_urls = json.load(file)

    amazon_urls = position_urls.get("Amazon", [])
    all_jobs = []
    num_jobs = 10  # You can adjust this as needed

    with ThreadPoolExecutor() as executor:
        tasks = [async_run_crawler(executor, url, num_jobs) for url in amazon_urls]
        for task in asyncio.as_completed(tasks):
            jobs = await task
            all_jobs.extend(jobs)
            if jobs:
                added_jobs = add_jobs_if_not_exists(jobs)
                print("Got the following new jobs from database")
                print(added_jobs)
                if added_jobs:
                    send_email(added_jobs)

    print(all_jobs)
    return all_jobs

# Uncomment the following lines to run the Amazon crawler asynchronously
# if __name__ == "__main__":
#     asyncio.run(run_crawler_for_amazon())
