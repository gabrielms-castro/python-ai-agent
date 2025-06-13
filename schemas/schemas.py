from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file (up to a maximum character limit) located within the working directory. Returns an error if the file is outside the allowed directory, does not exist, or cannot be read.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the target file, based on the working directory. Only files within the working directory are allowed.",
            ),
        },
    ),
)   

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a Python file located within the working directory. "
        "Returns the standard output and error messages (if any). "
        "Fails if the file is outside the working directory, does not exist, or execution results in an error."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Relative path to the Python file to be executed, based on the working directory. "
                    "Only files within the working directory are permitted."
                ),            
            ),
        },
    ),
)   

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Writes text content to a file within the working directory. "
        "Creates parent directories if they do not exist. "
        "Returns an error if the path is outside the working directory, targets a directory instead of a file, or writing fails."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Relative path to the file to be written, based on the working directory. "
                    "The file will be created if it does not exist."
                ),
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The text content to write into the specified file. "
                    "Any existing file at the path will be overwritten."
                ),
            ),
        },
    ),
)
