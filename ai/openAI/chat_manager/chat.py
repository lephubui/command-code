class ChatManager:
    def __init__(self):
        self.chat_sessions = {} # Store all active chat sessions
    
    # Define the create_chat method
    # Parameters: user_id, chat_id, system_prompt
    def create_chat(self, user_id, chat_id, system_prompt):
        """Create a new chat for a user"""
        # Check if user_id is not in self.chat_sessions and initialize it
        if user_id not in self.chat_sessions:
            self.chat_sessions[user_id] = {}
        # Store the new chat with system_prompt and an empty messages list
        self.chat_sessions[user_id][chat_id] = {
            'system_prompt': system_prompt,
            'messages': []
        }
    
    # Define the get_chat method
    # Parameters: user_id, chat_id
    def get_chat(self, user_id, chat_id):
        """Retrieve the chat using user_id and chat_id"""
        return self.chat_sessions.get(user_id, {}).get(chat_id)
    
    # Define the add_message method
    # - Parameters: user_id, chat_id, role, content
    # - Retrieve the chat using get_chat method
    # - If chat exists, append the message with role and content to the chat's message list
    def add_message(self, user_id, chat_id, role, content):
        if chat := self.get_chat(user_id, chat_id):
            chat["messages"].append({"role": role, "content": content}) 
        else:
            print(f"Chat not found for user {user_id} and chat {chat_id}. Message not added.")

    # Define the get_conversation method
    # - Parameters: user_id, chat_id
    # - Retrieve the chat using get_chat method
    # - If chat exists:
    #   - Create a list starting with a dictionary for the system prompt:
    #     {"role": "system", "content": chat['system_prompt']}
    #   - Append each message from chat['messages'] to this list
    # - If chat does not exist, return an empty list
    def get_conversation(self, user_id, chat_id):
        """Get the full conversation including system message"""
        if chat := self.get_chat(user_id, chat_id):
            system_message =  {"role": "system", "content": chat['system_prompt']}
            return [system_message] + chat['message']
        return []