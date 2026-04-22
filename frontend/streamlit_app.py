import streamlit as st
import requests

st.title("IT Support Chatbot")
st.write("Ask IT support questions")

session_id = st.text_input("Session ID", "demo-session")
user_query = st.text_area("Enter your issue")

if st.button("Submit"):
    payload = {
        "session_id": session_id,
        "user_query": user_query
    }
    response = requests.post("http://127.0.0.1:8000/chat", json=payload)

    if response.status_code == 200:
        result = response.json()
        st.subheader("Predicted Intent")
        st.write(result["predicted_intent"])

        st.subheader("Confidence")
        st.write(result["confidence"])

        st.subheader("Retrieved Docs")
        st.write(result["retrieved_docs"])

        st.subheader("Answer")
        st.write(result["answer"])
    else:
        st.error(response.text)
