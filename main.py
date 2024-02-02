import streamlit as st
import sqlite3
import json

# Create a SQLite database connection
conn = sqlite3.connect('local_database.db')
c = conn.cursor()

# Create a table to store form data if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS user_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                json_data TEXT
             )''')
conn.commit()

# Streamlit app
st.title("User Data Collection App")

# Define the form to collect user data
with st.form("User Data Form"):
    name = st.text_input("Name")
    email = st.text_input("Email")

    json_data = st.text_area("JSON Data (In the specified format)")

    submit_button = st.form_submit_button("Submit")

if submit_button:
    # Insert the user data and JSON data into the database
    c.execute("INSERT INTO user_data (name, email, json_data) VALUES (?, ?, ?)", (name, email, json_data))
    conn.commit()
    st.success("Data submitted successfully!")

# Display the collected data
st.header("Collected Data")
data = c.execute("SELECT id, name, email, json_data FROM user_data").fetchall()
for row in data:
    st.write("ID:", row[0])
    st.write("Name:", row[1])
    st.write("Email:", row[2])

    # Parse and display JSON data
    try:
        json_obj = json.loads(row[3])
        st.json(json_obj)
    except json.JSONDecodeError:
        st.warning("Invalid JSON data")

# Close the database connection
conn.close()
