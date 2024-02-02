import streamlit as st
import requests
import time  # Import the time module for auto-refresh
import sqlite3

# Define the API URL
api_url = "http://localhost:5000/conversations"  # URL of your Flask API

# Function to fetch conversations from the API and reverse the order
def fetch_conversations():
    response = requests.get(api_url)
    if response.status_code == 200:
        conversations = response.json()
        return conversations[::-1]  # Reverse the order
    else:
        st.error("Failed to fetch conversations.")
        return []

# Streamlit app interface
st.title("清大科越AI客服训练集合")

with st.form("Conversation Form"):
    user_message = st.text_input("用户提问")
    assistant_message = st.text_input("清大科越AI回答")
    conversation_id = st.text_input("修改对话ID (仅需要修改对话时填写)")
    submit_button = st.form_submit_button("提交")
    update_button = st.form_submit_button("修改")

if submit_button:
    # Send the conversation data to the API
    data = {"user_message": user_message, "assistant_message": assistant_message}
    response = requests.post(api_url, json=data)
    if response.status_code == 201:
        st.success("Conversation added successfully!")
    else:
        st.error("An error occurred.")

if update_button:
    # Check if conversation_id is provided
    if conversation_id:
        # Send the conversation data to the API for updating
        data = {"user_message": user_message, "assistant_message": assistant_message}
        update_url = f"{api_url}/{conversation_id}"
        response = requests.put(update_url, json=data)
        if response.status_code == 200:
            st.success("Conversation updated successfully!")
        else:
            st.error(f"Failed to update conversation. Error: {response.text}")
    else:
        st.warning("Please provide a Conversation ID for updating.")

# Auto-refresh every 5 seconds
if time.time() % 5 < 1:
    st.experimental_rerun()

# Display conversations in the specified format with the most recent at the top
st.header("Collected Conversations")
structured_data = fetch_conversations()

# Create a list to store the conversations
conversations_list = []

for entry in structured_data:
    conversation = {
        "id": f"identity_{entry['id']}",
        "conversations": [
            {"from": "user", "value": entry["user_message"]},
            {"from": "assistant", "value": entry["assistant_message"]}
        ]
    }
    conversations_list.append(conversation)

# Display the entire list as a JSON object
st.json(conversations_list)

conn = sqlite3.connect('local_database.db')

# Close the database connection
conn.close()
