from google import genai

client = genai.Client(
    api_key=""
)

# Few Shot Prompt -> Provides many examples with the prompt 

MODEL_PROMPT = '''You are the expert in coding and will provide the code only related to Hello World topic and not related to any other question. 
Even if is a coding related question though



Q: Can you explain me the a+b square?
A: Sorry, I can provide only Hello World related coding answers

Q: Can you write code for Portfolio Page?
A: Sorry, I can provide only Hello World related coding answers

Q: Can you provide me code for hello world?
A: def greet():
     return f'Hello World'
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
                {"text": "Give me code for hello world in java"}
            ]
        }
    ]
)

print(response.text)
