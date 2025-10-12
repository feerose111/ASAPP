import streamlit as st
import requests
from ASAPP.backend.utils.config_loader import CHAT_URL

def show_chat():
    st.title("Project Plan Chatbot")

    # Ensure project plan is available
    if "api_result" not in st.session_state or "project_plan" not in st.session_state.api_result:
        st.warning("No project plan available. Please go back and generate one first.")
        if st.button("Go Back"):
            st.session_state.page = "result"
            st.rerun()
        return

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display existing chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    user_input = st.chat_input("Ask about your project plan...")

    if user_input:
        # Show user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Send message to FastAPI backend
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(CHAT_URL, json={"message": user_input})
                    if response.status_code == 200:
                        reply = response.json()["reply"]
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})
                        st.markdown(reply)
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Failed to reach backend: {e}")

    # Navigation controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Result", key="back_to_result"):
            st.session_state.page = "result"
            st.rerun()
    with col2:
        if st.button("Create Another Project", key="new_project"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = "menu"
            st.rerun()
