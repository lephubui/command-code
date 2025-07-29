import uuid
from openai import OpenAI
from models.chat import ChatManager

class ChatService:
    def __init__(self):
        # Initialize ChatManager to handle chat data
        self.chat_manager = ChatManager()
        self.system_prompt = self.load_system_prompt('data/system_prompt.txt')
    
    def load_system_prompt(self, file_path: str) -> str:
        """Load the system prompt from file."""
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading system prompt: {e}")
            return "You are a helpful assistant."
    
    # Define the create_chat method
    # - Parameters: user_id
    # - Generate a unique chat ID using uuid
    # - Use chat_manager to create a chat session with user_id, chat_id, and system_prompt
    # - Return the chat_id
    def create_chat(self, user_id: str) -> str:
        """Create a new chat session"""
        chat_id = str(uuid.uuid4())
        self.chat_manager.create_chat(user_id, chat_id, self.system_prompt)
        return chat_id