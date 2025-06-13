import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import call_function

from schemas.schemas import (
    schema_get_files_info,
    schema_get_files_content,
    schema_run_python_file,
    schema_write_file
)

def main():
    load_dotenv()
    
    # Arguments
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    if not args:
        print("Usage: python main.py '<your prompt>'")
        sys.exit(1)

    # AI Agent Settings
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_api_key)
    model_name = "gemini-2.0-flash-001"
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """   

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=sys.argv[1])]
        )
    ]

    
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_files_content,
            schema_run_python_file,
            schema_write_file
        ]
    )     
    
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
        )
    )

    if verbose:
        print("User prompt: {user_prompt}".format(user_prompt=sys.argv[1]))
        print("Prompt tokens: {prompt_tokens}".format(prompt_tokens=response.usage_metadata.prompt_token_count))
        print("Response tokens: {response_tokens}".format(response_tokens=response.usage_metadata.candidates_token_count))
    
    if not response.function_calls:
        print("\nResponse:\n", response.text)
    
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")    
    
    
if __name__ == "__main__":
    main()