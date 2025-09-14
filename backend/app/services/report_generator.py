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
                model="claude-sonnet-4-20250514",
                max_tokens=6000,
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
אתה יועץ עסקי מקצועי המתמחה ברישוי עסקים בישראל. צור דוח מותאם אישית בעברית עבור:

## נתוני העסק:
- **סוג עסק**: עסק מזון
- **גודל**: {survey.size} מ"ר
- **תפוסה מקסימלית**: {survey.max_people} מקומות ישיבה
- **שימוש בגז**: {'כן' if survey.uses_gas else 'לא'}
- **שירות משלוחים**: {'כן' if survey.has_delivery else 'לא'}
- **הגשת בשר**: {'כן' if survey.serves_meat else 'לא'}

## דרישות רגולטוריות רלוונטיות:
{json.dumps(requirements_summary, ensure_ascii=False, indent=2)}

---

צור דוח מקצועי ומפורט הכולל את הסעיפים הבאים:

### 1. 📋 סיכום מנהלים (2-3 שורות)
- סך הכל רישיונות נדרשים
- זמן כולל משוער לקבלת כל הרישיונות
- עלות כוללת משוערת
- המלצה עיקרית אחת

### 2. 📜 רישיונות ואישורים נדרשים
עבור כל רישיון ציין:
- **שם הרישיון**: [שם מדויק]
- **גוף מוסמך**: [רשות/משרד]
- **זמן טיפול**: [מסגרת זמן]
- **עלות משוערת**: [טווח מחירים]
- **מסמכים נדרשים**: [אם ידוע]
- **למה זה חשוב**: [הסבר קצר למה הדרישה חלה על העסק הזה]

### 3. ⏰ לוח זמנים מומלץ (סדר עדיפויות)
ארגן את הרישיונות לפי סדר המומלץ:
- **שלב 1 (התחלה)**: רישיונות שחובה לקבל קודם
- **שלב 2 (במקביל)**: רישיונות שאפשר לטפל בהם בו-זמנית
- **שלב 3 (סיום)**: רישיונות אחרונים לפני פתיחה

### 4. 💰 עלויות משוערות
- פירוט עלויות לפי רישיון
- סך הכל משוער
- עלויות נוספות אפשריות (עורכי דין, יועצים)
- טיפים לחיסכון

### 5. ✅ רשימת מטלות לביצוע (צ'קליסט)
רשימה מסודרת של פעולות:
- [ ] משימה 1
- [ ] משימה 2
- וכו...

### 6. ⚠️ הערות חשובות
- מה קורה אם לא מקבלים רישיון מסוים?
- על מה חשוב לשמור מיוחד?
- טעויות נפוצות להימנע מהן
- לא להמציא מידע, רק על סמך הנתונים
- שים לב לדרישות שבאמת נדרש לצורך אישור העסק
- שים לב לגופים שלא נדרשים באישור העסק אם קיימים ציין זאת או התעלם מדרישות שלהם



---

**הנחיות לכתיבה:**
- השתמש בשפה עסקית ברורה ופשוטה, לא "שפת חוק"
- כתוב בגוף שני ("אתה צריך", "עליך לעשות")
- הוסף אייקונים (📋, ⏰, 💰, ✅, ⚠️, 📞) לקריאות טובה יותר
- תן דגש על היבטים מעשיים ופעולות קונקרטיות
- הסבר למה כל דרישה חלה על העסק הספציפי הזה
- ציין מסגרות זמן ברורות
- כלול טיפים מעשיים וטעויות להימנע מהן
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