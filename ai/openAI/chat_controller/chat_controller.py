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
