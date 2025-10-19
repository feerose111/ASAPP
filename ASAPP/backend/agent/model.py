from langchain_huggingface import ChatHuggingFace
from langchain.prompts import ChatPromptTemplate
from ASAPP.backend.utils.prompt_generator import generate_prompt
from ASAPP.backend.utils.logger import LoggerManager

class Planner:
    def __init__(self, llm):
        self.chat = ChatHuggingFace(llm=llm)
        self.logger = LoggerManager(use_console=True)


    def main(self, project_data: dict):
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful AI assistant specializing in giving out project plans."),
                ("user", generate_prompt(project_data))
            ])
            response = self.chat.invoke(prompt.format())

            self.logger.log("INFO", "Plan Generated", {
                "project_name": project_data.get("project_name", "Untitled Project"),
                "response_preview": response.content[:100]
            })
            return response.content
        except Exception as e:
            self.logger.log("ERROR", "Plan Generation Failed", {"message": str(e)})

