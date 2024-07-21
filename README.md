# Transcriber Flask App

This is a Flask-based web application that allows users to upload video files and receive transcriptions. The application uses `moviepy` for video processing and `speech_recognition` for extracting text from audio.

## Features

- Upload video files (mp4, wav)
- Extract audio from video segments
- Transcribe audio to text
- Download the transcription as a document
- Clean up temporary files after processing
- Bootstrap 5.3.3 for responsive design

## Requirements

- Python 3.10.14
- Flask 2.2.5
- Werkzeug 2.2.3
- python-docx 1.1.0
- SpeechRecognition 3.8.1
- moviepy 1.0.3
- flasgger 0.9.7.1
- ffmpeg 1.4
- python-dotenv 1.0.1
- pyflac 2.2.0

## Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/Transcriber-Flask-App.git
    cd Transcriber-Flask-App
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file in the root directory with the following content:**
    ```env
    UPLOAD_FOLDER=../temp
    TEMPLATE_FOLDER=../templates
    STATIC_FOLDER=../static
    LOG_DIR=logs
    LOG_FILE=app.log
    ALLOWED_EXTENSIONS=mp4,wav
    SWAGGER_TITLE=Transcriber API
    SWAGGER_DESCRIPTION=This is the Transcriber API documentation.
    ```

5. **Run the application:**
    ```bash
    python run.py
    ```

6. **Access the application:**
    Open your browser and go to `http://127.0.0.1:8082`.

## Project Structure

### Root Directory
- `.env`: Environment variables
- `requirements.txt`: Python dependencies
- `run.py`: Entry point to run the Flask application

### app/
- `__init__.py`: Initialize Flask app and register routes
- `routes.py`: Application routes and request handlers

#### app/config/
- `config.py`: Configuration settings loaded from .env
- `logging_config.py`: Logging configuration

#### app/utils/
- `audio_processing.py`: Functions for processing video and extracting audio
- `file_handling.py`: Functions for saving and removing files
- `file_deletion.py`: Function for removing old files
- `cleanup.py`: Function for cleaning up temporary files

### templates/
- `index.html`: Main page template for file upload
- `success.html`: Success page template with download link
- `invalid_file.html`: Error page template for invalid file uploads

### static/css/
- `bootstrap-grid.css`
- `bootstrap-grid.min.css`
- `bootstrap-reboot.css`
- `bootstrap-reboot.min.css`
- `bootstrap-utilities.css`
- `bootstrap-utilities.min.css`
- `bootstrap.css`
- `bootstrap.min.css`
- `styles.css`: Custom styles

### static/js/
- `bootstrap.bundle.min.js`

### temp/
- Temporary storage for uploaded and processed files

### logs/
- Directory for log files

## Usage

- **Upload a File:** On the main page, select a video file and a language for transcription, then click "Upload".
- **Download Transcription:** After processing, download the transcription document from the success page.

## Logging

Logs are stored in the `logs` directory. The logging configuration is set up to use a rotating file handler with a maximum file size of 2MB and a backup count of 5.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
