from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, request, jsonify
from llm.prompter import prompt


app = Flask(__name__)

app.config['SERVER_PORT'] = os.getenv('SERVER_PORT', '5000')
debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'


@app.route('/prompt', methods=['POST'])
def prompt_route():
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "Missing 'prompt' in request body"}), 400

    user_prompt = data['prompt']
    response = prompt(user_prompt)
    return jsonify({"response": response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['SERVER_PORT'], debug=debug_mode)

