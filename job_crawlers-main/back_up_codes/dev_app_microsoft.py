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
url = "https://jobs.careers.microsoft.com/global/en/search?q=product%20manager&lc=United%20States&l=en_us&pg=1&pgSz=20&o=Recent"

def check_new_jobs():
    num_job= 10
    list_of_jobs = []
    wait = WebDriverWait(driver, 10)  # 10 seconds wait time
    try:
        for i in range(num_job):
            driver.get(url)
            job_card_selector = f'.ms-List-cell[data-list-index="{i}"]'
            # job_card = driver.find_element(By.CSS_SELECTOR, job_card_selector)
            # job_card = driver.find_element(By.CSS_SELECTOR, '.ms-List-cell[data-list-index="{job_index}"]')
            job_card = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, job_card_selector)))
            job_card.click()
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1')))
            
            job_title = driver.find_element(By.CSS_SELECTOR, 'h1').text
            job_number = driver.find_element(By.XPATH, '//div[text()="Job number"]/following-sibling::div').text
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
    
    return list_of_jobs

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
    text = msg.cleas_string()
    server.sendmail(from_email, to_emails, text)
    server.quit()

if __name__ == "__main__":
    job_details = check_new_jobs()
    print(job_details)
    driver.quit()