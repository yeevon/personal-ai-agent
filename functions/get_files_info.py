import os
from functions.helper_funcitons import get_abs_path
from pathlib import Path

def get_files_info(working_directory, directory ="."):
    file_data = []
    try:
        tar_dir, is_valid = get_abs_path(working_directory=working_directory, path=directory)

        if not is_valid:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(tar_dir):
            return f"f'Error: \"{tar_dir}\" is not a directory'"
        
        path = Path(tar_dir)
        for item in path.iterdir():
            file_data.append(f"- {item.name}: file_size={os.path.getsize(item)} bytes, is_dir={item.is_dir()}")
            
    except Exception as err:
        return f"Error:{ err}"
    
    return "\n".join(file_data)