import cv2
from deepface import DeepFace
import streamlit as st
import time
from streamlit.components.v1 import html

def detect_emotion_opencv(duration=10):
    stframe = st.empty()
    status = st.empty()
    timer_text = st.empty()
    breathing_anim = st.empty()

    cap = cv2.VideoCapture(0)
    detected_emotion = None
    start_time = time.time()
    

    # Add simple CSS animation for breathing
    breathing_anim.html(
    """
    <div style="
        margin-top: 20px;
        width: 150px;
        height: 150px;
        background: #aadffd;
        border-radius: 50%;
        animation: pulse 3s ease-in-out infinite;
        margin-left: auto;
        margin-right: auto;
    "></div>
    <style>
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.3); }
        100% { transform: scale(1); }
    }
    </style>
    """)

    # Optional: play gentle background audio (looping)
    html("""
    <audio autoplay loop>
      <source src="..." type="audio/mpeg">
    </audio>
        """)


    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        elapsed = time.time() - start_time
        remaining = duration - int(elapsed)
        timer_text.markdown(f"⏳ Detecting... Auto-stop in: **{remaining}** seconds")

        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            if result and isinstance(result, list) and 'dominant_emotion' in result[0]:
                detected_emotion = result[0]['dominant_emotion']
                label = f"Detected: {detected_emotion}"
            else:
                label = "No face detected"
        except:
            label = "No face detected"


        cv2.putText(frame, label, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        stframe.image(frame, channels="BGR")
        status.info(label)

        if elapsed >= duration:
            break

        time.sleep(0.3)

    cap.release()
    cv2.destroyAllWindows()
    return detected_emotion or "No face detected"
