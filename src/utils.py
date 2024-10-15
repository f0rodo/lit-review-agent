import os
import json
import logging

# Utility function to ensure folders exist
def ensure_folders_exist(folders):
    """
    Ensure that the specified folders exist.

    Args:
        folders (list): List of folder paths to check/create.
    """
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

# Utility function to clear a folder
def clear_folder(folder_path):
    """
    Clear all files in the specified folder.

    Args:
        folder_path (str): Path to the folder to clear.
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)

# Utility function to load rules from a JSON file
def load_rules(file_path):
    """
    Load rules from a JSON file.

    Args:
        file_path (str): Path to the JSON file containing rules.

    Returns:
        list: List of rules loaded from the file.
    """
    with open(file_path, 'r') as f:
        return json.load(f)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')