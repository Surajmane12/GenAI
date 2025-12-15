#tiktoken -> model provided by OpenAI to generate tokens!!
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey There! I am Suraj Mane"

tokens = enc.encode(text)

print(tokens)


decoded_token = enc.decode([25216, 3274, 0, 357, 939, 9568, 1255, 119328])
print(decoded_token)