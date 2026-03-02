from flask import Flask, send_from_directory
from dotenv import load_dotenv
import os

from .extensions import mongo
from .webhook.routes import webhook

def create_app():
    load_dotenv()
    print("ii")

    app = Flask(__name__, static_folder="../ui", static_url_path="/ui")

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")

    mongo.init_app(app)

    app.register_blueprint(webhook)

    @app.route("/")
    def home():
        return "Webhook server running"

    @app.route("/ui")
    def ui():
        return send_from_directory("../ui", "index.html")

    return app