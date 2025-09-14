import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from call_function import call_function, available_functions
from config import MAX_ITERS
from prompts import system_prompt


def main():
    # Load environment variables from .env file (e.g., GEMINI_API_KEY)
    load_dotenv()

    # Check if verbose flag is passed
    verbose = "--verbose" in sys.argv

    # Collect non-flag arguments (the user’s actual prompt)
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    # If no arguments provided, show usage instructions and exit
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    # Get the Gemini API key from environment variables
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Combine all user arguments into a single prompt string
    user_prompt = " ".join(args)

    # Print the user prompt if verbose mode is enabled
    if verbose:
        print(f"User prompt: {user_prompt}\n")

    # Create the initial user message to send to the model
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # Control loop to prevent infinite generation cycles
    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)

        try:
            # Generate response content from the model
            final_response = generate_content(client, messages, verbose)
            if final_response:
                # If a final text response is generated, print it and stop
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            # Catch and print any errors from generate_content
            print(f"Error in generate_content: {e}")


def generate_content(client, messages, verbose):
    # Call the Gemini model with the current conversation state
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],  # Functions the model can call
            system_instruction=system_prompt,  # System-level guidance prompt
        ),
    )

    # Print token usage details if verbose mode is enabled
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    # Append model candidates (possible responses) to the conversation
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    # If no function calls were requested, return the text response
    if not response.function_calls:
        return response.text

    # If function calls are requested, execute them
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")

        # Print function responses in verbose mode
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

        # Collect the function response parts
        function_responses.append(function_call_result.parts[0])

    # If no valid function responses were returned, stop with an error
    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    # Add the function responses back into the conversation context
    messages.append(types.Content(role="user", parts=function_responses))


if __name__ == "__main__":
    # Run main only when executing this script directly
    main()
