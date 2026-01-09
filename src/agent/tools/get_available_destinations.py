"""Tool to get available ski destinations."""

import json
from langchain_core.tools import tool

from agent.ski_data import DATA_SUMMARY


@tool
def get_available_destinations() -> str:
    """Get a list of all available ski destinations organized by country.
    
    Returns a summary of all countries and resorts available in the system.
    Use this when customer asks what destinations are available.
    
    Returns:
        JSON string with countries and their resorts.
    """
    return json.dumps(DATA_SUMMARY, ensure_ascii=False, indent=2)

