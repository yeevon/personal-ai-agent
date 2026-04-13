from .agent import agent_loop
from google.genai import types

import argparse


def main():
    args = get_cl_arg()
    user_prompts = [types.Content(
         role="user",
         parts=[types.Part(text=args.user_prompt)]
    )]

    agent_loop(user_prompts=user_prompts, args=args)


def get_cl_arg():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


if __name__ == "__main__":
    main()


