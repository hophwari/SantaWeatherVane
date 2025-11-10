import requests

def get_weather(lat, lon ):
    print (f"Getting Weather for {lat} & {lon} ")

    """
    Fetch current weather data from the Open-Meteo API for the given latitude and longitude.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
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
