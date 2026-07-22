import re
from typing import List, Dict, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Comprehensive Tech & Soft Skills Taxonomy Database
SKILL_TAXONOMY = {
    "languages": {
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "golang", "rust",
        "ruby", "php", "swift", "kotlin", "r", "sql", "html", "css", "bash", "shell"
    },
    "frameworks": {
        "react", "react.js", "next.js", "vue", "vue.js", "angular", "node.js", "express",
        "fastapi", "flask", "django", "spring boot", "dot net", ".net", "laravel", "tailwind"
    },
    "ai_ml_data": {
        "machine learning", "deep learning", "nlp", "natural language processing", "llm",
        "llms", "rag", "retrieval-augmented generation", "transformers", "pytorch",
        "tensorflow", "keras", "scikit-learn", "pandas", "numpy", "opencv", "spacy",
        "langchain", "llama-index", "huggingface", "vector search", "faiss", "chromadb"
    },
    "databases_cloud": {
        "mongodb", "postgresql", "postgres", "mysql", "sqlite", "redis", "dynamodb",
        "elasticsearch", "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
        "terraform", "git", "github", "gitlab", "ci/cd", "kafka", "rabbitmq"
    },
    "soft_skills": {
        "communication", "leadership", "problem solving", "teamwork", "collaboration",
        "agile", "scrum", "time management", "critical thinking", "adaptability",
        "project management", "analytical skills"
    }
}

ALL_SKILLS = set()
for category_skills in SKILL_TAXONOMY.values():
    ALL_SKILLS.update(category_skills)


class NLPService:
    """NLP parsing engine for skill extraction, TF-IDF similarity, and ATS readability analytics."""

    @staticmethod
    def extract_skills(text: str) -> Dict[str, List[str]]:
        text_lower = text.lower()
        extracted_by_category = {}
        all_extracted = set()

        for category, skill_set in SKILL_TAXONOMY.items():
            found = []
            for skill in skill_set:
                # Word boundary search to avoid false substrings (e.g., 'c' inside 'cat')
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text_lower):
                    found.append(skill.title())
                    all_extracted.add(skill.lower())
            extracted_by_category[category] = found

        return {
            "by_category": extracted_by_category,
            "all_skills": sorted(list({s.title() for s in all_extracted}))
        }

    @staticmethod
    def calculate_tfidf_similarity(resume_text: str, job_description: str) -> float:
        """Calculate TF-IDF Cosine Similarity score between 0.0 and 100.0."""
        if not resume_text.strip() or not job_description.strip():
            return 0.0

        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        try:
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return round(float(similarity) * 100, 2)
        except Exception:
            return 0.0

    @staticmethod
    def evaluate_ats_structure(parsed_resume: dict) -> Dict:
        """Evaluate structural readiness of the resume for ATS parsers."""
        sections = parsed_resume.get("sections", {})
        contact = parsed_resume.get("contact_info", {})
        word_count = parsed_resume.get("word_count", 0)

        score = 0
        checks = []

        # Check contact info
        if contact.get("email"):
            score += 15
            checks.append({"item": "Email Address", "status": "Passed"})
        else:
            checks.append({"item": "Email Address", "status": "Missing"})

        if contact.get("phone"):
            score += 10
            checks.append({"item": "Phone Number", "status": "Passed"})
        else:
            checks.append({"item": "Phone Number", "status": "Missing"})

        # Check vital sections
        vital_sections = ["skills", "experience", "education", "projects"]
        for sec in vital_sections:
            if sec in sections and len(sections[sec]) > 20:
                score += 15
                checks.append({"item": f"{sec.title()} Section", "status": "Passed"})
            else:
                checks.append({"item": f"{sec.title()} Section", "status": "Missing/Weak"})

        # Check word length (300 to 1200 words is optimal)
        if 300 <= word_count <= 1200:
            score += 15
            checks.append({"item": f"Word Count ({word_count} words)", "status": "Optimal Length"})
        else:
            score += 5
            checks.append({"item": f"Word Count ({word_count} words)", "status": "Too short or wordy"})

        return {
            "ats_readability_score": min(score, 100),
            "audit_checks": checks
        }

    @classmethod
    def match_job_role(cls, resume_text: str, job_description: str) -> Dict:
        """Determine matched skills, missing skills, and TF-IDF alignment."""
        resume_skills_set = set([s.lower() for s in cls.extract_skills(resume_text)["all_skills"]])
        jd_skills_set = set([s.lower() for s in cls.extract_skills(job_description)["all_skills"]])

        matched = sorted(list(resume_skills_set.intersection(jd_skills_set)))
        missing = sorted(list(jd_skills_set.difference(resume_skills_set)))

        skill_match_percentage = (
            round((len(matched) / len(jd_skills_set)) * 100, 2) if jd_skills_set else 100.0
        )
        tfidf_similarity = cls.calculate_tfidf_similarity(resume_text, job_description)

        # Composite match score: 60% skill overlap + 40% TF-IDF contextual similarity
        composite_score = round((skill_match_percentage * 0.6) + (tfidf_similarity * 0.4), 2)

        return {
            "composite_score": composite_score,
            "skill_match_percentage": skill_match_percentage,
            "tfidf_similarity": tfidf_similarity,
            "matched_skills": [s.title() for s in matched],
            "missing_skills": [s.title() for s in missing],
            "jd_required_skills": [s.title() for s in sorted(list(jd_skills_set))]
        }
