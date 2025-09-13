"""
Database loader service from requirements.json
"""

import json
import os
from typing import Dict, Optional

class DatabaseLoader:
    def __init__(self):
        self.requirements_db = None
        
    async def load_requirements_database(self):
        """Load the processed requirements JSON file"""
        db_path = os.path.join("data", "processed", "requirements.json")
        
        try:
            if os.path.exists(db_path):
                with open(db_path, 'r', encoding='utf-8') as f:
                    self.requirements_db = json.load(f)
                
                total_reqs = self.requirements_db.get('summary', {}).get('total_requirements', 0)
                print(f"✅ Requirements database loaded: {total_reqs} requirements")
                return self.requirements_db
            else:
                print(f"❌ Requirements database not found at: {db_path}")
                print("Please run document_processor.py first to create the database")
                return None
                
        except Exception as e:
            print(f"❌ Error loading requirements database: {e}")
            return None
    
    def get_database(self):
        """Get the loaded database"""
        return self.requirements_db
    
    def is_loaded(self):
        """Check if database is loaded"""
        return self.requirements_db is not None
    
    def get_requirements_info(self):
        """Get summary information about the requirements database"""
        if not self.requirements_db:
            return {
                "total_requirements": 0,
                "categories": {},
                "regulatory_authorities": [],
                "last_processed": "unknown"
            }
        
        db = self.requirements_db
        
        return {
            "total_requirements": db.get('summary', {}).get('total_requirements', 0),
            "categories": {
                "general": len(db.get('general_requirements', [])),
                "size_specific": len(db.get('size_specific_requirements', [])),
                "capacity_specific": len(db.get('capacity_specific_requirements', [])),
                "feature_specific": len(db.get('feature_specific_requirements', []))
            },
            "regulatory_authorities": db.get('document_analysis', {}).get('regulatory_authorities', []),
            "last_processed": db.get('processing_metadata', {}).get('processed_at', 'unknown')
        }