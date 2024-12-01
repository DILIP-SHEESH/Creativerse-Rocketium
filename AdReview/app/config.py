import os

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 's3cr3tK3yForFlaskApp')  # Set a default for local use
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
