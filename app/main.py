from flask import Flask
from app.config import Config
from app.routes.face_routes import face_bp

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(face_bp)
    return app