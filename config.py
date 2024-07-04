import os


class Config:
    SECRET_KEY = 'your_secret_key'  # Replace with a real secret key
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
