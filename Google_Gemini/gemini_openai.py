from openai import OpenAI

client = OpenAI(
    api_key="",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

response = client.responses.create(
    model="models/gemini-2.5-flash", 
    input=[
        {
            "role": "system",
            "content": "You are a friendly assistant."
        },
        {
            "role": "user",
            "content": "Hey, I am Suraj!"
        }
    ]
)

print(response.output_text)
