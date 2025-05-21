import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["mental_health_ai"]
chats = db["chat_history"]

def save_chat(username, user_input, bot_response, mood):
    chat_doc = {
        "username": username,
        "timestamp": datetime.utcnow(),
        "user_input": user_input,
        "bot_response": bot_response,
        "mood": mood
    }
    chats.insert_one(chat_doc)

def get_user_chats(username):
    return list(chats.find({"username": username}).sort("timestamp", -1))

def export_user_chats_to_csv(username, filename="chat_export.csv"):
    user_chats = get_user_chats(username)
    df = pd.DataFrame(user_chats)
    df.drop(columns=["_id"], inplace=True, errors='ignore')
    df.to_csv(filename, index=False)
    return filename
