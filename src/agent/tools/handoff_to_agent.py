"""Tool for handing off conversation to a human agent."""

import json
from langchain_core.tools import tool


@tool
def handoff_to_agent(
    customer_name: str = None,
    phone: str = None,
    email: str = None,
    destination: str = None,
    dates: str = None,
    num_people: int = None,
    ages: str = None,
    ski_level: str = None,
    needs_ski_school: bool = None,
    needs_equipment: bool = None,
    hotel_preference: str = None,
    budget: str = None,
    spa_preference: bool = None,
    insurance_interest: bool = None,
    additional_notes: str = None,
) -> str:
    """Hand off the conversation to a human sales agent with all collected details.
    
    Use this tool when:
    - Customer is ready to book/close the deal
    - Payment details need to be collected
    - You don't have certain information and need human assistance
    - Customer explicitly asks to speak with a human
    
    Args:
        customer_name: Customer's name in Hebrew
        phone: Customer's phone number
        email: Customer's email address
        destination: Preferred destination/resort/country
        dates: Travel dates or date range
        num_people: Number of travelers
        ages: Ages of travelers (especially children)
        ski_level: Skiing experience level (beginner/intermediate/advanced)
        needs_ski_school: Whether they need ski school/lessons
        needs_equipment: Whether they need equipment rental
        hotel_preference: Preferred hotel or hotel type
        budget: Budget range or constraints
        spa_preference: Whether spa is important
        insurance_interest: Interest in Trip Guaranty/insurance
        additional_notes: Any other relevant information from the conversation
    
    Returns:
        Confirmation message with handoff summary.
    """
    summary = {
        "סוג_פעולה": "העברה לנציג אנושי",
        "פרטי_לקוח": {},
        "פרטי_חופשה": {},
        "העדפות": {},
        "הערות_נוספות": additional_notes or "",
    }
    
    # Customer details
    if customer_name:
        summary["פרטי_לקוח"]["שם"] = customer_name
    if phone:
        summary["פרטי_לקוח"]["טלפון"] = phone
    if email:
        summary["פרטי_לקוח"]["אימייל"] = email
    
    # Trip details
    if destination:
        summary["פרטי_חופשה"]["יעד"] = destination
    if dates:
        summary["פרטי_חופשה"]["תאריכים"] = dates
    if num_people:
        summary["פרטי_חופשה"]["מספר_נוסעים"] = num_people
    if ages:
        summary["פרטי_חופשה"]["גילאים"] = ages
    if ski_level:
        summary["פרטי_חופשה"]["רמת_סקי"] = ski_level
    
    # Preferences
    if needs_ski_school is not None:
        summary["העדפות"]["בית_ספר_לסקי"] = "כן" if needs_ski_school else "לא"
    if needs_equipment is not None:
        summary["העדפות"]["השכרת_ציוד"] = "כן" if needs_equipment else "לא"
    if hotel_preference:
        summary["העדפות"]["העדפת_מלון"] = hotel_preference
    if budget:
        summary["העדפות"]["תקציב"] = budget
    if spa_preference is not None:
        summary["העדפות"]["ספא"] = "כן" if spa_preference else "לא"
    if insurance_interest is not None:
        summary["העדפות"]["ביטוח_Trip_Guaranty"] = "כן" if insurance_interest else "לא"
    
    # Print the handoff summary
    print("\n" + "=" * 60)
    print("🔔 העברה לנציג אנושי - סיכום שיחה")
    print("=" * 60)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("=" * 60 + "\n")
    
    return json.dumps({
        "סטטוס": "הועבר לנציג",
        "הודעה": "פרטי הלקוח הועברו לנציג אנושי שייצור קשר בהקדם.",
        "סיכום": summary,
    }, ensure_ascii=False, indent=2)

