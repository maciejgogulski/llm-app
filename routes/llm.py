import logging
from flask import Blueprint, request, jsonify
from llm.prompter import prompt
from rag.rag import perform_rag

bp = Blueprint('llm', __name__, url_prefix='/llm')

log = logging.getLogger(__name__)

@bp.route('/prompt', methods=['POST'])
def prompt_route():
    log.info("Recieved prompt request")
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "Missing 'prompt' in request body"}), 400

    user_prompt = data['prompt']
    response = prompt(user_prompt)
    return jsonify({"response": response})

@bp.route('/rag', methods=['POST'])
def rag_route():
    log.info("Recieved RAG request")
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "Missing 'prompt' in request body"}), 400

    user_prompt = data['prompt']
    response = perform_rag(user_prompt)
    return jsonify({"response": response})

