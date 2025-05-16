from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# in memory list of applications, append applications to the list
applications = []


# full application 
class Application(BaseModel):
    candidate_id: str
    name: str
    email: str
    job_id: str

class UpdateApplication(BaseModel):
    email: str
    job_id: str

class PartialUpdateApplication(BaseModel):
    email: Optional[str] = None  #default is None
    job_id: Optional[str] = None 

# response when accessing the root url
@app.get("/")
def read_root():
    return "Welcome to the Karen's API!"

#submit an application and save to the list
@app.post("/applications")
def post_application(application: Application):
    applications.append(application) #append application to the list
    return {
        "status": "success",
        "message": f"Application submitted for {application.name}"
    }

#get applications, optional query params for company name or candidate email
@app.get("/applications")
def get_applications(company_name: str = Query(None, description="Optional query param for company name"), candidate_email: str = Query(None, description="Optional query param for candidate email")):
    
    if company_name:
        return {"message": f"Here is your application for {company_name}"}
    elif candidate_email:
        return {"message": f"Here is your application for {candidate_email}"}
    else: 
        return {"message": "Here are all your applications"}
    
#get applications using candidate id
@app.get("/applications/{candidate_id}")    
def get_candidate_id(candidate_id: str):
    return {
        "message": f"Application found for candidate ID: {candidate_id}"
    }

 #update an application using candidate id and save to the list 
@app.put("/applications/{candidate_id}")
def update_application(candidate_id: str, update: UpdateApplication):
    #loop through applications list and update the application with the candidate id
    for app in applications:
        if app.candidate_id == candidate_id:
            app.email = update.email
            app.job_id = update.job_id
            return { "message": f"Application for {candidate_id} successfully updated" }
    return {"error": f"Application not found for candidate ID: {candidate_id}"}

#partial update an application, email or job id, save to the list
@app.patch("/applications/{candidate_id}")
def partial_update_application(candidate_id: str, update: PartialUpdateApplication):
    #loop through list of applications and update email or job id
    for app in applications:
        #find candidate id in the list
        if app.candidate_id == candidate_id:
            #keep track of update data and return it in a message
            update_data = []
            #update email or job id
            if update.email is not None:
                app.email = update.email
                update_data.append("email")
            if update.job_id is not None:
                app.job_id = update.job_id
                update_data.append("job_id")
            if not update_data:
                return {"message": "There were not fields updated"}
            return {"message": f"Application for {candidate_id} successfully updated with {','.join(update_data)}"}
    return {"error": f"Application not found for candidate ID: {candidate_id}"} 

#delete an application using candidate id
@app.delete("/applications/{candidate_id}")
def delete_application(candidate_id: str):
    #loop through list to find candidate id
    for app in applications:
        if app.candidate_id == candidate_id:
            applications.remove(app) #remove application from list
            return {
                "status": "success",
                "message": f"Application for {candidate_id} successfully deleted"
            }
    return {"error": f"Application not found for candidate ID: {candidate_id}"}

