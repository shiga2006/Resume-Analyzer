import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"

st.title("Login")

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)

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

            st.session_state["logged_in"] = True

            st.session_state["user_id"] = data[
                "user"
            ]["id"]

            st.session_state["username"] = data[
                "user"
            ]["username"]

            st.success(
                "Login Successful"
            )

        else:

            st.error(
                data["message"]
            )

    except Exception as e:

        st.error(str(e))