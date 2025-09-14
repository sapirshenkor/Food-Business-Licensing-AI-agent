# 🏢 Business Licensing AI System

מערכת AI מתקדמת לסיוע ברישוי עסקים בישראל - עיבוד מסמכים רגולטוריים ויצירת דוחות מותאמים אישית

## 📋 תיאור הפרויקט

### מטרות המערכת

מערכת Business Licensing AI נועדה לעזור לבעלי עסקים בישראל להבין את דרישות הרישוי הרלוונטיות לעסק שלהם. המערכת מעבדת מסמכים רגולטוריים בעברית באמצעות AI ומחזירה דוחות מותאמים אישית עם הדרישות הרגולטוריות הרלוונטיות.

### בעיה שנפתרת

- **מורכבות רגולטורית**: עסקים צריכים לנווט בין דרישות של רשויות שונות
- **מידע מפוזר**: דרישות מפוזרות בין משרדים ומסמכים שונים
- **שפת חוק**: מסמכים רגולטוריים כתובים בשפה מורכבת ולא נגישה
- **התאמה אישית**: כל עסק צריך דרישות שונות לפי גודל, תפוסה ומאפיינים

### הפתרון

מערכת חכמה המשלבת:

- **עיבוד מסמכים בעברית** באמצעות Claude AI
- **התאמה אלגוריתמית** בין מאפייני העסק לדרישות רגולטוריות
- **יצירת דוחות מותאמים אישית** בשפה עסקית ברורה
- **ממשק משתמש ידידותי** בעברית עם תמיכה ב-RTL

## 🏗️ ארכיטקטורת המערכת

### דיאגרמת מערכת

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   📄 Hebrew     │    │   🤖 Claude AI   │    │   💾 Structured │
│   Regulatory    │───▶│   Document       │───▶│   Requirements  │
│   Document      │    │   Processor      │    │   Database      │
│   (59 pages)    │    │   (Phase 1)      │    │   (JSON)        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   📱 React      │    │   🖥️ FastAPI     │    │   🎯 Smart      │
│   Frontend      │◀──▶│   Backend        │◀───│   Requirements │
│   (Survey UI)   │    │   (API Server)   │    │   Matcher       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                ▲
                                │
                       ┌──────────────────┐
                       │   🤖 Claude AI   │
                       │   Report         │
                       │   Generator      │
                       │   (Phase 2)      │
                       └──────────────────┘
```

### רכיבי המערכת

#### Phase 1: עיבוד מסמכים (One-time)

- **Document Extractor**: חילוץ טקסט מ-Word/PDF
- **AI Document Processor**: עיבוד חכם עם Claude API
- **Requirements Database**: מאגר דרישות מובנה (JSON)

#### Phase 2: שירות למשתמשים (Real-time)

- **React Frontend**: ממשק משתמש לשאלון ותצוגת דוחות
- **FastAPI Backend**: שרת API לעיבוד בקשות
- **Requirements Matcher**: אלגוריתם התאמת דרישות
- **AI Report Generator**: יצירת דוחות מותאמים אישית

## 🚀 הוראות התקנה והרצה

### דרישות מערכת

- **Python 3.8+**
- **Node.js 16+**
- **npm או yarn**
- **חשבון Anthropic Claude API**

### התקנה

#### 1. שכפול הפרויקט

```bash
git clone <repository-url>
cd business-licensing-ai
```

#### 2. הגדרת Backend

```bash
# מעבר לתיקיית backend
cd backend

# יצירת סביבה וירטואלית
python -m venv venv

# הפעלת סביבה וירטואלית
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# התקנת תלות
pip install -r requirements.txt

# הגדרת משתני סביבה
cp .env.example .env
# ערוך את .env והוסף את ה-API key שלך:
# ANTHROPIC_API_KEY=your_api_key_here
```

#### 3. עיבוד מסמך רגולטורי (Phase 1)

```bash
# הנח את המסמך בתיקיית data/raw/
# הרץ עיבוד המסמך:
python document_processor.py
```

#### 4. הגדרת Frontend

```bash
# מעבר לתיקיית frontend
cd ../frontend

# התקנת תלות
npm install

# או עם yarn:
yarn install
```

### הרצת המערכת

#### 1. הפעלת Backend

```bash
cd backend
uvicorn app.main:app --reload OR pythom -m app.man
# השרת יעלה על: http://localhost:8000
```

#### 2. הפעלת Frontend

```bash
cd frontend
npm start
# האתר יעלה על: http://localhost:3000
```

#### 3. בדיקת חיבור

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000

## 📦 Dependencies וגרסאות

### Backend Dependencies

```
# AI & Document Processing
anthropic==0.67.0           # Claude API integration
python-docx==0.8.11         # Word document processing
python-dotenv==1.0.0        # Environment variables

# Web Framework
fastapi==0.104.1            # API framework
uvicorn[standard]==0.24.0   # ASGI server
pydantic==2.9.2             # Data validation

# HTTP & Data
httpx==0.28.1               # HTTP client
python-multipart==0.0.12    # File uploads

# Utilities
json5==0.9.14               # Enhanced JSON
pytest==7.4.3               # Testing
```

### Frontend Dependencies

```
# React Framework
react==^18.2.0              # UI library
react-dom==^18.2.0          # React DOM
react-scripts==5.0.1        # Build tools

# HTTP & Markdown
axios==^1.6.0               # HTTP client
react-markdown==^8.0.7      # Markdown rendering
```

## 🔧 מבנה הנתונים

### סכמת מאגר הדרישות (requirements.json)

```json
{
  "document_analysis": {
    "total_requirements_found": 26,
    "main_categories": ["health", "fire", "business"],
    "regulatory_authorities": ["משרד הבריאות", "כבאות", "רשות מקומית"],
    "processing_notes": "הערות על העיבוד"
  },
  "general_requirements": [
    {
      "id": "general_001",
      "name": "רישיון עסק",
      "category": "רישוי כללי",
      "authority": "רשות מקומית",
      "description": "רישיון חובה לכל עסק",
      "timeline": "2-3 שבועות",
      "estimated_cost": "400-600 ₪",
      "priority": "גבוהה"
    }
  ],
  "size_specific_requirements": [
    {
      "id": "size_001",
      "name": "אישור כבאות מתקדם",
      "conditions": {
        "min_size_sqm": 100,
        "max_size_sqm": null
      },
      "authority": "כבאות",
      "timeline": "4-6 שבועות"
    }
  ],
  "capacity_specific_requirements": [
    {
      "id": "capacity_001",
      "name": "רישיון מקום ציבורי",
      "conditions": {
        "min_capacity": 50,
        "max_capacity": null
      }
    }
  ],
  "feature_specific_requirements": [
    {
      "id": "feature_001",
      "name": "רישיון גז",
      "conditions": {
        "requires_gas": true,
        "has_delivery": null,
        "serves_meat": null
      }
    }
  ]
}
```

### מודל נתוני שאלון

```typescript
interface SurveyRequest {
  size: number; // גודל במ"ר (10-10000)
  max_people: number; // תפוסה מקסימלית (1-1000)
  uses_gas: boolean; // שימוש בגז
  has_delivery: boolean; // שירות משלוחים
  serves_meat: boolean; // הגשת בשר
  business_name?: string; // שם העסק (אופציונלי)
  location?: string; // מיקום (אופציונלי)
}
```

## 🎯 אלגוריתם התאמת דרישות

### לוגיקת הסינון

המערכת מסננת דרישות בהתבסס על מאפייני העסק:

#### 1. דרישות כלליות

```python
# חלות על כל העסקים ללא תנאים
for req in general_requirements:
    relevant_requirements.append(req)
```

#### 2. דרישות לפי גודל

```python
# בדיקת התאמה לגודל העסק
if req.min_size_sqm <= business.size <= req.max_size_sqm:
    relevant_requirements.append(req)
```

#### 3. דרישות לפי תפוסה

```python
# בדיקת התאמה לתפוסה
if req.min_capacity <= business.max_people <= req.max_capacity:
    relevant_requirements.append(req)
```

#### 4. דרישות לפי מאפיינים

```python
# בדיקת התאמה למאפיינים מיוחדים
if (req.requires_gas == business.uses_gas and
    req.has_delivery == business.has_delivery and
    req.serves_meat == business.serves_meat):
    relevant_requirements.append(req)
```

### דוגמה למקרה בדיקה

**עסק: 80 מ"ר, 50 מקומות, גז=כן, משלוחים=לא, בשר=כן**

1. ✅ **רישיון עסק** (כללי - חל על כולם)
2. ✅ **רישיון מזון** (כללי - חל על מסעדות)
3. ❌ **אישור כבאות מתקדם** (דרוש מ-100 מ"ר)
4. ✅ **אישור מקום ציבורי** (דרוש מ-50 מקומות)
5. ✅ **רישיון גז** (העסק משתמש בגז)
6. ✅ **פיקוח כשרות** (העסק מגיש בשר)

## 📚 תיעוד API

### נקודות קצה עיקריות

#### POST /api/survey/submit

יצירת דוח רישוי מותאם אישית

**Request Body:**

```json
{
  "size": 80,
  "max_people": 50,
  "uses_gas": true,
  "has_delivery": false,
  "serves_meat": true,
  "business_name": "מסעדת הפלאפל",
  "location": "תל אביב"
}
```

**Response:**

```json
{
  "success": true,
  "survey_data": {...},
  "relevant_requirements": [...],
  "personalized_report": "# דוח רישוי עסקים...",
  "requirements_count": 5,
  "estimated_total_cost": "3,200 ₪ (אומדן)",
  "estimated_total_time": "8 שבועות (משוער)",
  "timestamp": "2024-12-19T10:30:00"
}
```

#### GET /api/health

בדיקת תקינות המערכת

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2024-12-19T10:30:00",
  "database_loaded": true,
  "total_requirements": 26,
  "ai_processor_ready": true
}
```

#### GET /api/requirements

מידע על מאגר הדרישות

**Response:**

```json
{
  "total_requirements": 26,
  "categories": {
    "general": 5,
    "size_specific": 6,
    "capacity_specific": 8,
    "feature_specific": 7
  },
  "regulatory_authorities": ["משרד הבריאות", "כבאות", "רשות מקומית"],
  "last_processed": "2024-12-19T09:15:00"
}
```

#### GET /api/survey/test

בדיקת חיבור API

**Response:**

```json
{
  "message": "Survey API is working",
  "timestamp": "2024-12-19T10:30:00",
  "endpoints": {
    "submit": "POST /api/survey/submit",
    "test": "GET /api/survey/test"
  }
}
```

## 🤖 תיעוד שימוש ב-AI

### כלי פיתוח שנעשה בהם שימוש

#### 1. Claude AI (Anthropic)

- **שימוש**: Assistant לפיתוח הקוד והארכיטקטורה
- **איך**: ייעוץ וכתיבת קוד, עיצוב מבנה, פתרון בעיות
- **יתרונות**: הבנת קוד מתקדמת, הצעות אופטימיזציה, תיעוד

### מודל השפה המרכזי

#### Claude 4 Sonnet (claude-sonnet-4-20250514)

**מדוע נבחר:**

- ✅ **תמיכה מעולה בעברית** - הבנה וכתיבה טבעית
- ✅ **חלון הקשר גדול** - 200K טוקנים (מתאים למסמך של 59 עמודים)
- ✅ **יכולות ניתוח מתקדמות** - הבנת הקשר ומבנה מסמכים
- ✅ **יצירת תוכן מובנה** - JSON וטקסט מעוצב
- ✅ **עלות סבירה** - $3/1M input, $15/1M output tokens

**השוואה למודלים אחרים:**

- **vs GPT-4**: תמיכה טובה יותר בעברית, חלון הקשר גדול יותר
- **vs Gemini**: API יציב יותר, תיעוד טוב יותר
- **vs Claude Haiku**: איכות גבוהה יותר למשימות מורכבות

### Prompts מרכזיים במערכת

#### 1. Prompt עיבוד מסמכים (Phase 1)

```
אתה מערכת AI מתקדמת המתמחה בעיבוד מסמכים רגולטוריים בעברית לצורך רישוי עסקים.

המשימה שלך: לנתח בצורה מקיפה ומדויקת את המסמך הבא ולחלץ את כל המידע הרלוונטי לבעלי עסקים.

מסמך לעיבוד:
{document_text}

חלץ מידע מובנה על:
1. דרישות כלליות לעסקים
2. דרישות ספציפיות לפי גודל
3. דרישות ספציפיות לפי תפוסה
4. דרישות למאפיינים מיוחדים
5. גופים רגולטוריים
6. זמנים ועלויות

החזר JSON מובנה עם כל הדרישות המסווגות.
```

את הפרומט המלא ניתן לראות ב - Business Licensing AI agent\backend\document_processor.py , פונקציה \_process_with_ai

#### 2. Prompt יצירת דוחות (Phase 2)

```
אתה יועץ עסקי מקצועי המתמחה ברישוי עסקים בישראל. צור דוח מותאם אישית בעברית עבור:

## נתוני העסק:
- גודל: {survey.size} מ"ר
- תפוסה מקסימלית: {survey.max_people} מקומות ישיבה
- שימוש בגז: {'כן' if survey.uses_gas else 'לא'}
- משלוחים: {'כן' if survey.has_delivery else 'לא'}
- הגשת בשר: {'כן' if survey.serves_meat else 'לא'}

## דרישות רגולטוריות רלוונטיות:
{requirements_summary}

צור דוח מקצועי ומפורט הכולל:

### 1. 📋 סיכום מנהלים (2-3 שורות)
### 2. 📜 רישיונות ואישורים נדרשים
### 3. ⏰ לוח זמנים מומלץ (סדר עדיפויות)
### 4. 💰 עלויות משוערות
### 5. ✅ רשימת מטלות לביצוע (צ'קליסט)
### 6. ⚠️ הערות חשובות
### 7. 📞 איש קשר ומשאבים

הנחיות לכתיבה:
- השתמש בשפה עסקית ברורה ופשוטה, לא "שפת חוק"
- כתוב בגוף שני ("אתה צריך", "עליך לעשות")
- הוסף אייקונים לקריאות טובה יותר
- תן דגש על היבטים מעשיים ופעולות קונקרטיות
```

את הפרומט המלא ניתן לראות ב - Business Licensing AI agent\backend\app\services\report_generator.py , פונקציה \_build_ai_prompt

#### 3. System Message לתגובות נקיות

```
You are a JSON extraction system. Return ONLY valid JSON. No explanations, no extra text, no markdown formatting. Just pure JSON.
```

### סטטיסטיקות שימוש

#### עלויות צפויות

- **עיבוד מסמך** (Phase 1): ~$0.30-0.50 לכל עיבוד
- **יצירת דוח** (Phase 2): ~$0.04-0.06 לכל משתמש
- **בדיקות פיתוח**: ~$1-2 סה"כ

#### ביצועים

- **עיבוד מסמך**: 2-3 דק'
- **יצירת דוח**: 20-40 שניות
- **דיוק התאמה**: >90% (בהתבסס על בדיקות)

## 🧪 בדיקות ואימות

### דוגמאות לבדיקה

#### מקרה בדיקה 1: מסעדה קטנה

```json
{
  "size": 60,
  "max_people": 30,
  "uses_gas": true,
  "has_delivery": false,
  "serves_meat": true
}
```

**תוצאה צפויה**: 4-5 רישיונות, עלות ~2,500 ₪

#### מקרה בדיקה 2: מסעדה גדולה

```json
{
  "size": 200,
  "max_people": 120,
  "uses_gas": true,
  "has_delivery": true,
  "serves_meat": false
}
```

**תוצאה צפויה**: 7-8 רישיונות, עלות ~4,500 ₪

## 🔮 שיפורים עתידיים

### תכונות מתוכננות

- [ ] **תמיכה בסוגי עסקים נוספים** (חנויות, משרדים)
- [ ] **אינטגרציה עם API ממשלתיים** לנתונים בזמן אמת
- [ ] **מערכת התרעות** על שינויים ברגולציה
- [ ] **אפליקציה ניידת** למעקב אחר תהליכי רישוי
- [ ] **צ'אטבוט אינטראקטיבי** לשאלות נוספות
- [ ] **יצוא ל-PDF/Word** מהדור הבא
- [ ] **מולטי-לשון** (אנגלית)

### אופטימיזציות טכניות

- [ ] **Cache של דוחות** לחזרות מהירות
- [ ] **בסיס נתונים** במקום JSON
- [ ] **Queue מתקדם** לעיבוד נפח גדול
- [ ] **אנליטיקה מתקדמת** על השימוש
- [ ] **A/B Testing** של prompts שונים

### פתרון בעיות נפוצות

#### שגיאת חיבור לשרת

```bash
# בדוק שהשרת פועל
curl http://localhost:8000/api/health

# בדוק משתני סביבה
echo $ANTHROPIC_API_KEY
```

שים לב למשתנים הבאים שהם צריכים להיות מוגדרים אצלך:

```
ANTHROPIC_API_KEY=**********

# Document Processing Settings
DOCUMENT_PATH=**********
OUTPUT_PATH=*******
```

#### שגיאות במסמך

- ודא שהמסמך ב-`.docx` format
- בדוק שהמסמך לא מוגן בסיסמה
- ודא שיש מספיק קרדיטים ב-API

#### ביצועים איטיים

- בדוק חיבור אינטרנט
- ודא שאין עומס על שרת Claude
- נסה להקטין את המסמך

### לוגים ו-Debug

```bash
# הפעל עם לוגים מפורטים
uvicorn app.main:app --reload --log-level debug

# בדוק לוגי Frontend
# פתח Developer Tools (F12) בדפדפן
```

---

**נבנה עם ❤️**
