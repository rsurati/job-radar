from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless Chrome, without opening a window

# Specify the path to chromedriver if it's not in your PATH
service = Service('/opt/homebrew/bin/chromedriver')

# Initialize the ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the Microsoft careers page for Product Manager jobs
url = "https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=recent&job_type%5B%5D=Full-Time&country%5B%5D=USA&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=&base_query=product%20manager&city=&country=&region=&county=&query_options=&"


def check_new_jobs():
    driver.get(url)
    wait = WebDriverWait(driver, 10)  # 10 seconds wait time
    
    # Collect all job tiles within the specified container up to 20 listings
    jobs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.job-tile')))
    job_details_list = []

    for job in jobs[:20]:  # Limit to first 20 job listings
        job_title = job.find_element(By.CSS_SELECTOR, 'h3.job-title a').text
        job_link = job.find_element(By.CSS_SELECTOR, 'h3.job-title a').get_attribute('href')
        job_id = job.find_element(By.XPATH, './/li[contains(text(), "Job ID:")]').text.split(': ')[1].strip()

        job_details = {
            "title": job_title,
            "number": job_id,
            "link": job_link
        }
        job_details_list.append(job_details)
    
    return job_details_list



def send_email(job_details):
    from_email = "djobs9171@gmail.com"
    from_password = "bzwr wsgu lvur qokh"
    to_emails = ["devanshu.vguj@gmail.com", "kanhaiyarmy@gmail.com", "abhisheksinhgohil81@gmail.com"] 

    subject = "New Microsoft Job Posting: Product Manager"
    body = (f"Job Title: {job_details['title']}\n"
            f"Job Number: {job_details['number']}\n"
            f"Job Link: {job_details['link']}")

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, from_password)
    text = msg.as_string()
    server.sendmail(from_email, to_emails, text)
    server.quit()

if __name__ == "__main__":
    job_list = check_new_jobs()
    for job_details in job_list:
        print(f"Title: {job_details['title']}, Number: {job_details['number']}, Link: {job_details['link']}")
    else:
        print("No job details found.")

    driver.quit()