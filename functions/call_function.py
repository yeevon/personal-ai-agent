from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_files_content
from functions.write_to_file import schema_write_to_file
from functions.run_python_files import schema_run_python_files
from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, 
        schema_get_files_content,
        schema_run_python_files,
        schema_write_to_file
        ]
)