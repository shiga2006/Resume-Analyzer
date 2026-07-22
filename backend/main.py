from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import auth_router
from routes.resume import resume_router
import uvicorn

app = FastAPI(
    title="AI Resume Analyzer API",
    description="Enterprise REST API for Resume Parsing, NLP Skill Extraction, ATS Scoring, RAG Contextual Feedback, and MongoDB Storage.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for Streamlit frontend and local clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router)
app.include_router(resume_router)


@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "AI Resume Analyzer FastAPI Engine",
        "version": "2.0.0",
        "documentation": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
