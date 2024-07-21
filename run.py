# Import the Flask application instance from the app package
from app import app

# Check if this script is executed as the main program and not imported as a module
if __name__ == '__main__':
    # Run the Flask application
    # debug=True enables debug mode, which provides detailed error messages and auto-reloads the server upon code changes
    # port=8082 specifies the port on which the Flask application will listen for incoming requests
    app.run(debug=True, port=8082)