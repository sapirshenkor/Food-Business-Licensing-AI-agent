"""
Survey API endpoints
"""

import os
import json
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from typing import List

from app.models import SurveyRequest, SurveyResponse, RequirementResponse
from app.services.database_loader import DatabaseLoader
from app.services.requirements_matcher import RequirementsMatcher
from app.services.report_generator import ReportGenerator

router = APIRouter()

_database_loader = None
_ai_processor = None

def set_dependencies(database_loader: DatabaseLoader, ai_processor):
    """Set dependencies from main.py"""
    global _database_loader, _ai_processor
    _database_loader = database_loader
    _ai_processor = ai_processor

def get_database_loader():
    """Dependency to get database loader"""
    if _database_loader is None:
        raise HTTPException(status_code=503, detail="Database loader not initialized")
    return _database_loader

def get_ai_processor():
    """Dependency to get AI processor"""
    return _ai_processor  

@router.post("/survey/submit", response_model=SurveyResponse)
async def submit_survey(
    survey_data: SurveyRequest,
    db_loader: DatabaseLoader = Depends(get_database_loader),
    ai_processor = Depends(get_ai_processor)
):
    """
    Process user survey and return personalized business licensing report
    
    Args:
        survey_data: User's business information
        
    Returns:
        SurveyResponse: Personalized report with relevant requirements
    """
    
    # Check if database is loaded
    if not db_loader or not db_loader.is_loaded():
        raise HTTPException(
            status_code=503, 
            detail="Requirements database not loaded. Please check server logs."
        )
    
    try:
        requirements_db = db_loader.get_database()
        
        # Initialize matcher service
        matcher = RequirementsMatcher(requirements_db)
        
        # Filter relevant requirements based on survey data
        relevant_requirements = matcher.filter_requirements_for_business(survey_data)
        
        if not relevant_requirements:
            raise HTTPException(
                status_code=404,
                detail="No relevant requirements found for your business profile"
            )
        
        # Initialize report generator
        report_generator = ReportGenerator(ai_processor)
        
        # Generate AI-powered personalized report
        personalized_report = await report_generator.generate_personalized_report(
            survey_data, 
            relevant_requirements
        )
        
        # Calculate estimates 
        total_cost_estimate = report_generator.calculate_total_cost_estimate(relevant_requirements)
        total_time_estimate = report_generator.calculate_total_time_estimate(relevant_requirements)
        
        # Save survey response for analytics (optional)
        await save_survey_response(survey_data, relevant_requirements)
        
        return SurveyResponse(
            success=True,
            survey_data=survey_data,
            relevant_requirements=relevant_requirements,
            personalized_report=personalized_report,
            requirements_count=len(relevant_requirements),
            estimated_total_cost=total_cost_estimate,
            estimated_total_time=total_time_estimate,
            timestamp=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Survey processing error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/survey/test")
async def test_survey_endpoint():
    """Test endpoint for survey API"""
    return {
        "message": "Survey API is working",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "submit": "POST /survey/submit",
            "test": "GET /survey/test"
        }
    }

async def save_survey_response(survey: SurveyRequest, requirements: List[RequirementResponse]):
    """Save survey response for analytics (optional)"""
    try:
        # Create responses directory if it doesn't exist
        responses_dir = os.path.join("data", "responses")
        os.makedirs(responses_dir, exist_ok=True)
        
        # Create response data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"survey_{timestamp}.json"
        
        response_data = {
            "timestamp": datetime.now().isoformat(),
            "survey_data": survey.dict(),
            "requirements_count": len(requirements),
            "requirements": [req.dict() for req in requirements]
        }
        
        # Save to file
        file_path = os.path.join(responses_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(response_data, f, ensure_ascii=False, indent=2)
        
        print(f"📊 Survey response saved: {filename}")
        
    except Exception as e:
        print(f"⚠️ Error saving survey response: {e}")
        # Don't raise error - this shouldn't block the main response