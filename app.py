import os
from flask import Flask, request, jsonify
import requests
import os
import json  

app = Flask(__name__)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")
TOKENS_FILE = 'tokens.json'

@app.route('/')
def home():
    return '<h1>Discord OAuth Flask Server is running!</h1>'

@app.route('/api/oauth2/callback', methods=['POST'])
def oauth_callback():
    data = request.json
    code = data.get('code')

    if not code:
        return jsonify({'error': 'No code provided'}), 400

    token_url = 'https://discord.com/api/oauth2/token'
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to get token', 'details': response.json()}), 400

    token_data = response.json()

    # 保存（本番ならDBを使おう）
    with open(TOKENS_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(token_data) + '\n')

    return jsonify({'status': 'success', 'token': token_data}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
