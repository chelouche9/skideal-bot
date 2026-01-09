"""Tool to get available camp resorts."""

import json
from langchain_core.tools import tool

from agent.data.camps import get_all_camp_resorts, get_camp_resorts_by_country


@tool
def get_camp_resorts(country: str = None) -> str:
    """Get a list of all resorts that offer ski camps (קייטנות).
    
    IMPORTANT: Resort names for camps may differ from hotel resort names!
    For example, Bulgaria has: "בנסקו", "בנסקו שבוע", "בנסקו סופש", "בנסקו א-ה"
    Each variant may have different camps and prices.
    
    Use this tool first to see available camp resorts before searching for specific camps.
    
    Args:
        country: Optional - filter by country in Hebrew (e.g., "צרפת", "בולגריה", "איטליה")
                 If not provided, returns all resorts organized by country.
    
    Returns:
        JSON string with resorts that offer camps.
    """
    if country:
        resorts = get_camp_resorts_by_country(country)
        if not resorts:
            return f"לא נמצאו קייטנות במדינה '{country}'. נסה לבדוק את שם המדינה או השאר ריק לראות את כל האפשרויות."
        
        result = {
            "מדינה": country,
            "אתרים_עם_קייטנות": resorts,
            "הערה": "שים לב - שמות האתרים עשויים להיות שונים מאתרי המלונות (למשל: בנסקו שבוע, בנסקו סופש)"
        }
    else:
        all_resorts = get_all_camp_resorts()
        result = {
            "אתרים_עם_קייטנות_לפי_מדינה": all_resorts,
            "הערה": "שים לב - שמות האתרים עשויים להיות שונים מאתרי המלונות (למשל: בנסקו שבוע, בנסקו סופש)"
        }
    
    return json.dumps(result, ensure_ascii=False, indent=2)

