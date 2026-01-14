"""Tool for handing off conversation to a human agent."""

import json
import re
from langchain_core.tools import tool


def validate_phone(phone: str) -> tuple[bool, str]:
    """Validate Israeli phone number format."""
    if not phone:
        return True, ""  # Optional field
    
    # Remove spaces and dashes
    cleaned = phone.replace(" ", "").replace("-", "")
    
    # Israeli mobile: 05XXXXXXXX (10 digits)
    israeli_mobile = re.match(r'^05\d{8}$', cleaned)
    
    # International format: +9725XXXXXXXX (13 chars)
    intl_format = re.match(r'^\+9725\d{8}$', cleaned)
    
    # Israeli landline: 0X-XXXXXXX (9-10 digits)
    israeli_landline = re.match(r'^0[2-9]\d{7,8}$', cleaned)
    
    if israeli_mobile or intl_format or israeli_landline:
        return True, ""
    
    return False, f"מספר טלפון לא תקין: '{phone}'. פורמט נדרש: 0501234567 או +972501234567"


def validate_email(email: str) -> tuple[bool, str]:
    """Validate email format."""
    if not email:
        return True, ""  # Optional field
    
    # Basic email regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, ""
    
    return False, f"אימייל לא תקין: '{email}'. פורמט נדרש: example@domain.com"


def validate_name(name: str) -> tuple[bool, str]:
    """Validate that name has at least first and last name."""
    if not name:
        return True, ""  # Optional field
    
    # Clean up the name - remove extra spaces
    cleaned = " ".join(name.strip().split())
    
    # Check if name has at least 2 words (first + last name)
    # Works for Hebrew names like "יונתן שלוש" or English "John Smith"
    words = cleaned.split()
    if len(words) >= 2:
        return True, ""
    
    # Single word name is not enough
    return False, f"שם לא מלא: '{name}'. נדרש שם פרטי ושם משפחה"


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
    
    IMPORTANT: This tool validates inputs! If validation fails, you must collect
    the correct information from the customer before calling again.
    
    Use this tool when:
    - Customer is ready to book/close the deal
    - Payment details need to be collected
    - You don't have certain information and need human assistance
    - Customer explicitly asks to speak with a human
    
    Args:
        customer_name: Customer's FULL name (first + last) in Hebrew
        phone: Phone in format 05XXXXXXXX (10 digits) or +9725XXXXXXXX (13 chars)
        email: Email in format example@domain.com
        destination: Preferred destination/resort/country
        dates: Travel dates (can be flexible like "מרץ" or exact like "15-22/03")
        num_people: Number of travelers (must be a number)
        ages: Ages of travelers (especially children) - must be numeric ages
        ski_level: Skiing experience level (beginner/intermediate/advanced)
        needs_ski_school: Whether they need ski school/lessons
        needs_equipment: Whether they need equipment rental
        hotel_preference: Preferred hotel or hotel type
        budget: Budget range or constraints
        spa_preference: Whether spa is important
        insurance_interest: Interest in Trip Guaranty/insurance
        additional_notes: Any other relevant information from the conversation
    
    Returns:
        Confirmation message with handoff summary, or validation errors if inputs are invalid.
    """
    # Validate inputs
    validation_errors = []
    
    # Validate phone
    is_valid, error = validate_phone(phone)
    if not is_valid:
        validation_errors.append(error)
    
    # Validate email
    is_valid, error = validate_email(email)
    if not is_valid:
        validation_errors.append(error)
    
    # Validate name
    is_valid, error = validate_name(customer_name)
    if not is_valid:
        validation_errors.append(error)
    
    # If there are validation errors, return them
    if validation_errors:
        return json.dumps({
            "סטטוס": "שגיאת אימות",
            "הודעה": "יש לתקן את הפרטים הבאים לפני העברה לנציג:",
            "שגיאות": validation_errors,
        }, ensure_ascii=False, indent=2)
    
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
