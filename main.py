import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    if not args:
        print("Usage: python main.py '<your prompt>'")
        sys.exit(1)


    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_api_key)

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=sys.argv[1])]
        )
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    if verbose:
        print("User prompt: {user_prompt}".format(user_prompt=sys.argv[1]))
        print("Prompt tokens: {prompt_tokens}".format(prompt_tokens=response.usage_metadata.prompt_token_count))
        print("Response tokens: {response_tokens}".format(response_tokens=response.usage_metadata.candidates_token_count))
    print("\nResponse:\n", response.text)
    
if __name__ == "__main__":
    main()