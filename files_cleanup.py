import os
import time

# Set the log file name dynamically
os.environ["LOG_FILE_NAME"] = "delete_old_files.log"
from logger import logging
def delete_old_files(folder_path, days_old=1):
    """
    Delete files older than the specified number of days in the given folder.
    
    Args:   folder_path: The path to the folder to clean up.
            days_old: The age of the files to delete, in days (default is 1 day).
    Returns None
    """
    # Get the current time
    current_time = time.time()
    logging.info(f"Deleting old files from folder {folder_path} at time {current_time}")
    # Check if the folder exists
    if not os.path.exists(folder_path):
        logging.error(f"Error: The folder {folder_path} does not exist.")
        return

    # Loop through the files in the directory
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if it is a file (not a directory)
        if os.path.isfile(file_path):
            # Get the file's last modified time
            file_age = current_time - os.path.getmtime(file_path)

            # Check if the file is older than the specified number of days
            if file_age > days_old * 86400:  # 86400 seconds in a day
                try:
                    os.remove(file_path)
                    logging.info(f"Deleted old file: {file_path}")
                except Exception as e:
                    logging.error(f"Error deleting file {file_path}: {e}")
                finally:
                    logging.info(f"Finished deleting old files from folder {folder_path}")
            else:
                logging.info(f"File {file_path} is younger than {days_old} days, Nothing to delete")

if __name__ == "__main__":
    delete_old_files("captures", 1)  # Delete files older than 7 days