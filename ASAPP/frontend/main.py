import streamlit as st
import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ASAPP.backend.utils.config_loader import CREATE_PROJECT_API

# Predefined options for tech stack
default_tech_options = [
    "Python", "Django", "FastAPI", "Flask",
    "React", "Next.js", "Angular", "Vue",
    "PostgreSQL", "MySQL", "MongoDB", "SQLite",
    "Docker", "Kubernetes", "AWS", "GCP", "Azure"
]

st.set_page_config(page_title="Project Input Form", layout="centered")
st.title("ASAPP - Planning done easy")

# Initialize session state for inputs
if "selected_stack" not in st.session_state:
    st.session_state.selected_stack = []
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

# Inputs - using default values instead of session state keys
project_name = st.text_input("Project Name", value=st.session_state.get("project_name", ""))
project_type = st.text_input("Project Type", value=st.session_state.get("project_type", ""),
                             placeholder="e.g. general, math, research")
duration = st.text_input("Duration (in weeks)", value=st.session_state.get("duration", ""))
goals = st.text_area("Project Goals", value=st.session_state.get("goals", ""))
description = st.text_area("Description (Optional)", value=st.session_state.get("description", ""),
                           placeholder="No description provided")

st.subheader("Select Tech Stack")

# Choose from defaults - Fixed: no default parameter that causes rerun
chosen_defaults = st.multiselect(
    "Choose from the predefined options",
    default_tech_options,
    key="chosen_defaults"
)

# Add custom tech input
custom_stack = st.text_input("Enter custom technology", key="custom_input")


def add_custom_tech():
    if st.session_state.custom_input and st.session_state.custom_input not in st.session_state.selected_stack:
        st.session_state.selected_stack.append(st.session_state.custom_input)
        st.session_state.custom_input = ""  # Clear the input


# Button with callback
if st.button("Add Tech"):
    add_custom_tech()

# Update selected stack with chosen defaults (avoid duplicates)
current_custom = [x for x in st.session_state.selected_stack if x not in default_tech_options]
st.session_state.selected_stack = list(set(chosen_defaults + current_custom))

# Show chosen tech stack
if st.session_state.selected_stack:
    st.write("### Current Tech Stack:")
    # Create a container to avoid rerun issues with dynamic buttons
    tech_container = st.container()

    with tech_container:
        for i, tech in enumerate(st.session_state.selected_stack):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"- {tech}")
            with col2:
                # Use unique key and check if button was clicked
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


# Submit Button
if st.button("Submit", type="primary"):
    # Store current form values in session state
    st.session_state.project_name = project_name
    st.session_state.project_type = project_type
    st.session_state.duration = duration
    st.session_state.goals = goals
    st.session_state.description = description

    project_data = {
        "project_name": project_name,
        "project_type": project_type,
        "duration": duration,
        "tech_stack": ", ".join(st.session_state.selected_stack),
        "goals": goals,
        "description": description or "No description provided",
    }

    # Basic validation
    if not project_name or not project_type or not duration:
        st.error("Please fill in all required fields (Project Name, Type, and Duration)")
    else:
        st.success("Form Submitted Successfully")

        try:
            with st.spinner("Sending request to API..."):
                response = requests.post(CREATE_PROJECT_API, json=project_data)

            if response.status_code == 200:
                api_result = response.json()
                st.success("API Response Received!")

                # Display the project plan
                if "project_plan" in api_result:
                    st.markdown("### Generated Project Plan:")
                    st.markdown(api_result["project_plan"])
                else:
                    st.info("No project plan received in response")

                # Add reset button after successful submission
                if st.button("Create Another Project", key="reset_after_submit"):
                    reset_form()
                    st.rerun()

            else:
                st.error(f"API Error: {response.status_code} - {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("Failed to connect to API. Please check if the server is running.")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

# Add a manual reset button at the bottom
st.markdown("---")
if st.button("Reset Form", key="manual_reset"):
    reset_form()
    st.rerun()