"""
The main FastAPI application
Clean, organized structure for Business Licensing AI System
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os
from app.api import health, survey, requirements
from app.services.database_loader import DatabaseLoader
from document_processor import ComprehensiveDocumentProcessor

# Add parent directory to path for document_processor import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Global application state
app_state = {}

# Initialize FastAPI app
app = FastAPI(
    title="Business Licensing AI API",
    description="AI-powered system for Israeli business licensing requirements",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",  # Alternative React port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(survey.router, prefix="/api", tags=["Survey"])
app.include_router(requirements.router, prefix="/api", tags=["Requirements"])

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize services on application startup"""
    print("🚀 Starting Business Licensing AI API...")
    
    # Initialize database loader
    print("📄 Loading requirements database...")
    app_state['database_loader'] = DatabaseLoader()
    db_result = await app_state['database_loader'].load_requirements_database()
    
    if db_result:
        info = app_state['database_loader'].get_requirements_info()
        print(f"✅ Database loaded: {info['total_requirements']} requirements")
    else:
        print("⚠️ Database loading failed")
    
    # Initialize AI processor
    print("🤖 Initializing AI processor...")
    try:
        app_state['ai_processor'] = ComprehensiveDocumentProcessor()
        print("✅ AI processor initialized")
    except Exception as e:
        print(f"⚠️ AI processor initialization failed: {e}")
        app_state['ai_processor'] = None
    
    health.set_dependencies(app_state['database_loader'], app_state['ai_processor'])
    survey.set_dependencies(app_state['database_loader'], app_state['ai_processor'])
    requirements.set_dependencies(app_state['database_loader'], app_state['ai_processor'])

    print("✅ API startup complete")
    print("📖 API Documentation available at: http://localhost:8000/docs")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    print("🛑 Shutting down Business Licensing AI API...")
    
    # Print final usage statistics if AI processor exists
    ai_processor = app_state.get('ai_processor')
    if ai_processor and hasattr(ai_processor, 'usage_tracker'):
        usage = ai_processor.usage_tracker
        print(f"📊 Final API Usage:")
        print(f"   • Total Calls: {usage.get('total_calls', 0)}")
        print(f"   • Total Cost: ${usage.get('total_cost', 0):.4f}")
    
    print("✅ Shutdown complete")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    db_loader = app_state.get('database_loader')
    total_reqs = 0
    
    if db_loader and db_loader.is_loaded():
        info = db_loader.get_requirements_info()
        total_reqs = info.get('total_requirements', 0)
    
    return {
        "message": "Business Licensing AI API",
        "version": "1.0.0",
        "status": "running",
        "database": {
            "loaded": db_loader.is_loaded() if db_loader else False,
            "total_requirements": total_reqs
        },
        "ai_processor": {
            "available": app_state.get('ai_processor') is not None
        },
        "endpoints": {
            "health": "/api/health",
            "survey_submit": "/api/survey/submit",
            "requirements_info": "/api/requirements",
            "documentation": "/docs"
        }
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Endpoint not found",
        "message": "The requested endpoint does not exist",
        "available_endpoints": {
            "root": "/",
            "health": "/api/health",
            "survey": "/api/survey/submit",
            "requirements": "/api/requirements",
            "docs": "/docs"
        }
    }

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "error": "Internal server error",
        "message": "An unexpected error occurred",
        "support": "Check server logs for details"
    }

# Run server
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        reload=True,
        
    )