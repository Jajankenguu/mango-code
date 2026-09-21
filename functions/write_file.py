import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_target_file = working_directory_abs == os.path.commonpath([working_directory_abs, os.path.abspath(target_file)])
    except Exception as e:
        return f"Error: failed resolving path - {e}"

    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    try:
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
    except Exception as e:
        return f'Error: Could not create parent directories: {e}'
    
    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{target_file}" as it is a directory'

    with open(target_file, "w") as file:
        file.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
