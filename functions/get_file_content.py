import os
from google.genai import types
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    """
    Reads the content of a file within the working directory.

    Args:
        working_directory (str): The base directory where file access is allowed.
        file_path (str): The relative path to the file to be read.

    Returns:
        str: The file contents (up to MAX_CHARS characters) or an error message.
    """

    # Get absolute paths for both the working directory and the target file
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Security check: prevent path traversal attacks
    # Ensures the target file path is inside the allowed working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # Check if the file exists and is a regular file
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        # Open the file in read mode
        with open(abs_file_path, "r") as f:
            # Read up to MAX_CHARS characters
            content = f.read(MAX_CHARS)

            # If the file is larger than MAX_CHARS, indicate it was truncated
            if os.path.getsize(abs_file_path) > MAX_CHARS:
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        return content

    except Exception as e:
        # Catch unexpected errors (e.g., permission issues) and return them
        return f'Error reading file "{file_path}": {e}'


# Define schema for the LLM so it knows how to call this function
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],  # file_path is required for the function to work
    ),
)
