import os
import time

def remove_old_files(directory, max_age_seconds=60):
    """
    Remove files older than max_age_seconds from the specified directory.

    Args:
        directory (str): The directory to clean up.
        max_age_seconds (int): The maximum age of files in seconds. Files older than this will be removed.
    """
    current_time = time.time()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > max_age_seconds:
                os.remove(file_path)