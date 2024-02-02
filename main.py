import streamlit as st
import requests
import time
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

# Function to update a conversation entry
def update_conversation(conversation_id, updated_user_message, updated_assistant_message):
    data = {
        "user_message": updated_user_message,
        "assistant_message": updated_assistant_message
    }
    response = requests.put(f"{api_url}/{conversation_id}", json=data)
    if response.status_code == 200:
        st.success("Conversation updated successfully!")
    else:
        st.error("Failed to update conversation.")

# Streamlit app interface
st.title("Conversation Collection App")

with st.form("Conversation Form"):
    edit_mode = st.checkbox("Edit Mode")
    if edit_mode:
        edit_conversation_id = st.number_input("Enter Conversation ID to Edit", min_value=1)
    user_message = st.text_input("User Message")
    assistant_message = st.text_input("Assistant Message")
    submit_button = st.form_submit_button("Submit")

if submit_button:
    # Send the conversation data to the API
    data = {"user_message": user_message, "assistant_message": assistant_message}
    response = requests.post(api_url, json=data)
    if response.status_code == 201:
        st.success("Conversation added successfully!")
    else:
        st.error("An error occurred.")

# Auto-refresh every 5 seconds
if time.time() % 5 < 1:
    st.experimental_rerun()

# Display conversations in the specified format with the most recent at the top
st.header("Collected Conversations")
structured_data = fetch_conversations()
formatted_data = []
for entry in structured_data:
    formatted_entry = {
        "id": f"identity_{entry['id']}",
        "conversations": [
            {"from": "user", "value": entry["user_message"]},
            {"from": "assistant", "value": entry["assistant_message"]}
        ]
    }
    formatted_data.append(formatted_entry)

# Display the formatted data without numbers at the beginning
for i, entry in enumerate(formatted_data):
    st.json(entry)
    if edit_mode and edit_conversation_id:
        if entry["id"] == f"identity_{edit_conversation_id}":
            # Input fields to edit the conversation
            edited_user_message = st.text_input("Edit User Message", value=entry["conversations"][0]["value"])
            edited_assistant_message = st.text_input("Edit Assistant Message", value=entry["conversations"][1]["value"])
            update_button = st.button("Update Conversation")
            if update_button:
                # Update the conversation entry
                update_conversation(edit_conversation_id, edited_user_message, edited_assistant_message)

conn = sqlite3.connect('local_database.db')

# Close the database connection
conn.close()
