"""Tool to get camps information by resort."""

import json
from langchain_core.tools import tool

from agent.data.camps import get_camps_by_resort


@tool
def get_camps_info(
    resorts: list[str],
    child_age: float = None,
) -> str:
    """Get information about ski camps (קייטנות) available at specific resorts.
    
    IMPORTANT: Use get_camp_resorts first to see available resort names!
    Resort names for camps may have variants like "בנסקו שבוע", "בנסקו סופש".
    
    Args:
        resorts: List of resort names in Hebrew to search for.
                 Example: ["בנסקו", "בנסקו שבוע", "בנסקו סופש"] to get all Bansko camps.
                 Or just ["ואל טורנס"] for a single resort.
        child_age: Optional - filter camps suitable for a child of this age.
    
    Returns:
        JSON string with list of camps including name, ages, price, schedule, and timing.
    """
    if not resorts:
        return "שגיאה: חייב לספק לפחות שם אתר אחד. השתמש ב-get_camp_resorts לראות את רשימת האתרים."
    
    # Collect camps from all requested resorts
    all_camps = []
    for resort in resorts:
        camps = get_camps_by_resort(resort)
        all_camps.extend(camps)
    
    # Filter by age if provided
    if child_age is not None:
        all_camps = [
            c for c in all_camps
            if c.get("גילאים", {}).get("מינימום", 0) <= child_age <= c.get("גילאים", {}).get("מקסימום", 99)
        ]
    
    if not all_camps:
        resorts_str = ", ".join(resorts)
        if child_age is not None:
            return f"לא נמצאו קייטנות באתרים '{resorts_str}' לגיל {child_age}. נסה לבדוק גיל אחר או השתמש ב-get_camp_resorts לראות את כל האתרים."
        return f"לא נמצאו קייטנות באתרים '{resorts_str}'. השתמש ב-get_camp_resorts לראות את רשימת האתרים הזמינים."
    
    # Format the results
    results = []
    for camp in all_camps:
        age_range = camp.get("גילאים", {})
        price_info = camp.get("מחיר", {})
        
        formatted = {
            "מדינה": camp.get("מדינה", ""),
            "אתר": camp.get("אתר", ""),
            "שם_קייטנה": camp.get("שם קייטנה", ""),
            "גילאים": f"{age_range.get('מינימום', '?')}-{age_range.get('מקסימום', '?')}",
            "מחיר": price_info.get("טקסט", "אין מידע"),
            "כולל_ארוחת_צהריים": "כן" if camp.get("כולל ארוחת צהריים") else "לא",
            "מתי": camp.get("מתי") or "לא צוין",
            "לוז": camp.get("לוז קייטנות") or "לא צוין",
        }
        
        # Add notes if exist
        if camp.get("הערות"):
            formatted["הערות"] = camp.get("הערות")
        
        results.append(formatted)
    
    # Group by resort variant for clarity
    resorts_found = sorted(set(c.get("אתר", "") for c in all_camps))
    
    return json.dumps({
        "אתרים_שנמצאו": resorts_found,
        "סה״כ_קייטנות": len(results),
        "קייטנות": results,
    }, ensure_ascii=False, indent=2)
