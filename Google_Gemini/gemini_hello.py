from google.genai import Client

client = Client(
    api_key=""
)

# Zero Shot Prompt -> Provides directly instructions to the Model

MODEL_PROMPT = 'You are the expert in coding and will provide the code only related to Hello World topic and not related to any other question. Even if is a coding related question though'

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
                {"text": "How are you"}
            ]
        }
    ]
)

print(response.text)
