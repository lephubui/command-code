# Import necessary modules 
import chat

def load_system_prompt(file_path: str) -> str:
    """Load the system prompt from file."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading system prompt: {e}")
        return "You are a helpful assistant."

# Load the system prompt
system_prompt = load_system_prompt('data/system_prompt.txt')

# Instantiate the ChatManager
manager = chat.ChatManager()

# Define user_id and chat_id variables
# - Set user_id to a test value, e.g., "test_user"
# - Set chat_id to a test value, e.g., "test_chat"
user_id = "user123"
chat_id = "chat123"

# Use create_chat method to create a new chat
# - Call the create_chat method on the ChatManager instance
# - Pass user_id, chat_id, and system_prompt as arguments
manager.create_chat(user_id, chat_id, system_prompt)

# Use get_chat method to check if the chat exists
# - Retrieve the chat using the get_chat method with user_id and chat_id
# - If the chat is found, print "Chat successfully created!"
# - If the chat is not found, print "Failed to create chat."
chat = manager.get_chat(user_id, chat_id)
if chat:
    print("Chat successfully created!")
else:
    print("Failed to create chat.")