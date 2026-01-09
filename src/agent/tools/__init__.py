"""Tools for the SkiDeal sales agent."""

from agent.tools.get_available_destinations import get_available_destinations
from agent.tools.get_hotels_list import get_hotels_list
from agent.tools.get_hotel_info import get_hotel_info
from agent.tools.search_hotels_by_criteria import search_hotels_by_criteria
from agent.tools.get_resort_camps_info import get_resort_camps_info
from agent.tools.handoff_to_agent import handoff_to_agent

__all__ = [
    "get_available_destinations",
    "get_hotels_list",
    "get_hotel_info",
    "search_hotels_by_criteria",
    "get_resort_camps_info",
    "handoff_to_agent",
]

