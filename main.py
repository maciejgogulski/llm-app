import os
from flask import Flask

app = Flask(__name__)

app.config['SERVER_PORT'] = os.getenv('SERVER_PORT', '5000')
debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'

app.config['GREETING'] = os.getenv('GREETING', 'Hello')

@app.route('/')
def home():
    return app.config['GREETING']

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['SERVER_PORT'], debug=debug_mode)

