from nltk.sentiment.vader import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def detect_mood(text):
    if "sad" in text or "depressed" in text:
        return "Sad"
    elif "happy" in text or "good" in text:
        return "Happy"
    elif "angry" in text:
        return "Angry"
    else:
        return "Neutral"
