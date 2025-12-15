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
 You are an expert AI assistance in resolving user queries using chai of thought. You work on START, PLAN and OUTPUT steps. You need to first PLAN what needs to be done. The PLAN can be multiple steps. Once you think enough PLAN has been done, finally you give an OUTPUT. 
 Rules: - Strictly Follow the given JSON output format 
 - Only run one step at a time. 
 - The sequence of steps is START(where user gives an input), 
 PLAN(That can be multiple times) and finally 
 OUTPUT(which is going tp the displayed to the user) 
 Output JSON Format: {"Step":"START" | "PLAN" | "OUTPUT", "content": "string"} 
 Example" START: Hey, can you give me 5+4*9/3 PLAN: {step:"PLAN":"content":"Seems user interested in maths"} PLAN: {step:"PLAN":"content":"looking at the problem, we should solve by BODMAS Method"} PLAN: {step:"PLAN":"content":"Yes, the BODMAS will be the better for solving this"} PLAN :{step:"PLAN":"content":"first we will multiply the 4 and 9 which will be 36"} PLAN: {step:"PLAN":"content":"Now the equation will be 5+36/3"} PLAN: {step:"PLAN":"content":"Now we will divide 36 by 3 which will give 12"} PLAN: {step:"PLAN":"content":"Now the equation will be 5+12"} PLAN: {step:"PLAN":"content":"Now the we will add 5 and 12 which will give the 17"} PLAN: {step:"PLAN":"content":"Great! we have solved this equation and its answer is: 17"} 
 '''


# print("\n\n\n")
# message_history = [
#     {"role":"model", "content": MODEL_PROMPT}
# ]

# user_query = input("")
# message_history.append({"role":"user", "content": user_query})

# while True:
#     response = client.models.generate_content(
#          model="gemini-2.5-flash",
#          config=config,
#          contents=message_history
#     )


#     raw_result = response.text
#     message_history.append({"role":"model","content":raw_result})
#     parsed_result = json.loads(raw_result)


#     if parsed_result.get("step")=="START":
#         print("Starting LLM Loop",parsed_result.get("content"))
#         continue

#     if parsed_result.get("step")=="PLAN":
#         print("Thinking Process",parsed_result.get("content"))
#         continue

#     if parsed_result.get("step")=="OUTPUT":
#         print("Result LLM Loop",parsed_result.get("content"))
#         break
print("\n\n\n")



chat_config = {
    **config,
    "system_instruction": MODEL_PROMPT
}

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=chat_config
)



# system / model prompt
chat.send_message(MODEL_PROMPT)


user_query = input("User: ")
response = chat.send_message(user_query)

while True:
    

    raw_result = response.text
    parsed_result = json.loads(raw_result)

    if parsed_result.get("step") == "START":
        print("Starting LLM Loop:", parsed_result.get("content"))
        response = chat.send_message("Continue")
        continue

    if parsed_result.get("step") == "PLAN":
        print("Thinking Process:", parsed_result.get("content"))
        response = chat.send_message("Continue")
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("Result LLM Loop:", parsed_result.get("content"))
        break

print("\n\n\n")
# response = client.models.generate_content(
#     model="gemini-2.5-flash",
     
     

#     # REQUIRED for JSON output
#      config=config,

#     contents=[
#         {
#             "role": "model",
#             "parts": [{"text": MODEL_PROMPT}]
#         },
#         {
#             "role": "user",
#             "parts": [{"text": "Give me a high protein veg soya meal"}]
#         },
#         {
#             "role": "model",
#             "parts": [
#                 {"text": json.dumps({"step": "START", "content": "Plan a high protein diet for weight gain."})}
#             ]
#         },
#         # We are manually adding the responses given by AI  here below
#          {
#             "role": "model",
#             "parts": [
#                 {"text": json.dumps({"step": "PLAN", "content": "I apologize for the previous incorrect response. It seems there was a misunderstanding of your request. I will now plan to provide you with a high protein vegetarian meal focusing on soya."})}
#             ]
#         },
#         # {
#         #     "role": "model",
#         #     "parts": [
#         #         {"text": json.dumps({"step": "START", "content": "User wants a cake recipe."})}
#         #     ]
#         # },


#         {
#             "role": "model",
#             "parts": [
#                 {"text": json.dumps({
#   "step": "PLAN",
#   "content": "The user wants a cake recipe. I need to choose a common and relatively simple cake, like a vanilla or chocolate cake, and list the ingredients with quantities, followed by clear, numbered instructions for preparation and baking. I will focus on a simple yet delicious recipe to ensure it's easy to follow."
# })}
#             ]
#         },
    #      {
    #         "role": "model",
    #         "parts": [
    #             {"text": json.dumps({"step": "OUTPUT", "content": "Here is a recipe for a Classic Vanilla Cake:INGREDIENTS:1 1/2 cups all-purpose flour1 1/2 teaspoons baking powder1/4 teaspoon salt1/2 cup (1 stick) unsalted butter, softened1 cup granulated sugar2 large eggs1 teaspoon vanilla extract1/2 cup milkINSTRUCTIONS:1. Preheat your oven to 350°F (175°C). Grease and flour an 8-inch round cake pan.2. In a medium bowl, whisk together the flour, baking powder, and salt. Set aside.3. In a large bowl, cream together the softened butter and granulated sugar with an electric mixer until light and fluffy (about 2-3 minutes).4. Beat in the eggs one at a time, mixing well after each addition. Stir in the vanilla extract.5. Gradually add the dry ingredients to the wet ingredients, alternating with the milk, beginning and ending with the dry ingredients. Mix until just combined and smooth, being careful not to overmix.6. Pour the batter into the prepared cake pan and spread evenly.7. Bake for 30-35 minutes, or until a wooden skewer inserted into the center comes out clean.8. Let the cake cool in the pan for 10 minutes before inverting it onto a wire rack to cool completely.9. Once cooled, frost with your favorite vanilla or chocolate buttercream frosting. Enjoy!"})}]
    #      }
        
    # ]

# )

print(response.text)
