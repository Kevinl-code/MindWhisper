import streamlit as st
import pandas as pd
import os
import datetime
from utils.predictor import analyze_text, compare_moods, predict_wellbeing
from utils.emotion_detector import detect_emotion_opencv
from utils.nudge_generator import generate_nudges
from utils.speech_feedback import speak_to_file
from utils.reader import extract_text_from_file

LOG_PATH = "logs/diary_log.csv"

st.set_page_config(page_title="MindWhisper", layout="wide")
st.title("🧠 MindWhisper")

# ------------------- Sidebar Navigation -------------------
pages = [
    "📓 Routine Diary Analysis",
    "📷 Emotion Detection",
    "📊 Well-being Prediction",
    "💡 CBT Nudge Generator",
    "📈 Summary Dashboard"
]

if "current_page" not in st.session_state:
    st.session_state.current_page = pages[0]

with st.sidebar:
    selected = st.selectbox("Navigate", pages, index=pages.index(st.session_state.current_page))
    if selected != st.session_state.current_page:
        st.session_state.current_page = selected
        st.rerun()

# ------------------- Load Log -------------------
if not os.path.exists(LOG_PATH):
    df = pd.DataFrame(columns=["date", "entry", "text_emotion", "face_emotion", "wellbeing"])
    df.to_csv(LOG_PATH, index=False)
else:
    df = pd.read_csv(LOG_PATH)

# ------------------- Routine Diary Analysis -------------------
if st.session_state.current_page == "📓 Routine Diary Analysis":
    st.header("📓 Upload Your Diary File")

    uploaded_file = st.file_uploader("Upload .txt or .docx file", type=["txt", "docx"])
    if uploaded_file is not None:
        diary_text = extract_text_from_file(uploaded_file)
        st.text_area("Extracted Text", diary_text, height=200)

        if st.button("🧠 Analyze Mood"):
            text_emotion = analyze_text(diary_text)
            st.success(f"Detected Text Emotion: {text_emotion}")
            audio_path = speak_to_file(f"Your text mood is {text_emotion}")
            st.audio(audio_path)

            st.session_state['diary_text'] = diary_text
            st.session_state['text_emotion'] = text_emotion
            st.session_state.current_page = "📷 Emotion Detection"
            st.rerun()

# ------------------- Emotion Detection -------------------
elif st.session_state.current_page == "📷 Emotion Detection":
    st.header("📷 Real-Time Emotion Detection")

    if st.button("📸 Start Face Emotion Detection"):
        face_emotion = detect_emotion_opencv(duration=10)
        st.session_state['face_emotion'] = face_emotion
        st.success(f"Detected Face Emotion: {face_emotion}")
        audio_path = speak_to_file(f"Your face mood is {face_emotion}")
        st.audio(audio_path)
        st.session_state.current_page = "📊 Well-being Prediction"
        st.rerun()

# ------------------- Well-being Prediction -------------------
elif st.session_state.current_page == "📊 Well-being Prediction":
    st.header("📊 Predict Your Mental Well-being")

    diary_text = st.session_state.get("diary_text", "")
    text_emotion = st.session_state.get("text_emotion", "")
    face_emotion = st.session_state.get("face_emotion", "")

    if diary_text and text_emotion and face_emotion:
        wellbeing_status = predict_wellbeing(diary_text, text_emotion, face_emotion)
        st.session_state['wellbeing'] = wellbeing_status
        st.success(f"🧬 Predicted Well-being: {wellbeing_status}")
        audio_path = speak_to_file(f"Your predicted mental well-being is {wellbeing_status}")
        st.audio(audio_path)
        st.session_state.current_page = "💡 CBT Nudge Generator"
        st.rerun()
    else:
        st.warning("Missing diary or emotion data.")

# ------------------- CBT Nudge Generator -------------------
elif st.session_state.current_page == "💡 CBT Nudge Generator":
    st.header("💡 Personalized CBT Nudges")

    diary_text = st.session_state.get("diary_text", "")
    text_emotion = st.session_state.get("text_emotion", "")
    face_emotion = st.session_state.get("face_emotion", "")
    wellbeing_status = st.session_state.get("wellbeing", "")

    if face_emotion and wellbeing_status:
        nudges = generate_nudges(face_emotion, wellbeing_status)
        st.subheader("Suggestions for You:")
        for nudge in nudges:
            st.markdown(f"👉 {nudge}")
            audio_path = speak_to_file(nudge)
            st.audio(audio_path)

        # Log it
        log_entry = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "entry": diary_text,
            "text_emotion": text_emotion,
            "face_emotion": face_emotion,
            "wellbeing": wellbeing_status
        }
        df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
        df.to_csv(LOG_PATH, index=False)
        st.success("📝 Session logged successfully!")
    else:
        st.warning("No emotion data available.")

# ------------------- Summary Dashboard -------------------
elif st.session_state.current_page == "📈 Summary Dashboard":
    st.header("📈 MindWhisper Summary Dashboard")
    if df.empty:
        st.info("No logs available yet.")
    else:
        st.dataframe(df[::-1])
        st.metric("Total Entries", len(df))
        st.metric("Most Common Text Mood", df["text_emotion"].mode()[0])
        st.metric("Most Common Face Mood", df["face_emotion"].mode()[0])
        st.metric("Most Common Well-being", df["wellbeing"].mode()[0])
        st.bar_chart(df["text_emotion"].value_counts())
