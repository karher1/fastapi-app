from fastapi import FastAPI, Query, Depends, Path, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session

#SQL alchemy setup
DATABASE_URL = "postgresql://postgres:Mydatabaseforjobs@db.evnavtrdejauwdcjvvzf.supabase.co:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


app = FastAPI()


# This is our data model - what an application looks like
class Candidate(BaseModel):
    candidate_id: str 
    name: str
    email: str
    job_id: str | None = None

# This is our "database" - just a list in memory - cache memory
applications: List[Candidate] = []

#creating a db connection session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 


@app.get("/jobs")
def get_all_job_postings(db: Session = Depends(get_db)):
    result = db.execute(text('SELECT * FROM "JobPosting"'))
    
    rows = result.fetchall()

    #format each row as a String
    output = []
    for row in rows:
        output.append(str(dict(row._mapping)))

    return output 
# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Age Calculator API"}


# @app.post("/application")
# def postApplication():
#     return {"message": "Application submitted successfully"} 

# @app.post("/apply/{candidate_id}")
# def applyForCandidate(candidate_id: int):
#     return {
#         "status": "success",
#         "message": f"Application for candidateID: {candidate_id} successfully submitted"}
    

@app.post("/applications")
def postApplications(candidate: Candidate):
    applications.append(candidate)
    return {
        "status": "success",
        "message": f"Application submitted for {candidate.name}"
    }

@app.get("/applications")
def getApplication(
    company_name: str = Query(None, description="optional query param for company name"),
    candidate_email: str = Query(None, description="optional query param for candidate email")
):
    if company_name:
        return {
            "status": "success",
            "message": f"Here is your application for {company_name}"
        }
    elif candidate_email:
        return {
            "status": "success",
            "message": f"Here is your application for {candidate_email}"
        }
    else:
        return {
            "status": "success",
            "message": "Here are all of your applications"
        }

@app.get("/applications/{candidate_id}")
def getApplicationById(candidate_id: str):
    for app in applications:
        if app.candidate_id == candidate_id:
            return {
                "status": "success",
                "message": f"Application found for candidate ID: {candidate_id}"
            }
    return {
        "status": "success",
        "message": "Application not found"
    }

@app.put("/applications/{candidate_id}")
def putApplications(
    candidate_id: str = Path(..., description="The ID of the candidate to update"),
    email: str = Query(None, description="New email address"),
    job_id: str = Query(None, description="New job ID")
):
    for app in applications:
        if app.candidate_id == candidate_id:
            if email:
                app.email = email
                return {
                    "status": "success",
                    "message": f"Email updated to {email}"
                }
            if job_id:
                app.job_id = job_id
                return {
                    "status": "success",
                    "message": f"Job ID updated to {job_id}"
                }
    return {
        "status": "success",
        "message": "Application not found"
    }

@app.delete("/applications/{candidate_id}")
def deleteApplication(candidate_id: str):
    for i, app in enumerate(applications):
        if app.candidate_id == candidate_id:
            applications.pop(i)
            return {
                "status": "success",
                "message": f"Application for {candidate_id} has been deleted"
            }
    return {
        "status": "success",
        "message": "Application not found"
    }




# # in memory list of applications, append applications to the list, 
# #cache  memory only leaves data while the server is running, fatest data i can access within the application
# applications = []


# # full application 
# class Application(BaseModel):
#     candidate_id: str
#     name: str
#     email: str
#     job_id: Optional[str] = None

# def get_db():
#     db = SessionLocal() #create a new connection to the database
#     try:
#         yield db
#     finally:
#         db.close()

# @app.get("/jobs")
# def get_all_job_postings(db: Session = Depends(get_db)):
#     result = db.execute(text('SELECT * FROM "JobPosting"'))
    
#     rows = result.fetchall()

#     #format each row as a String
#     output = []
#     for row in rows:
#         output.append(str(dict(row._mapping)))

#     return output   
    

# class UpdateApplication(BaseModel):
#     email: str
#     job_id: str

# class PartialUpdateApplication(BaseModel):
#     email: Optional[str] = None  #default is None
#     job_id: Optional[str] = None 

# # response when accessing the root url
# @app.get("/")
# def read_root():
#     return "Welcome to the Karen's API!"

# #submit an application and save to the list
# @app.post("/applications")
# def post_application(application: Application):
#     #input sanitation --> if the email fits the format
#     #name is at least 2 characters
#     applications.append(application) #append application to the list
#     return {
#         "status": "success",
#         "message": f"Application submitted for {application.name}"
#     }

# #get applications, optional query params for company name or candidate email
# @app.get("/applications")
# def get_applications(company_name: str = Query(None, description="Optional query param for company name"), candidate_email: str = Query(None, description="Optional query param for candidate email")):
    
#     if company_name:
#         return {"message": f"Here is your application for {company_name}"}
#     elif candidate_email:
#         return {"message": f"Here is your application for {candidate_email}"}
#     else: 
#         return {"message": "Here are all your applications"}
    
# #get applications using candidate id
# @app.get("/applications/{candidate_id}")    
# def get_candidate_id(candidate_id: str):
#     return {
#         "message": f"Application found for candidate ID: {candidate_id}"
#     }

#  #update an application using candidate id and save to the list 
# @app.put("/applications/{candidate_id}")
# def update_application(candidate_id: str, update: UpdateApplication):
#     #loop through applications list and update the application with the candidate id
#     for app in applications:
#         if app.candidate_id == candidate_id:
#             app.email = update.email
#             app.job_id = update.job_id
#             return { "message": f"Application for {candidate_id} successfully updated" }
#     return {"error": f"Application not found for candidate ID: {candidate_id}"}

# #partial update an application, email or job id, save to the list
# @app.patch("/applications/{candidate_id}")
# def partial_update_application(candidate_id: str, update: PartialUpdateApplication):
#     #loop through list of applications and update email or job id
#     for app in applications:
#         #find candidate id in the list
#         if app.candidate_id == candidate_id:
#             #keep track of update data and return it in a message
#             update_data = []
#             #update email or job id
#             if update.email is not None:
#                 app.email = update.email
#                 update_data.append("email")
#             if update.job_id is not None:
#                 app.job_id = update.job_id
#                 update_data.append("job_id")
#             if not update_data:
#                 return {"message": "There were not fields updated"}
#             return {"message": f"Application for {candidate_id} successfully updated with {','.join(update_data)}"}
#     return {"error": f"Application not found for candidate ID: {candidate_id}"} 

# #delete an application using candidate id
# @app.delete("/applications/{candidate_id}")
# def delete_application(candidate_id: str):
#     #loop through list to find candidate id
#     for app in applications:
#         if app.candidate_id == candidate_id:
#             applications.remove(app) #remove application from list
#             return {
#                 "status": "success",
#                 "message": f"Application for {candidate_id} successfully deleted"
#             }
#     return {"error": f"Application not found for candidate ID: {candidate_id}"}

