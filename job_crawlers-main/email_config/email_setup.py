import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(job_details_list, receiverEmail = None):
    from_email = "ENTER_YOUR_EMIAL"
    from_password = "ENTER_EMAIL_PASSWORD"
    print("In send email function " +receiverEmail)
    to_email = receiverEmail

    subject = "New " + job_details_list[0]['company'] +  " Job Posting: "

    # Concatenate job details for all jobs into a single string
    body = ""
    for job_details in job_details_list:
        body += f"Job Title: {job_details['title']} "
        body += f"Job Number: {job_details['number']}\n"
        body += f"Job Link: {job_details['link']}\n\n"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = "".join(to_email)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        print("Email sent successfully.")
    except smtplib.SMTPAuthenticationError:
        print("Failed to authenticate with the email server. Check the username/password.")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    finally:
        # Ensure the server is always closed, even if error occurs
        server.quit()
