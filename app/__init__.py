from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from dotenv import load_dotenv
from flask_migrate import Migrate
from .config import Config

import os

db = SQLAlchemy()
mail = Mail()

def create_app():
    load_dotenv()  # Load environment variables from .env

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)
    migrate = Migrate(app, db)  # Initialize Migrate after app creation

    with app.app_context():
        from . import routes  # Import routes inside the app context to avoid circular import

    return app
