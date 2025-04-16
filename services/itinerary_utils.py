
def format_day_itinerary(day: int, activities: list) -> str:
    formatted = f"## Day {day}\n"
    for act in activities:
        formatted += f"- {act}\n"
    return formatted
