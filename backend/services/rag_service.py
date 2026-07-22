import numpy as np
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Built-in Knowledge Base for RAG Retrieval (ATS Standards, Guidelines & Rewrites)
ATS_KNOWLEDGE_BASE = [
    {
        "id": "kb-001",
        "category": "bullet_formula",
        "title": "Google XYZ Bullet Point Formula",
        "content": "Structure every experience bullet using the Google XYZ formula: 'Accomplished [X], as measured by [Y], by doing [Z]'. Example: 'Optimized SQL query performance by 40%, reducing API latency from 250ms to 150ms through index optimization and Redis caching.'"
    },
    {
        "id": "kb-002",
        "category": "skill_gap",
        "title": "Addressing Missing Technical Skills",
        "content": "If you lack a required technology mentioned in the Job Description, highlight related foundational frameworks or recent hands-on projects. Demonstrate transferrable concepts like REST APIs, microservices, cloud deployments, or database optimization."
    },
    {
        "id": "kb-003",
        "category": "metrics",
        "title": "Quantifying Impact with Metrics",
        "content": "Resumes with quantifiable achievements receive 40% higher ATS parser prioritization. Always include metrics such as percentage performance gains, throughput improvements, user acquisition counts, percentage reduction in bugs, or system uptime."
    },
    {
        "id": "kb-004",
        "category": "action_verbs",
        "title": "Strong Technical Action Verbs",
        "content": "Replace passive language ('was responsible for', 'worked on') with impactful action verbs: Engineered, Architected, Spearheaded, Implemented, Deployed, Streamlined, Orchestrated, Automated, and Refactored."
    },
    {
        "id": "kb-005",
        "category": "formatting",
        "title": "ATS Parsing Readability & Clean Layout",
        "content": "Avoid multi-column tables, graphics, text boxes, or non-standard fonts that corrupt ATS parsers. Use standard section titles: Technical Skills, Work Experience, Projects, Education, Certifications."
    },
    {
        "id": "kb-006",
        "category": "rag_llm",
        "title": "Contextual Alignment for Job Roles",
        "content": "Mirror exact keywords and technical terminology from the Job Description in your Summary and Skills sections. Ensure acronyms are spelled out alongside their short form (e.g., Natural Language Processing (NLP), Retrieval-Augmented Generation (RAG))."
    }
]


class RAGVectorStore:
    """In-memory Vector Retrieval Store using TF-IDF Embeddings & Cosine Similarity."""

    def __init__(self, knowledge_base: List[Dict]):
        self.kb = knowledge_base
        self.corpus = [item["content"] for item in knowledge_base]
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        if self.corpus:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve top_k most relevant knowledge base chunks matching query vector."""
        if not query.strip() or not self.corpus:
            return self.kb[:top_k]

        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]

        # Get indices of top_k similarity scores
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            item = dict(self.kb[idx])
            item["relevance_score"] = round(score, 4)
            results.append(item)

        return results


class RAGService:
    """RAG (Retrieval-Augmented Generation) Engine for contextual resume feedback."""

    def __init__(self):
        self.vector_store = RAGVectorStore(ATS_KNOWLEDGE_BASE)

    def generate_contextual_feedback(
        self,
        resume_text: str,
        job_description: str,
        missing_skills: List[str],
        llm_service=None
    ) -> Dict:
        """
        Step 1: Construct Query from resume gap analysis.
        Step 2: Retrieve top context chunks from Vector Store.
        Step 3: Augment prompt & Generate personalized feedback.
        """
        # Formulate query based on missing skills and JD requirement
        query = f"Missing skills: {', '.join(missing_skills)}. Target JD: {job_description[:300]}"
        retrieved_contexts = self.vector_store.retrieve(query, top_k=3)

        context_str = "\n".join([
            f"- [{c['title']}]: {c['content']}" for c in retrieved_contexts
        ])

        # If LLM service is available, pass augmented context to Gemini
        if llm_service and hasattr(llm_service, 'generate_rag_suggestions'):
            llm_suggestions = llm_service.generate_rag_suggestions(
                resume_text=resume_text,
                job_description=job_description,
                retrieved_context=context_str
            )
            return {
                "retrieved_context_chunks": retrieved_contexts,
                "personalized_suggestions": llm_suggestions.get("suggestions", []),
                "bullet_rewrites": llm_suggestions.get("bullet_rewrites", []),
                "rag_pipeline_status": "Success (LLM Augmented)"
            }

        # Dynamic Rule Engine fallback if LLM key is absent
        fallback_suggestions = []
        for c in retrieved_contexts:
            fallback_suggestions.append({
                "category": c["category"],
                "title": c["title"],
                "recommendation": f"Based on retrieved benchmark guideline '{c['title']}': {c['content']}"
            })

        if missing_skills:
            fallback_suggestions.append({
                "category": "skill_gap",
                "title": "Actionable Skill Gap Plan",
                "recommendation": f"Priority skills to incorporate into your Projects/Skills section: {', '.join(missing_skills[:4])}."
            })

        sample_rewrites = [
            {
                "original": "Worked on backend APIs and database.",
                "improved": "Engineered scalable REST APIs using FastAPI and MongoDB, improving payload throughput by 35%."
            },
            {
                "original": "Implemented machine learning models for classification.",
                "improved": "Developed and deployed LLM & NLP pipelines using PyTorch and Scikit-Learn, achieving an F1-score of 0.92."
            }
        ]

        return {
            "retrieved_context_chunks": retrieved_contexts,
            "personalized_suggestions": fallback_suggestions,
            "bullet_rewrites": sample_rewrites,
            "rag_pipeline_status": "Success (Deterministic Vector RAG)"
        }
