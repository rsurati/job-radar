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


app = Flask(__name__)
CORS(app)  # Enable CORS on all routes

def check_new_job():    
    #asyncio.run(run_crawler_for_gm_financial())  # Ensure the async function is run properly
    asyncio.run(run_crawler_for_amd())  # Ensure the async function is run properly
    asyncio.run(run_crawler_for_goldman_sachs())  # Ensure the async function is run properly
    # asyncio.run(run_crawler_for_nvidia())  # Ensure the async function is run properly
    asyncio.run(run_crawler_for_amazon())  # Ensure the async function is run properly
    # asyncio.run(run_crawler_for_docusign())  # Ensure the async function is run properly
    asyncio.run(run_crawler_for_microsoft())  # Ensure the async function is run properly
    print("Checking for new job...")

@app.route('/check_new_job', methods=['GET'])
def handle_check_new_job():
    check_new_job()
    return {"message": "Job check complete"}, 200

def schedule_job_checks():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_new_job, 'interval', minutes=2)
    scheduler.start()

@app.route('/main', methods=['GET'])
def handle_check_periodically():
    schedule_job_checks()
    return {"message": "Scheduled job checks every 15 minutes"}, 200

if __name__ == '__main__':
    app.run(debug=True)
