from functions.helper_functions import get_abs_path
from google.genai import types
from pathlib import Path

import os


def get_files_info(working_directory, directory ="."):
    file_data = []
    try:
        tar_dir, is_valid = get_abs_path(working_directory=working_directory, path=directory)

        if not is_valid:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(tar_dir):
            return f"Error: \"{directory}\" is not a directory"
        
        path = Path(tar_dir)
        for item in path.iterdir():
            file_data.append(f"- {item.name}: file_size={os.path.getsize(item)} bytes, is_dir={item.is_dir()}")
            
    except Exception as err:
        return f"Error: {err}"
    
    return "\n".join(file_data)


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