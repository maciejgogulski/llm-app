import os
from flask import render_template, request, redirect, url_for, flash, Blueprint
import requests

bp = Blueprint('frontend', __name__, template_folder='templates')

API_BASE_URL = os.getenv('API_BASE_URL')

@bp.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        mode = request.form.get("mode")
        prompt = request.form.get("prompt")

        if not prompt:
            error = "Prompt cannot be empty."
        else:
            endpoint = f"{API_BASE_URL}/{mode}"
            try:
                response = requests.post(endpoint, json={"prompt": prompt})
                response.raise_for_status()
                response_json = response.json()
                result = response_json.get("response", {}).get("result")
            except Exception as e:
                error = str(e)

    return render_template("index.html", result=result, error=error)
