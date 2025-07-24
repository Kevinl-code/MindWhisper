from textblob import TextBlob

def analyze_text(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.5:
        return "happy"
    elif polarity > 0:
        return "neutral"
    elif polarity < -0.3:
        return "sad"
    else:
        return "neutral"

def compare_moods(text_emotion, face_emotion):
    if text_emotion == face_emotion:
        return "✅ Your expressed and visible mood match."
    else:
        return "⚠️ There's a mismatch between your written and visible emotion."

def predict_wellbeing(text, text_emotion, face_emotion):
    if text_emotion == face_emotion and text_emotion in ["happy", "neutral"]:
        return "Stable"
    elif text_emotion != face_emotion:
        return "Inconsistent"
    else:
        return "At Risk"
