import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin123@localhost/user_auth"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("hoeunsorunpythontest@gmail.com")
    MAIL_PASSWORD = os.getenv("hoeunsorun001")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")
