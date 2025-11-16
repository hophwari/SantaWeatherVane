# Santa Weather Vane
import argparse

from Hue.HueSwitch import HueSwitch
from OpenMeteo.OpenMeteo import get_weather, get_next_hour_gust, get_next_hour_windspeed

def main():

    parser = argparse.ArgumentParser(description="Get current weather data from Open-Meteo.")
    parser.add_argument("--lat", type=float, required=True, help="Latitude coordinate")
    parser.add_argument("--lon", type=float, required=True, help="Longitude coordinate")
    parser.add_argument("--windlimit", type=float, required=True, help="Longitude coordinate")
    parser.add_argument("--bridge", type=str, required=True, help="Hue Bridge IP address")
    parser.add_argument("--user", type=str, required=True, help="Hue Bridge User Name")
    parser.add_argument("--lightname", type=str, required=True, help="Hue Bridge User Name")
    args = parser.parse_args()

    weather = get_weather(args.lat, args.lon)

    windspeed = get_next_hour_windspeed(weather)["windspeed_kmh"]
    windgust  = get_next_hour_gust(weather)["wind_gust_kmh"]

    print(f"Wind Speed:  {windspeed}")
    print(f"Wind Speed Gust:  {windgust}")
    print(f"Wind Gust Limit:  {args.windlimit}")


    BRIDGE_IP = args.bridge
    USERNAME = args.user
    NAME = args.lightname
    LIGHT_ID = HueSwitch.find_light_by_name(BRIDGE_IP, USERNAME, NAME )

    hue = HueSwitch(BRIDGE_IP, USERNAME, LIGHT_ID)


    if windgust < args.windlimit:
        print(hue.turn_on())
    else:
        print(hue.turn_off())

    print(hue.get_state())


if __name__ == "__main__":
    main()

