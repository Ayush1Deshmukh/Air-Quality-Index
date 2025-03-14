import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

class OpenWeatherMapClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        if not self.api_key:
            raise ValueError("OpenWeatherMap API key not found in environment variables")
        if not self.api_key.strip():
            raise ValueError("OpenWeatherMap API key cannot be empty")
        self.base_url = "http://api.openweathermap.org/data/2.5"

    def get_air_quality(self, lat, lon):
        url = f"{self.base_url}/air_pollution?lat={lat}&lon={lon}&appid={self.api_key}"
        try:
            response = requests.get(url)
            if response.status_code == 401:
                raise Exception("Invalid API key. Please ensure your OpenWeatherMap API key is correct and activated.")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            error_msg = f"Failed to fetch air quality data: {str(e)}"
            if hasattr(e.response, 'json'):
                try:
                    error_details = e.response.json()
                    error_msg += f" - API Response: {error_details}"
                except:
                    pass
            raise Exception(error_msg)

    def get_historical_data(self, lat, lon, start_time, end_time):
        start = int(start_time.timestamp())
        end = int(end_time.timestamp())
        url = f"{self.base_url}/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={self.api_key}"
        try:
            response = requests.get(url)
            if response.status_code == 401:
                raise Exception("Invalid API key. Please ensure your OpenWeatherMap API key is correct and activated.")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            error_msg = f"Failed to fetch historical data: {str(e)}"
            if hasattr(e.response, 'json'):
                try:
                    error_details = e.response.json()
                    error_msg += f" - API Response: {error_details}"
                except:
                    pass
            raise Exception(error_msg)

    def get_coordinates(self, city):
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={self.api_key}"
        try:
            response = requests.get(url)
            if response.status_code == 401:
                raise Exception("Invalid API key. Please ensure your OpenWeatherMap API key is correct and activated.")
            response.raise_for_status()
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon']
            raise Exception(f"City '{city}' not found")
        except requests.RequestException as e:
            error_msg = f"Failed to fetch coordinates: {str(e)}"
            if hasattr(e.response, 'json'):
                try:
                    error_details = e.response.json()
                    error_msg += f" - API Response: {error_details}"
                except:
                    pass
            if e.response and e.response.status_code == 404:
                raise Exception(f"City '{city}' not found")
            raise Exception(error_msg)