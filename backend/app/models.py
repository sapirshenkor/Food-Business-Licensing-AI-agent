"""
Pydantic models for Business Licensing AI API
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class SurveyRequest(BaseModel):
    """User survey data model"""
    size: float = Field(..., ge=10, le=10000, description="Business size in square meters")
    max_people: int = Field(..., ge=1, le=1000, description="Maximum occupancy")
    uses_gas: bool = Field(..., description="Uses gas for cooking")
    has_delivery: bool = Field(..., description="Provides delivery service")
    serves_meat: bool = Field(..., description="Serves meat dishes")
    business_name: Optional[str] = Field(None, description="Business name (optional)")
    location: Optional[str] = Field(None, description="Business location (optional)")
    
    @validator('size')
    def validate_size(cls, v):
        if v <= 0:
            raise ValueError("Size must be positive")
        return v
    
    @validator('max_people')
    def validate_capacity(cls, v):
        if v <= 0:
            raise ValueError("Capacity must be positive")
        return v

class RequirementResponse(BaseModel):
    """Single requirement response model"""
    id: str
    name: str
    category: str
    authority: str
    description: str
    timeline: Optional[str] = None
    estimated_cost: Optional[str] = None
    priority: Optional[str] = "medium"
    source_location: Optional[str] = None
    why_relevant: str  # Why this requirement applies to the user's business

class SurveyResponse(BaseModel):
    """Complete survey response model"""
    success: bool
    survey_data: SurveyRequest
    relevant_requirements: List[RequirementResponse]
    personalized_report: str
    requirements_count: int
    estimated_total_cost: Optional[str] = None
    estimated_total_time: Optional[str] = None
    timestamp: datetime

class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    database_loaded: bool
    total_requirements: int
    ai_processor_ready: bool

class RequirementsInfo(BaseModel):
    """Requirements database info"""
    total_requirements: int
    categories: dict
    regulatory_authorities: List[str]
    last_processed: str

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)