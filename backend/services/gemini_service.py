import json
from google import genai
from config import GEMINI_API_KEY


class GeminiService:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def analyze_resume(
            self,
            resume_text,
            job_description
    ):

        prompt = f"""
You are an expert ATS Resume Analyzer.

Analyze the resume against the given Job Description.

Return ONLY valid JSON.

Required JSON Format:

{{
    "ats_score": 0,
    "matched_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "recommendations": []
}}

SCORING RULES:
- ATS score must be between 0 and 100.
- Compare technical skills.
- Compare tools and technologies.
- Compare experience relevance.
- Identify missing requirements.
- Give actionable recommendations.

JOB DESCRIPTION:

{job_description}

RESUME:

{resume_text}
"""

        try:

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            result = response.text.strip()

            result = result.replace(
                "```json",
                ""
            )

            result = result.replace(
                "```",
                ""
            )

            parsed = json.loads(result)

            return parsed

        except Exception as e:

            return {
                "ats_score": 0,
                "matched_skills": [],
                "missing_skills": [],
                "strengths": [],
                "weaknesses": [],
                "recommendations": [],
                "error": str(e)
            }

    def generate_interview_questions(
            self,
            resume_text,
            job_description
    ):

        prompt = f"""
Based on the resume and job description,
generate 10 interview questions.

Return ONLY JSON.

{{
    "questions": []
}}

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}
"""

        try:

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            result = response.text.strip()

            result = result.replace(
                "```json",
                ""
            )

            result = result.replace(
                "```",
                ""
            )

            return json.loads(result)

        except Exception as e:

            return {
                "questions": [],
                "error": str(e)
            }