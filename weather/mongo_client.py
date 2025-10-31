from pymongo import MongoClient
from django.conf import settings

MONGO_URI = settings.MONGO_URI

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()  # test the connection
    db = client.get_default_database()
    print("✅ MongoDB connected successfully!")
except Exception as e:
    print("⚠️ MongoDB connection failed:", e)
    db = None
