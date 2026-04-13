import os
from functions.helper_functions import get_abs_path
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        tar_dir, is_valid = get_abs_path(working_directory=working_directory, path=file_path)

        if not is_valid:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(tar_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        # Creates any missing dirs
        os.makedirs(os.path.dirname(tar_dir), exist_ok=True)

        with open(tar_dir, 'w') as f:
            chars_written = f.write(content)

        if chars_written != len(content):
            raise RuntimeError(f"write_file failed: expected {len(content)} chars, wrote {chars_written}")
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as err:
        return f'Error: {err}'
    
schema_write_to_file = types.FunctionDeclaration(
    name="write_file",
    description="Allow the llm the ability to update and modify files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write to the file",
            )
        },
        required=["file_path", "content"]
    ),
)