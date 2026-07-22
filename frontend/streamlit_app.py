import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="AI Resume Analyzer & RAG Coach",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #6B7280;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #1E293B;
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid #334155;
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #38BDF8;
    }
    .badge-matched {
        background-color: #064E3B;
        color: #34D399;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 3px;
    }
    .badge-missing {
        background-color: #7F1D1D;
        color: #FCA5A5;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 3px;
    }
    .rag-box {
        background-color: #0F172A;
        border-left: 4px solid #8B5CF6;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "page" not in st.session_state:
    st.session_state.page = "dashboard"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = "guest"
if "username" not in st.session_state:
    st.session_state.username = "Guest User"
if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None


# Helper function to check API health
def check_api_health():
    try:
        r = requests.get(f"{API_URL}/health", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🤖 AI Resume Platform")
    st.caption("LLMs | NLP | RAG | FastAPI | MongoDB")
    st.divider()

    if st.session_state.logged_in:
        st.success(f"Logged in as: **{st.session_state.username}**")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_id = "guest"
            st.session_state.username = "Guest User"
            st.rerun()
    else:
        st.info("Operating in Guest Mode")
        col_side1, col_side2 = st.columns(2)
        with col_side1:
            if st.button("🔐 Login", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
        with col_side2:
            if st.button("📝 Signup", use_container_width=True):
                st.session_state.page = "signup"
                st.rerun()

    st.divider()
    nav_selection = st.radio(
        "Navigation",
        ["📊 ATS Analyzer & Match", "🧠 RAG Contextual Feedback", "🔍 NLP Resume Parser", "📜 MongoDB History"],
        index=0 if st.session_state.page == "dashboard" else 0
    )


# ---------------------------------------------------------
# AUTHENTICATION PAGES
# ---------------------------------------------------------
def login_page():
    st.markdown("<h2 class='main-header'>🔐 Account Login</h2>", unsafe_allow_html=True)
    with st.form("login_form"):
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign In")
        if submit:
            try:
                res = requests.post(f"{API_URL}/login", json={"email": email, "password": password})
                data = res.json()
                if data.get("success"):
                    st.session_state.logged_in = True
                    st.session_state.user_id = data["user"]["id"]
                    st.session_state.username = data["user"]["username"]
                    st.session_state.page = "dashboard"
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error(data.get("message", "Invalid credentials"))
            except Exception as e:
                st.error(f"Connection Error: {e}")

    if st.button("← Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()


def signup_page():
    st.markdown("<h2 class='main-header'>📝 Create Account</h2>", unsafe_allow_html=True)
    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Register")
        if submit:
            try:
                res = requests.post(f"{API_URL}/signup", json={"username": username, "email": email, "password": password})
                data = res.json()
                if data.get("success"):
                    st.success("Account created successfully! Please login.")
                else:
                    st.error(data.get("message", "Signup failed"))
            except Exception as e:
                st.error(f"Connection Error: {e}")

    if st.button("← Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()


# ---------------------------------------------------------
# TAB 1: ATS ANALYZER & JOB-ROLE MATCHING
# ---------------------------------------------------------
def render_ats_analyzer():
    st.markdown("<h1 class='main-header'>AI Resume Analyzer & ATS Evaluator</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Powered by LLM Scoring, NLP Skill Extraction, and Job-Role Alignment</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. Upload Candidate Resume")
        uploaded_file = st.file_uploader("Upload PDF or DOCX format", type=["pdf", "docx"])

    with col2:
        st.subheader("2. Target Job Description")
        jd_text = st.text_area("Paste target job requirements and qualifications...", height=180)

    if st.button("⚡ Run Full ATS & LLM Analysis", use_container_width=True, type="primary"):
        if not uploaded_file:
            st.error("Please upload a resume file first.")
            return
        if not jd_text.strip():
            st.error("Please paste a target job description.")
            return

        with st.spinner("Parsing text, extracting skills, and generating ATS evaluation..."):
            try:
                files = {"resume": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {
                    "job_description": jd_text,
                    "user_id": st.session_state.user_id
                }
                response = requests.post(f"{API_URL}/analyze", files=files, data=data)
                result = response.json()

                if result.get("success"):
                    st.session_state.last_analysis = result
                    st.success("Analysis complete!")
                else:
                    st.error(f"Analysis Error: {result.get('message')}")
            except Exception as e:
                st.error(f"API Connection Failed ({e}). Ensure FastAPI server is running on port 5000.")

    # Render Analysis Results if Available
    res = st.session_state.last_analysis
    if res:
        st.divider()
        st.subheader("📊 ATS Evaluation & Match Results")

        m1, m2, m3 = st.columns(3)
        with m1:
            score = res.get("ats_score", 0)
            score_color = "#34D399" if score >= 75 else ("#FBBF24" if score >= 50 else "#F87171")
            st.markdown(f"""
            <div class='metric-card'>
                <div style='color: #94A3B8; font-size: 0.9rem;'>COMPOSITE ATS SCORE</div>
                <div class='metric-value' style='color: {score_color};'>{score} / 100</div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            matched_count = len(res.get("matched_skills", []))
            st.markdown(f"""
            <div class='metric-card'>
                <div style='color: #94A3B8; font-size: 0.9rem;'>MATCHED TECHNICAL SKILLS</div>
                <div class='metric-value' style='color: #34D399;'>{matched_count}</div>
            </div>
            """, unsafe_allow_html=True)

        with m3:
            missing_count = len(res.get("missing_skills", []))
            st.markdown(f"""
            <div class='metric-card'>
                <div style='color: #94A3B8; font-size: 0.9rem;'>MISSING CRITICAL SKILLS</div>
                <div class='metric-value' style='color: #F87171;'>{missing_count}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("### ✅ Matched Keywords & Skills")
            matched_html = "".join([f"<span class='badge-matched'>{s}</span>" for s in res.get("matched_skills", [])])
            st.markdown(matched_html or "No skills matched.", unsafe_allow_html=True)

            st.markdown("### 💪 Candidate Strengths")
            for strength in res.get("strengths", []):
                st.info(f"• {strength}")

        with col_b:
            st.markdown("### ⚠️ Missing Required Skills")
            missing_html = "".join([f"<span class='badge-missing'>{s}</span>" for s in res.get("missing_skills", [])])
            st.markdown(missing_html or "No missing skills identified!", unsafe_allow_html=True)

            st.markdown("### 🎯 Areas for Improvement")
            for weakness in res.get("weaknesses", []):
                st.warning(f"• {weakness}")

        st.subheader("💡 Strategic Recommendations")
        for rec in res.get("recommendations", []):
            st.write(f"👉 **{rec}**")


# ---------------------------------------------------------
# TAB 2: RAG CONTEXTUAL FEEDBACK ENGINE
# ---------------------------------------------------------
def render_rag_feedback():
    st.markdown("<h1 class='main-header'>🧠 RAG Contextual Feedback Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Retrieval-Augmented Generation retrieving benchmark ATS guidelines & bullet rewrites</p>", unsafe_allow_html=True)

    res = st.session_state.last_analysis
    if not res:
        st.info("ℹ️ Please run an ATS analysis in the first tab to view RAG contextual recommendations.")
        return

    rag_data = res.get("rag_feedback", {})
    context_chunks = rag_data.get("retrieved_context_chunks", [])
    suggestions = res.get("rag_suggestions", [])
    bullet_rewrites = res.get("bullet_rewrites", [])

    st.subheader("1. Retrieved Knowledge Base Vector Chunks")
    st.caption("Top-k guidelines retrieved from vector store matching candidate's resume gaps:")

    for chunk in context_chunks:
        relevance = chunk.get("relevance_score", 1.0)
        st.markdown(f"""
        <div class='rag-box'>
            <div style='color: #A78BFA; font-weight: 700;'>📌 [{chunk.get('category').upper()}] {chunk.get('title')} (Vector Score: {relevance})</div>
            <div style='color: #E2E8F0; font-size: 0.95rem; margin-top: 4px;'>{chunk.get('content')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("2. Contextual Improvement Suggestions")
    for s in suggestions:
        title = s.get("title", "Recommendation")
        rec = s.get("recommendation", "")
        st.success(f"**{title}**: {rec}")

    st.divider()
    st.subheader("3. High-Impact Bullet Point Rewrites (Google XYZ Formula)")
    for rw in bullet_rewrites:
        col_orig, col_imp = st.columns(2)
        with col_orig:
            st.error(f"**Original Bullet:**\n\n{rw.get('original')}")
        with col_imp:
            st.success(f"**AI-Optimized Impact Bullet:**\n\n{rw.get('improved')}")


# ---------------------------------------------------------
# TAB 3: NLP PARSER & ENTITY EXTRACTOR
# ---------------------------------------------------------
def render_nlp_parser():
    st.markdown("<h1 class='main-header'>🔍 NLP Resume Parser & Skill Extractor</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Inspect text extraction, section segmentation, contact parsing, and skill taxonomies</p>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload PDF or DOCX to test NLP Parsing", type=["pdf", "docx"], key="nlp_uploader")
    if uploaded_file and st.button("Parse File"):
        with st.spinner("Running NLP parser..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                r = requests.post(f"{API_URL}/parse", files=files)
                data = r.json()

                if data.get("success"):
                    st.subheader("Contact Information")
                    st.json(data.get("contact_info", {}))

                    st.subheader("ATS Structural Readability Audit")
                    st.metric("Readability Score", f"{data['ats_readability']['ats_readability_score']}/100")
                    st.dataframe(pd.DataFrame(data['ats_readability']['audit_checks']), use_container_width=True)

                    st.subheader("Extracted Skill Taxonomies")
                    st.json(data.get("skills_by_category", {}))

                    st.subheader("Segmented Resume Sections")
                    st.json(data.get("sections", {}))
                else:
                    st.error("Failed to parse file.")
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")


# ---------------------------------------------------------
# TAB 4: MONGODB HISTORY
# ---------------------------------------------------------
def render_mongodb_history():
    st.markdown("<h1 class='main-header'>📜 MongoDB Analysis History</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Historical record of candidate ATS analyses stored in MongoDB</p>", unsafe_allow_html=True)

    user_id = st.session_state.user_id
    try:
        r = requests.get(f"{API_URL}/history/{user_id}")
        data = r.json()

        if data.get("success"):
            history = data.get("history", [])
            if not history:
                st.info("No past analyses found for this account/session.")
            else:
                df = pd.DataFrame(history)
                st.dataframe(df, use_container_width=True)
        else:
            st.error("Could not fetch history.")
    except Exception as e:
        st.error(f"Error fetching history from backend: {e}")


# ---------------------------------------------------------
# MAIN ROUTING LOGIC
# ---------------------------------------------------------
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
else:
    if nav_selection == "📊 ATS Analyzer & Match":
        render_ats_analyzer()
    elif nav_selection == "🧠 RAG Contextual Feedback":
        render_rag_feedback()
    elif nav_selection == "🔍 NLP Resume Parser":
        render_nlp_parser()
    elif nav_selection == "📜 MongoDB History":
        render_mongodb_history()