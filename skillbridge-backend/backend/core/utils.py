import google.generativeai as genai
from django.conf import settings


# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

# ✅ CORRECT MODEL (WORKING)
model = genai.GenerativeModel("models/gemini-1.0-pro")


def analyze_resume(resume_text, job_role):
    prompt = f"""
You are an AI career assistant.

Resume Text:
{resume_text}

Target Job Role:
{job_role}

Tasks:
1. Extract technical skills
2. Identify missing skills for the role
3. Give skill match percentage
4. Generate a learning roadmap

Respond ONLY in valid JSON with keys:
skill_match_percentage, matched_skills, missing_skills, roadmap
"""

    response = model.generate_content(prompt)

    return response.text
