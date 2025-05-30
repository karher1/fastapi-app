from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List

#Company Schemas
class CompanyBase(BaseModel):
    name: str #required
    industry: Optional[str] = None
    url: Optional[HttpUrl] = None
    headcount: Optional[int] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    is_public: Optional[bool] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    name: Optional[str] = None #here we are making name optional

class Company(CompanyBase):
    id: int

    class Config:
        from_attributes = True

#Job Posting Schemas
class JobPostingBase(BaseModel):
    title: str 
    company_id: int
    compensation_min: Optional[float] = None
    compensation_max: Optional[float] = None
    location_type: Optional[str] = None
    employment_type: Optional[str] = None
    description: Optional[str] = None

class JobPostingCreate(JobPostingBase):
    pass

class JobPostingUpdate(JobPostingBase):
    company_id: Optional[int] = None
    title: Optional[str] = None

class JobPosting(JobPostingBase):
    id: int

    class Config:
        from_attributes = True

class JobDescription(BaseModel): #this is for the inputs for the job description
    required_tools: List[str] = None
    company_culture: List[str] = None

#need job descripton response
class JobDescriptionResponse(BaseModel):
    about_company: str = Field(description="A compelling section about the company, including the company culture if provided")
    key_responsibilities: List[str] = Field(description="responsiblities of the job")
    required_qualifications: List[str] = Field(description="required qualifications for the job")
    preferred_qualifications: List[str] = Field(default=None,description="preferred qualifications for the job")
