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
st.title("Conversation Collection App")

with st.form("Conversation Form"):
    user_message = st.text_input("User Message")
    assistant_message = st.text_input("Assistant Message")
    conversation_id = st.text_input("Conversation ID (for update)")
    submit_button = st.form_submit_button("Submit")
    update_button = st.form_submit_button("Update")

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

conn = sqlite3.connect('local_database.db')

# Close the database connection
conn.close()
