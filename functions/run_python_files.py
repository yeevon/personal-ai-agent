import os, subprocess
from functions.helper_funcitons import get_abs_path
from google.genai import types

def run_python_files(working_directory, file_path, args=None):
    try:
        tar_dir, is_valid = get_abs_path(working_directory=working_directory, path=file_path)

        if not is_valid:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(tar_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif tar_dir[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", tar_dir]
        if args:
            command.extend(args)

        completed_process = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, timeout=30)

        output = ""
        if completed_process.returncode != 0:
            output += f"Process exited with code {completed_process.returncode}\n"
        
        if not completed_process.stderr and not completed_process.stdout:
            output += "No output produced"
        else:
            output += f"STDOUT: {completed_process.stdout}\n"
            output += f"STDERR: {completed_process.stderr}\n"

        return output
    
    except Exception as err:
        return f'Error: executing Python file: {err}'
    
schema_run_python_files = types.FunctionDeclaration(
    name="run_python_files",
    description="Allow the llm to run execute python files located in specific directories",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the python file to run, relative to working dir.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of argument to pass to the python script"
            )
        },
        required=["file_path"]
    ),
)