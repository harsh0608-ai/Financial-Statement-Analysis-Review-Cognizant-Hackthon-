import os

from dotenv import load_dotenv
from google import genai


# Load variables from .env
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY was not found in .env")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Send a simple test request
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Explain in one sentence what financial statement review means."
)

print("Gemini is working!")
print()
print("Response:")
print(response.text)