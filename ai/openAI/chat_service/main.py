from services.chat_service import ChatService

# Initialize the chat service
chat_service = ChatService()

# Simulate a user ID
user_id = "user123"

# Create a new chat session
chat_id = chat_service.create_chat(user_id)
print(f"Chat session created with ID: {chat_id}")

# Define a user message
user_message = "How can I contact your company by email?"
print(f"User Message: {user_message}")

try:
    ai_response = chat_service.process_message(user_id, chat_id, user_message)
    print(f"AI Response: {ai_response}")
except Exception as e:
    print(f"Error: {e}")

# Define and print a follow-up question
follow_up = "What is the company mailing address?"
print(f"Follow-up: {follow_up}")

# Send the follow-up question to test context retention
try:
    ai_response = chat_service.process_message(user_id, chat_id, follow_up)
except Exception as e:
    print(f"Error: {e}")

# Print the AI's response to the follow-up question
print(f"AI's response: {ai_response}")