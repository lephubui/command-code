from flask import Flask
from controllers.chat_controller import ChatController

# Initialize the Flask application
app = Flask(__name__)

# Set a secret key for session management
app.secret_key = 'your_secret_key_here'

# Create an instance of ChatController to handle chat operations
chat_controller = ChatController()

# Define a route for the index page that ensures a user session
@app.route('/')
def index():
    chat_controller.ensure_user_session()
    return "Welcome to the Chatbot Service!"

# Define a route for creating a new chat session
@app.route('/api/create_chat', methods=['POST'])
def create_chat():
    return chat_controller.create_chat()
    
# Define a route for sending a message in an existing chat session
# - Listen for POST requests at '/api/send_message'
# - Delegate message handling to ChatController's send_message
# - Return the response from the controller
@app.route('/api/send_message', methods=['POST'])
def send_message():
    return chat_controller.send_message()

# Run the Flask application if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)