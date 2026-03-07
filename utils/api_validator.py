import os
from google import genai
from dotenv import load_dotenv

def validate_gemini_api_key() -> bool:
    """
    Validates if the Gemini API key is present in environment variables and works.
    
    Returns:
        bool: True if key is valid and connection works, False otherwise.
    """
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY")
    
    if not key:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        return False
        
    try:
        client = genai.Client(api_key=key)
        # Attempt a lightweight call to list models to verify authentication
        # In new SDK, client.models.list() is a generator
        # We just try to fetch one item
        next(client.models.list(config={"page_size": 1}))
        return True
    except Exception as e:
        print(f"Error validating Gemini API key: {e}")
        return False
