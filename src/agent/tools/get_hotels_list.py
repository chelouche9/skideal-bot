"""Tool to get list of hotels."""

import json
from langchain_core.tools import tool

from agent.data.resorts import (
    get_hotels,
    get_hotels_by_country,
    get_hotels_by_resort,
)


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

