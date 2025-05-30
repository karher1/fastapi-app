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
    title: str = Field(description="The title of the job posting")
    company_id: int = Field(description="The id of the company that is posting the job")
    compensation_min: Optional[float] = Field(default=None, description="The minimum compensation for the job")
    compensation_max: Optional[float] = Field(default=None, description="The maximum compensation for the job")
    location_type: Optional[str] = Field(default=None, description="The location type of the job")
    employment_type: Optional[str] = Field(default=None, description="The employment type of the job")
    description: Optional[str] = Field(default=None, description="The description of the job")

class JobPostingCreate(JobPostingBase):
    pass

class JobPostingUpdate(JobPostingBase):
    company_id: Optional[int] = None
    title: Optional[str] = None

class JobPosting(JobPostingBase):
    id: int

    class Config:
        from_attributes = True

class JobDescription(BaseModel):
    required_tools: List[str] = Field(default=None,description="List of tools the company is requiring for the job")
    company_culture: List[str] = Field(default=None,description="List of company culture values")
