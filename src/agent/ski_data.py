"""SkiDeal Bot - Ski Trip Data Loader.

Loads and organizes ski trip data from the JSONL file.
Data sourced from SkiDeal internal sheets.
"""

import json
from pathlib import Path
from typing import Any

# Path to the JSONL data file
DATA_FILE = Path(__file__).parent.parent.parent / "super_info_bot_rows.jsonl"


def load_all_data() -> list[dict[str, Any]]:
    """Load all records from the JSONL file."""
    records = []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def get_hotels() -> list[dict[str, Any]]:
    """Get all hotel records from the data.
    
    Returns hotels with record_type 'hotel_or_item' that have hotel details.
    """
    all_data = load_all_data()
    hotels = []
    
    for record in all_data:
        meta = record.get("_meta", {})
        record_type = meta.get("record_type", "")
        hotel_name = record.get("שם מלון באנגלית", "")
        
        # Skip section records (כללי, הערות כלליות, etc.)
        if hotel_name in ["כללי", "הערות כלליות", "הערות כלליות על האתר"]:
            continue
            
        # Only include records that have hotel details (נתונים יבשים)
        if "נתונים יבשים" in record:
            hotels.append(record)
    
    return hotels


def get_resorts_info() -> list[dict[str, Any]]:
    """Get resort-level information (sections with general info).
    
    Returns section records that contain general resort info, 
    camp info (קייטנות), and credit info (זיכויים).
    """
    all_data = load_all_data()
    resorts = []
    
    for record in all_data:
        hotel_name = record.get("שם מלון באנגלית", "")
        
        # Include section records (כללי, הערות כלליות, etc.)
        if hotel_name in ["כללי", "הערות כלליות", "הערות כלליות על האתר"]:
            resorts.append(record)
    
    return resorts


def get_countries() -> list[str]:
    """Get list of all unique countries."""
    hotels = get_hotels()
    countries = set()
    for hotel in hotels:
        country = hotel.get("מדינה", "")
        if country:
            countries.add(country)
    return sorted(list(countries))


def get_resorts_by_country(country: str) -> list[str]:
    """Get list of resorts for a specific country."""
    hotels = get_hotels()
    resorts = set()
    for hotel in hotels:
        if hotel.get("מדינה", "").lower() == country.lower():
            resort = hotel.get("אתר", "")
            if resort:
                resorts.add(resort)
    return sorted(list(resorts))


def get_hotels_by_resort(resort: str) -> list[dict[str, Any]]:
    """Get all hotels in a specific resort."""
    hotels = get_hotels()
    return [h for h in hotels if h.get("אתר", "").lower() == resort.lower()]


def get_hotels_by_country(country: str) -> list[dict[str, Any]]:
    """Get all hotels in a specific country."""
    hotels = get_hotels()
    return [h for h in hotels if h.get("מדינה", "").lower() == country.lower()]


def get_hotel_by_name(hotel_name: str) -> dict[str, Any] | None:
    """Get a specific hotel by its English name."""
    hotels = get_hotels()
    for hotel in hotels:
        if hotel.get("שם מלון באנגלית", "").lower() == hotel_name.lower():
            return hotel
    return None


def get_resort_info(country: str, resort: str) -> dict[str, Any] | None:
    """Get resort-level info including camps and credits."""
    resorts = get_resorts_info()
    for r in resorts:
        if (r.get("מדינה", "").lower() == country.lower() and 
            r.get("אתר", "").lower() == resort.lower()):
            return r
    return None


def search_hotels(
    country: str | None = None,
    resort: str | None = None,
    min_stars: int | None = None,
    has_spa: bool | None = None,
    suitable_for: str | None = None,
) -> list[dict[str, Any]]:
    """Search hotels by various criteria.
    
    Args:
        country: Filter by country name (e.g., "אוסטריה", "צרפת")
        resort: Filter by resort name (e.g., "ואל טורנס", "אישגיל")
        min_stars: Minimum star rating (3, 4, or 5)
        has_spa: True to filter for hotels with spa
        suitable_for: Filter by target audience (e.g., "זוגות", "משפחה")
    
    Returns:
        List of matching hotels.
    """
    hotels = get_hotels()
    results = []
    
    for hotel in hotels:
        # Country filter
        if country and hotel.get("מדינה", "").lower() != country.lower():
            continue
            
        # Resort filter
        if resort and hotel.get("אתר", "").lower() != resort.lower():
            continue
        
        # Star rating filter
        if min_stars:
            dry_data = hotel.get("נתונים יבשים", {})
            stars = dry_data.get("כוכבים", 0)
            if isinstance(stars, int) and stars < min_stars:
                continue
            elif isinstance(stars, str) and not stars.isdigit():
                continue  # Skip if stars is not a number (e.g., "מלון דירות")
            elif isinstance(stars, str) and int(stars) < min_stars:
                continue
        
        # Spa filter
        if has_spa is True:
            spa_info = hotel.get("ספא", {})
            spa_cost = spa_info.get("עלות כניסה לספא", "")
            if spa_cost in ["אין", "אין ספא", ""]:
                continue
        
        # Suitable for filter
        if suitable_for:
            dry_data = hotel.get("נתונים יבשים", {})
            target = dry_data.get("למי מתאים המלון", "")
            if suitable_for.lower() not in target.lower():
                continue
        
        results.append(hotel)
    
    return results


# Pre-load data summary for quick access
def get_data_summary() -> dict[str, Any]:
    """Get a summary of available data."""
    hotels = get_hotels()
    resorts = get_resorts_info()
    countries = get_countries()
    
    return {
        "total_hotels": len(hotels),
        "total_resorts_info": len(resorts),
        "countries": countries,
        "resorts_by_country": {
            country: get_resorts_by_country(country) 
            for country in countries
        }
    }


# For convenience, export commonly used data
HOTELS_DATA = get_hotels()
RESORTS_INFO = get_resorts_info()
DATA_SUMMARY = get_data_summary()
