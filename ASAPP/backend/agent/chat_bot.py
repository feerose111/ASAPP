from db.chroma_db_connect import DbConnector
from langchain_huggingface import ChatHuggingFace
from langchain.prompts import ChatPromptTemplate
from utils.logger import LoggerManager
from datetime import datetime

class ContextChatbot:
    def __init__(self, project_plan, llm, chroma=None, has_project=False):
        self.chroma = chroma
        self.has_context = has_project

        if chroma is None:
            self.logger = LoggerManager(use_console=True)
        else:
            self.logger = LoggerManager(use_console=True)
            if project_plan and project_plan.strip():
                self.chroma.add_context(project_plan)

        self.chat = ChatHuggingFace(llm=llm)

    def get_response(self, user_query):
        """Retrieve enriched context and generate response"""
        try:
            self.logger.log("INFO", "Chat Start", {
                "query_preview": user_query[:100],
                "has_context": self.has_context,
                "timestamp": datetime.now().isoformat()
            })

            if self.has_context:
                enriched_context = self.chroma.build_context(query_text=user_query)
                self.chroma.add_chat_message(user_query=user_query, llm_response="")

            else:
                enriched_context = "No project context available."

            prompt = ChatPromptTemplate.from_messages([
                ("system",
                 "You are a project planning assistant. Base your answers strictly on the provided project plan and chat history. If the context doesn't include enough information, say so clearly."),
                ("user", f"""
                Question: {user_query}
                
                Context:
                {enriched_context}
                """)
            ])

            messages = prompt.format_messages()
            response = self.chat.invoke(messages)

            response_text = response if isinstance(response, str) else response.content

            if not response_text:
                response_text = "I couldn't generate a response. Please try again."

            if self.has_context:
                self.chroma.add_chat_message(user_query=user_query, llm_response=response_text)

            return response_text

        except Exception as e:
            self.logger.log("ERROR", "Chat Bot Error", {"message": str(e)})
            return None