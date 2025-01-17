"""
Time Service Module
"""
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

class TimeService:
    """
    Time Service Class
    """
    def __init__(self):
        """
        Time Service Constructor
        """
        self.geolocator = Nominatim(user_agent="timezone_locator")
        self.timezone_finder = TimezoneFinder()

    def get_local_time(self, city: str) -> dict:
        """
        Get local time by city name.

        Args:
            city (str): The name of the city.

        Returns:
            dict: Contains the city, timezone, local time, or an error message.
        """
        try:
            # Get city coordinates using geopy
            location = self.geolocator.geocode(city)
            if not location:
                return {"status": "error", "message": f"City '{city}' not found."}

            # Get timezone using coordinates
            timezone_str = self.timezone_finder.timezone_at(
                lat=location.latitude, lng=location.longitude
            )
            if not timezone_str:
                return {"status": "error", "message": "Timezone could not be determined."}

            # Get the current local time
            timezone = pytz.timezone(timezone_str)
            local_time = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")

            return {
                "status": "success",
                "city": city.title(),
                "timezone": timezone_str,
                "local_time": local_time,
            }
        except (ConnectionError, TimeoutError, ValueError) as e:
            return {"status": "error", "message": str(e)}
