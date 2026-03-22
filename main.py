import os, argparse
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("API Key not found")

client = genai.Client(api_key=api_key)

def main():
    response = llm_request("Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
    display_token_data(metadata=response.usage_metadata)

    print(f"Repsonse:\n{response.text}")


def llm_request(content: str):
    model = 'gemini-2.5-flash'
    
    return client.models.generate_content(
        model=model, contents=content
    )


def display_token_data(metadata):
    if metadata == None:
        raise RuntimeError("API Request FAILED!")
    else:
        print(f"Prompt tokens: {metadata.prompt_token_count}")
        print(f"Response tokens: {metadata.candidates_token_count}")


if __name__ == "__main__":
    main()


