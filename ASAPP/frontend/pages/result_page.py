import streamlit as st

def show():
    st.title("Generated Project Plan")

    if "api_result" in st.session_state:
        api_result = st.session_state.api_result
        if "error" in api_result:
            st.error(api_result["error"])
        elif "project_plan" in api_result:
            st.success("API Response Received!")
            st.markdown("### Project Plan")
            st.markdown(api_result["project_plan"])
        else:
            st.info("No project plan received in response")
    else:
        st.warning("No result to show. Please submit the form first.")
        if st.button("Go Back"):
            st.session_state.page = "menu"
            st.rerun()

    if st.button("Create Another Project"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.page = "menu"
        st.rerun()


    col1, col2 = st.columns(2)

    with col1:
        if st.button("Chat with Project"):
            if "api_result" in st.session_state and "project_plan" in st.session_state.api_result:
                st.session_state.page = "chat"
                st.session_state.chat_initialized = False
                st.rerun()
            else:
                st.error("No project plan to chat about")

    with col2:
        if st.button("Create Another Project", key="create_new_project"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = "menu"
            st.rerun()