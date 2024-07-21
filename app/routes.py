from flask import render_template, request, redirect, url_for, send_from_directory, current_app, flash, after_this_request
import os
import uuid
from app.config.logging_config import log_request_info, log_response_info
from app.utils.audio_processing import process_video, allowed_file
from app.utils.file_handling import save_file, remove_file
from app.utils.file_deletion import remove_old_files
from app.utils.cleanup import cleanup_temp_files_only
from app import app

# Log request and response info
log_request_info(app)
log_response_info(app)

@app.route('/')
def index():
    """
    This endpoint renders the main index page for file upload.
    -------
    tags:
      - Main Page
    responses:
      '200':
        description: Main page rendered successfully.
        content:
          text/html:
            schema:
              type: string
              description: HTML content of the main page.
    """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    This endpoint handles file upload, processes the video, and returns the transcription document.
    -------
    tags:
      - File Upload
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The file to be uploaded.
      - name: language
        in: formData
        type: string
        required: true
        description: Language preference for the transcription ('en', 'de', 'tr').
    responses:
      '200':
        description: File uploaded and processed successfully.
        content:
          application/json:
            schema:
              type: object
              properties:
                filename:
                  type: string
                  description: The name of the processed transcription file.
      '400':
        description: Bad request or invalid file type.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Description of the error.
      '500':
        description: Internal server error.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Description of the error.
    """
    transcripts_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'transcripts')
    remove_old_files(transcripts_folder, max_age_seconds=60)

    if 'file' not in request.files or 'language' not in request.form:
        flash('No file part or language selected.')
        return redirect(request.url)
    
    file = request.files['file']
    language = request.form.get('language', 'en')
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        video_filename = f"{uuid.uuid4()}.mp4"
        file_path = save_file(file, video_filename, upload_folder)

        transcription = process_video(file_path, language)
        
        unique_filename = f"{uuid.uuid4()}.docx"
        transcripts_folder = os.path.join(upload_folder, 'transcripts')
        if not os.path.exists(transcripts_folder):
            os.makedirs(transcripts_folder)
        output_path = os.path.join(transcripts_folder, unique_filename)
        
        with open(output_path, 'w') as f:
            f.write(transcription)
        
        remove_file(file_path)

        return redirect(url_for('success', filename=unique_filename))
    else:
        return render_template('invalid_file.html')

@app.route('/success/<filename>')
def success(filename):
    """
    This endpoint renders the success page with a link to download the file.
    -------
    tags:
      - Success Page
    parameters:
      - name: filename
        in: path
        type: string
        required: true
        description: The name of the processed transcription file.
    responses:
      '200':
        description: Success page rendered successfully.
        content:
          text/html:
            schema:
              type: string
              description: HTML content of the success page.
      '404':
        description: File not found.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Description of the error.
    """
    return render_template('success.html', filename=filename)

@app.route('/download/<filename>')
def download_file(filename):
    """
    This endpoint allows the user to download the specified file.
    -------
    tags:
      - File Download
    parameters:
      - name: filename
        in: path
        type: string
        required: true
        description: The name of the file to be downloaded.
    responses:
      '200':
        description: File downloaded successfully.
        content:
          application/octet-stream:
            schema:
              type: string
              format: binary
              description: The binary content of the file.
      '404':
        description: File not found.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Description of the error.
      '500':
        description: Internal server error.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Description of the error.
    """
    directory = os.path.abspath(os.path.join(current_app.config['UPLOAD_FOLDER'], 'transcripts'))

    @after_this_request
    def remove_file_after_response(response):
        try:
            os.remove(os.path.join(directory, filename))
        except Exception as error:
            app.logger.error("Error removing file: %s", error)
        return response

    return send_from_directory(directory, filename, as_attachment=True)

@app.teardown_appcontext
def cleanup(exception=None):
    """
    This endpoint cleans up temporary files and directories after each request.
    -------
    tags:
      - Cleanup
    responses:
      '200':
        description: Cleanup completed successfully.
    """
    cleanup_temp_files_only(current_app.config['UPLOAD_FOLDER'])