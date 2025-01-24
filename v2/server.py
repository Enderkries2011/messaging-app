import os
import json
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# File to store messages
message_file = os.path.join(os.getcwd(), 'messages.txt')

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
    return render_template_string('''
        <h1>This is a simple messaging Server</h1>
        <button id="clearMessagesBtn">Clear All Messages</button>
        <script>
            document.getElementById('clearMessagesBtn').onclick = function() {
                fetch('/clear_messages', {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        alert(data.message);  // Show success message
                    } else if (data.error) {
                        alert(data.error);  // Show error message
                    }
                })
                .catch(error => {
                    alert('An error occurred: ' + error);
                });
            };
        </script>
    ''')

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

@app.route('/clear_messages', methods=['POST'])
def clear_messages():
    try:
        save_messages([])
        return jsonify({'message': 'All messages cleared successfully'})
    except Exception as e:
        app.logger.error(f'Error clearing messages: {str(e)}')
        return jsonify({'error': 'An error occurred while clearing messages'}), 500

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error(f'Internal Server Error: {str(error)}')
    return jsonify({'error': 'An internal server error occurred'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
