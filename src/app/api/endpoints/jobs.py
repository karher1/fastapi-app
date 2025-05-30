from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.responses import StreamingResponse
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime

from app.db.session import get_db
from app.models import models
from app.schemas import schemas
from app.core.config import settings
from app.api.services.job_generator import openai_stream

import openai
import json

router = APIRouter()

openai.api_key = settings.OPENAI_API_KEY

@router.post("/", response_model=schemas.JobPosting)
def create_job_posting(job: schemas.JobPostingCreate, db: Session = Depends(get_db)):
    # Verify company exists
    company = db.query(models.Company).filter(models.Company.id == job.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_job = models.JobPosting(**job.model_dump()) #create a JobPosting Object with default values (**job.model_dump()) just pass all the required constructor values
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/", response_model=List[schemas.JobPosting])
def read_job_postings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(models.JobPosting).offset(skip).limit(limit).all()
    return jobs

#jobs/6
@router.get("/{job_id}", response_model=schemas.JobPosting)
def read_job_posting(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job posting not found")
    return db_job

@router.put("/{job_id}", response_model=schemas.JobPosting)
def update_job_posting(job_id: int, job: schemas.JobPostingUpdate, db: Session = Depends(get_db)):
    db_job = db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job posting not found")
    
    # If company_id is being updated, verify the new company exists
    if job.company_id is not None:
        company = db.query(models.Company).filter(models.Company.id == job.company_id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
    
    update_data = job.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_job, field, value)
    
    db.commit()
    db.refresh(db_job)
    return db_job

@router.delete("/{job_id}")
def delete_job_posting(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job posting not found")
    
    db.delete(db_job)
    db.commit()
    return {"message": "Job posting deleted successfully"} 

#this is post to get the job description to the clien using langchain
@router.post("/{job_id}/description")
def generate_job_description(job_id: int, request: schemas.JobDescription, db: Session = Depends(get_db)):
    # 1. get the job posting
    db_job = db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail= "Job posting not found")
    
    # 2. Optional JSON data for required tools and company culture
    tools_required = (", ").join(request.required_tools)
    company_culture = (", ").join(request.company_culture)
    
    # 3. Create the prompt
    
    messages = ChatPromptTemplate.from_messages([
        SystemMessage(content="You are a helpful assistant that generates professional job descriptions for job postings."),
        HumanMessage(content=f"""Write a professional job description for the following job:
                    Job Title: {db_job.title}
                    Company: {db_job.company.name}
                    Required tools: {tools_required}
                    Respond in structured plain text, without using markdown or # symbols for headers. Include:
                    1. About the Company a compellling section, with the company culture if provided: {company_culture}
                    2. Key Responsibilities
                    3. Required Qualifications
                    4. Optional: Preferred qualifications
                    Use professional language and make it engaging and interesting
                     """)
    ])

    # 4. format the response
    formatted_messages = messages.format_messages(
        job_title = db_job.title,
        company=db_job.company.name,
        tools_required=tools_required,
    )
    # 5. call the model
    model = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0, max_tokens=300)
    response = model.invoke(formatted_messages)

    # 6. Save the job description to the database
    db_job.description = response.content
    db.commit()
    db.refresh(db_job)
   
    # 7. return the response
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "job_id": job_id,
        "description": response.content,
        "message": "Job descripton was successfully generated and saved",
        "timestamp": now

    }


# #this will be for getting the job description in chunks
# @router.get("/{job_id}/description/stream")
# def stream_job_description(job_id: int, db: Session = Depends(get_db)):
#     db_job = db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first()
#     if db_job is None:
#         raise HTTPException(status_code=404, detail="Job posting not found")
    
#     try: 
#         #parse the required tools
#         if db_job.required_tools:
#             try:
#                 tools_list_raw = json.loads(db_job.required_tools)
#             except json.JSONDecodeError:
#                 tools_list_raw = []
#         else:
#             tools_list_raw = []

#     #create the prompt for OPENAI
#         tools_list = ", ".join(tools_list_raw)if tools_list_raw else "N/S"
#         prompt = f"""Write a professional job description for the following the job title:
#     Job Title:{db_job.title} 
#     Company: {db_job.company.name}
#     Required tools: {tools_list}, respond in structured plain tect, without using Markdown or # symbols for headers.
#     make sure to include:
#     1. About the Company a compelling section
#     2. Key responsiblilities
#     3. Required Qualifications
#     4. Optional: Preferred qualifications
#     5. Use professiona language and make it engaging and interesting
#     """
#     #call OPENAI API
#         return StreamingResponse(openai_stream(prompt), media_type="text/plain")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Streaming failed: {str(e)}")

