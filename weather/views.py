import requests
from django.shortcuts import render
from django.utils import timezone
import pytz
from .mongo_client import db  # ✅ use your MongoDB connection here


def home(request):
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.POST.get("city")

        # Free weather API (no API key required)
        url = f"https://wttr.in/{city}?format=j1"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()

            current = data["current_condition"][0]
            temp = current["temp_C"]
            desc = current["weatherDesc"][0]["value"]

            # Convert time to IST
            ist = pytz.timezone("Asia/Kolkata")
            now_ist = timezone.now().astimezone(ist).strftime("%Y-%m-%d %H:%M:%S")

            weather_data = {
                "city": city.capitalize(),
                "temp": temp,
                "desc": desc,
                "time": now_ist,
            }

            # ✅ Save to MongoDB if connected
            if db is not None:
                db.weather_history.insert_one(weather_data)

        except Exception as e:
            error = f"Error fetching weather: {e}"

    # ✅ Fetch last 5 search history from MongoDB
    if db is not None:
        history_cursor = db.weather_history.find().sort("_id", -1).limit(5)
    else:
        history_cursor = []

    history = list(history_cursor)

    return render(
        request,
        "weather/home.html",
        {"weather": weather_data, "error": error, "history": history},
    )
