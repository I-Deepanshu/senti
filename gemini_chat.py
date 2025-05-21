import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=API_KEY)

def chat_with_gemini(prompt, history=[]):
    model = genai.GenerativeModel('gemini-2.0-flash')
    chat = model.start_chat(history=history)
    response = chat.send_message(prompt)
    return response.text
