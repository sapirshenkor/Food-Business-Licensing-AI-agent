"""
Comprehensive Document Processor for Business Licensing Requirements
Processes Hebrew regulatory documents with AI to extract all requirements accurately
"""

import anthropic
import docx
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

class ComprehensiveDocumentProcessor:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.usage_tracker={
            'total_calls': 0,
            'total_cost': 0.0,
            'input_tokens': 0,
            'output_tokens': 0
        }
    
    def process_document(self, file_path:str,output_path:str):
        """
        Main processing function - extracts all requirements from document
        
        Args:
            file_path: Path to Word document
            output_path: Where to save the processed requirements
            
        Returns:
            Dict: Complete requirements database
        """
        print("Starting comprehensive document processing...")

        # Step 1: Extract text from Word document
        print("🔍 Extracting text from Word document...")
        document_text = self._extract_text_from_word(file_path)
        if not document_text:
            raise Exception("Failed to extract text from Word document")
        
        print(f"✅ Successfully extracted {len(document_text)} characters from Word document")
        print(f"📊 Estimated tokens: {len(document_text.split()) * 1.3:.0f}")

        # Step 2: Process document with AI using comprehensive prompt
        print("🤖 Processing document with AI, this may take a few minutes...")
        requirements_data=self._process_with_ai(document_text)
        if not requirements_data:
            raise Exception("Failed to process document with AI")
        print("✅ Successfully processed document with AI")

        # Step 3 validate and claen results
        print("🔍 Validating and cleaning extracted requirements...")
        validated_data=self._validate_and_clean_requirements(requirements_data)

        # Stage 4: save to json file
        print(f"💾 Saving validated requirements to JSON file {output_path}")
        self._save_to_json(validated_data, output_path)

        # Step 5: Print summary
        self._print_summary(validated_data)

        return validated_data
    
    def _extract_text_from_word(self, file_path:str):
        """
        Extracts text from a Word document using python-docx with structure preservation
        
        Args:
            file_path: Path to Word document
        """
        try:
            doc=docx.Document(file_path)
            full_text=""

            for paragraph in doc.paragraphs:
                text=paragraph.text.strip()
                if text:
                    # Adding structure markers based on paragraph style
                    style = paragraph.style.name.lower()
                    
                    if 'heading' in style or 'title' in style:
                        full_text += f"\n\n=== SECTION_HEADER: {text} ===\n"
                    elif paragraph.runs and paragraph.runs[0].bold:
                        full_text += f"\n--- SUBSECTION: {text} ---\n"
                    else:
                        full_text += f"{text}\n"
            
            # Clean and normalize
            full_text = self._clean_text(full_text)
            
            return full_text
            
        except Exception as e:
            print(f"❌ Error extracting from Word: {e}")
            return None
    
    def _clean_text(self, text:str):
        """
        Cleans and normalizes text for better AI processing
        
        Args:
            text: Raw text to clean
        """

        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                cleaned_lines.append(line)
        
        # Join with single newlines
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Remove BOM and other artifacts
        cleaned_text = cleaned_text.replace('\ufeff', '')
        return cleaned_text
    
    def _process_with_ai(self, document_text:str):
        """
        Processes document text with AI using comprehensive prompt.
        
        Args:
            document_text: Raw text to process
        """

        prompt = f"""
        אתה מערכת AI מתקדמת המתמחה בעיבוד מסמכים רגולטוריים בעברית לצורך רישוי עסקים.

        המשימה שלך: לנתח בצורה מקיפה ומדויקת את המסמך הבא ולחלץ את כל המידע הרלוונטי לבעלי עסקים.

        המסמך לעיבוד:
        {document_text}

        עליך לחלץ מידע מובנה ומפורט על:

        1. **דרישות כלליות לעסקים** - דרישות שחלות על כל סוגי העסקים
        2. **דרישות ספציפיות לפי גודל** - דרישות המתייחסות לגודל העסק במ"ר
        3. **דרישות ספציפיות לפי תפוסה** - דרישות המתייחסות למספר אנשים
        4. **דרישות למאפיינים מיוחדים** - גז, משלוחים, הגשת בשר
        5. **גופים רגולטוריים** - כל הרשויות והמשרדים הרלוונטיים
        6. **זמנים ועלויות** - לוחות זמנים ועלויות לכל דרישה
        7. **פרטים חשובים נוספים** - כל מידע רלוונטי אחר

        עבור כל דרישה, ציין בדיוק:
        - שם הדרישה המדויק (כפי שמופיע במסמך)
        - הגוף/רשות המוסמכת
        - תיאור מפורט של הדרישה
        - תנאי התפוסה (מספר מקומות/אנשים - אם רלוונטי)
        - תנאי שטח (גודל במ"ר - אם רלוונטי)  
        - תנאים מיוחדים (שימוש בגז, משלוחים, הגשת בשר - אם רלוונטי)
        - זמן טיפול משוער
        - עלות משוערת
        - רמת חשיבות/עדיפות
        - היכן במסמך הדרישה מופיעה
        - הערות או תנאים נוספים
        - הערות חשובות 

        שים לב מיוחד לגופים רגולטוריים כמו:
        - דרישות של משרד הבריאות
        - דרישות כבאות ובטיחות
        - רישיונות עסק ברשויות מקומיות
        - דרישות לעסקי מזון
        - אישורי בנייה ותכנון
        - דרישות סביבתיות
        - דרישות עבודה וביטחון
        - מיסוי ורישום

        החזר תשובה בפורמט JSON הבא:
        {{
        "document_analysis": {{
            "total_requirements_found": מספר_כולל,
            "document_sections": ["רשימת החלקים הראשיים במסמך"],
            "regulatory_authorities": ["רשימת כל הגופים המוסמכים"],
            "processing_notes": "הערות על תהליך העיבוד",
            "document_length": מספר_מילים,
            "extraction_confidence": "גבוהה/בינונית/נמוכה"
        }},
        "general_requirements": [
            {{
            "id": "general_001",
            "name": "שם הדרישה",
            "category": "קטגוריה כללית",
            "authority": "הגוף המוסמך",
            "description": "תיאור מפורט של הדרישה",
            "applies_to": "כל העסקים/עסקים מסוג מסוים",
            "timeline": "זמן טיפול",
            "estimated_cost": "עלות משוערת",
            "priority": "גבוהה/בינונית/נמוכה",
            "source_location": "היכן במסמך",
            "additional_notes": "הערות נוספות"
            }}
        ],
        "size_specific_requirements": [
            {{
            "id": "size_001",
            "name": "שם הדרישה",
            "category": "דרישות לפי גודל",
            "authority": "הגוף המוסמך",
            "description": "תיאור מפורט",
            "conditions": {{
                "min_size_sqm": מספר_או_null,
                "max_size_sqm": מספר_או_null,
                "size_notes": "הערות על הגודל"
            }},
            "timeline": "זמן טיפול",
            "estimated_cost": "עלות",
            "priority": "רמת חשיבות",
            "source_location": "מיקום במסמך",
            "additional_notes": "הערות"
            }}
        ],
        "capacity_specific_requirements": [
            {{
            "id": "capacity_001",
            "name": "שם הדרישה",
            "category": "דרישות לפי תפוסה",
            "authority": "הגוף המוסמך",
            "description": "תיאור מפורט",
            "conditions": {{
                "min_capacity": מספר_או_null,
                "max_capacity": מספר_או_null,
                "capacity_notes": "הערות על התפוסה"
            }},
            "timeline": "זמן טיפול",
            "estimated_cost": "עלות",
            "priority": "רמת חשיבות",
            "source_location": "מיקום במסמך",
            "additional_notes": "הערות"
            }}
        ],
        "feature_specific_requirements": [
            {{
            "id": "feature_001",
            "name": "שם הדרישה",
            "category": "דרישות לפי מאפיינים",
            "authority": "הגוף המוסמך",
            "description": "תיאור מפורט",
            "conditions": {{
                "requires_gas": true/false/null,
                "has_delivery": true/false/null,
                "serves_meat": true/false/null,
                "feature_notes": "הערות על המאפיינים"
            }},
            "timeline": "זמן טיפול",
            "estimated_cost": "עלות",
            "priority": "רמת חשיבות",
            "source_location": "מיקום במסמך",
            "additional_notes": "הערות"
            }}
        ],
        "important_information": [
            {{
            "topic": "נושא חשוב",
            "description": "מידע חשוב שלא נכנס לקטגוריות הקודמות",
            "relevance": "למה זה חשוב",
            "source_location": "מיקום במסמך"
            }}
        ]
        }}

        הוראות חשובות:
        1. אל תמציא מידע - רק מה שמופיע במסמך
        2. אם משהו לא ברור, ציין "לא מוגדר" או "דורש בדיקה נוספת"
        3. שמור על דיוק מקסימלי - זה ייושם במערכת אמיתית
        4. התמקד בדרישות מעשיות לבעלי עסקים קטנים-בינוניים
        5. זהה קשרים בין דרישות שונות
        6. שים לב לחריגים ותנאים מיוחדים
        """
        try:
            print("📤 Sending document to Claude AI...")
            
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=10000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Track usage
            self._update_usage_tracker(response.usage)
            
            # Extract JSON response
            response_text = response.content[0].text
            requirements_data = self._extract_json_from_response(response_text)
            
            print("✅ AI processing completed successfully")
            
            return requirements_data
            
        except Exception as e:
            print(f"❌ AI processing error: {e}")
            return None
        
    def _extract_json_from_response(self, response_text:str):
        """
        Extracts JSON from AI response
        
        Args:
            response_text: Raw response text
        """
        try:
            # JSON boundaries without the start and end text that Claude adds
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                data = json.loads(json_str)
                return data
            else:
                raise ValueError("No JSON found in response")
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print("Raw response preview:", response_text[:500])
            
            # Save problematic response for debugging
            with open(f"debug_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", 'w', encoding='utf-8') as f:
                f.write(response_text)
            
            return {
                "error": "JSON parsing failed",
                "raw_response": response_text
            }
    
    def _validate_and_clean_requirements(self, data:dict):
        """
        Validates and cleans extracted requirements
        
        Args:
            data: Raw requirements data
        """
        # Ensure required sections exist
        required_sections = [
            'document_analysis',
            'general_requirements', 
            'size_specific_requirements',
            'capacity_specific_requirements',
            'feature_specific_requirements'
        ]
        
        for section in required_sections:
            if section not in data:
                data[section] = []
                print(f"⚠️ Missing section: {section} - added empty list")
        
        # Add metadata
        data['processing_metadata'] = {
            'processed_at': datetime.now().isoformat(),
            'processor_version': '1.0.0',
            'api_calls_used': self.usage_tracker['total_calls'],
            'total_cost': round(self.usage_tracker['total_cost'], 4)
        }
        
        # Count total requirements
        total_reqs = (
            len(data.get('general_requirements', [])) +
            len(data.get('size_specific_requirements', [])) +
            len(data.get('capacity_specific_requirements', [])) +
            len(data.get('feature_specific_requirements', []))
        )
        
        data['summary'] = {
            'total_requirements': total_reqs,
            'general_requirements_count': len(data.get('general_requirements', [])),
            'size_specific_count': len(data.get('size_specific_requirements', [])),
            'capacity_specific_count': len(data.get('capacity_specific_requirements', [])),
            'feature_specific_count': len(data.get('feature_specific_requirements', []))
        }
        
        return data

    def _save_to_json(self, data:dict, output_path:str):
        """
        Saves data to a JSON file
        
        Args:
            data: Data to save
            output_path: Path to save the JSON file
        """
        try:
            # Create directory if needed
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            # Save with pretty formatting
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Data saved to {output_path}")
            
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            raise 
    
    def _print_summary(self, data:dict):
        """Print processing summary"""
        print("\n" + "="*60)
        print("📊 PROCESSING SUMMARY")
        print("="*60)
        
        summary = data.get('summary', {})
        analysis = data.get('document_analysis', {})
        metadata = data.get('processing_metadata', {})
        
        print(f"📄 Total Requirements Found: {summary.get('total_requirements', 0)}")
        print(f"   • General Requirements: {summary.get('general_requirements_count', 0)}")
        print(f"   • Size-Specific: {summary.get('size_specific_count', 0)}")
        print(f"   • Capacity-Specific: {summary.get('capacity_specific_count', 0)}")
        print(f"   • Feature-Specific: {summary.get('feature_specific_count', 0)}")
        
        if analysis:
            print(f"\n🏛️ Regulatory Authorities Found: {len(analysis.get('regulatory_authorities', []))}")
            for auth in analysis.get('regulatory_authorities', [])[:5]:  # Show first 5
                print(f"   • {auth}")
        
        print(f"\n💰 API Usage:")
        print(f"   • API Calls: {metadata.get('api_calls_used', 0)}")
        print(f"   • Total Cost: ${metadata.get('total_cost', 0):.4f}")
        print(f"   • Remaining Credits: ${5.0 - metadata.get('total_cost', 0):.4f}")
        
        print(f"\n⏰ Processing Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        print("\n✅ Document processing completed successfully!")
    
    def _update_usage_tracker(self, usage:dict):
        """
        Updates usage tracker with AI API usage
        
        Args:
            usage: Usage data from AI API
        """
        self.usage_tracker['total_calls'] += 1
        self.usage_tracker['input_tokens'] += usage.input_tokens
        self.usage_tracker['output_tokens'] += usage.output_tokens
        
        # Calculate cost (Claude 3.5 Sonnet pricing)
        input_cost = (usage.input_tokens / 1_000_000) * 3.0
        output_cost = (usage.output_tokens / 1_000_000) * 15.0
        call_cost = input_cost + output_cost
        
        self.usage_tracker['total_cost'] += call_cost
        
        print(f"💸 API Call Cost: ${call_cost:.4f}")
        print(f"💰 Total Cost So Far: ${self.usage_tracker['total_cost']:.4f}")
    
if __name__ == "__main__":
    # Initialize processor
    processor = ComprehensiveDocumentProcessor()
    
    # Process document
    document_path =os.getenv("DOCUMENT_PATH","regulatory_document.docx")
    output_path = os.getenv("OUTPUT_PATH","requirements.json")
    
    try:
        if not os.path.exists(document_path):
            print(f"❌ Document not found: {document_path}")
            print("Please place your Word document in the same directory and update the path.")
        else:
            # Process the document
            results = processor.process_document(document_path, output_path)
            
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check that your Word document exists")
        print("2. Verify your ANTHROPIC_API_KEY in .env file")
        print("3. Ensure you have sufficient API credits")