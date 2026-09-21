import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))
        valid_target_dir = working_directory_abs == os.path.commonpath([working_directory_abs, os.path.abspath(target_dir)])
    except Exception as e:
        return f"Error: failed resolving path - {e}"

    if not os.path.isdir(target_dir):
        return f'Error: "{target_dir}" is not a directory'

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    current_dir: list[str] = []
    for item in os.listdir(target_dir):
        try:
            current_dir.append(f"- {item}: file_size={os.path.getsize(os.path.join(target_dir, item))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, item))}")
        except Exception as e:
            return f"Error: failed getting file information - {e}"

    return "\n".join(current_dir)
