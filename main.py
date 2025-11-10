# Santa Weather Vane
import argparse

from Hue.HueSwitch import HueSwitch
from OpenMeteo.OpenMeteo import get_weather

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
    print(weather)

    windspeed = weather['current_weather']['windspeed']

    BRIDGE_IP = args.bridge
    USERNAME = args.user
    NAME = args.lightname
    LIGHT_ID = HueSwitch.find_light_by_name(BRIDGE_IP, USERNAME, NAME )

    hue = HueSwitch(BRIDGE_IP, USERNAME, LIGHT_ID)

    print(f"Wind speed {windspeed} vs wind limit  {args.windlimit}")


    if windspeed < args.windlimit:
        print(hue.turn_on())
    else:
        print(hue.turn_off())

    print(hue.get_state())


if __name__ == "__main__":
    main()

