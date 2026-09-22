from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    # Import blueprint INSIDE factory
    from app.routes.webhook import webhook_bp

    # Register blueprint correctly
    app.register_blueprint(webhook_bp, url_prefix="/webhook")

    # Health check
    @app.route("/")
    def home():
        return {
            "app": "FinMate AI",
            "status": "running",
            "message": "Welcome to FinMate AI!"
        }

    return app