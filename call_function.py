from google.genai import types

# Import function implementations and their schemas
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file_content import write_file, schema_write_file
from config import WORKING_DIR

# Define all available functions and their schemas so the LLM knows what it can call
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def call_function(function_call_part, verbose=False):
    """
    Executes a function requested by the LLM.

    Args:
        function_call_part: The function call request from the LLM,
                            including the name and arguments.
        verbose (bool): Whether to print detailed logs.

    Returns:
        types.Content: A function response wrapped in a format
                       that the LLM can understand.
    """
    # Show what function is being called
    if verbose:
        print(
            f" - Calling function: {function_call_part.name}({function_call_part.args})"
        )
    else:
        print(f" - Calling function: {function_call_part.name}")

    # Map function names (strings) to their actual implementations
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    # Check if the requested function exists in the map
    function_name = function_call_part.name
    if function_name not in function_map:
        # Return an error response if function is unknown
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Prepare arguments for the function, adding the working directory
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIR

    # Execute the mapped function with the provided arguments
    function_result = function_map[function_name](**args)

    # Return the function result wrapped in a response format
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
