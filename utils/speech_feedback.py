import pyttsx3
import os

def speak_to_file(text, output_file="voice_output.mp3"):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    return output_file
