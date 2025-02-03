import os
import time
import json
from selenium.webdriver.common.by import By
from email_config.email_setup import send_email
from crawlers.config_crawler import driver
from database.mongo import ensure_company_document, add_jobs_if_not_exists

def run_crawler(url, num_job):

    list_of_jobs = []

    try:
        driver.get(url)
        time.sleep(6)  # Let the page load

        # Use mat-expansion-panel as the main container for each job listing
        job_elements = driver.find_elements(By.CSS_SELECTOR, 'mat-expansion-panel')[:num_job]

        for i, job_element in enumerate(job_elements):
            try:
                # Extract job title from the anchor tag within the job title element
                job_link_element = job_element.find_element(By.CSS_SELECTOR, 'a.job-title-link')
                job_url = job_link_element.get_attribute("href")
                job_title = job_link_element.find_element(By.CSS_SELECTOR, 'span[itemprop="title"]').text

                # Extract job number from the text content of the element with class 'req-id'
                job_number_element = job_element.find_element(By.CSS_SELECTOR, 'p.req-id')
                job_number = job_number_element.text.split(": ")[-1]

                job_details = {
                    "company": "GM Financial",  # Assuming company name is GM Financial
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

    return list_of_jobs

def run_crawler_for_gm_financial():

    file_path = "urls/urls.json"
    ensure_company_document("GM Financial")

    with open(file_path, 'r') as file:
        position_urls = json.load(file)

    try:
        num_jobs = 20
        for url in position_urls.get("GM FINANCIAL", []):
            list_of_jobs = run_crawler(url, num_jobs)
            print(list_of_jobs)

            jobs = add_jobs_if_not_exists(list_of_jobs)
            print("Sent job list from database")
            print(jobs)

            if jobs:
                # Call function to send email notification (assuming you have a send_email function)
                send_email(jobs)
    finally:
        driver.quit()

