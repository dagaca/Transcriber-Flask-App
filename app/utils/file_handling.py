import os
from werkzeug.utils import secure_filename

def save_file(file, filename, upload_folder):
    """
    Save the uploaded file to the specified folder.

    Args:
        file (FileStorage): The uploaded file.
        filename (str): The name to save the file as.
        upload_folder (str): The folder to save the file in.

    Returns:
        str: The path to the saved file.
    """
    filename = secure_filename(filename)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    return file_path

def remove_file(file_path):
    """
    Remove the specified file if it exists.

    Args:
        file_path (str): The path to the file to be removed.
    """
    if os.path.exists(file_path):
        os.remove(file_path)