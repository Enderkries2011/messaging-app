from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# File to store messages
message_file = 'messages.txt'

def save_messages(messages):
    with open(message_file, 'w') as file:
        json.dump(messages, file)

def load_messages():
    try:
        with open(message_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

@app.route('/')
def home():
    return "This is a simple messaging Server"

@app.route('/store_message', methods=['POST'])
def store_message():
    data = request.json
    messages = load_messages()
    messages.append(data)
    save_messages(messages)
    return jsonify({'message': 'Message stored successfully'})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    messages = load_messages()
    return jsonify(messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) # made to run on replit but i cant make anymore repls so u cant clone it
