from ASAPP.backend.db.chroma_db_connect import DbConnector
from langchain_huggingface import ChatHuggingFace
from langchain.prompts import ChatPromptTemplate
from ASAPP.backend.utils.logger import LoggerManager
from datetime import datetime

class ContextChatbot:
    def __init__(self, project_plan, llm, chroma=None):
        if chroma is None:
            self.chroma = DbConnector()
            if project_plan and project_plan.strip():
                self.chroma.add_context(project_plan)
        else:
            self.chroma = chroma

        self.logger = LoggerManager(use_console=True)
        self.chat = ChatHuggingFace(llm=llm)

    def get_response(self, user_query):
        """Retrieve enriched context and generate response"""
        try:
            self.logger.log("INFO", "Chat Start", {
                "query_preview": user_query[:100],
                "timestamp": datetime.now().isoformat()
            })
            enriched_context = self.chroma.build_context(query_text=user_query)

            self.chroma.add_chat_message(user_query=user_query, llm_response="")

            prompt = ChatPromptTemplate.from_messages([
                ("system",
                 "You are a project planning assistant. Base your answers strictly on the provided project plan and chat history. If the context doesn't include enough information, say so clearly."),
                ("user", f"""
                Question: {user_query}
                
                Context:
                {enriched_context}    def add_chat_message(self, user_query, llm_response):
    
                """)
            ])

            messages = prompt.format_messages()
            response = self.chat.invoke(messages)

            response_text = response if isinstance(response, str) else response.content

            self.chroma.add_chat_message(user_query=user_query, llm_response=response_text)

            return response_text

        except Exception as e:
            self.logger.log("ERROR", "Chat Bot Error", {"message": str(e)})