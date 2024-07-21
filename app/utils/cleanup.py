import os

def cleanup_temp_files_only(temp_folder):
    """
    Cleans up temporary files and directories in the specified folder,
    excluding any directories or files within directories named 'transcripts'.

    Args:
        temp_folder (str): The path to the temporary folder to clean up.
    """
    for root, dirs, files in os.walk(temp_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if 'transcripts' not in file_path:
                os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if dir != 'transcripts':
                os.rmdir(dir_path)