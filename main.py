from dotenv import load_dotenv
from google import genai
import os, argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
        raise RuntimeError("API Key not found")

def main():
    args = get_cl_arg()
    user_prompts = [genai.types.Content(
         role="user",
         parts=[genai.types.Part(text=args.user_prompt)]
    )]

    response = llm_request(user_prompts)
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")  
        display_token_data(metadata=response.usage_metadata)
        
    print(f"Response:\n{response.text}")


def get_cl_arg():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


def llm_request(contents: list[genai.types.Content]):    
    client = genai.Client(api_key=api_key)
    model = 'gemini-2.5-flash'
    
    return client.models.generate_content(
        model=model, contents=contents # type: ignore
    )


def display_token_data(metadata):
    if metadata is None:
        raise RuntimeError("API Request FAILED!")
    else:
        print(f"Prompt tokens: {metadata.prompt_token_count}")
        print(f"Response tokens: {metadata.candidates_token_count}")


if __name__ == "__main__":
    main()


