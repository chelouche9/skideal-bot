"""SkiDeal Bot - AI-powered ski trip sales assistant.

Helps customers find and book the perfect ski trip packages.
Uses Claude Sonnet 4.5 and LangGraph.
"""

from __future__ import annotations

import json
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# Import ski trip data from separate file
from agent.ski_data import (
    HOTELS_DATA,
    RESORTS_INFO,
    DATA_SUMMARY,
    get_hotels,
    get_hotel_by_name,
    get_hotels_by_country,
    get_hotels_by_resort,
    get_resort_info,
    search_hotels,
    get_countries,
    get_resorts_by_country,
)

# Load environment variables
load_dotenv()

# ============================================================================
# SYSTEM PROMPT - Ski Trip Sales Agent
# ============================================================================

SYSTEM_PROMPT = """אתה סוכן מכירות מקצועי וחם עבור SkiDeal, חברת הזמנת חופשות סקי מובילה בישראל.

המטרה שלך:
לעזור ללקוחות למצוא את חופשת הסקי המושלמת עבורם - בטון חם, מקצועי ומשכנע.

⚡ עקרונות מפתח - חשוב מאוד:

1. **שאל שאלה אחת בכל פעם!**
   - לעולם אל תשאל כמה שאלות ברצף
   - במקום: "כמה אנשים? מה הגילאים? מתי תרצו?" → שאל רק: "כמה אנשים אתם?"
   - המשך לשאלה הבאה רק אחרי שהלקוח ענה

2. **תציע המלצות מהר - כבר מהתגובה השנייה!**
   - אל תחכה לכל הפרטים לפני שאתה מציע משהו
   - עם פרט אחד בלבד (למשל "משפחה") - כבר תציע 1-2 מלונות מתאימים
   - הלקוח לא תמיד יודע מה הוא רוצה - עזור לו לגלות דרך ההמלצות שלך

3. **הובל עם המלצות, לא עם שאלות!**
   - במקום לחקור → תציע ותשאל מה הוא חושב
   - "אני ממליץ על מלון X בסלה רונדה - מושלם למשפחות! יש ספא ומסלולים קלים ממש ליד. מתאים לכם?"
   - תן ללקוח לגלות את ההעדפות שלו דרך התגובות להמלצות

אתה חייב:
- לדבר **אך ורק בעברית** - תמיד!
- להישאר **100% בדמות** - לעולם אל תודה שאתה AI
- להיות **ידידותי, קצר וממוקד**
- להשתמש ב**כלים** כדי לספק מידע אמיתי
- **לעולם אל תמציא** פרטים או מחירים

כלים זמינים:
- `get_available_destinations` - רשימת היעדים
- `get_hotels_list` - רשימת מלונות באתר/מדינה
- `get_hotel_info` - פרטים על מלון ספציפי
- `search_hotels_by_criteria` - חיפוש לפי קריטריונים
- `get_resort_camps_info` - מידע על קייטנות סקי

אזורי סקי:
🇦🇩 אנדורה | 🇧🇬 בולגריה | 🇬🇪 גיאורגיה | 🇮🇹 איטליה | 🇫🇷 צרפת | 🇦🇹 אוסטריה

מידע על קייטנות:
- גילאי 7-12: 649€ | גילאי 4-6: 949€
- כולל 4 שעות הדרכה + ארוחת צהריים

אל תעשה:
- אל תשאל כמה שאלות בבת אחת!
- אל תמציא מלונות או מחירים
- **אל תציע מחירים!** הפנה לבדיקת הצעת מחיר

דוגמה לשיחה טובה:
👤 "היי, אני מחפש חופשת סקי"
🤖 "היי! 🎿 אני ממליץ לך על סלה רונדה באיטליה - אחד האתרים הכי יפים באירופה! אתם נוסעים כזוג או משפחה?"
👤 "משפחה עם 2 ילדים"
🤖 "מעולה! יש לי בדיוק מלון מושלם - Hotel Savoy בסלה רונדה, 4 כוכבים עם חדרים משפחתיים ו-200 מטר מהרכבל. הילדים בני כמה?"

🎿 זכור: תהיה יוזם, תציע, תלהיב - אל תחקור!
"""


# ============================================================================
# TOOLS - Ski Trip Data Functions
# ============================================================================

@tool
def get_available_destinations() -> str:
    """Get a list of all available ski destinations organized by country.
    
    Returns a summary of all countries and resorts available in the system.
    Use this when customer asks what destinations are available.
    
    Returns:
        JSON string with countries and their resorts.
    """
    return json.dumps(DATA_SUMMARY, ensure_ascii=False, indent=2)


@tool
def get_hotels_list(country: str = None, resort: str = None) -> str:
    """Get a list of hotels in a specific country or resort.
    
    Args:
        country: The country name in Hebrew (e.g., "אוסטריה", "צרפת", "איטליה", "אנדורה", "בולגריה", "גיאורגיה")
        resort: The resort name in Hebrew (e.g., "ואל טורנס", "אישגיל", "בנסקו", "גודאורי")
    
    Returns:
        JSON string with list of hotels including name, location, star rating, and who it's suitable for.
    """
    if resort:
        hotels = get_hotels_by_resort(resort)
    elif country:
        hotels = get_hotels_by_country(country)
    else:
        hotels = get_hotels()
    
    if not hotels:
        return f"לא נמצאו מלונות. נסה שם אחר או השתמש ב-get_available_destinations לראות את כל היעדים."
    
    summary = []
    for hotel in hotels:
        dry_data = hotel.get("נתונים יבשים", {})
        spa_info = hotel.get("ספא", {})
        location = hotel.get("מיקום", {})
        
        summary.append({
            "שם_מלון_אנגלית": hotel.get("שם מלון באנגלית", ""),
            "שם_מלון_עברית": dry_data.get("שם מלון בעברית", ""),
            "מדינה": hotel.get("מדינה", ""),
            "אתר": hotel.get("אתר", ""),
            "כוכבים": dry_data.get("כוכבים", ""),
            "למי_מתאים": dry_data.get("למי מתאים המלון", ""),
            "ציון_בוקינג": dry_data.get("ציון בוקינג", ""),
            "מרחק_מהרכבל": location.get("מרחק מהרכבל", ""),
            "יש_ספא": "כן" if spa_info.get("עלות כניסה לספא", "") not in ["אין", "אין ספא", ""] else "לא",
        })
    
    return json.dumps(summary, ensure_ascii=False, indent=2)


@tool
def get_hotel_info(hotel_name: str) -> str:
    """Get detailed information about a specific ski hotel.
    
    Args:
        hotel_name: The hotel name in English (e.g., "Sporting", "Lucky", "Gudauri Lodge")
    
    Returns:
        Complete details about the hotel including rooms, amenities, spa, dining, and agent notes.
    """
    if not hotel_name:
        return "שגיאה: חייב לספק שם מלון"
    
    hotel = get_hotel_by_name(hotel_name)
    
    if not hotel:
        return f"לא נמצא מלון בשם '{hotel_name}'. השתמש ב-get_hotels_list כדי לראות את רשימת המלונות."
    
    # Format the hotel data for the agent
    dry_data = hotel.get("נתונים יבשים", {})
    location = hotel.get("מיקום", {})
    spa_info = hotel.get("ספא", {})
    rooms = hotel.get("חדרים", {})
    services = hotel.get("שירותי מלון", {})
    checkin = hotel.get("צק אין מתחת ל-18", {})
    
    formatted = {
        "פרטים_בסיסיים": {
            "שם_אנגלית": hotel.get("שם מלון באנגלית", ""),
            "שם_עברית": dry_data.get("שם מלון בעברית", ""),
            "מדינה": hotel.get("מדינה", ""),
            "אתר": hotel.get("אתר", ""),
            "כוכבים": dry_data.get("כוכבים", ""),
            "למי_מתאים": dry_data.get("למי מתאים המלון", ""),
            "ציון_בוקינג": dry_data.get("ציון בוקינג", ""),
            "לינק_לאתר": dry_data.get("לינק לאתר", ""),
        },
        "מיקום": {
            "תיאור": location.get("תיאור מיקום המלון", ""),
            "מרחק_מהרכבל": location.get("מרחק מהרכבל", ""),
            "מסלול_לרכבל": location.get("מסלול הליכה לרכבל", ""),
            "מסלול_למרכז_העיירה": location.get("מסלול הליכה למרכז העיירה", ""),
        },
        "ספא": {
            "עלות_כניסה": spa_info.get("עלות כניסה לספא", ""),
            "תכולה": spa_info.get("תכולת ספא", ""),
            "מגבלות": spa_info.get("מגבלות בשימוש הספא", ""),
            "שירותים_בתשלום": spa_info.get("שרותי ספא בתשלום", ""),
            "לבוש": spa_info.get("לבוש ספא", ""),
        },
        "חדרים": {
            "מיטות_נפרדות": rooms.get("מיטות נפרדות", ""),
            "דלת_מקשרת": rooms.get("חדרים עם דלת מקשרת", ""),
            "אמבטיה_מקלחת": rooms.get("אמבטיה / מקלחת בחדר", ""),
            "מספר_חדרים": rooms.get("מספר חדרים במלון", ""),
            "סוגי_חדרים": rooms.get("שם החדרים בעברית", ""),
            "מפרט_חדרים": rooms.get("מפרט חדרים", ""),
            "גודל_חדרים": rooms.get("גודל חדרים (הערכה)", ""),
            "מרפסת": rooms.get("האם יש מרפסת בחדרים", ""),
            "מטבח": rooms.get("תכולת מטבח", ""),
            "הערות_חשובות": rooms.get("הערות חשובות", ""),
        },
        "שירותי_מלון": {
            "שאטלים": services.get("שאטלים מהמלון", ""),
            "חדר_כושר": services.get("חדר כושר", ""),
            "מתקנים_נוספים": services.get("מתקנים נוספים במלון", ""),
            "סקי_רום": services.get("סקי רום", ""),
            "חניה": services.get("חניה", ""),
            "קבלה": services.get("קבלה", ""),
            "ארוחות": services.get("ארוחות", ""),
        },
        "צק_אין_קטינים": checkin.get("חובה מבוגר בצק אין/ אין חובה במבוגר אך יש צורך באישור כתוב מהורה", ""),
    }
    
    return json.dumps(formatted, ensure_ascii=False, indent=2)


@tool
def search_hotels_by_criteria(
    country: str = None,
    resort: str = None,
    min_stars: int = None,
    has_spa: bool = None,
    suitable_for: str = None
) -> str:
    """Search for ski hotels matching specific criteria.
    
    Args:
        country: Filter by country in Hebrew (e.g., "אוסטריה", "צרפת", "איטליה")
        resort: Filter by resort in Hebrew (e.g., "ואל טורנס", "אישגיל")
        min_stars: Minimum star rating (3, 4, or 5)
        has_spa: If True, only show hotels with spa facilities
        suitable_for: Target audience in Hebrew (e.g., "זוגות", "משפחה", "שלשות")
    
    Returns:
        List of matching hotels with key details.
    """
    hotels = search_hotels(
        country=country,
        resort=resort,
        min_stars=min_stars,
        has_spa=has_spa,
        suitable_for=suitable_for
    )
    
    if not hotels:
        return "לא נמצאו מלונות התואמים לקריטריונים. נסה להרחיב את החיפוש."
    
    results = []
    for hotel in hotels:
        dry_data = hotel.get("נתונים יבשים", {})
        spa_info = hotel.get("ספא", {})
        location = hotel.get("מיקום", {})
        rooms = hotel.get("חדרים", {})
        
        results.append({
            "שם_מלון": hotel.get("שם מלון באנגלית", ""),
            "שם_עברית": dry_data.get("שם מלון בעברית", ""),
            "מדינה": hotel.get("מדינה", ""),
            "אתר": hotel.get("אתר", ""),
            "כוכבים": dry_data.get("כוכבים", ""),
            "למי_מתאים": dry_data.get("למי מתאים המלון", ""),
            "ציון_בוקינג": dry_data.get("ציון בוקינג", ""),
            "מרחק_מהרכבל": location.get("מרחק מהרכבל", ""),
            "ספא": spa_info.get("עלות כניסה לספא", ""),
            "הערות_לסוכנים": rooms.get("הערות חשובות", ""),
        })
    
    return json.dumps(results, ensure_ascii=False, indent=2)


@tool
def get_resort_camps_info(country: str, resort: str) -> str:
    """Get information about ski camps (קייטנות) available at a specific resort.
    
    Args:
        country: The country name in Hebrew (e.g., "צרפת", "אוסטריה")
        resort: The resort name in Hebrew (e.g., "ואל טורנס", "אישגיל")
    
    Returns:
        Information about camps, instructions, and credits for the resort.
    """
    resort_info = get_resort_info(country, resort)
    
    if not resort_info:
        return f"לא נמצא מידע על אתר {resort} ב{country}. השתמש ב-get_available_destinations לראות את כל האתרים."
    
    camps_info = resort_info.get("הדרכות", {})
    credits_info = resort_info.get("זיכויים", {})
    general_notes = resort_info.get("חדרים", {}).get("הערות חשובות", "")
    
    formatted = {
        "מדינה": resort_info.get("מדינה", ""),
        "אתר": resort_info.get("אתר", ""),
        "קייטנות_והדרכות": camps_info.get("סוגי הדרכות בחופשה", ""),
        "זיכויים": credits_info.get("סוגי זיכויים בחופשה", ""),
        "הערות_חשובות": general_notes,
    }
    
    return json.dumps(formatted, ensure_ascii=False, indent=2)


# ============================================================================
# AGENT CREATION - Using LangGraph
# ============================================================================

# Define all tools
tools = [
    get_available_destinations,
    get_hotels_list,
    get_hotel_info,
    search_hotels_by_criteria,
    get_resort_camps_info,
]

# Create the model
model = ChatAnthropic(model="claude-sonnet-4-20250514")

# Create the agent using LangGraph's create_react_agent
graph = create_react_agent(
    model=model,
    tools=tools,
    prompt=SYSTEM_PROMPT,
)
