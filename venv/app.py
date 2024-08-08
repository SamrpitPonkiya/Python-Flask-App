from flask import Flask, request
import pyodbc
import json
from datetime import datetime

app = Flask(__name__)

VERIFY_TOKEN = 'MySecureWebhookToken2024!'

# Database connection
conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.1.145,1435;DATABASE=Exam;UID=yash;PWD=Sit@321#'

def log_message(timestamp, group_id, user_id, message_id, message_type, message_content, participant_id):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO WhatsAppMessages (timestamp, group_id, user_id, message_id, message_type, message_body, participant_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (timestamp, group_id, user_id, message_id, message_type, message_content, participant_id))
        conn.commit()
    except Exception as e:
        print(f"Error inserting message: {e}")
    finally:
        conn.close()

@app.route('/whatsapp-webhook', methods=['GET'])
def verify_webhook():
    token_sent = request.args.get("hub.verify_token")
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token', 403

@app.route('/whatsapp-webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    for entry in data.get('entry', []):
        for change in entry.get('changes', []):
            for message in change.get('value', {}).get('messages', []):
                try:
                    timestamp = int(message['timestamp'])
                    user_id = message.get('from', '')
                    message_id = message.get('id', '')
                    message_type = message.get('type', '')
                    message_content = message.get('text', {}).get('body', '') or message.get('image', {}).get('caption', '')
                    
                    # Handle group chat context
                    group_id = message.get('context', {}).get('group_id', '')
                    participant_id = message.get('context', {}).get('participant', '')

                    log_message(timestamp, group_id, user_id, message_id, message_type, message_content, participant_id)
                except Exception as e:
                    print(f"Error processing message: {e}")

    return 'OK', 200

if __name__ == '__main__':
    app.run(port=5000) 

