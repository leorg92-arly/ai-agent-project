import os
import argparse
import sys

# Importing third party libraries
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Importing from project files
from prompts import system_prompt
from call_functions import available_functions
from call_functions import call_function
from config import MAX_ITER

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Validating for api_key
    if not api_key:
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
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    # Call Gemini Loop
    for _ in range(MAX_ITER):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")
    
    print(f"Maximum iterations ({MAX_ITER}) reached")
    sys.exit(1)

# Create a generative response
def generate_content(client, messages, is_verbose):
    # Calling Gemini
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        # temperature helps with consistency
        config=types.GenerateContentConfig(tools=[available_functions],
                                             system_instruction=system_prompt,
                                             temperature=0
                                        ),
    )
    
    #Token Usage Metadata check
    if not response.usage_metadata:
        raise RuntimeError("Usage metadata is empty")

    # Print response and token usage metadata to terminal
    if is_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print("Response:")

    # Checks for response candidates (previous responses) and add them to the messages list.
    # It's for keeping history of the conversation.
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)
    
    # Break the loop and return to main
    if not response.function_calls:
        return response.text

    response_list = []

    result_function_calls(response, is_verbose, response_list)
    
    messages.append(types.Content(role="user", parts=response_list))

# Handles the function calls of the agent
def result_function_calls(response, is_verbose, response_list):
    if not response.function_calls:
        print(response.text)
        return

    for function_call in response.function_calls:
        result = call_function(function_call, is_verbose)

        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
            ):
            raise Exception(f"Empty function response for {function_call.name}")
        
        if is_verbose:
            print(f"-> {result.parts[0].function_response.response}")

        # The function doesn't return anything. Lists are mutable objects.
        response_list.append(result.parts[0])

if __name__ == "__main__":
    main()