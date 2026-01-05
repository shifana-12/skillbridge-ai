import google.generativeai as genai
from django.conf import settings
import json
import re

genai.configure(api_key=settings.GEMINI_API_KEY)

# ✅ USE STABLE MODEL
model = genai.GenerativeModel("gemini-pro")


def analyze_resume(resume_text, role):
    prompt = f"""
You are an AI Skill Gap Analyzer.

Return ONLY valid JSON.
No explanation.
No markdown.

JSON FORMAT (STRICT):

{{
  "skill_match_percentage": number,
  "matched_skills": [string],
  "missing_skills": [string],
  "roadmap": [
    {{
      "level": "Beginner | Intermediate | Advanced",
      "skills": [string],
      "estimated_hours": number,
      "priority": "High | Medium | Low"
    }}
  ]
}}

Resume:
{resume_text}

Target Role:
{role}
"""

    response = model.generate_content(prompt)

    raw = response.text.strip()
    raw = re.sub(r"```json|```", "", raw).strip()

    try:
        return json.loads(raw)
    except Exception:
        return {
            "error": "Gemini returned invalid JSON",
            "raw_response": raw
        }
