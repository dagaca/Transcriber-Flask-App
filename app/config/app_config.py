import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Get the base path for uploads from environment variable or use 'temp' as default
    base_upload_folder = os.getenv('UPLOAD_FOLDER', 'temp')

    # Combine the base path with the current directory to get the absolute upload path
    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), base_upload_folder))

    # Get allowed file extensions from environment variable or use default set {'mp4', 'wav'}
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'mp4,wav').split(','))

    # Swagger configuration for API documentation
    SWAGGER = {
        'title': os.getenv('SWAGGER_TITLE', 'Transcriber API'),  # Title for Swagger UI
        'description': os.getenv('SWAGGER_DESCRIPTION', 'This is the Transcriber API documentation.')  # Description for Swagger UI
    }

    # Template and static folders for Flask application
    TEMPLATE_FOLDER = os.getenv('TEMPLATE_FOLDER', 'templates')  # Folder for HTML templates
    STATIC_FOLDER = os.getenv('STATIC_FOLDER', 'static')  # Folder for static files like CSS, JS, images

    # Logging configuration
    LOG_DIR = os.getenv('LOG_DIR', 'logs')  # Directory to store log files
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')  # Name of the log file