import json
import os
from google import genai
from config import GEMINI_API_KEY


class GeminiService:
    """LLM Service utilizing Google GenAI SDK for ATS parsing, scoring, and RAG contextual generation."""

    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Gemini Client Init Warning: {e}")

    def analyze_resume(self, resume_text: str, job_description: str) -> dict:
        if not self.client:
            return {"error": "GEMINI_API_KEY not configured. Using NLP Engine fallback."}

        prompt = f"""
You are an enterprise-grade ATS (Applicant Tracking System) Resume Evaluator and Senior Technical Recruiter.

Analyze the given Candidate Resume against the Job Description.

Return ONLY valid JSON matching this schema:
{{
    "ats_score": 85,
    "matched_skills": ["Python", "FastAPI", "MongoDB"],
    "missing_skills": ["Docker", "Kubernetes"],
    "strengths": ["Strong background in building scalable REST APIs", "Demonstrated ML expertise"],
    "weaknesses": ["Lack of cloud deployment metrics", "Missing CI/CD toolchain"],
    "recommendations": ["Add metric-driven results to backend project bullets", "Highlight Docker containerization experience"]
}}

SCORING RULES:
- ats_score must be an integer between 0 and 100 based on technical skill match, domain relevance, experience, and clarity.
- Compare hard skills, soft skills, tools, frameworks, and job duties.

JOB DESCRIPTION:
{job_description}

CANDIDATE RESUME:
{resume_text}
"""
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            raw = response.text.strip()
            clean_json = raw.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except Exception as e:
            return {"error": f"Gemini API Error: {str(e)}"}

    def generate_rag_suggestions(self, resume_text: str, job_description: str, retrieved_context: str) -> dict:
        if not self.client:
            return {"error": "GEMINI_API_KEY not configured."}

        prompt = f"""
You are an expert AI Resume Coach. Using the RETRIEVED BENCHMARK GUIDELINES below, generate hyper-personalized resume feedback and high-impact bullet point rewrites for the candidate.

RETRIEVED BENCHMARK GUIDELINES:
{retrieved_context}

JOB DESCRIPTION:
{job_description}

CANDIDATE RESUME:
{resume_text}

Return ONLY valid JSON with this format:
{{
    "suggestions": [
        {{
            "category": "bullet_formula",
            "title": "Quantify API Performance",
            "recommendation": "Rewrite your experience bullet using the XYZ formula: Accomplished [X] as measured by [Y] by doing [Z]."
        }}
    ],
    "bullet_rewrites": [
        {{
            "original": "Worked on backend APIs",
            "improved": "Engineered 12+ RESTful microservices in FastAPI with 99.9% uptime, reducing endpoint response times by 35%."
        }}
    ]
}}
"""
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            raw = response.text.strip()
            clean_json = raw.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except Exception as e:
            return {"error": f"Gemini RAG API Error: {str(e)}"}