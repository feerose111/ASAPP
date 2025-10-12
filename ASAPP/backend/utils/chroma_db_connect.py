import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
import uuid
from datetime import datetime, timezone


class DbConnector:
    def __init__(self):
        self.chroma_client = chromadb.Client()
        self.chat_collection = self.chroma_client.get_or_create_collection(name="chat_messages")
        self.context_collection = self.chroma_client.get_or_create_collection(name="chat_context")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", " ", ""])

    def add_context(self, api_result):
        chunks = self.text_splitter.split_text(api_result)
        ids = [str(uuid.uuid4()) for _ in chunks]
        metadata = [{"chunk": i + 1, "type": "context"} for i in range(len(chunks))]

        self.context_collection.add(
            ids=ids,
            documents=chunks,
            metadatas=metadata
        )

    def add_chat_message(self, user_query, llm_response):
        """Store the chat message both user query and llm response separately"""

        timestamp = datetime.now(timezone.utc).isoformat()
        # Store user message
        self.chat_collection.add(
            ids=[str(uuid.uuid4())],
            documents=[user_query],
            metadatas=[{"type": "user_query", "timestamp": timestamp}]
        )

        # Store bot message
        self.chat_collection.add(
            ids=[str(uuid.uuid4())],
            documents=[llm_response],
            metadatas=[{"type": "llm_response", "timestamp": timestamp}]
        )

    def build_context(self, query_text, n_chat_results=4, n_context_results=2):
        """Retrieve and concatenate chat history and project context for richer context"""

        # Retrieve from chat collection
        chat_results = self.chat_collection.query(
            query_texts=[query_text],
            n_results=n_chat_results
        )

        # Retrieve from context collection
        context_results = self.context_collection.query(
            query_texts=[query_text],
            n_results=n_context_results
        )

        context = ""

        # Add project context first
        if context_results and context_results['documents']:
            context += "=== PROJECT CONTEXT ===\n"
            for doc in context_results['documents'][0]:
                context += f"{doc}\n"
            context += "\n"

        # Add chat history
        if chat_results and chat_results['documents']:
            context += "=== CHAT HISTORY ===\n"
            for doc, metadata in zip(chat_results['documents'][0], chat_results['metadatas'][0]):
                msg_type = metadata.get('type', 'unknown')
                if msg_type == 'user_query':
                    context += f"User: {doc}\n"
                elif msg_type == 'llm_response':
                    context += f"Assistant: {doc}\n"

        return context