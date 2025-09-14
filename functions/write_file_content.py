import os
from google.genai import types


def write_file(working_directory, file_path, content):
    # Get the absolute path of the working directory
    abs_working_dir = os.path.abspath(working_directory)
    # Build the absolute path for the target file
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Security check: prevent writing outside the working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # If the file doesn't exist, create any necessary parent directories
    if not os.path.exists(abs_file_path):
        try:
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"

    # Prevent writing if the target path is actually a directory
    if os.path.exists(abs_file_path) and os.path.isdir(abs_file_path):
        return f'Error: "{file_path}" is a directory, not a file'

    try:
        # Open the file in write mode and save the provided content
        with open(abs_file_path, "w") as f:
            f.write(content)

        # Return a success message including how many characters were written
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        # Catch and return any errors during the write process
        return f"Error: writing to file: {e}"


# Schema definition for integrating with Google GenAI functions
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
