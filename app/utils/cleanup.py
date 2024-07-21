import os
import shutil

def cleanup_temp_files_only(temp_folder):
    """
    Cleans up temporary files and directories except for the 'transcripts' folder.

    Args:
        temp_folder (str): The path to the temporary folder to clean up.
    """
    for root, dirs, files in os.walk(temp_folder, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            if 'transcripts' not in file_path:
                os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if dir != 'transcripts':
                try:
                    os.rmdir(dir_path)
                except OSError:
                    shutil.rmtree(dir_path)
