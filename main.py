# Santa Weather Vane
import argparse
import time
from datetime import datetime

from Hue.HueSwitch import HueSwitch
from OpenMeteo.OpenMeteo import get_weather, get_next_hour_gust, get_next_hour_windspeed


def apply_wind_logic(windgust, windlimit, hue):
    """
    Turns a Hue light on/off based on time window and wind gust threshold.

    Time windows:
      - 07:00 to 09:00
      - 16:00 to 22:00
    """

    now = datetime.now()
    hour = now.hour
    weekday = now.weekday()  # Monday = 0 ... Sunday = 7

    weekday_names = ["Mon", "Tues", "Weds", "Thurs", "Fri", "Sat", "Sun"]
    weekday_str = weekday_names[now.weekday()]

    # Existing weekday windows
    in_morning_window = 7 <= hour < 9
    in_evening_window = 16 <= hour < 22

    # New weekend window (Saturday=5, Sunday=6)
    is_weekend = weekday >= 5
    in_weekend_window = is_weekend and (12 <= hour < 22)

    # Final combined condition
    in_time_window = in_morning_window or in_evening_window or in_weekend_window

    # Get Current State of Switch
    current_state = hue.get_state()['on']
    print (f"Current State: {current_state}")

    if in_time_window:
        print(f"Within time window at {now.strftime('%H:%M')} on day {weekday_str}.")

        if windgust < windlimit:
            result = hue.turn_on()
            print("Wind OK — turning Santa ON.")
            return result
        else:
            result = hue.turn_off()
            print("Wind too high — turning Santa OFF.")
            return result

    else:
        if current_state:
            result = hue.turn_off()
            print(f"Outside active time window at {now.strftime('%H:%M')} — turning Santa OFF.")
            return result
        else:
            print(f"Outside active time window at {now.strftime('%H:%M')}. Doing nothing.")

        return None


def main():

    parser = argparse.ArgumentParser(description="Get current weather data from Open-Meteo.")
    parser.add_argument("--lat", type=float, required=True, help="Latitude coordinate")
    parser.add_argument("--lon", type=float, required=True, help="Longitude coordinate")
    parser.add_argument("--windlimit", type=float, required=True, help="Longitude coordinate")
    parser.add_argument("--bridge", type=str, required=True, help="Hue Bridge IP address")
    parser.add_argument("--user", type=str, required=True, help="Hue Bridge User Name")
    parser.add_argument("--lightname", type=str, required=True, help="Hue Bridge User Name")
    args = parser.parse_args()

    BRIDGE_IP = args.bridge
    USERNAME = args.user
    NAME = args.lightname
    LIGHT_ID = HueSwitch.find_light_by_name(BRIDGE_IP, USERNAME, NAME)

    hue = HueSwitch(BRIDGE_IP, USERNAME, LIGHT_ID)

    while True:

        now = datetime.now()
        print(f"Time: {now}")

        try:
            weather = get_weather(args.lat, args.lon)

            windspeed = get_next_hour_windspeed(weather)["windspeed_kmh"]
            windgust  = get_next_hour_gust(weather)["wind_gust_kmh"]

            print(f"Wind Speed:  {windspeed}")
            print(f"Wind Speed Gust:  {windgust}")
            print(f"Wind Gust Limit:  {args.windlimit}")

            apply_wind_logic(windgust, args.windlimit, hue)
        except:
            print("Error getting weather forecast")

        print(f"Sleeping...")

        time.sleep(600)  # 600 seconds = 10 minutes


if __name__ == "__main__":
    main()

