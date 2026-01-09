"""Data modules for SkiDeal Bot."""

from agent.data.resorts import (
    HOTELS_DATA,
    RESORTS_INFO,
    DATA_SUMMARY,
    get_hotels,
    get_hotel_by_name,
    get_hotels_by_country,
    get_hotels_by_resort,
    get_resort_info,
    search_hotels,
    get_countries,
    get_resorts_by_country,
)

from agent.data.camps import (
    CAMPS_DATA,
    CAMPS_SUMMARY,
    get_camps,
    get_camps_by_resort,
    get_camps_by_country,
    get_camp_countries,
    get_camp_resorts_by_country,
    get_all_camp_resorts,
    search_camps_by_resort_prefix,
    search_camps,
)

__all__ = [
    # Resorts/Hotels
    "HOTELS_DATA",
    "RESORTS_INFO",
    "DATA_SUMMARY",
    "get_hotels",
    "get_hotel_by_name",
    "get_hotels_by_country",
    "get_hotels_by_resort",
    "get_resort_info",
    "search_hotels",
    "get_countries",
    "get_resorts_by_country",
    # Camps
    "CAMPS_DATA",
    "CAMPS_SUMMARY",
    "get_camps",
    "get_camps_by_resort",
    "get_camps_by_country",
    "get_camp_countries",
    "get_camp_resorts_by_country",
    "get_all_camp_resorts",
    "search_camps_by_resort_prefix",
    "search_camps",
]

