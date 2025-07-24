from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

# Initialize conversation history as an empty list
conversation_history = []

# Function to send a message and receive a response
def send_message(user_message):
    # Automatically append the user message to conversation history
    conversation_history.append({"role": "user", "content": user_message})
    
    # Send the updated conversation to the AI
    response = client.chat.completions.create(
        model="gpt-4",
        messages=conversation_history
    )
    
    # Get the AI's response
    ai_response = response.choices[0].message.content.strip()
    
    # Append the AI's response to conversation history
    conversation_history.append({"role": "assistant", "content": ai_response})
    
    # Return the AI's response as a string
    return ai_response

# Driver code to demonstrate functionality
if __name__ == "__main__":
    # Example usage
    user_input = "What is the main ingredient in guacamole?"
    print("User:", user_input)
    
    # Send the message and get the AI's response
    ai_reply = send_message(user_input)
    print("Assistant:", ai_reply)

    # Follow-up question with maintained conversation context
    follow_up_reply = send_message("Can you name a popular dish that uses guacamole?")
    print("Assistant follow-up:", follow_up_reply)