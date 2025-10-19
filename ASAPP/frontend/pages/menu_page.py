import streamlit as st
import requests
import os ,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ASAPP.backend.utils.config_loader import CREATE_PROJECT_URL

default_tech_options = [
    "Python", "Django", "FastAPI", "Flask",
    "React", "Next.js", "Angular", "Vue",
    "PostgreSQL", "MySQL", "MongoDB", "SQLite",
    "Docker", "Kubernetes", "AWS", "GCP", "Azure"
]

def show():
    st.title("ASAPP - Planning done easy")

    # Initialize session state for form
    if "selected_stack" not in st.session_state:
        st.session_state.selected_stack= []
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False

    # Form inputs
    project_name = st.text_input("Project Name", value=st.session_state.get("project_name", ""))
    project_type = st.text_input("Project Type", value=st.session_state.get("project_type", ""),
                                placeholder="e.g. general, math, research")
    duration = st.text_input("Duration (in weeks)", value=st.session_state.get("duration", ""))
    goals = st.text_area("Project Goals", value=st.session_state.get("goals", ""))
    description = st.text_area("Description (Optional)", value=st.session_state.get("description", ""),
                            placeholder="No description provided")

    st.subheader("Select Tech Stack")
    chosen_defaults = st.multiselect("Choose from the predefined options",
                                    default_tech_options,
                                    key="chosen_defaults")
    st.text_input("Enter custom technology", key="custom_input")

    def add_custom_tech():
        if st.session_state.custom_input and st.session_state.custom_input not in st.session_state.selected_stack:
            st.session_state.selected_stack.append(st.session_state.custom_input)
            st.session_state.custom_input = ""

    if st.button("Add Tech"):
        add_custom_tech()

    current_custom = [x for x in st.session_state.selected_stack if x not in default_tech_options]
    st.session_state.selected_stack = list(set(chosen_defaults + current_custom))

    if st.session_state.selected_stack:
        st.write("### Current Tech Stack:")
        for i, tech in enumerate(st.session_state.selected_stack):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"- {tech}")
            with col2:
                if st.button("×", key=f"remove_{tech}_{i}", help=f"Remove {tech}"):
                    st.session_state.selected_stack.remove(tech)
                    st.rerun()

    def reset_form():
        """Reset all form fields"""
        keys_to_reset = [
            "project_name", "project_type", "duration",
            "goals", "description", "selected_stack",
            "custom_input", "chosen_defaults", "form_submitted"
        ]
        for key in keys_to_reset:
            if key in st.session_state:
                if key == "selected_stack":
                    st.session_state[key] = []
                else:
                    del st.session_state[key]


    # Submit button
    if st.button("Submit", type="primary"):
        if not project_name or not project_type or not duration:
            st.error("Please fill in all required fields")
        else:
            st.session_state.project_name = project_name
            st.session_state.project_type = project_type
            st.session_state.duration = duration
            st.session_state.goals = goals
            st.session_state.description = description
            st.session_state.form_submitted = True

            # Build request payload
            project_data = {
                "project_name": project_name,
                "project_type": project_type,
                "duration": duration,
                "tech_stack": ", ".join(st.session_state.selected_stack),
                "goals": goals,
                "description": description or "No description provided",
            }

            try:
                response = requests.post(CREATE_PROJECT_URL, json=project_data)
                if response.status_code == 200:
                    st.session_state.api_result = response.json()
                else:
                    st.session_state.api_result = {"error": f"{response.status_code} - {response.text}"}
            except Exception as e:
                st.session_state.api_result = {"error": str(e)}

            # 🔑 Switch page
            st.session_state.page = "result"
            st.rerun()

    #manual reset
    st.markdown("---")
    if st.button("Reset Form", key="manual_reset"):
        reset_form()
        st.rerun()