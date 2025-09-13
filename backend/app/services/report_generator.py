"""
AI-powered report generation service
"""

import json
import re
from typing import List
from app.models import SurveyRequest, RequirementResponse

class ReportGenerator:
    def __init__(self, ai_processor=None):
        self.ai_processor = ai_processor
    
    async def generate_personalized_report(self, survey: SurveyRequest, requirements: List[RequirementResponse]):
        """Generate AI-powered personalized report"""
        
        if not self.ai_processor:
            # Fallback: Generate basic report without AI
            return self._generate_basic_report(survey, requirements)
        
        try:
            # Prepare data for AI
            requirements_summary = []
            for req in requirements:
                requirements_summary.append({
                    'name': req.name,
                    'authority': req.authority,
                    'timeline': req.timeline,
                    'cost': req.estimated_cost,
                    'description': req.description,
                    'why_relevant': req.why_relevant
                })
            
            prompt = self._build_ai_prompt(survey, requirements_summary)
            
            # Generate report with AI
            response = self.ai_processor.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=3000,
                system="Generate clear, practical business guidance in Hebrew.",
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Track usage
            self.ai_processor._update_usage_tracker(response.usage)
            
            return response.content[0].text
            
        except Exception as e:
            print(f"❌ AI report generation failed: {e}")
            return self._generate_basic_report(survey, requirements)
    
    def _build_ai_prompt(self, survey: SurveyRequest, requirements_summary: List[dict]):
        """Build AI prompt for report generation"""
        return f"""
צור דוח רישוי עסקים מותאם אישית בעברית עבור:

מאפייני העסק:
- גודל: {survey.size} מ"ר
- תפוסה מקסימלית: {survey.max_people} אנשים
- שימוש בגז: {'כן' if survey.uses_gas else 'לא'}
- משלוחים: {'כן' if survey.has_delivery else 'לא'}
- הגשת בשר: {'כן' if survey.serves_meat else 'לא'}

דרישות רלוונטיות:
{json.dumps(requirements_summary, ensure_ascii=False, indent=2)}

צור דוח מקצועי הכולל:
1. **סיכום מנהלים** - העיקרים בקצרה
2. **רישיונות נדרשים** - רשימה ברורה עם זמנים
3. **לוח זמנים מומלץ** - איך לתעדף
4. **עלויות משוערות** - סיכום כספי
5. **רשימת פעולות** - צ'קליסט מעשי

השתמש בשפה עסקית ברורה, לא "שפת חוק".
        """
    
    def _generate_basic_report(self, survey: SurveyRequest, requirements: List[RequirementResponse]):
        """Generate basic report without AI (fallback)"""        
        report = f"""
# דוח רישוי עסקים

## פרטי העסק
- **גודל**: {survey.size} מ"ר
- **תפוסה**: {survey.max_people} אנשים
- **שימוש בגז**: {'כן' if survey.uses_gas else 'לא'}
- **משלוחים**: {'כן' if survey.has_delivery else 'לא'}
- **הגשת בשר**: {'כן' if survey.serves_meat else 'לא'}

## רישיונות ואישורים נדרשים ({len(requirements)})

"""
        
        for i, req in enumerate(requirements, 1):
            report += f"""
### {i}. {req.name}
- **גוף מוסמך**: {req.authority}
- **זמן טיפול**: {req.timeline or 'לא מוגדר'}
- **עלות משוערת**: {req.estimated_cost or 'לא מוגדר'}
- **סיבה**: {req.why_relevant}
- **תיאור**: {req.description}

"""
        
        total_cost = self.calculate_total_cost_estimate(requirements)
        total_time = self.calculate_total_time_estimate(requirements)
        
        report += f"""
## סיכום
- **סך הכל רישיונות**: {len(requirements)}
- **עלות משוערת**: {total_cost}
- **זמן משוער**: {total_time}

**המלצה**: התחל בדרישות הכלליות ולאחר מכן עבור לדרישות הספציפיות.
        """
        
        return report
    
    def calculate_total_cost_estimate(self, requirements: List[RequirementResponse]):
        """Calculate estimated total cost from requirements"""
        costs = []
        
        for req in requirements:
            cost_str = req.estimated_cost
            if cost_str and cost_str != "לא מוגדר" and "₪" in cost_str:
                try:
                    # Extract numbers from strings like "500-800 ₪"
                    numbers = re.findall(r'\d+', cost_str)
                    if numbers:
                        if len(numbers) >= 2:
                            # Take average if range given
                            avg_cost = (int(numbers[0]) + int(numbers[1])) / 2
                        else:
                            # Use single number
                            avg_cost = int(numbers[0])
                        costs.append(avg_cost)
                except:
                    continue
        
        if costs:
            total = sum(costs)
            return f"{int(total):,} ₪ (אומדן)"
        
        return "לא מוגדר"

    def calculate_total_time_estimate(self, requirements: List[RequirementResponse]):
        """Calculate estimated total time from requirements"""
        times = []
        
        for req in requirements:
            timeline = req.timeline
            if timeline and "שבוע" in timeline:
                try:
                    # Extract weeks from strings like "4-6 שבועות"
                    weeks = re.findall(r'\d+', timeline)
                    if weeks:
                        # Take maximum weeks if range given
                        max_weeks = max([int(w) for w in weeks])
                        times.append(max_weeks)
                except:
                    continue
        
        if times:
            max_time = max(times)
            return f"{max_time} שבועות (משוער)"
        
        return "לא מוגדר"