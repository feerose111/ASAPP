from langchain_huggingface import ChatHuggingFace
from langchain.prompts import ChatPromptTemplate
from ASAPP.backend.utils.prompt_generator import generate_prompt

class Planner:
    def __init__(self, llm):
        self.chat = ChatHuggingFace(llm=llm)

    def main(self, project_data: dict):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant specializing in giving out project plans."),
            ("user", generate_prompt(project_data))
        ])
        response = self.chat.invoke(prompt.format())
        return response.content
