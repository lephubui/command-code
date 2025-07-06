from flask import Flask
from flask_cors import CORS
import openai
from config import Config
from routes import api  # Import the api blueprint

app = Flask(__name__)
CORS(app)

# Load configuration
app.config.from_object(Config)

# Configure OpenAI API key
openai.api_key = app.config['OPENAI_API_KEY']

# Register blueprints
app.register_blueprint(api)  # Register the api blueprint

if __name__ == '__main__':
    app.run(debug=True, port=5001)