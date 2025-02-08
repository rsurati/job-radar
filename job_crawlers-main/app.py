import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_cors import CORS
from crawlers.microsoft import run_crawler_for_microsoft
from crawlers.amazon_crawler import run_crawler_for_amazon
from crawlers.docusign import run_crawler_for_docusign
from crawlers.goldmanSachs import run_crawler_for_goldman_sachs
from crawlers.nvidia import run_crawler_for_nvidia
from crawlers.amd_crawler import run_crawler_for_amd
from crawlers.gmfinancial import run_crawler_for_gm_financial
from flask import request


app = Flask(__name__)
CORS(app)  # Enable CORS on all routes

def check_new_job(receiverEmail=None):  
    #data = request.json  # Get JSON data from frontend
    #receiver_email = "Here is the receiver email"#data.get("receiver_email")  # Extract receiver email  
    asyncio.run(run_crawler_for_gm_financial(receiverEmail=None)) #done # Ensure the async function is run properly
    asyncio.run(run_crawler_for_amd(receiverEmail=None))  # Ensure the async function is run properly
    asyncio.run(run_crawler_for_goldman_sachs(receiverEmail=None))  # Ensure the async function is run properly
    asyncio.run(run_crawler_for_nvidia(receiverEmail=None))  # Ensure the async function is run properly
    asyncio.run(run_crawler_for_amazon(receiverEmail=None))  # Ensure the async function is run properly
    asyncio.run(run_crawler_for_docusign(receiverEmail))  # Ensure the async function is run properly
    asyncio.run(run_crawler_for_microsoft(receiverEmail=None))  # Ensure the async function is run properly
    print("Checking for new job...")

@app.route('/check_new_job', methods=['GET'])
def handle_check_new_job():
    check_new_job()
    return {"message": "Job check complete"}, 200

def schedule_job_checks(receiverEmail):
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_new_job, 'interval', minutes=2, args=[receiverEmail])
    scheduler.start()

# @app.route('/main', methods=['GET'])
# def handle_check_periodically():
#     schedule_job_checks()
#     return {"message": "Scheduled job checks every 15 minutes"}, 200

@app.route('/main', methods=['POST'])  # Change to POST to accept data
def handle_check_periodically():
    data = request.get_json()  # Get JSON data from frontend request
    receiver_email = data.get("email")  # Extract the email from the request
    print("Received email: ", receiver_email)

    if not receiver_email:
        return {"error": "Email is required"}, 400  # Return error if email is missing

    schedule_job_checks(receiver_email)  # Pass email to job function
    return {"message": f"Scheduled job checks every 15 minutes for {receiver_email}"}, 200

# @app.route("/api/send-email", methods=["POST"])
# def send_email_api():
#     try:
#         data = request.get_json()
#         receiver_email = data.get("email")

#         if not receiver_email:
#             return jsonify({"message": "Email is required"}), 400

#         # Sample email content (Modify as needed)
#         subject = "New Job Alert!"
#         body = "Here are the latest jobs from AMD."

#         # Call your send_email function
#         send_email(receiver_email, subject, body)

#         return jsonify({"message": "Email sent successfully!"}), 200
#     except Exception as e:
#         return jsonify({"message": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
