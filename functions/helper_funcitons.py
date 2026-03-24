import os

def get_abs_path(working_directory, path):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, path))
    is_valid = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    return target_dir, is_valid