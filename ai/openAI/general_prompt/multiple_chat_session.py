import uuid
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

# Store all active chat sessions
chat_sessions = {}

# Define a common system prompt for all conversations
system_prompt = {
    "role": "system",
    "content": """You are an experienced software engineer with 20 years of expertise across multiple technologies. Your background includes:

- Compiled programming languages: C and C++
- Interpreted languages: Python, Java, and C#
- Web development: Full-stack development with various frameworks
- Web server programming languages
- Database expertise: Both SQL and NoSQL
- Framework proficiency: MEAN stack, React, and many others

You provide professional, technical guidance and solutions based on your extensive experience across these diverse technology stacks."""
}

# Create a new chat session with a unique identifier
def create_chat():
    chat_id = str(uuid.uuid4())  # Create unique session identifier
    chat_sessions[chat_id] = []  # Initialize empty conversation history
    chat_sessions[chat_id].append(system_prompt)  # Add system prompt to conversation history
    return chat_id

# Send a message in a specific chat session and get a response
def send_message(chat_id, user_message):
    # Ensure we're adding to a valid conversation
    if chat_id not in chat_sessions:
        raise ValueError("Chat session not found!")
    
    # Add the new message to conversation history
    chat_sessions[chat_id].append({"role": "user", "content": user_message})
    
    # Get AI's response while maintaining conversation context
    response = client.chat.completions.create(
        model="gpt-4",
        messages=chat_sessions[chat_id]  # Full history for context
    )
    
    # Process response and maintain conversation history
    answer = response.choices[0].message.content.strip()
    chat_sessions[chat_id].append({"role": "assistant", "content": answer})
    return answer

if __name__ == "__main__":
    # Chat ID 1
    chat_id1 = create_chat()
    id1_message = send_message(chat_id1, "What's the difference between compiled and interpreted programming languages?")
    print("Chat 1, First Message:", id1_message)
    id1_followup = send_message(chat_id1, "Can you give me specific examples of each type?")
    print("Chat 1, Follow-up Message:", id1_followup)
    
    # Chat ID 2
    chat_id2 = create_chat()
    id2_message = send_message(chat_id2, "I'm building a web application. Should I use SQL or NoSQL database?")
    print("Chat 2, First Message:", id2_message)
    id2_followup = send_message(chat_id2, "What are the main advantages of using React over other frontend frameworks?")
    print("Chat 2, Follow-up Message:", id2_followup)

    # Print both conversation histories to confirm they are separate
    print(chat_sessions[chat_id1])
    print(chat_sessions[chat_id2])