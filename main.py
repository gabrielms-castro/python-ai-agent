import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import AGENT_MAX_ITERATIONS, MODEL_NAME, SYSTEM_PROMPT
from functions.call_function import (
    call_function,
    available_functions
)


def main():
    load_dotenv()
    
    # Arguments
    verbose = "--verbose" in sys.argv
    # args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    # if not args:
    #     print("Usage: python main.py '<your prompt>'")
    #     sys.exit(1)

    # AI Agent Settings
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_api_key)
    messages = []
    
    welcome_message = """
    Bem-vindo ao Coder AI!
    Este é um agente de IA que pode ajudar com tarefas de programação.
    Você pode fazer perguntas ou solicitar ações relacionadas a código.
    Digite 'sair' para encerrar a sessão."""
    print(f"{"="*100}{welcome_message}\n{"="*100}\n")
    while True:
        user_input = input("Usuário: ")
        if user_input.strip().lower() in ["sair", "exit", "quit", "fim", "q"]:
            print("Encerrando o Coder AI... Até logo!")
            sys.exit(1)
        
        messages.append(
            types.Content(
                role="user",
                parts=[types.Part(text=user_input)]
            )
        )
        iterations = 0
        while True:
            iterations += 1
            if iterations > AGENT_MAX_ITERATIONS:
                print(f"[WARNING] Maximum iterations ({AGENT_MAX_ITERATIONS}) reached.")
                sys.exit(1)
                
            try:
                final_response = generate_content(client, messages, verbose)
                if final_response:
                    print("\nFinal response: \n", final_response)
                    break
                    
            except Exception as e:
                print(f"Error in generate_content: {e}")                
                    

def generate_content(client, messages, verbose):

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=SYSTEM_PROMPT
        )
    )    
    
    if verbose:
        print("User prompt: {user_prompt}".format(user_prompt=sys.argv[1]))
        print("Prompt tokens: {prompt_tokens}".format(prompt_tokens=response.usage_metadata.prompt_token_count))
        print("Response tokens: {response_tokens}".format(response_tokens=response.usage_metadata.candidates_token_count))        

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(candidate.content)        

    if not response.function_calls:
        return response.text
    
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
        raise Exception("No function responses generated, exiting.")        
    
    messages.append(
        types.Content(
            role="tool",
            parts=function_responses
        )
    )
    

if __name__ == "__main__":
    main()