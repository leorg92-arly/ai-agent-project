import os
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Check for api_key
    if api_key == None:
        raise RuntimeError("Create a valid API key first!")

    # Create a client for Google Gen AI
    client = genai.Client(api_key=api_key)

    # Create a generative response
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )
    
    #Token Usage Metadata
    if response.usage_metadata != None:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        raise RuntimeError("Usage metadata is empty")

    print(response.text)



if __name__ == "__main__":
    main()
