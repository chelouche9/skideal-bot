"""SkiDeal Bot - Camps Data Loader.

Loads and organizes ski camps data from the JSONL file.
Data sourced from SkiDeal internal sheets.
"""

import json
from pathlib import Path
from typing import Any

# Path to the JSONL data file (in the same directory as this file)
CAMPS_FILE = Path(__file__).parent / "camps.jsonl"


def load_all_camps() -> list[dict[str, Any]]:
    """Load all camp records from the JSONL file."""
    records = []
    with open(CAMPS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def get_camps() -> list[dict[str, Any]]:
    """Get all camp records from the data."""
    return load_all_camps()


def get_camp_countries() -> list[str]:
    """Get list of all unique countries that have camps."""
    camps = get_camps()
    countries = set()
    for camp in camps:
        country = camp.get("מדינה", "")
        if country:
            countries.add(country)
    return sorted(list(countries))


def get_camp_resorts_by_country(country: str) -> list[str]:
    """Get list of resorts with camps for a specific country."""
    camps = get_camps()
    resorts = set()
    for camp in camps:
        if camp.get("מדינה", "").lower() == country.lower():
            resort = camp.get("אתר", "")
            if resort:
                resorts.add(resort)
    return sorted(list(resorts))


def get_all_camp_resorts() -> dict[str, list[str]]:
    """Get all resorts that have camps, organized by country."""
    countries = get_camp_countries()
    return {
        country: get_camp_resorts_by_country(country)
        for country in countries
    }


def get_camps_by_resort(resort: str) -> list[dict[str, Any]]:
    """Get all camps in a specific resort (exact match)."""
    camps = get_camps()
    return [c for c in camps if c.get("אתר", "").lower() == resort.lower()]


def get_camps_by_country(country: str) -> list[dict[str, Any]]:
    """Get all camps in a specific country."""
    camps = get_camps()
    return [c for c in camps if c.get("מדינה", "").lower() == country.lower()]


def search_camps_by_resort_prefix(resort_prefix: str) -> list[dict[str, Any]]:
    """Search camps where resort name starts with or contains the given prefix.
    
    Useful for finding all variants like "בנסקו", "בנסקו שבוע", "בנסקו סופש".
    """
    camps = get_camps()
    resort_lower = resort_prefix.lower()
    return [
        c for c in camps 
        if resort_lower in c.get("אתר", "").lower()
    ]


def search_camps(
    country: str | None = None,
    resort: str | None = None,
    min_age: float | None = None,
    max_age: float | None = None,
    includes_lunch: bool | None = None,
) -> list[dict[str, Any]]:
    """Search camps by various criteria.
    
    Args:
        country: Filter by country name (e.g., "צרפת", "בולגריה")
        resort: Filter by resort name or partial name
        min_age: Minimum age of child
        max_age: Maximum age of child
        includes_lunch: True to filter for camps that include lunch
    
    Returns:
        List of matching camps.
    """
    camps = get_camps()
    results = []
    
    for camp in camps:
        # Country filter
        if country and camp.get("מדינה", "").lower() != country.lower():
            continue
            
        # Resort filter (partial match)
        if resort and resort.lower() not in camp.get("אתר", "").lower():
            continue
        
        # Age filter - check if the age range overlaps
        if min_age is not None or max_age is not None:
            age_range = camp.get("גילאים", {})
            camp_min = age_range.get("מינימום", 0)
            camp_max = age_range.get("מקסימום", 99)
            
            if min_age is not None and camp_max < min_age:
                continue
            if max_age is not None and camp_min > max_age:
                continue
        
        # Lunch filter
        if includes_lunch is True:
            if not camp.get("כולל ארוחת צהריים"):
                continue
        
        results.append(camp)
    
    return results


def get_camps_summary() -> dict[str, Any]:
    """Get a summary of available camps data."""
    camps = get_camps()
    countries = get_camp_countries()
    
    return {
        "total_camps": len(camps),
        "countries": countries,
        "resorts_by_country": get_all_camp_resorts(),
    }


# For convenience, export commonly used data
CAMPS_DATA = get_camps()
CAMPS_SUMMARY = get_camps_summary()

