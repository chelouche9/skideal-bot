"""Tool to get resort camps information."""

import json
from langchain_core.tools import tool

from agent.ski_data import get_resort_info


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

