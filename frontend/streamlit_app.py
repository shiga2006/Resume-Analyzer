import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ----------------------------------
# Session Variables
# ----------------------------------

if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ----------------------------------
# LOGIN PAGE
# ----------------------------------

def login_page():

    st.title("🔐 Login")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Login"):

            payload = {
                "email": email,
                "password": password
            }

            try:

                response = requests.post(
                    f"{API_URL}/login",
                    json=payload
                )

                data = response.json()

                if data["success"]:

                    st.session_state.logged_in = True

                    st.session_state.user_id = \
                        data["user"]["id"]

                    st.session_state.username = \
                        data["user"]["username"]

                    st.session_state.page = \
                        "dashboard"

                    st.rerun()

                else:

                    st.error(
                        data["message"]
                    )

            except Exception as e:

                st.error(str(e))

    with col2:

        if st.button("Signup"):

            st.session_state.page = "signup"

            st.rerun()


# ----------------------------------
# SIGNUP PAGE
# ----------------------------------

def signup_page():

    st.title("📝 Signup")

    username = st.text_input(
        "Username"
    )

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Create Account"):

            payload = {
                "username": username,
                "email": email,
                "password": password
            }

            try:

                response = requests.post(
                    f"{API_URL}/signup",
                    json=payload
                )

                data = response.json()

                if data["success"]:

                    st.success(
                        "Account Created"
                    )

                else:

                    st.error(
                        data["message"]
                    )

            except Exception as e:

                st.error(str(e))

    with col2:

        if st.button("Back To Login"):

            st.session_state.page = \
                "login"

            st.rerun()


# ----------------------------------
# DASHBOARD
# ----------------------------------

def dashboard_page():

    st.title(
        f"Welcome {st.session_state.username}"
    )

    st.subheader(
        "Resume Analyzer Dashboard"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "📄 Analyze Resume",
            use_container_width=True
        ):

            st.session_state.page = \
                "analyzer"

            st.rerun()

    with col2:

        if st.button(
            "📜 History",
            use_container_width=True
        ):

            st.session_state.page = \
                "history"

            st.rerun()

    with col3:

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.clear()

            st.session_state.page = \
                "login"

            st.rerun()


# ----------------------------------
# ANALYZER PAGE
# ----------------------------------

def analyzer_page():

    st.title("📄 Resume Analyzer")

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"]
    )

    jd = st.text_area(
        "Paste Job Description"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Analyze"):

            if uploaded_file is None:

                st.error(
                    "Upload a Resume"
                )

                return

            if jd.strip() == "":

                st.error(
                    "Enter Job Description"
                )

                return

            with st.spinner(
                "Analyzing..."
            ):

                files = {
                    "resume": (
                        uploaded_file.name,
                        uploaded_file
                    )
                }

                form_data = {

                    "user_id":
                    st.session_state.user_id,

                    "job_description":
                    jd
                }

                try:

                    response = requests.post(
                        f"{API_URL}/analyze",
                        files=files,
                        data=form_data
                    )

                    result = response.json()

                    if result["success"]:

                        st.success(
                            "Analysis Completed"
                        )

                        st.metric(
                            "ATS Score",
                            result["ats_score"]
                        )

                        matched_count = len(
                            result["matched_skills"]
                        )
                        missing_count = len(
                            result["missing_skills"]
                        )
                        strengths_count = len(
                            result["strengths"]
                        )
                        weaknesses_count = len(
                            result["weaknesses"]
                        )

                        chart_df = pd.DataFrame({
                            "Count": [matched_count, missing_count]
                        }, index=["Matched Skills", "Missing Skills"])

                        sentiment_df = pd.DataFrame({
                            "Count": [strengths_count, weaknesses_count]
                        }, index=["Strengths", "Weaknesses"])

                        st.subheader("Analysis Visualizations")
                        colA, colB = st.columns(2)

                        with colA:
                            st.write("### Skill Match Overview")
                            st.bar_chart(chart_df)

                        with colB:
                            st.write("### Strengths vs Weaknesses")
                            st.bar_chart(sentiment_df)

                        st.subheader(
                            "Matched Skills"
                        )

                        for skill in result[
                            "matched_skills"
                        ]:

                            st.success(skill)

                        st.subheader(
                            "Missing Skills"
                        )

                        for skill in result[
                            "missing_skills"
                        ]:

                            st.error(skill)

                        st.subheader(
                            "Strengths"
                        )

                        for item in result[
                            "strengths"
                        ]:

                            st.info(item)

                        st.subheader(
                            "Weaknesses"
                        )

                        for item in result[
                            "weaknesses"
                        ]:

                            st.warning(item)

                        st.subheader(
                            "Recommendations"
                        )

                        for rec in result[
                            "recommendations"
                        ]:

                            st.write(
                                f"• {rec}"
                            )

                    else:

                        st.error(
                            result["message"]
                        )

                except Exception as e:

                    st.error(str(e))

    with col2:

        if st.button("Back"):

            st.session_state.page = \
                "dashboard"

            st.rerun()


# ----------------------------------
# HISTORY PAGE
# ----------------------------------

def history_page():

    st.title(
        "📜 Resume Analysis History"
    )

    try:

        response = requests.get(
            f"{API_URL}/history/"
            f"{st.session_state.user_id}"
        )

        data = response.json()

        if data["success"]:

            history = data["history"]

            if len(history) == 0:

                st.info(
                    "No history available"
                )

            else:

                df = pd.DataFrame(
                    history
                )

                st.dataframe(
                    df,
                    use_container_width=True
                )

    except Exception as e:

        st.error(str(e))

    if st.button("Back"):

        st.session_state.page = \
            "dashboard"

        st.rerun()


# ----------------------------------
# ROUTER
# ----------------------------------

if st.session_state.page == "login":

    login_page()

elif st.session_state.page == "signup":

    signup_page()

elif st.session_state.page == "dashboard":

    dashboard_page()

elif st.session_state.page == "analyzer":

    analyzer_page()

elif st.session_state.page == "history":

    history_page()


def get_match_label(score):

    if score >= 80:
        return "🟢 Strong Match"

    elif score >= 60:
        return "🟡 Moderate Match"

    else:
        return "🔴 Weak Match"