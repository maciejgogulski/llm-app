from .llm import bp as llm_bp
from .rag import bp as rag_bp

# Optional helper to register all routes at once
def register_blueprints(app):
    app.register_blueprint(llm_bp)
    app.register_blueprint(rag_bp)
