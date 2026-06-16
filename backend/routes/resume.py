from flask import Blueprint, request, jsonify
from config import resume_collection
from services.parser_service import ResumeParser
from services.gemini_service import GeminiService
from datetime import datetime


resume_bp = Blueprint(
    "resume",
    __name__
)

gemini_service = GeminiService()


@resume_bp.route(
    "/analyze",
    methods=["POST"]
)
def analyze_resume():

    try:

        if "resume" not in request.files:

            return jsonify({
                "success": False,
                "message": "Resume file missing"
            }), 400

        file = request.files["resume"]

        if file.filename == "":

            return jsonify({
                "success": False,
                "message": "No file selected"
            }), 400

        user_id = request.form.get(
            "user_id",
            ""
        )

        job_description = request.form.get(
            "job_description",
            ""
        )

        if not job_description:

            return jsonify({
                "success": False,
                "message": "Job Description required"
            }), 400

        resume_text = ResumeParser.extract_text(
            file
        )

        analysis = gemini_service.analyze_resume(
            resume_text,
            job_description
        )

        document = {

            "user_id": user_id,

            "filename": file.filename,

            "resume_text": resume_text,

            "job_description": job_description,

            "ats_score": analysis.get(
                "ats_score",
                0
            ),

            "matched_skills": analysis.get(
                "matched_skills",
                []
            ),

            "missing_skills": analysis.get(
                "missing_skills",
                []
            ),

            "strengths": analysis.get(
                "strengths",
                []
            ),

            "weaknesses": analysis.get(
                "weaknesses",
                []
            ),

            "recommendations": analysis.get(
                "recommendations",
                []
            ),

            "created_at": datetime.utcnow()
        }

        result = resume_collection.insert_one(
            document
        )

        return jsonify({

            "success": True,

            "analysis_id": str(
                result.inserted_id
            ),

            "filename": file.filename,

            "ats_score": analysis.get(
                "ats_score",
                0
            ),

            "matched_skills": analysis.get(
                "matched_skills",
                []
            ),

            "missing_skills": analysis.get(
                "missing_skills",
                []
            ),

            "strengths": analysis.get(
                "strengths",
                []
            ),

            "weaknesses": analysis.get(
                "weaknesses",
                []
            ),

            "recommendations": analysis.get(
                "recommendations",
                []
            )
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500