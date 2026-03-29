import os
from google import genai
from google.genai import types

# Working directory is set by the user. Limits the scope of the AI agent.
# directory is a directory within the working directory. Set by the AI agent.
def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir])

        if not valid_target_dir == working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        dir_items = os.listdir(target_dir)

        build_string = ""
        for item in dir_items:
            build_string += f"- {item}: file_size={os.path.getsize(os.path.join(target_dir, item))}, is_dir={os.path.isdir(os.path.join(target_dir, item))}\n"
        
        return build_string
    except Exception as e:
        return f"Error: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
    
