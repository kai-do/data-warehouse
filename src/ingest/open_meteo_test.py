import json
from datetime import datetime, timezone
from pathlib import Path

import requests

latitude = 34.101333
longitude = -84.519389

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": latitude,
    "longitude": longitude,
    "minutely_15": (
        "temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,"
        "pressure_msl,surface_pressure,cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high,"
        "wind_speed_10m,wind_speed_80m,wind_speed_120m,wind_speed_180m,"
        "wind_direction_10m,wind_direction_80m,wind_direction_120m,wind_direction_180m,wind_gusts_10m,"
        "shortwave_radiation,direct_radiation,direct_normal_irradiance,diffuse_radiation,global_tilted_irradiance,"
        "vapour_pressure_deficit,cape,evapotranspiration,et0_fao_evapotranspiration,"
        "precipitation,snowfall,precipitation_probability,rain,showers,weather_code,snow_depth,"
        "freezing_level_height,visibility,"
        "soil_temperature_0cm,soil_temperature_6cm,soil_temperature_18cm,soil_temperature_54cm,"
        "soil_moisture_0_to_1cm,soil_moisture_1_to_3cm,soil_moisture_3_to_9cm,soil_moisture_9_to_27cm,soil_moisture_27_to_81cm,"
        "is_day"
    )
}

response = requests.get(url, params=params)
response.raise_for_status()

payload = response.json()

current = payload["minutely_15"]

# print(json.dumps(payload, indent=2))

# print just the first 15-minute interval
first_interval = current["time"][0]
first_interval_data = {key: current[key][0] for key in current if key != "time"}
print(f"First 15-minute interval: {first_interval}")
print(json.dumps(first_interval_data, indent=2))    