"""Tool to search hotels by criteria."""

import json
from langchain_core.tools import tool

from agent.data.resorts import search_hotels


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

