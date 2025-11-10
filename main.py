# Santa Weather Vane
import argparse

from OpenMeteo.OpenMeteo import get_weather

def main():

    parser = argparse.ArgumentParser(description="Get current weather data from Open-Meteo.")
    parser.add_argument("latitude", type=float, help="Latitude coordinate")
    parser.add_argument("longitude", type=float, help="Longitude coordinate")
    args = parser.parse_args()


    weather = get_weather(args.latitude, args.longitude)
    print(weather)
    print(f"Wind speed: {weather['windspeed']}")

if __name__ == "__main__":
    main()


