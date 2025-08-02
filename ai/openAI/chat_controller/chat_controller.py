import uuid
from services.chat_service import ChatService

class ChatController:
    def __init__(self):
        self.chat_service = ChatService()
        self.test_session = {}

    def ensure_user_session(self):
        """Ensure user has a session ID in the test session."""
        if 'user_id' not in self.test_session:
            self.test_session['user_id'] = str(uuid.uuid4())
        return self.test_session['user_id']
    
    # Define the create_chat method
        # Retrieve the user_id from the test_session
        # Check if the user_id is valid, if not return an error
        # Create a new chat session using the chat_service
        # Return the chat_id and a success message
    def create_chat(self):
        user_id = self.test_session.get('user_id')
        if not user_id:
            return {'error': 'Session expired'}, 401
        
        chat_id = self.chat_service.create_chat(user_id)
        return {
            'chat_id': chat_id,
            'message': 'Chat created successfully'
        }

# Define the send_message method
    def send_message(self, chat_id, user_message):
        """Handle message sending request."""
        # Check if 'user_id' exists in the test_session dictionary
        # If it doesn't exist, return an error message indicating the session
        # has expired with a status code of 401
        user_id = self.test_session.get('user_id')
        
        if not user_id:
            return {'error': 'Session expired'}, 401
                
        # Ensure both chat_id and user_message are provided and not empty
        # If either is missing, return an error message with a status code of 400
        if not chat_id or not user_message:
            return {'error': 'Missing chat_id or message'}, 400

        # Process the message using chat_service within a try-except block
        # Catch ValueError and return an error message with a status code of 404.
        # Catch RuntimeError and return an error message with a status code of 500.
        try:
            ai_response = self.chat_service.process_message(user_id, chat_id, user_message)
            return {'message': ai_response}
        except ValueError as e:
            return {'error': str(e)}, 404
        except RuntimeError as e:
            return {'error': str(e)}, 500
