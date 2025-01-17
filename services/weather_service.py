"""
    Weather service module
"""
import requests

class WeatherService:
    """
        Weather service class
    """

    def __init__(self, api_key: str) -> None:
        """
            Weather service constructor
        """
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city: str) -> dict:
        """
            Get weather by city name
        """
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }

        response = requests.get(self.base_url, params=params, timeout=300)
        response.raise_for_status()
        return response.json()
    
if __name__ == "__main__":
    weather_service = WeatherService(api_key="71e19f904836127f07ac016cf20c9402")
    weather = weather_service.get_weather(city="Bahawalpur")
    print(weather)