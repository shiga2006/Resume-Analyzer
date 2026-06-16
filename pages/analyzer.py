import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"

st.title("Resume Analyzer")

if "logged_in" not in st.session_state:

    st.warning(
        "Please login first."
    )

    st.stop()

st.write(
    f"Welcome {st.session_state['username']}"
)

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

job_description = st.text_area(
    "Paste Job Description"
)

if st.button("Analyze Resume"):

    if not uploaded_file:

        st.error(
            "Upload Resume First"
        )

    elif not job_description:

        st.error(
            "Enter Job Description"
        )

    else:

        with st.spinner(
            "Analyzing Resume..."
        ):

            files = {
                "resume": (
                    uploaded_file.name,
                    uploaded_file
                )
            }

            data = {

                "user_id":
                st.session_state["user_id"],

                "job_description":
                job_description
            }

            response = requests.post(
                f"{API_URL}/analyze",
                files=files,
                data=data
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