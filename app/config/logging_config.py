import os
import logging
from logging.handlers import RotatingFileHandler
from flask import request, current_app

def configure_logging(app):
    """
    Configure logging for the Flask application.

    Args:
        app (Flask): The Flask application instance.

    This function sets up a rotating file handler that writes logs to a file.
    The log directory and file name are retrieved from the Flask app configuration.
    The log level is set to INFO and logs are formatted with a timestamp, logger name, log level, and message.
    """
    log_dir = current_app.config['LOG_DIR']
    log_file = current_app.config['LOG_FILE']
    log_path = os.path.join(log_dir, log_file)
    
    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Set log level to INFO
    app.logger.setLevel(logging.INFO)

    # Create a RotatingFileHandler
    handler = RotatingFileHandler(log_path, maxBytes=2*1024*1024, backupCount=5)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # Add the handler to the app's logger
    app.logger.addHandler(handler)

def log_request_info(app):
    """
    Log information about incoming requests.

    Args:
        app (Flask): The Flask application instance.

    This function logs the URL, method, and data of incoming requests.
    It is registered as a before_request handler in Flask.
    """
    @app.before_request
    def log_request():
        app.logger.info('Request URL: %s', request.url)
        app.logger.info('Request Method: %s', request.method)
        app.logger.info('Request Data: %s', request.data)

def log_response_info(app):
    """
    Log information about outgoing responses.

    Args:
        app (Flask): The Flask application instance.

    This function logs the status of outgoing responses.
    It is registered as an after_request handler in Flask.
    """
    @app.after_request
    def log_response(response):
        app.logger.info('Response Status: %s', response.status)
        return response