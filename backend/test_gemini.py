from services.gemini_service import GeminiService

gemini = GeminiService()

resume = """
Python Developer

Skills:
Python
Flask
MongoDB
Machine Learning
"""

jd = """
Looking for Python Developer.

Requirements:
Python
Flask
Docker
AWS
MongoDB
"""

result = gemini.analyze_resume(
    resume,
    jd
)

print(result)