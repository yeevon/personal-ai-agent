import os

def get_abs_path(working_directory, path):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, path))
    is_valid_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not is_valid_dir:
        raise RuntimeError(f'Error: Cannot read "{path}" as it is outside the permitted working directory')
    
    return target_dir