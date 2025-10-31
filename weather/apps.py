from django.apps import AppConfig
import os
from dotenv import load_dotenv
load_dotenv()

class WeatherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather'

    def ready(self):
        # Connect to MongoDB using mongoengine on startup
        import mongoengine
        mongo_uri = os.getenv("MONGO_URI")
        if mongo_uri:
            mongoengine.connect(host=mongo_uri)
        else:
            # fallback: local default
            mongoengine.connect("weatherdb")