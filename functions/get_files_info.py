import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    """
    Lists files and directories inside a given directory, constrained to the working directory.

    Args:
        working_directory (str): The base directory where file access is allowed.
        directory (str): The relative path of the directory to list (default: current working directory).

    Returns:
        str: A formatted string containing file names, sizes, and whether they are directories,
             or an error message if the operation fails.
    """

    # Convert working directory and target directory into absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))

    # Security check: ensure target_dir is inside the permitted working directory
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # Validate that target_dir actually exists and is a directory
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        files_info = []

        # Loop through all items in the target directory
        for filename in os.listdir(target_dir):
            filepath = os.path.join(target_dir, filename)

            # Check if the current item is a directory
            is_dir = os.path.isdir(filepath)

            # Get file size (works for both files and directories, though size of dirs may vary by OS)
            file_size = os.path.getsize(filepath)

            # Append formatted info string for each file/directory
            files_info.append(
                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            )

        # Return the list joined into a single string with line breaks
        return "\n".join(files_info)

    except Exception as e:
        # Handle unexpected errors (permissions, IO issues, etc.)
        return f"Error listing files: {e}"


# Define schema so the LLM knows how to call this function
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. "
                "If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
