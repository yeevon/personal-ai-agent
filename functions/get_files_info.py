import os
from functions.helper_funcitons import get_abs_path
from pathlib import Path

def get_files_info(working_directory, directory ="."):
    file_data = []
    try:
        tar_dir = get_abs_path(working_directory=working_directory, path=directory)
        if not os.path.isdir(tar_dir):
            return f"f'Error: \"{tar_dir}\" is not a directory'"
        
        path = Path(tar_dir)
        for item in path.iterdir():
            name = item.name
            size = os.path.getsize(item)
            is_dir = item.is_dir()
            file_data.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")
            
    except Exception as err:
        return f"Error:{ err}"
    
    return "\n".join(file_data)