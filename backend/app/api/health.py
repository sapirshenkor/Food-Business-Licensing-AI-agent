"""
Health check API endpoints
"""

from fastapi import APIRouter, Depends
from datetime import datetime
from app.models import HealthCheck
from app.services.database_loader import DatabaseLoader

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
    return _database_loader

@router.get("/health", response_model=HealthCheck)
async def health_check(db_loader: DatabaseLoader = Depends(get_database_loader)):
    """API health check endpoint"""
    
    # Check database status
    db_loaded = db_loader.is_loaded() if db_loader else False
    total_reqs = 0
    
    if db_loaded:
        info = db_loader.get_requirements_info()
        total_reqs = info.get('total_requirements', 0)
    
    # Check AI processor status
    ai_ready = _ai_processor is not None
    
    return HealthCheck(
        status="healthy" if db_loaded else "degraded",
        timestamp=datetime.now(),
        database_loaded=db_loaded,
        total_requirements=total_reqs,
        ai_processor_ready=ai_ready
    )

@router.get("/health/detailed")
async def detailed_health_check(db_loader: DatabaseLoader = Depends(get_database_loader)):
    """Detailed health check with more information"""
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "components": {
            "database": {
                "status": "healthy" if db_loader and db_loader.is_loaded() else "unhealthy",
                "details": db_loader.get_requirements_info() if db_loader else {}
            },
            "ai_processor": {
                "status": "healthy" if _ai_processor else "unhealthy",
                "details": {
                    "initialized": _ai_processor is not None,
                    "usage_tracker": getattr(_ai_processor, 'usage_tracker', {})
                }
            }
        },
        "overall_status": "healthy" if all([
            db_loader and db_loader.is_loaded(),
            _ai_processor
        ]) else "degraded"
    }
    
    return result