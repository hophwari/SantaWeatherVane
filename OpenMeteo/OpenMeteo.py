import requests
from datetime import datetime, timedelta, timezone

def get_next_hour_gust(data):
    # Create next hour timestamp such as "2025-11-16T22:00"
    now = datetime.now(timezone.utc)
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    next_hour_str = next_hour.strftime("%Y-%m-%dT%H:00")

    times = data["hourly"]["time"]
    gusts = data["hourly"]["wind_gusts_10m"]

    if next_hour_str in times:
        idx = times.index(next_hour_str)
        return {
            "time": next_hour_str,
            "wind_gust_kmh": gusts[idx]
        }
    else:
        return {"error": f"No gust data for next hour: {next_hour_str}"}



def get_next_hour_windspeed(data):
    """
    Returns the wind speed (km/h) for the next full hour
    from an Open-Meteo response.
    """

    # Get next full UTC hour
    now = datetime.now(timezone.utc)
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    next_hour_str = next_hour.strftime("%Y-%m-%dT%H:00")

    # Extract arrays from the dataset
    times = data["hourly"]["time"]
    speeds = data["hourly"]["windspeed_10m"]

    # Find index for next-hour timestamp
    if next_hour_str in times:
        idx = times.index(next_hour_str)
        return {
            "time": next_hour_str,
            "windspeed_kmh": speeds[idx]
        }

    return {
        "error": f"No wind speed data available for next hour: {next_hour_str}"
    }


def get_weather(lat, lon ):
    print (f"Getting Weather for {lat} & {lon} ")

    """
    Fetch current weather data from the Open-Meteo API for the given latitude and longitude.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["weathercode","windspeed_10m", "wind_gusts_10m"],
        "current_weather": True,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data:
            return data
        else:
            return {"error": "No current weather data available"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

