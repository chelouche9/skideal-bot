"""Tool to get information about SKIPA kosher ski vacations."""

from langchain_core.tools import tool

from agent.data.kosher import SKIPA_INFO


@tool
def get_kosher_info() -> str:
    """Get information about SKIPA - SKIDEAL's kosher ski vacations department.
    
    Use this when the customer asks about:
    - Kosher food options (אוכל כשר, כשרות)
    - Religious/observant travelers (דתיים, שומרי מסורת)
    - Shabbat arrangements (שבת)
    - Prayer/minyan options (תפילות, מניין)
    - SKIPA specifically
    
    Returns:
        Text with all information about kosher vacation options.
    """
    return SKIPA_INFO
