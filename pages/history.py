import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:5000"

st.title("Resume History")

if "logged_in" not in st.session_state:

    st.warning(
        "Please login first."
    )

    st.stop()

user_id = st.session_state[
    "user_id"
]

response = requests.get(
    f"{API_URL}/history/{user_id}"
)

data = response.json()

if data["success"]:

    history = data["history"]

    if len(history) == 0:

        st.info(
            "No analysis history found."
        )

    else:

        df = pd.DataFrame(history)

        st.dataframe(
            df,
            use_container_width=True
        )