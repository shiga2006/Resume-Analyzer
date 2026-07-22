# 📄 AI Resume Analyzer & RAG Feedback Platform

An enterprise AI platform for resume parsing, NLP skill extraction, job-role matching, ATS scoring, and RAG (Retrieval-Augmented Generation) contextual feedback.

![Stack](https://img.shields.io/badge/Stack-FastAPI%20|%20Streamlit%20|%20MongoDB%20|%20LLM%20|%20RAG-blue)

---

## 🌟 Key Features

1. **📄 Multi-Format Resume Parsing & NLP Segmentation**:
   - Extract raw text from PDF and DOCX files using `pdfplumber` and `python-docx`.
   - Parse contact info (Email, Phone, LinkedIn/GitHub links) via regex.
   - Categorize resume text into standard sections (Skills, Experience, Education, Projects).

2. **🧠 LLM & NLP Skill Extraction**:
   - Taxonomical skill extraction matching against 100+ technologies across 5 domains.
   - TF-IDF Cosine Similarity calculation between resume and target job description.
   - ATS structural readability audit (section completeness, word count, contact details).

3. **🚀 RAG (Retrieval-Augmented Generation) Engine**:
   - Vector Store indexing ATS benchmark guidelines and Google XYZ impact bullet formulas.
   - Top-k vector retrieval matching candidate skill gaps.
   - Augmented generation providing hyper-personalized feedback and before/after bullet rewrites.

4. **⚡ FastAPI REST Services**:
   - High-performance asynchronous backend built with FastAPI, Pydantic validation, and Uvicorn.
   - OpenAPI Swagger documentation available out-of-the-box at `/docs`.

5. **🍃 MongoDB Persistence**:
   - Store parsed resumes, ATS evaluation records, skill match metrics, and historical logs.
   - Automatic zero-downtime fallback store when database daemon is offline.

6. **📊 Streamlit UI Dashboard**:
   - Interactive UI tabs for ATS Analysis, RAG Contextual Feedback, NLP Entity Parser, and MongoDB History.

---

## 🛠️ Project Structure

```
Resume analyzer/
├── backend/
│   ├── main.py                # FastAPI Application & OpenAPI Docs
│   ├── app.py                 # Runner Entry point
│   ├── config.py              # MongoDB & Environment Configs
│   ├── requirements.txt       # Dependencies
│   ├── routes/
│   │   ├── auth.py            # Authentication Endpoints
│   │   └── resume.py          # Analyze, Parse, RAG, and History Endpoints
│   └── services/
│       ├── parser_service.py  # PDF/DOCX Parsing & Text Extraction
│       ├── nlp_service.py     # Skill Taxonomy & Cosine Similarity
│       ├── rag_service.py     # Vector Store & RAG Retrieval Engine
│       └── gemini_service.py  # Google GenAI LLM Integration
├── frontend/
│   └── streamlit_app.py       # Streamlit UI Dashboard
├── INTERVIEW_GUIDE.md         # Detailed Working Mechanics & Study Guide
└── README.md                  # Project Documentation
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Configure Environment Variables (Optional)
Create a `.env` file in the `backend/` directory:
```env
MONGO_URI=mongodb://localhost:27017/
DB_NAME=resume_analyzer_db
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 3. Run FastAPI Backend
```bash
cd backend
python main.py
```
*Open API docs at [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs)*

### 4. Run Streamlit Frontend
```bash
streamlit run frontend/streamlit_app.py
```
*Access UI dashboard at [http://localhost:8501](http://localhost:8501)*

---

## 🎓 Interview Study Guide

For a complete breakdown of the data lifecycle, vector search mathematics, LLM prompts, and top 15 interview questions with answers, see [INTERVIEW_GUIDE.md](file:///c:/Users/DELL-7420/OneDrive/Desktop/DataPlan/Resume%20analyzer/INTERVIEW_GUIDE.md).
