from dotenv import load_dotenv
from functions.call_function import available_functions, call_function
from google.genai import types, Client
from .config import LOOPS, MODEL
from .system_prompt import system_prompt as sp

import os


load_dotenv()
_api_key = os.environ.get("GEMINI_API_KEY")

if _api_key is None:
        raise RuntimeError("API Key not found")

def agent_loop(user_prompts: list, args):
    client = Client(api_key=_api_key)
    model = MODEL
    messages = list(user_prompts)

    for _ in range(LOOPS):        
        response = _llm_request(client, model, messages)

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")  
            _display_token_data(metadata=response.usage_metadata)

        if not response.function_calls:
            print(f"Response:\n{response.text}")
            return
    
        func_results = []
        if response.candidates:
            for rc in response.candidates:
                if rc.content and rc.content.parts:
                    messages.append(types.Content(role="model", parts=rc.content.parts))

        for fc in response.function_calls:
            function_call_result = call_function(fc, args.verbose)

            if not function_call_result.parts:
                raise Exception(f"Error: {fc.name} parts list is empty")
            
            if not function_call_result.parts[0].function_response:
                raise Exception(f"Error: {fc.name} contains invalid response")

            func_results.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response}")
        
        messages.append(types.Content(role="user", parts=func_results))
    
    print(f"Error: unable to complete {messages}")
    return 1


def _llm_request(client, model, contents: list[types.Content]):    
    
    return client.models.generate_content(
        model=model, 
        contents=contents, # type: ignore
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=sp,
            temperature=0,
            )
    )


def _display_token_data(metadata):
    if metadata is None:
        raise RuntimeError("API Request FAILED!")
    else:
        print(f"Prompt tokens: {metadata.prompt_token_count}")
        print(f"Response tokens: {metadata.candidates_token_count}")