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
        Get local time by city name using UTC time to ensure accuracy.
        """
        try:
            # Get city coordinates using geopy
            location = self.geolocator.geocode(city)
            if not location:
                return {"status": "error", "message": f"City '{city}' not found."}

            # Get timezone from coordinates
            timezone_str = self.timezone_finder.timezone_at(
                lat=location.latitude,
                lng=location.longitude
            )
            if not timezone_str:
                return {"status": "error", "message": "Timezone could not be determined."}

            # Use UTC time and convert it to the target timezone
            timezone = pytz.timezone(timezone_str)
            utc_now = datetime.now(timezone.utc).replace(tzinfo=pytz.utc)
            local_time = utc_now.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S")

            return {
                "status": "success",
                "city": city.title(),
                "timezone": timezone_str,
                "local_time": local_time,
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}
