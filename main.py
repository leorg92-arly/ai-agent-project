import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_functions import available_functions

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Check for api_key
    if api_key == None:
        raise RuntimeError("Create a valid API key first!")

    # Create a client for Google Gen AI
    client = genai.Client(api_key=api_key)

    # User text input
    parser = argparse.ArgumentParser(description="AI Code Agent")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt` as the contents for Gemini call.

    # Message Content List
    messages = [types.Content(role="user", 
                              parts=[types.Part(text=args.user_prompt)])
                ]
    
    # Call Gemini
    generate_content(client, messages, args.verbose)

# Create a generative response
def generate_content(client, messages, is_verbose):
    # Calling Gemini
    response = client.models.generate_content(
        model = 'gemini-2.5-flash', 
        contents = messages,
        # temperature helps with consistency
        config = types.GenerateContentConfig(tools=[available_functions]
                                             ,system_instruction=system_prompt
                                             ,temperature=0),
    )
    
    #Token Usage Metadata
    if not response.usage_metadata:
        raise RuntimeError("Usage metadata is empty")
    
    # Print response and token usage metadata to terminal
    if is_verbose:
        print(f"User prompt: {messages[0].parts[0].text}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print("Response:")
        print_function_calls(response)
    else:
        print_function_calls(response)

def print_function_calls(response):
    if response.function_calls:
       for function_call in response.function_calls:
           print(f"Calling function: {function_call.name}({function_call.args})")
    
    else:
       print(response.text)

if __name__ == "__main__":
    main()

