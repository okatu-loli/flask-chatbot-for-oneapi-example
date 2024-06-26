from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

# One-API的URL和你的API密钥
load_dotenv()
ONE_API_URL = os.getenv('ONE_API_URL')
API_KEY = os.getenv('API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ],
        "temperature": 0.7
    }
    response = requests.post(ONE_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        bot_response = response.json().get('choices')[0]['message']['content']
        return jsonify({'response': bot_response})
    else:
        return jsonify({'error': 'Failed to get response from One-API'}), 500

if __name__ == '__main__':
    app.run(debug=True)
