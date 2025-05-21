import streamlit as st
from auth import create_user, authenticate_user
from db import save_chat, get_user_chats, export_user_chats_to_csv
from mood_detector import detect_mood
import google.generativeai as genai
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

# --- Session states
# Session states initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "page" not in st.session_state:
    st.session_state.page = "login"
import re  # Add this at the top of your file

# Email validation function
def is_valid_email(email):
    # Only allow gmail.com addresses
    pattern = r"^[\w\.-]+@gmail\.com$"
    return re.match(pattern, email)
# Login/Register UI
def login_ui():
    st.title("🧠 AI Mental Health Companion")
    st.subheader("🔐 Login or Register")
    choice = st.radio("Choose an action:", ["Login", "Register"])
    username = st.text_input("Email (must end with @gmail.com)")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        if not is_valid_email(username):
            st.error("❌ Please enter a valid Gmail address (e.g., yourname@gmail.com)")
            return

        if choice == "Register":
            if create_user(username, password):
                st.success("✅ Registered successfully. Please log in.")
            else:
                st.error("❌ Username already exists.")
        else:
            if authenticate_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.page = "chat"
                st.rerun()
            else:
                st.error("❌ Invalid credentials.")

# Main App Logic
if st.session_state.page == "login":
    login_ui()
    st.stop()

# ---- Chat Page ----
st.title(f"🧠 Mental Health Chat – {st.session_state.username}")
user_input = st.text_area("What's on your mind?")

if st.button("Send"):
    mood = detect_mood(user_input)
    st.success(f"Detected Mood: {mood}")
    response = model.generate_content(user_input).text
    st.markdown("### 🤖 AI Response:")
    st.write(response)
    save_chat(st.session_state.username, user_input, response, mood)

# ---- History Section ----
st.subheader("🕓 Chat History")
if st.checkbox("Show Past Chats"):
    history = get_user_chats(st.session_state.username)
    for h in history[:5]:
        st.markdown(f"**🕒 {h['timestamp']}**")
        st.markdown(f"**You:** {h['user_input']}")
        st.markdown(f"**AI:** {h['bot_response']}")
        st.markdown(f"**Mood:** {h['mood']}")
        st.markdown("---")

# ---- Mood Analytics ----
st.subheader("📊 Mood Analytics")
if st.checkbox("Show Mood Chart"):
    df = pd.DataFrame(get_user_chats(st.session_state.username))
    if not df.empty:
        mood_counts = df["mood"].value_counts()
        st.bar_chart(mood_counts)
    else:
        st.info("No data yet.")

# ---- CSV Export ----
st.subheader("📁 Export Chat History")
if st.button("Export as CSV"):
    path = export_user_chats_to_csv(st.session_state.username)
    with open(path, "rb") as f:
        st.download_button("📥 Download", f, file_name="chat_history.csv")

# 🔓 Logout Button
if st.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.page = "login"
    st.rerun()
