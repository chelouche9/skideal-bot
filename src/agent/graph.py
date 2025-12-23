"""Shlomo Sixt Car Sales Agent - Hebrew-speaking AI assistant.

A warm, professional car sales agent that helps Israeli customers find the perfect vehicle.
Uses Claude Sonnet 4.5 and real-time data from Shlomo Sixt APIs.
"""

from __future__ import annotations

import httpx
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool

# Load environment variables
load_dotenv()

# System prompt in Hebrew for the car sales agent
SYSTEM_PROMPT = """אתה סוכן מכירות רכב חם ומקצועי מהשורה הראשונה עבור שלמה סיקסט, אחד מספקי הרכב המובילים בישראל.

המטרה שלך:
המשימה היחידה שלך היא לעזור ללקוחות **למצוא ולבחור את הרכב הטוב ביותר** לצרכיהם - בטון חם, מקצועי ומשכנע.

אתה חייב:
- לדבר **רק בעברית**
- להישאר **100% בדמות** כל הזמן - לעולם אל תודה שאתה AI או מודל שפה
- להיות **ידידותי, סבלני, ברור ומשכנע מאוד**
- להיות **מאזין מצוין** שמתאים את הצעת הרכב על בסיס הצרכים המדויקים של הלקוח
- תמיד להשתמש ב**כלי נתונים בזמן אמת** (פונקציות) כדי לספק כל מידע על רכבים, זמינות או תמחור
- **לעולם אל תנחש, תאלתר או תמציא** פרטים, מחירים או דגמים

כשאתה מציע רכבים:
- תמיד לכלול אפשרויות **אפס קילומטר**, **יד ראשונה**, ו**יד שנייה** - על בסיס העדפות הלקוח
- הצג **3-5 רכבים רלוונטיים בלבד** שמתאימים לתקציב הלקוח, לצרכי המשפחה ולסגנון
- **חובה להציג תמונה של כל רכב** - חלץ את נתיב התמונה מהשדות הבאים בסדר העדיפויות:
  1. מהמערך `images[0].src` (התמונה הראשונה)
  2. או מ-`carExperienceImage.src`
  בנה כתובת מלאה: `https://d2g1tfejh04fgu.cloudfront.net` + נתיב התמונה
  הצג בפורמט markdown: `![שם הרכב](https://d2g1tfejh04fgu.cloudfront.net/media/...)` 
- הדגש את **נקודות המכירה העיקריות** לכל רכב (גודל תא מטען, נוחות, חיסכון בדלק, בטיחות וכו')
- הצע להמשיך לעזור ("רוצה שאבדוק עבורך פרטים נוספים?" / "אפשר גם לבדוק דגמים דומים אם תרצה")

כלי נתונים (אתה חייב להשתמש בהם):
- `get_available_models` - כל הרכבים במלאי
- `get_zero_km_cars` - רכבים חדשים בלבד
- `get_first_hand_car_details` - מפרטים, מחיר ותיאור של דגם יד ראשונה ספציפי
- `get_zero_km_car_details` - מפרטים, מחיר ותיאור של דגם אפס ק"מ ספציפי

אל תעשה:
- ענה על סמך זיכרון או ידע כללי
- תמציא פרטי רכב או מחירים
- תגיד משהו לא קשור או לא רלוונטי לבחירת רכב
- תציע רכבים שלא במלאי

פרסונות יעד:
אתה תפגוש לקוחות שונים. התאם את הטון וההצעות שלך בהתאם:

1. **משפחתי**: בן 45, מחפש רכב מרווח ואמין למשפחה עם בגאז' גדול, תקציב 150,000 ש"ח
2. **צעיר**: בן 23, אחרי צבא, מחפש רכב ראשון במחיר נגיש, אולי גם חסכוני
3. **יוקרה**: לקוח שמחפש רכב ספורט/יוקרה, פחות רגיש למחיר, רוצה ביצועים, עיצוב ונוכחות

---

תמיד סיים עם קריאה חזקה וידידותית לפעולה:
"מתאים לך שנמשיך משם?" / "רוצה שאבדוק לך גם רכב דומה עם תקציב קצת שונה?" / "זה הדגם שהכי מתאים לך לפי מה שתיארת."
"""


# ============================================================================
# TOOLS - API Integration with Shlomo Sixt
# ============================================================================


@tool
def get_available_models() -> str:
    """Get all available first-hand car models from Shlomo Sixt.
    
    Returns a list of all car models currently available for purchase (first-hand/יד ראשונה).
    Use this when customer asks what cars are available or to see the full inventory.
    
    Returns:
        JSON string with list of available models including their details.
    """
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                "https://sales-backend-prod.shlomo.co.il/api/shlomo/models"
            )
            response.raise_for_status()
            data = response.json()
            return f"רכבים זמינים ביד ראשונה: {data}"
    except Exception as e:
        return f"שגיאה בטעינת רשימת הדגמים: {str(e)}"


@tool
def get_zero_km_cars() -> str:
    """Get all available zero kilometer (brand new) cars from Shlomo Sixt.
    
    Returns a list of all zero-kilometer/brand new cars available for immediate purchase.
    Use this when customer specifically asks for new cars or 0 km vehicles.
    
    Returns:
        JSON string with list of zero km cars including their details.
    """
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                "https://sales-backend-prod.shlomo.co.il/api/shlomo/zero-km-cars"
            )
            response.raise_for_status()
            data = response.json()
            return f"רכבים זמינים ב-0 ק״מ: {data}"
    except Exception as e:
        return f"שגיאה בטעינת רכבי 0 ק״מ: {str(e)}"


@tool
def get_first_hand_car_details(importer_model: str) -> str:
    """Get detailed information about a specific first-hand car model.
    
    Args:
        importer_model: The importer model ID (e.g., "1VS4K6A1TEV1"). 
                       Get this from the models list returned by get_available_models.
    
    Returns:
        Detailed specifications, pricing, and description for the specific car model.
    """
    if not importer_model:
        return "שגיאה: חייב לספק מזהה דגם (importer_model)"
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                f"https://sales-backend-prod.shlomo.co.il/api/shlomo/first-hand-cars/{importer_model}"
            )
            response.raise_for_status()
            data = response.json()
            return f"פרטי רכב יד ראשונה: {data}"
    except Exception as e:
        return f"שגיאה בטעינת פרטי הרכב: {str(e)}"


@tool
def get_zero_km_car_details(car_id: str) -> str:
    """Get detailed information about a specific zero kilometer car.
    
    Args:
        car_id: The car ID (e.g., "8VFACG"). 
               Get this from the zero km cars list returned by get_zero_km_cars.
    
    Returns:
        Detailed specifications, pricing, and description for the specific zero km car.
    """
    if not car_id:
        return "שגיאה: חייב לספק מזהה רכב (car_id)"
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                f"https://sales-backend-prod.shlomo.co.il/api/shlomo/zero-km-cars/{car_id}"
            )
            response.raise_for_status()
            data = response.json()
            return f"פרטי רכב 0 ק״מ: {data}"
    except Exception as e:
        return f"שגיאה בטעינת פרטי הרכב: {str(e)}"


# ============================================================================
# AGENT CREATION - Using LangChain v1
# ============================================================================

# Define all tools
tools = [
    get_available_models,
    get_zero_km_cars,
    get_first_hand_car_details,
    get_zero_km_car_details,
]

# Create the agent using LangChain v1's create_agent
# This uses Claude Sonnet 4.5 with the Hebrew system prompt
graph = create_agent(
    model="anthropic:claude-sonnet-4-20250514",  # Claude Sonnet 4.5
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
)
