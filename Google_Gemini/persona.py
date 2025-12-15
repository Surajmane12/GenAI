
from google.genai import Client
import json

client = Client(
    api_key=""
)

config = {
    "response_mime_type": "application/json",
    "response_schema": {
        "type": "object",
        "properties": {
            "step": {"type": "string"},
            "content": {"type": "string"}
        },
        "required": ["step", "content"]
    }
}
# Few Shot Prompt
MODEL_PROMPT = '''
  You are an AI Persona Assistant named Suraj Mane.
  You are acting on behalf of Suraj Mane who is 22 years old Tech enthusiatic and full stack developer. 
  Your main tech task is React JS, NodeJS, SQL and you are learning GenAI these days.

  Examples:
  Q: Hey
  A: Hey, whats up!
 '''

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        {
            "role": "model",
            "parts": [
                {"text": MODEL_PROMPT}
            ]
        },
        {
            "role": "user",
            "parts": [
                {"text": "Hey, how are you? "}
            ]
        }
    ]
)

print(response.text)
