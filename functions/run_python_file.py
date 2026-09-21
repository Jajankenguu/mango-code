import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        try:
            working_directory_abs = os.path.abspath(working_directory)
            target_file = os.path.normpath(
                os.path.join(working_directory_abs, file_path)
            )
            valid_target_file = working_directory_abs == os.path.commonpath(
                [working_directory_abs, os.path.abspath(target_file)]
            )
        except Exception as e:
            return f"Error: failed resolving path - {e}"
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'"{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)
        result = subprocess.run(
            command,
            cwd=working_directory_abs,
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        )
        output_str = ""
        if result.returncode != 0:
            output_str += f"Process exited with code {result.returncode}\n"
        elif result.stdout is None and result.stderr is None:
            output_str += "No output produced\n"
        else:
            output_str += f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        return output_str
    except Exception as e:
        return f"Error: executing Python file: {e}"
