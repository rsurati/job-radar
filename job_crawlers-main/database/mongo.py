import pymongo

# Replace <connection_string> with your MongoDB Atlas connection string
client = pymongo.MongoClient("mongodb://localhost:27017")

# Connect to the database and collection
db = client["crawler"]  # Replace with your database name
collection = db["companies"]  # Replace with your collection name

def ensure_company_document(company_name):
    """Ensure a document for the given company exists. Create it if it doesn't exist."""
    if collection.count_documents({"company": company_name}) == 0:
        collection.insert_one({"company": company_name, "jobs": []})
        print(f"Created a new document for {company_name}.")
        return 0
    else:
        print(f"Document for {company_name} already exists.")
        return 1

def add_jobs_if_not_exists(jobs_list):
    """Check if job IDs are present in the company's document. Add them if they are not present."""
    new_jobs = []
    for job in jobs_list:
        company_name = job['company']
        job_title = job['title']
        job_number = job['number']
        job_link = job['link']

        # Ensure the company document exists
        # ensure_company_document(company_name)

        # Use the aggregation framework to check if the job number already exists
        pipeline = [
            {"$match": {"company": company_name}},
            {"$unwind": "$jobs"},
            {"$match": {"jobs.number": job_number}},
            {"$project": {"_id": 1}}
        ]
        job_exists = list(collection.aggregate(pipeline))

        if not job_exists:
            new_job = {
                "title": job_title,
                "number": job_number,
                "link": job_link,
                "company":company_name
            }
            collection.update_one(
                {"company": company_name},
                {"$push": {"jobs": new_job}}
            )
            new_jobs.append(new_job)
            print(f"Added new job {job_number} to {company_name}.")
        else:
            print(f"Job {job_number} already exists in {company_name}.")

    return new_jobs

# Example job details input
# jobs_list = [
#     {'company': 'microsoft', 'title': 'Principal Technical Program Manager, Industrial Controls Transformation', 'number': '1792', 'link': 'https://jobs.careers.microsoft.com/global/en/job/1718892/Principal-Technical-Program-Manager%2C-Industrial-Controls-Transformation'},
#     {'company': 'microsoft', 'title': 'Principal UX Engineering Manager', 'number': '26', 'link': 'https://jobs.careers.microsoft.com/global/en/job/1719326/Principal-UX-Engineering-Manager'},
#     {'company': 'microsoft', 'title': 'Principal Technical Program Manager', 'number': '5', 'link': 'https://jobs.careers.microsoft.com/global/en/job/1711145/Principal-Technical-Program-Manager'},
#     {'company': 'microsoft', 'title': 'Senior Director Software Program Manager', 'number': '121', 'link': 'https://jobs.careers.microsoft.com/global/en/job/1719791/Senior-Director-Software-Program-Manager'},
#     {'company': 'microsoft', 'title': 'Principal Product Manager - Privacy', 'number': '00', 'link': 'https://jobs.careers.microsoft.com/global/en/job/1719983/Principal-Product-Manager---Privacy'}
# ]

# Adding jobs to the database and getting the list of new jobs
# new_jobs = add_jobs_if_not_exists(jobs_list)
# print("New jobs added:", new_jobs)
