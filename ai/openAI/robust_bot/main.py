from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

def load_system_prompt(file_path: str) -> str:
    """Load the system prompt from file."""
    try:
        # Open and read the system prompt from the specified file
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        # Print an error message if the file cannot be read
        print(f"Error loading system prompt: {e}")
        # Return a default prompt if there's an error
        return "You are a helpful assistant."

def send_message(messages):
    """Send a message and receive a response"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    return response.choices[0].message.content.strip()

# Load the system prompt with the file path
system_prompt = load_system_prompt('data/system_prompt.txt')

# Create a conversation with the system prompt and a user message
conversation = [
    {"role": "system", "content": system_prompt},
    # Modify the user message to match with the new system prompt
    {"role": "user", "content": "I’m feeling overwhelmed trying to keep up with my IT needs. My team is frustrated whenever something breaks. Do you have a way to reassure us that issues are resolved quickly? Also, I’m on a tight budget—what do you recommend?"}
]

# Send the message and get a response
response = send_message(conversation)

# Print the user's question and the response
print(f"User:\n{conversation[1]['content']}\n")
print(f"Chatbot:\n{response}")