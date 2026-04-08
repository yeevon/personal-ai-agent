import os
from functions.helper_functions import get_abs_path
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        target_dir, is_valid = get_abs_path(working_directory=working_directory, path=file_path)

        if not is_valid:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'      
         
        if not os.path.isfile(target_dir):
            return f"Error: \"{target_dir}\" is not a file"
        
        return read_file(target_dir)
 
    except Exception as err:
        return f"Error: {err}"


def read_file(target_dir) -> str:
    try:
        with open(target_dir, 'r', encoding='utf-8') as file:
            content =  file.read(MAX_CHARS)

            if file.read(1):
                content += f'[...File "{target_dir}" truncated at {MAX_CHARS} characters]'
                
        return content 

    except Exception as err:
        raise RuntimeError(f"read_file failed: No such file or dir was found. - '{target_dir}' - {err}")
    
schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="CAT content from a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Returns the content of the spcified file",
            ),
        },
        required=["file_path"]
    ),
)