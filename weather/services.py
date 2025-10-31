# weather/services.py
import requests
from datetime import datetime
from .models import CachedWeather


def fetch_weather_from_api(city):
    """Fetch weather data from wttr.in API (free, no key needed)."""
    url = f"https://wttr.in/{city}?format=j1"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    current = data["current_condition"][0]
    weather_info = {
        "city": city.title(),
        "temp_c": current.get("temp_C"),
        "feels_like_c": current.get("FeelsLikeC"),
        "desc": current["weatherDesc"][0]["value"],
        "humidity": current.get("humidity"),
        "wind_kph": current.get("windspeedKmph"),
        "updated_at": datetime.utcnow().isoformat(),
        "source": "wttr.in",
    }
    return weather_info


def get_weather(city, use_cache=True, ttl_minutes=15):
    """Check cache, else fetch from API."""
    city_key = city.lower()
    cached = CachedWeather.objects(city=city_key).first()

    if use_cache and cached and cached.is_fresh(ttl_minutes=ttl_minutes):
        return {"source": "cache", "data": cached.data, "fetched_at": cached.fetched_at}

    # Fetch from API
    data = fetch_weather_from_api(city)
    if cached:
        cached.data = data
        cached.fetched_at = datetime.utcnow()
        cached.save()
    else:
        CachedWeather(city=city_key, data=data).save()

    return {"source": "api", "data": data, "fetched_at": datetime.utcnow()}
