from dotenv import load_dotenv
load_dotenv()

from config.logging_conf import setup_logging
setup_logging()

from routes import register_blueprints
from flask import Flask
import os


def create_app():
    app = Flask(__name__)
    register_blueprints(app)
    return app

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app = create_app()
    app.run(host='0.0.0.0', port=os.getenv('SERVER_PORT', '5000'), debug=debug_mode)

