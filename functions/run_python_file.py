import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_path = os.path.commonpath([working_dir_abs, target_file])

        if not valid_path == working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not target_file.endswith(".py"):
             return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]

        if args is not None:
            command.extend(args)
        
        # capture_output=True to get stdout and stderr
        # text=True to get the answer in text and not in bytes.
        # timeout=30 to have a 30 seconds timeout and not allow the subprocess to run indefinitely
        # cwd is the working directory that we allow the subprocess to run in.
        result = subprocess.run(command, capture_output=True, text=True, timeout=30, cwd=working_dir_abs)

        output_string = []

        if result.returncode != 0:
            output_string.append(f"Process exited with code {result.returncode}")
        
        if not result.stdout and not result.stderr:
            output_string.append("No output produced")
        
        if result.stdout:
            output_string.append(f"STDOUT:\n{result.stdout}")

        if result.stderr:
            output_string.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output_string)


    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file=types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python file within the working directory or a subdirectory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path":types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file relative to the working directory."
            ),
            "args":types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional command-line arguments to pass to the Python file."
            )
        },
        required=["file_path"]
    )
)