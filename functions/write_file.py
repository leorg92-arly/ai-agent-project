import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_write_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_path = os.path.commonpath([working_dir_abs, target_write_path])

        if not valid_path == working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_write_path):
                return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_write_path), exist_ok=True)
        
        with open(target_write_path, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
         return f"Error: {e}"
    

schema_write_file = types.FunctionDeclaration(
     name="write_file",
     description="Write to a new or existing file in the working directory or a subdirectory.",
     parameters=types.Schema(
          type=types.Type.OBJECT,
          properties={
               "file_path":types.Schema(
                    type=types.Type.STRING,
                    description="Path to the file relative to the working directory."
               ),
               "content":types.Schema(
                    type=types.Type.STRING,
                    description="Text to write or overwrite in the target file"
               )
          },
          required=["file_path", "content"]
     )
)