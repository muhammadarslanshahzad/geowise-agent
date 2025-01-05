"""
    The get_local_time.py script uses the geopy and timezonefinder libraries to get the timezone and local time for a given city.

"""
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from langchain.tools import tool
import pytz

@tool
def get_local_time(city: str) -> dict:
    """
    Get the timezone and local time for a given city.

    Args:
        city (str): The name of the city.

    Returns:
        dict: Contains the timezone and local time or an error message.
    """
    try:
        # Get city coordinates using geopy
        geolocator = Nominatim(user_agent="timezone_locator")
        location = geolocator.geocode(city)
        if not location:
            return {"status": "error", "message": f"City '{city}' not found."}

        # Get timezone using coordinates
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=location.latitude, lng=location.longitude)
        if not timezone_str:
            return {"status": "error", "message": "Timezone could not be determined."}

        # Get the current local time
        timezone = pytz.timezone(timezone_str)
        local_time = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")

        return f"The local time in {city.title()} ({timezone_str}) is {local_time}."
    except Exception as e:
        return {"status": "error", "message": str(e)}
