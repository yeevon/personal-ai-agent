import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    tar_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    print(f"\n\ndir test:\n{tar_dir}")


get_files_info("../calculator/calculator.py")