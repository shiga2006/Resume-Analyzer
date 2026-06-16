import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"

st.title("Signup")

username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input(
    "Password",
    type="password"
)

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
                "Account Created Successfully"
            )

        else:

            st.error(
                data["message"]
            )

    except Exception as e:

        st.error(str(e))