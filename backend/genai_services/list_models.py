from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

print("Models available to your API key:")
print()

for model in client.models.list():
    print(model.name)