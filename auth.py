from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["mental_health_ai"]
users = db["users"]

def create_user(username, password):
    if users.find_one({"username": username}):
        return False  # user already exists
    users.insert_one({"username": username, "password": password})
    return True

def authenticate_user(username, password):
    user = users.find_one({"username": username, "password": password})
    return user is not None
