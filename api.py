from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('local_database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/conversations', methods=['GET', 'POST'])
def conversations():
    conn = get_db_connection()
    if request.method == 'POST':
        data = request.json
        conn.execute("INSERT INTO conversations (user_message, assistant_message) VALUES (?, ?)",
                     (data['user_message'], data['assistant_message']))
        conn.commit()
        return jsonify({"success": True}), 201

    elif request.method == 'GET':
        conversations = conn.execute("SELECT * FROM conversations").fetchall()
        return jsonify([{"id": x["id"], "user_message": x["user_message"], "assistant_message": x["assistant_message"]} for x in conversations])

    conn.close()

@app.route('/conversations/<int:conversation_id>', methods=['PUT'])
def update_conversation(conversation_id):
    conn = get_db_connection()
    data = request.json
    try:
        conn.execute("UPDATE conversations SET user_message=?, assistant_message=? WHERE id=?",
                     (data['user_message'], data['assistant_message'], conversation_id))
        conn.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
