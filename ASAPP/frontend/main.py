import streamlit as st
st.set_page_config(page_title="ASAPP - Planning done easy", layout="centered")

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "menu"

# Navigation logic
if st.session_state.page == "menu":
    from ASAPP.frontend.pages import menu_page
    menu_page.show()
elif st.session_state.page == "result":
    from ASAPP.frontend.pages import result_page
    result_page.show()
elif st.session_state.page == "chat":
    from ASAPP.frontend.pages import chatbot_page
    chatbot_page.show_chat()