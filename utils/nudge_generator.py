def generate_nudges(emotion, wellbeing=None):
    nudges_dict = {
        "happy": ["Celebrate the moment!", "Share your joy with someone."],
        "sad": ["Try journaling feelings.", "Take a walk or call a friend."],
        "angry": ["Take deep breaths.", "Distract with something calming."],
        "fear": ["Practice grounding techniques.", "Talk to someone you trust."],
        "neutral": ["Keep reflecting.", "Maintain your positive habits."]
    }

    default = ["Take a mindful pause.", "Check in with yourself today."]
    nudges = nudges_dict.get(emotion.lower(), default)

    if wellbeing == "At Risk":
        nudges.append("Consider talking to a counselor.")
    elif wellbeing == "Stable":
        nudges.append("Keep up the good routine!")

    return nudges
