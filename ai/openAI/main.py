# Using for creating mutiple chat sessions with OpenAI API
from flask import Flask, render_template
from controllers.chat_controller import ChatController

# Initialize the Flask application
app = Flask(__name__)

# Set a secret key for session management
app.secret_key = 'your_secret_key_here'

# Create an instance of ChatController
chat_controller = ChatController()

# Initialize session and render chat interface
@app.route('/')
def index():
    chat_controller.ensure_user_session()
    return render_template('chat.html')