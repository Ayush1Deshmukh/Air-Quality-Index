import numpy as np

class AQICalculator:
    def __init__(self):
        self.breakpoints = {
            'PM2.5': [(0, 12, 0, 50), (12.1, 35.4, 51, 100), (35.5, 55.4, 101, 150)],
            'PM10': [(0, 54, 0, 50), (55, 154, 51, 100), (155, 254, 101, 150)],
            'O3': [(0, 54, 0, 50), (55, 70, 51, 100), (71, 85, 101, 150)],
            'CO': [(0, 4.4, 0, 50), (4.5, 9.4, 51, 100), (9.5, 12.4, 101, 150)]
        }

    def calculate_aqi(self, pollutant, concentration):
        if pollutant not in self.breakpoints:
            return None
        
        for low_conc, high_conc, low_aqi, high_aqi in self.breakpoints[pollutant]:
            if low_conc <= concentration <= high_conc:
                return self._linear(concentration, low_conc, high_conc, low_aqi, high_aqi)
        return None

    def _linear(self, conc, conc_low, conc_high, aqi_low, aqi_high):
        return int(((aqi_high - aqi_low) / (conc_high - conc_low)) * (conc - conc_low) + aqi_low)

    def get_aqi_category(self, aqi):
        if aqi <= 50:
            return "Good", "#28A745"
        elif aqi <= 100:
            return "Moderate", "#FFC107"
        else:
            return "Unhealthy", "#DC3545"

    def get_health_recommendation(self, aqi):
        if aqi <= 50:
            return "Air quality is satisfactory, and air pollution poses little or no risk."
        elif aqi <= 100:
            return "Air quality is acceptable. However, there may be a risk for some people."
        else:
            return "Everyone may begin to experience health effects."
