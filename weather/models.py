from django.db import models

# Create your models here.
# weather/models.py

from datetime import datetime, timedelta
import mongoengine as me

class CachedWeather(me.Document):
    city = me.StringField(required=True, unique=True)
    data = me.DictField()
    fetched_at = me.DateTimeField(default=datetime.now)

    meta = {"collection": "cached_weather"}

    def is_fresh(self, ttl_minutes=10):
        return datetime.utcnow() - self.fetched_at < timedelta(minutes=ttl_minutes)

