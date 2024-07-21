from flask import Flask
from flasgger import Swagger
from app.config.app_config import Config
from app.config.logging_config import configure_logging

# Initialize the Flask application
app = Flask(__name__, template_folder=Config.TEMPLATE_FOLDER, static_folder=Config.STATIC_FOLDER)
app.config.from_object(Config)

# Initialize Swagger for API documentation
swagger = Swagger(app)

# Configure logging
with app.app_context():
    configure_logging(app)

# Import and register the routes module to the app
from app import routes