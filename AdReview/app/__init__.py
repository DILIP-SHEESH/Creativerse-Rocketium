from flask import Flask
from app.routes.main import main_bp  # Import main_bp here
from app.routes.company import company_bp
from app.routes.design import design_bp

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'jawoifaoppjf'
    # Register blueprints
    app.register_blueprint(main_bp)  # Register the landing page blueprint here
    app.register_blueprint(company_bp)
    app.register_blueprint(design_bp)

    return app
