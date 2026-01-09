"""Tool to get detailed hotel information."""

import json
from langchain_core.tools import tool

from agent.data.resorts import get_hotel_by_name


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

