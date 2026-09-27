import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes to a file with a specified path, relative to the working directory, providing output on whether writing was successfull",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file to write to, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file",
                },
            },
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_target_file = working_directory_abs == os.path.commonpath(
            [working_directory_abs, os.path.abspath(target_file)]
        )
    except Exception as e:
        return f"Error: failed resolving path - {e}"

    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    try:
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
    except Exception as e:
        return f"Error: Could not create parent directories: {e}"

    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{target_file}" as it is a directory'

    with open(target_file, "w") as file:
        file.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
