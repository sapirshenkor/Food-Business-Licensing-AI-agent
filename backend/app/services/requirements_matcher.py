"""
Requirements matching service - matches user survey to relevant requirements
"""

from typing import List, Dict
from app.models import SurveyRequest, RequirementResponse

class RequirementsMatcher:
    def __init__(self, requirements_db: Dict):
        self.db = requirements_db
    
    def filter_requirements_for_business(self, survey: SurveyRequest):
        """Filter requirements based on business characteristics"""
        relevant_requirements = []
        
        # Get all requirement categories
        all_requirements = (
            self.db.get('general_requirements', []) +
            self.db.get('size_specific_requirements', []) +
            self.db.get('capacity_specific_requirements', []) +
            self.db.get('feature_specific_requirements', [])
        )
        
        for req in all_requirements:
            relevance_result = self._check_requirement_relevance(req, survey)
            
            if relevance_result['is_relevant']:
                relevant_requirements.append(RequirementResponse(
                    id=req.get('id', 'unknown'),
                    name=req.get('name', 'unknown'),
                    category=req.get('category', 'unknown'),
                    authority=req.get('authority', 'unknown'),
                    description=req.get('description', ''),
                    timeline=req.get('timeline'),
                    estimated_cost=req.get('estimated_cost'),
                    priority=req.get('priority', 'medium'),
                    source_location=req.get('source_location'),
                    why_relevant=relevance_result['reason']
                ))
        
        return relevant_requirements
    
    def _check_requirement_relevance(self, req: Dict, survey: SurveyRequest):
        """Check if a requirement is relevant to the business and return reason"""
        
        # Check general requirements (usually apply to all)
        if req in self.db.get('general_requirements', []):
            return {
                'is_relevant': True,
                'reason': 'חובה על כל העסקים'
            }
        
        # Check size-specific requirements
        elif req in self.db.get('size_specific_requirements', []):
            conditions = req.get('conditions', {})
            min_size = conditions.get('min_size_sqm')
            max_size = conditions.get('max_size_sqm')
            
            # Check size constraints
            if min_size is not None and survey.size < min_size:
                return {'is_relevant': False, 'reason': ''}
            if max_size is not None and survey.size > max_size:
                return {'is_relevant': False, 'reason': ''}
                
            return {
                'is_relevant': True,
                'reason': f'חל על עסקים בגודל {survey.size} מ"ר'
            }
        
        # Check capacity-specific requirements
        elif req in self.db.get('capacity_specific_requirements', []):
            conditions = req.get('conditions', {})
            min_capacity = conditions.get('min_capacity')
            max_capacity = conditions.get('max_capacity')
            
            # Check capacity constraints
            if min_capacity is not None and survey.max_people < min_capacity:
                return {'is_relevant': False, 'reason': ''}
            if max_capacity is not None and survey.max_people > max_capacity:
                return {'is_relevant': False, 'reason': ''}
                
            return {
                'is_relevant': True,
                'reason': f'חל על עסקים עם תפוסה של {survey.max_people} אנשים'
            }
        
        # Check feature-specific requirements
        elif req in self.db.get('feature_specific_requirements', []):
            conditions = req.get('conditions', {})
            
            # Check gas requirement
            if conditions.get('requires_gas') is True and not survey.uses_gas:
                return {'is_relevant': False, 'reason': ''}
            if conditions.get('requires_gas') is False and survey.uses_gas:
                return {'is_relevant': False, 'reason': ''}
                
            # Check delivery requirement
            if conditions.get('has_delivery') is True and not survey.has_delivery:
                return {'is_relevant': False, 'reason': ''}
            if conditions.get('has_delivery') is False and survey.has_delivery:
                return {'is_relevant': False, 'reason': ''}
                
            # Check meat serving requirement
            if conditions.get('serves_meat') is True and not survey.serves_meat:
                return {'is_relevant': False, 'reason': ''}
            if conditions.get('serves_meat') is False and survey.serves_meat:
                return {'is_relevant': False, 'reason': ''}
            
            # If we get here, it's relevant - build reason from features
            features = []
            if survey.uses_gas: features.append("שימוש בגז")
            if survey.has_delivery: features.append("משלוחים")
            if survey.serves_meat: features.append("הגשת בשר")
            
            return {
                'is_relevant': True,
                'reason': f'רלוונטי למאפיינים: {", ".join(features)}' if features else 'רלוונטי למאפיינים מיוחדים'
            }
        
        # Default: not relevant
        return {'is_relevant': False, 'reason': ''}