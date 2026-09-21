import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_target_file = working_directory_abs == os.path.commonpath([working_directory_abs, os.path.abspath(target_file)])
    except Exception as e:
        return f"Error: failed resolving path - {e}"

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{target_file}"'

    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    with open(target_file, "r") as file:
        content = file.read(MAX_CHARS)
        if file.read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
