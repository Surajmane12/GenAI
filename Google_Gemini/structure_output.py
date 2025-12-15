from google import genai

client = genai.Client(
    api_key=""
)

# Few Shot Prompt -> Provides many examples with the prompt 

MODEL_PROMPT = '''You are the expert in coding and will provide the code only related to Hello World topic and not related to any other question. 
Even if is a coding related question though

Rule:
- Strictly follow the output in JSON format

Output Format:
{{
"code":"string" or None
"isCodingQuestion": boolean
}}

Q: Can you explain me the a+b square?
A: {{"code":null, "isCodingQuestion": false}}

Q: Can you write code for Portfolio Page?
A: {{"code":null, "isCodingQuestion": false}}

Q: Can you provide me code for hello world?
A:{{"code":'def greet():
     return f'Hello World'',
    "isCodingQuestion": false}}

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
                {"text": "Give me a cake reciepe"}
            ]
        }
    ]
)

print(response.text)
