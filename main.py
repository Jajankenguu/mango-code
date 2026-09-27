import sys
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from skills.call_function import available_functions
from skills import call_function


def main():
    print("Hello from mango-code!")

    load_dotenv()

    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    )

    parser = argparse.ArgumentParser(description="Mangobot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):
        response = client.chat.completions.create(
            model="qwen3.6:35b-a3b",
            messages=messages,
            temperature=0,
            tools=available_functions,
        )
        if response == None:
            raise RuntimeError("failed API request")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function.call_function(tool_call, args.verbose)
                if not result_message["content"]:
                    raise Exception("Error: resulting content of tool call empty")
                messages.append(result_message)
                if args.verbose:
                    print(f"-> {result_message['content']}")
        else:
            print("Response:")
            print(message.content)
            return
    print("Error: agent loop limit reached before producing final result")
    sys.exit(1)


if __name__ == "__main__":
    main()
