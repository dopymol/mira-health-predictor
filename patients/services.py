import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


def fallback_prediction(glucose, haemoglobin, cholesterol):
    if glucose > 180 and cholesterol > 240:
        return "High risk of diabetes and cardiovascular disease."
    elif glucose > 140:
        return "Elevated glucose level detected. Possible diabetes risk."
    elif haemoglobin < 12:
        return "Low haemoglobin detected. Possible anemia risk."
    elif cholesterol > 200:
        return "High cholesterol detected. Possible heart health risk."
    else:
        return "Health indicators appear within normal range."


def generate_health_remark(glucose, haemoglobin, cholesterol):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return fallback_prediction(glucose, haemoglobin, cholesterol)

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
        You are a healthcare AI assistant.
        Analyze these blood test values:

        Glucose: {glucose}
        Haemoglobin: {haemoglobin}
        Cholesterol: {cholesterol}

        Give one short disease-risk prediction.
        Do not give medicine advice.
        Keep it under 20 words.
        """

        response = model.generate_content(prompt)

        if response and response.text:
            return response.text.strip()

        return fallback_prediction(glucose, haemoglobin, cholesterol)

    except Exception:
        return fallback_prediction(glucose, haemoglobin, cholesterol)