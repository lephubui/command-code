from controllers.chat_controller import ChatController

# Initialize the ChatController
chat_controller = ChatController()

# Ensure a user session for testing
user_id = chat_controller.ensure_user_session()

# Create a new chat session
chat_response = chat_controller.create_chat()

# Check if there is an error in the chat_response
if 'error' in chat_response:
    print(f"Error: {chat_response['error']}") # If there is an error, print the error message
else: # If there is no error:
    # Extract chat_id from the response
    chat_id = chat_response['chat_id']
    print(chat_id)

    # Send the user message using the send_message method and retrieve the AI's response
    response = chat_controller.send_message(chat_id, "What are the top service?")

    # Handle message response
    # If 'error' is in the response, print the error message
    # Otherwise, print the AI's response
    if 'error' in response:
        print(f"Error: {response['error']}")
    else:
        print(f"AI Response: {response['message']}")