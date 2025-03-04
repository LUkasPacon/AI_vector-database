import os
import openai
import traceback
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

def test_openai_api():
    """
    Test the OpenAI API connection using the provided API key.
    """
    # Get API key from environment variable or prompt user
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = input("Zadejte váš OpenAI API klíč: ")
        
    print(f"Používám API klíč: {api_key[:8]}...{api_key[-4:]}")
    
    # Set up the OpenAI client
    client = openai.OpenAI(api_key=api_key)
    
    try:
        # Test API connection with a simple completion request
        print("Odesílám požadavek na OpenAI API...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Jsi užitečný asistent."},
                {"role": "user", "content": "Kolik je 1+1?"}
            ]
        )
        
        # Print the response
        print("\nÚspěšné připojení k OpenAI API!")
        print(f"Model: {response.model}")
        print(f"Odpověď: {response.choices[0].message.content}")
        print(f"Tokeny: {response.usage.total_tokens}")
        
    except Exception as e:
        print(f"\nChyba při připojení k OpenAI API: {e}")
        print("\nPodrobnosti chyby:")
        traceback.print_exc()
        
if __name__ == "__main__":
    print("Test OpenAI API")
    print("--------------")
    test_openai_api() 