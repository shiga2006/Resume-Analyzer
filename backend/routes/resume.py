from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import datetime
import uuid

from services.parser_service import ResumeParser
from services.nlp_service import NLPService
from services.rag_service import RAGService
from services.gemini_service import GeminiService
from config import resume_collection

resume_router = APIRouter(prefix="", tags=["Resume Analysis"])

nlp_service = NLPService()
rag_service = RAGService()
gemini_service = GeminiService()


@resume_router.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    try:
        content = await file.read()
        parsed_data = ResumeParser.parse_file(content, file.filename)
        extracted_skills = nlp_service.extract_skills(parsed_data["raw_text"])
        ats_structure = nlp_service.evaluate_ats_structure(parsed_data)

        return {
            "success": True,
            "filename": file.filename,
            "word_count": parsed_data["word_count"],
            "contact_info": parsed_data["contact_info"],
            "sections": parsed_data["sections"],
            "skills": extracted_skills["all_skills"],
            "skills_by_category": extracted_skills["by_category"],
            "ats_readability": ats_structure
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@resume_router.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    user_id: Optional[str] = Form("guest")
):
    try:
        content = await resume.read()
        parsed_data = ResumeParser.parse_file(content, resume.filename)
        resume_text = parsed_data["raw_text"]

        # Step 1: Deterministic NLP Job Role & Skill Matching
        nlp_results = nlp_service.match_job_role(resume_text, job_description)
        ats_structure = nlp_service.evaluate_ats_structure(parsed_data)

        # Step 2: LLM Deep Analysis via Gemini (with NLP fallback)
        gemini_response = gemini_service.analyze_resume(resume_text, job_description)

        if "error" not in gemini_response and "ats_score" in gemini_response:
            final_ats_score = int(gemini_response["ats_score"])
            matched_skills = gemini_response.get("matched_skills", nlp_results["matched_skills"])
            missing_skills = gemini_response.get("missing_skills", nlp_results["missing_skills"])
            strengths = gemini_response.get("strengths", [])
            weaknesses = gemini_response.get("weaknesses", [])
            recommendations = gemini_response.get("recommendations", [])
        else:
            # Fallback to NLP engine composite score
            final_ats_score = int(nlp_results["composite_score"])
            matched_skills = nlp_results["matched_skills"]
            missing_skills = nlp_results["missing_skills"]
            strengths = [
                f"Matched {len(matched_skills)} core technical skills required by the JD.",
                f"Resume structure score: {ats_structure['ats_readability_score']}/100."
            ]
            weaknesses = [
                f"Missing {len(missing_skills)} target keywords from job description.",
                "Ensure bullet points follow metric-driven impact format."
            ]
            recommendations = [
                f"Incorporate missing key technical skills: {', '.join(missing_skills[:5])}.",
                "Quantify project achievements with percentages and throughput numbers."
            ]

        # Step 3: Trigger RAG Retrieval Engine for Contextual Feedback
        rag_feedback = rag_service.generate_contextual_feedback(
            resume_text=resume_text,
            job_description=job_description,
            missing_skills=missing_skills,
            llm_service=gemini_service if gemini_service.client else None
        )

        analysis_id = str(uuid.uuid4())
        record = {
            "_id": analysis_id,
            "user_id": user_id,
            "filename": resume.filename,
            "ats_score": final_ats_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "rag_suggestions": rag_feedback.get("personalized_suggestions", []),
            "bullet_rewrites": rag_feedback.get("bullet_rewrites", []),
            "created_at": datetime.datetime.utcnow().isoformat()
        }

        # Store in MongoDB database
        resume_collection.insert_one(record)

        return {
            "success": True,
            "analysis_id": analysis_id,
            "ats_score": final_ats_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "rag_feedback": rag_feedback,
            "contact_info": parsed_data["contact_info"],
            "ats_structure": ats_structure
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


@resume_router.post("/rag-feedback")
async def get_rag_feedback(
    resume_text: str = Form(...),
    job_description: str = Form(...),
    missing_skills: str = Form("")
):
    try:
        missing_list = [s.strip() for s in missing_skills.split(",") if s.strip()]
        rag_feedback = rag_service.generate_contextual_feedback(
            resume_text=resume_text,
            job_description=job_description,
            missing_skills=missing_list,
            llm_service=gemini_service if gemini_service.client else None
        )
        return {"success": True, "rag_feedback": rag_feedback}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@resume_router.get("/history/{user_id}")
def get_history(user_id: str):
    try:
        records = resume_collection.find({"user_id": user_id})
        history = []
        for r in records:
            history.append({
                "id": str(r.get("_id")),
                "filename": r.get("filename", "Resume"),
                "ats_score": r.get("ats_score", 0),
                "matched_skills_count": len(r.get("matched_skills", [])),
                "missing_skills_count": len(r.get("missing_skills", [])),
                "date": r.get("created_at", "")[:10]
            })
        return {"success": True, "history": history}
    except Exception as e:
        return {"success": False, "message": str(e), "history": []}