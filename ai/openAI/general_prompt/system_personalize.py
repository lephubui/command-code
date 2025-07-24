from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

# Function to send a message and receive a response
def send_message(messages):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    return response.choices[0].message.content.strip()

# Define the AI's personality and role
system_prompt = "You answer with a single word"

# Structure the conversation history with system and user messages
conversation = [
    # System message defines the AI's behavior and tone
    {"role": "system", "content": system_prompt},
    # User message contains the actual question
    {"role": "user", "content": "What's a popular type of pizza?"},
]

# Request response from the personality-customized AI
reply = send_message(conversation)
print("Response 1:", reply)

# Append the AI's first response to the conversation
conversation.append({"role": "assistant", "content": reply})

# Add another user message to the conversation
conversation.append({"role": "user", "content": "What do I need to make it?"})

# Request another response from the AI
reply = send_message(conversation)
print("Response 2:", reply)