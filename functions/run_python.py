import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    """
    Executes a Python file inside the specified working directory and returns its output.

    Args:
        working_directory (str): The base directory where execution is allowed.
        file_path (str): Path to the Python file, relative to the working directory.
        args (list, optional): Extra command-line arguments to pass to the Python file.

    Returns:
        str: The captured output (stdout and/or stderr), or an error message if execution fails.
    """

    # Convert working directory and file path into absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Security check: ensure file path stays inside the working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # Ensure file exists
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    # Only allow Python files
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        # Build the command to execute the Python file
        commands = ["python", abs_file_path]
        if args:
            commands.extend(args)  # Add optional arguments if provided

        # Run the subprocess, capturing stdout and stderr with a timeout
        result = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,  # Prevent infinite loops or hangs
            cwd=abs_working_dir,  # Ensure execution happens in working directory
        )

        output = []

        # Capture stdout (program output)
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")

        # Capture stderr (errors or warnings)
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        # Append return code if non-zero (indicates errors)
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        # Return combined output, or fallback if nothing was produced
        return "\n".join(output) if output else "No output produced."

    except Exception as e:
        # Handle unexpected subprocess or OS-level errors
        return f"Error: executing Python file: {e}"


# Define schema so the LLM knows how to call this function
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],  # file_path must always be provided
    ),
)
