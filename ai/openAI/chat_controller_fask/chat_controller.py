import uuid
from flask import session, request # Import the 'request' object from Flask to handle incoming request data
from services.chat_service import ChatService

class ChatController:
    def __init__(self):
        self.chat_service = ChatService()
    
    def ensure_user_session(self):
        """Ensure user has a session ID."""
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())
        return session['user_id']
    
    def create_chat(self):
        """Handle chat creation request."""
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Session expired'}, 401
        
        chat_id = self.chat_service.create_chat(user_id)
        return {
            'chat_id': chat_id,
            'message': 'Chat created successfully'
        }
    
    def send_message(self):
        """Handle message sending request."""
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Session expired'}, 401
        
        # Use the 'request' object to get 'chat_id' and 'user_message' from the JSON payload
        chat_id = request.json.get('chat_id')
        user_message = request.json.get('message')

        if not chat_id or not user_message:
            return {'error': 'Missing chat_id or message'}, 400
            
        try:
            ai_response = self.chat_service.process_message(user_id, chat_id, user_message)
            return {'message': ai_response}
        except ValueError as e:
            return {'error': str(e)}, 404
        except RuntimeError as e:
            return {'error': str(e)}, 500