import requests
from typing import Dict, Optional
from config import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL


def get_weather(city: str, api_key: str = OPENWEATHER_API_KEY) -> Optional[Dict]:
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "ru"
    }

    response = requests.get(OPENWEATHER_BASE_URL, params=params)
    response.raise_for_status()
    return response.json()


def display_weather(weather_data: Dict) -> None:
    temperature = weather_data["main"]["temp"]
    description = weather_data["weather"][0]["description"]
    city_name = weather_data["name"]

    print(f"Город: {city_name}")
    print(f"Температура: {temperature}°C")
    print(f"Описание: {description}")


def main():
    city = input("Введите название города: ")

    try:
        weather_data = get_weather(city)
        display_weather(weather_data)
    except requests.RequestException as e:
        print(f"Ошибка при получении данных: {e}")


if __name__ == "__main__":
    main()
