from services.chat_service import ChatService

# Initialize a ChatService instance
chat_service = ChatService()

# Define a variable with a sample user identifier, e.g., "user123"
user_id = "user123"

# Call the create_chat method with the user ID and store the chat ID
chat_id = chat_service.create_chat(user_id)

# Print the chat ID
print(chat_id)