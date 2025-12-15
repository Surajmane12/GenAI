from google.genai import Client
from dotenv import load_dotenv

import json
import os
import requests
from pydantic import BaseModel,Field
from typing import Optional
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = Client(api_key=api_key)

def get_weather(city:str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "Something went wrong!!"


config = {
    "response_mime_type": "application/json",
    "response_schema": {
        "type": "object",
        "properties": {
            "step": {
                "type": "string",
                "enum": ["START", "PLAN", "TOOL", "OBSERVE", "OUTPUT"]
            },
            "content": {"type": "string"},
            "tool": {"type": "string"},
            "input": {"type": "string"},
            "output": {"type": "string"}
        },
        "required": ["step"]
    }
}


available_tools = {
"get_weather":get_weather
}

MODEL_PROMPT = '''
 You are an expert AI assistance in resolving user queries using chai of thought. You work on START, PLAN and OUTPUT steps. You need to first PLAN what needs to be done. The PLAN can be multiple steps. Once you think enough PLAN has been done, finally you give an OUTPUT. 
 You can also call a tool if required from the list of available tools
 for every tool call wait for the observer step which is the output from the called tool

 Rules: - Strictly Follow the given JSON output format 
 - Only run one step at a time. 
 - The sequence of steps is START(where user gives an input), PLAN(That can be multiple times) and finally OUTPUT(which is going tp the displayed to the user) 

Output JSON Format:
{"step":"START" | "PLAN" | "OUTPUT" | "TOOL" | "OBSERVE", "content":"string", "tool":"string", "input":"string"}

 
 Available Tools:
 -get_weather: Takes city name as an input string and returns the weather info about the city in the degree Celcius

 Example 1: "
   START: Hey, can you give me 5+4*9/3 
   PLAN: {step:"PLAN":"content":"Seems user interested in maths"} 
   PLAN: {step:"PLAN":"content":"looking at the problem, we should solve by BODMAS Method"} 
   PLAN: {step:"PLAN":"content":"Yes, the BODMAS will be the better for solving this"} 
   PLAN :{step:"PLAN":"content":"first we will multiply the 4 and 9 which will be 36"} 
   PLAN: {step:"PLAN":"content":"Now the equation will be 5+36/3"} 
   PLAN: {step:"PLAN":"content":"Now we will divide 36 by 3 which will give 12"} 
   PLAN: {step:"PLAN":"content":"Now the equation will be 5+12"} 
   PLAN: {step:"PLAN":"content":"Now the we will add 5 and 12 which will give the 17"} 
   PLAN: {step:"PLAN":"content":"Great! we have solved this equation and its answer is: 17"} 

 Example 2:
 START : what is the weather of Mumbai?
 PLAN  : {step: "PLAN":"content":"Seems like user is interested to know the weather of city Mumbai of India"}
 PLAN  : {step: "PLAN": "content":"Let's see if we have any available tool from list of available tools"}
 PLAN  : {step: "PLAN": "content":"Great! We have  get_weather  tool available for this."}
 PLAN  : {step: "PLAN": "content":"I need to call get_weather tool for mumbai as input for City"}
 PLAN  : {step: "PLAN": "tool":"get_weather" "input":"mumbai"}
 PLAN  : {step: "OBSERVER": "tool": "get_weather" "output":"The temp of mumbai is cloudy with 20 C"}
 PLAN  : {step: "PLAN": "content":"Great, I got the weather about the mumbai"}
 PLAN  : {step: "OUTPUT": "content":"The current weather in mumbai is 20 C with some cloudy sky"}

 '''



print("\n\n\n")



class WeatherResult(BaseModel):
    step: str  = Field(...,description="The ID of the step. Example: PLAN, OUTPUT,TOOL,etc.")
    content: Optional[str] = Field(None, description="The optional string content for call")
    tool: Optional[str] = Field(None, description="The ID of the tool to call")
    input: Optional[str]  =Field(None, description="The input query provided by user")

chat_config = {
    **config,
    "system_instruction": MODEL_PROMPT
}

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=chat_config
)


message_history = [
    {"role":"SYSTEM", "content": MODEL_PROMPT}
]

chat.send_message(MODEL_PROMPT)

while True:
    user_query = input("User: ")
    response = chat.send_message(user_query)

    while True:
    

        raw_result = response.text
    
        # parsed_result = json.loads(raw_result)
        parsed_result =  WeatherResult.model_validate_json(raw_result)

        if parsed_result.step == "START":
            print("Starting LLM Loop:", parsed_result.content)
            response = chat.send_message("Continue")
            continue
    


        if parsed_result.step == "TOOL":

            calling_tool = parsed_result.tool
            tool_input = parsed_result.input

        # 🚨 CASE 1: TOOL intent, but no actual tool call yet
            if not calling_tool or not tool_input:
                print("🧠 Tool intent detected, waiting for explicit tool call...")
                response = chat.send_message(
                "Please emit a TOOL step with valid 'tool' and 'input' fields."
                )
                continue

        # 🚨 CASE 2: Invalid tool name
            if calling_tool not in available_tools:
                print(f"❌ Unknown tool requested: {calling_tool}")
                response = chat.send_message(
                    f"The tool '{calling_tool}' is not available. Choose from {list(available_tools.keys())}."
                )
                continue

                # ✅ CASE 3: Valid tool execution
            print(f"🔨 Calling tool: {calling_tool}({tool_input})")

            tool_response = available_tools[calling_tool](tool_input)

            response = chat.send_message(json.dumps({
            "step": "OBSERVE",
            "tool": calling_tool,
            "output": tool_response
            }))

            continue

        if parsed_result.step == "OBSERVE":
            response = chat.send_message("Continue")
            continue
    
        if parsed_result.step == "PLAN":
            print("Thinking Process:", parsed_result.content)
            response = chat.send_message("Continue")
            continue

        if parsed_result.step == "OUTPUT":
            print("Result LLM Loop:", parsed_result.content)
            break

    print("\n\n\n")

    print(response.text)
