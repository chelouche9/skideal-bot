"""SkiDeal Bot - AI-powered ski trip sales assistant.

Helps customers find and book the perfect ski trip packages.
Uses Claude Sonnet 4.5 and LangGraph.
"""

from __future__ import annotations

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent

# Import system prompt
from agent.prompt import SYSTEM_PROMPT

# Import tools
from agent.tools import (
    get_available_destinations,
    get_hotels_list,
    get_hotel_info,
    search_hotels_by_criteria,
    get_resort_camps_info,
    get_camp_resorts,
    get_camps_info,
    get_kosher_info,
    handoff_to_agent,
)

# Load environment variables
load_dotenv()


# ============================================================================
# AGENT CREATION - Using LangGraph
# ============================================================================

# Define all tools
tools = [
    get_available_destinations,
    get_hotels_list,
    get_hotel_info,
    search_hotels_by_criteria,
    get_resort_camps_info,
    get_camp_resorts,
    get_camps_info,
    get_kosher_info,
    handoff_to_agent,
]

# Create the model
model = ChatAnthropic(model="claude-sonnet-4-20250514")

# Create the agent using LangGraph's create_react_agent
graph = create_react_agent(
    model=model,
    tools=tools,
    prompt=SYSTEM_PROMPT,
)
