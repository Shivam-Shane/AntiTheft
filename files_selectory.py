import os
import glob
from logger import logging

def get_most_recent_files(directory, extensions):
    """
    Get the most recent file for each type from a specified directory.

    :param directory: The directory to scan for files.
    :param extensions: A list of file extensions to look for (e.g., ['.jpg', '.mp4', '.wav']).
    :return: A dictionary with file extensions as keys and the most recent file paths as values.
    """
    most_recent_files = {}

    for ext in extensions:
        # Use glob to find all files with the specified extension
        files = glob.glob(os.path.join(directory, f"*{ext}"))
        
        if files:
            # Sort the files by modification time and get the most recent one
            most_recent_file = max(files, key=os.path.getmtime)
            most_recent_files[ext] = most_recent_file
            logging.info(f"Most recent {ext} file: {most_recent_file}")

    return most_recent_files