import os
from pathlib import Path

def get_files_info(working_directory, directory ="."):
    file_data = []
    try:
        working_dir_abs = os.path.abspath(working_directory)
        tar_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        is_valid_dir = os.path.commonpath([working_dir_abs, tar_dir]) == working_dir_abs

        if not is_valid_dir:
            return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
        
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