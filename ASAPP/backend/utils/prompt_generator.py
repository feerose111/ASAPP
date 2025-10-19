from langchain.prompts import PromptTemplate
from ASAPP.backend.utils.logger import LoggerManager

logger = LoggerManager(use_console=True)

prompt_template = PromptTemplate(
    input_variables=["project_name", "project_type", "duration", "tech_stack", "goals", "description"],
    template="""
            You are a software planning assistant.
            
            Create a detailed project plan for the following:
            - Project Name: {project_name}
            - Type: {project_type}
            - Duration: {duration} weeks
            - Tech Stack: {tech_stack}
            - Goals: {goals}
            - Description: {description}
            
            Break the plan into weekly tasks, each with clear objectives, tools needed, and expected outcomes.
            Only output the structured plan without additional commentary.
            """
    )

def generate_prompt(inputs):
    try:

        prompt = prompt_template.format(
            project_name=inputs.get("project_name", "Untitled Project"),
            project_type=inputs.get("project_type", "General"),
            duration=inputs.get("duration", "1"),
            tech_stack=inputs.get("tech_stack", "none"),
            goals=inputs.get("goals", "Build a simple working prototype."),
            description=inputs.get("description", "None")
        )
        logger.log("INFO", "Prompt Generated.", {
            "project_name": inputs.get("project_name", "Untitled Project"),
            "project_type": inputs.get("project_type", "General")
        })

        return prompt
    except Exception as e:
        logger.log("ERROR","Prompt Generation Failed", {"message": str(e)})
        return None