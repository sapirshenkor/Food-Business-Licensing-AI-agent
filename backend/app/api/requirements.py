"""
Requirements API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from app.models import RequirementsInfo
from app.services.database_loader import DatabaseLoader

router = APIRouter()

_database_loader = None

def set_dependencies(database_loader: DatabaseLoader, ai_processor):
    """Set dependencies from main.py"""
    global _database_loader
    _database_loader = database_loader

def get_database_loader():
    """Dependency to get database loader"""
    if _database_loader is None:
        raise HTTPException(status_code=503, detail="Database loader not initialized")
    return _database_loader

@router.get("/requirements", response_model=RequirementsInfo)
async def get_requirements_info(db_loader: DatabaseLoader = Depends(get_database_loader)):
    """Get information about available requirements"""
    
    if not db_loader or not db_loader.is_loaded():
        raise HTTPException(status_code=503, detail="Requirements database not loaded")
    
    info = db_loader.get_requirements_info()
    
    return RequirementsInfo(
        total_requirements=info["total_requirements"],
        categories=info["categories"],
        regulatory_authorities=info["regulatory_authorities"],
        last_processed=info["last_processed"]
    )

@router.get("/requirements/categories")
async def get_requirements_by_category(db_loader: DatabaseLoader = Depends(get_database_loader)):
    """Get requirements organized by category"""
    
    if not db_loader or not db_loader.is_loaded():
        raise HTTPException(status_code=503, detail="Requirements database not loaded")
    
    db = db_loader.get_database()
    
    return {
        "general_requirements": db.get('general_requirements', []),
        "size_specific_requirements": db.get('size_specific_requirements', []),
        "capacity_specific_requirements": db.get('capacity_specific_requirements', []),
        "feature_specific_requirements": db.get('feature_specific_requirements', [])
    }

@router.get("/requirements/authorities")
async def get_regulatory_authorities(db_loader: DatabaseLoader = Depends(get_database_loader)):
    """Get list of all regulatory authorities"""
    
    if not db_loader or not db_loader.is_loaded():
        raise HTTPException(status_code=503, detail="Requirements database not loaded")
    
    info = db_loader.get_requirements_info()
    
    return {
        "authorities": info["regulatory_authorities"],
        "count": len(info["regulatory_authorities"])
    }

@router.get("/requirements/search")
async def search_requirements(
    query: str = None,
    authority: str = None,
    category: str = None,
    db_loader: DatabaseLoader = Depends(get_database_loader)
):
    """Search requirements by query, authority, or category"""
    
    if not db_loader or not db_loader.is_loaded():
        raise HTTPException(status_code=503, detail="Requirements database not loaded")
    
    db = db_loader.get_database()
    
    # Get all requirements
    all_requirements = (
        db.get('general_requirements', []) +
        db.get('size_specific_requirements', []) +
        db.get('capacity_specific_requirements', []) +
        db.get('feature_specific_requirements', [])
    )
    
    filtered_requirements = []
    
    for req in all_requirements:
        # Filter by authority if specified
        if authority and authority.lower() not in req.get('authority', '').lower():
            continue
            
        # Filter by category if specified
        if category and category.lower() not in req.get('category', '').lower():
            continue
            
        # Filter by query if specified (search in name and description)
        if query:
            query_lower = query.lower()
            if (query_lower not in req.get('name', '').lower() and 
                query_lower not in req.get('description', '').lower()):
                continue
        
        filtered_requirements.append(req)
    
    return {
        "results": filtered_requirements,
        "count": len(filtered_requirements),
        "filters": {
            "query": query,
            "authority": authority,
            "category": category
        }
    }