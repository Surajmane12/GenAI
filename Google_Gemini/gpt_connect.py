from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


response = client.chat.completions.create(
    model="gpt-5.2",
    messages=[
        {
            "role":"user", 
            "content":"Hey There"
        }
    ]
)

print(response.choices[0].message.content)


