import os
from config import MAX_CHARS
from pathlib import Path

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        is_valid_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not is_valid_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_dir):
            return f"Error: \"{target_dir}\" is not a file"
        
        return read_file(target_dir)
 
    except Exception as err:
        return f"Error: {err}"
    


def read_file(target_dir) -> str:
    try:
        with open(target_dir, 'r') as file:
            content =  file.read(MAX_CHARS)
            if file.read(1):
                content += f'[...File "{target_dir}" truncated at {MAX_CHARS} characters]'
        return content 

    except Exception as err:
        raise RuntimeError(f"read_file failed: No such file or dir was found. - '{target_dir}'")