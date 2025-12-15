from google.genai import Client
from dotenv import load_dotenv
import json
import os
import requests
import time

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = Client(api_key=api_key)

def get_weather(city: str):
    """Fetch weather for a city"""
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    return "Something went wrong!!"

available_tools = {
    "get_weather": get_weather
}

MODEL_PROMPT = '''
You are an expert AI assistant that resolves user queries using chain of thought. You work in START, PLAN, TOOL, OBSERVE, and OUTPUT steps.

IMPORTANT RULES:
- Process ALL planning steps in ONE response (don't wait for "Continue")
- Output a JSON array of steps: [{"step":"PLAN","content":"..."}, {"step":"TOOL","tool":"get_weather","input":"mumbai"}, ...]
- When done planning, include the final OUTPUT step in the same array
- Available tools: get_weather (takes city name, returns weather)

Output Format: Return a JSON array of step objects.

Example:
User: "What's the weather in Mumbai?"
Response:
[
  {"step":"PLAN","content":"User wants Mumbai weather"},
  {"step":"PLAN","content":"I'll use get_weather tool"},
  {"step":"TOOL","tool":"get_weather","input":"mumbai"},
  {"step":"PLAN","content":"Waiting for tool response..."}
]

After OBSERVE (tool result), continue:
[
  {"step":"PLAN","content":"Received weather data"},
  {"step":"OUTPUT","content":"The weather in Mumbai is 28°C and cloudy"}
]
'''

config = {
    "response_mime_type": "application/json",
}

def safe_api_call(chat_func, *args, max_retries=3, **kwargs):
    """Wrapper with exponential backoff for rate limits"""
    for attempt in range(max_retries):
        try:
            return chat_func(*args, **kwargs)
        except Exception as e:
            error_str = str(e)
            
            # Check for rate limit error
            if "RESOURCE_EXHAUSTED" in error_str or "Quota exceeded" in error_str:
                # Extract retry delay (default to 60s if not found)
                wait_time = 60
                if "retry in" in error_str.lower():
                    try:
                        import re
                        match = re.search(r'retry in (\d+(?:\.\d+)?)', error_str)
                        if match:
                            wait_time = float(match.group(1)) + 5  # Add 5s buffer
                    except:
                        pass
                
                print(f"⏳ Rate limit hit. Waiting {wait_time:.0f}s (attempt {attempt+1}/{max_retries})...")
                time.sleep(wait_time)
                continue
            
            # Other errors
            print(f"❌ API Error: {error_str}")
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"Retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise
    
    raise Exception("Max retries exceeded")

def process_steps(steps_array, chat):
    """Process an array of steps from the model"""
    for step_obj in steps_array:
        step_type = step_obj.get("step")
        
        if step_type == "START":
            print(f"🚀 START: {step_obj.get('content')}")
            
        elif step_type == "PLAN":
            print(f"🧠 PLAN: {step_obj.get('content')}")
            
        elif step_type == "TOOL":
            tool_name = step_obj.get("tool")
            tool_input = step_obj.get("input")
            
            if not tool_name or not tool_input:
                print("⚠️  Incomplete TOOL step, skipping...")
                continue
            
            if tool_name not in available_tools:
                print(f"❌ Unknown tool: {tool_name}")
                continue
            
            print(f"🔨 Calling: {tool_name}({tool_input})")
            tool_output = available_tools[tool_name](tool_input)
            
            # Send tool result back
            observe_msg = json.dumps([{
                "step": "OBSERVE",
                "tool": tool_name,
                "output": tool_output
            }])
            
            response = safe_api_call(chat.send_message, observe_msg)
            next_steps = json.loads(response.text)
            
            # Recursively process next steps
            if isinstance(next_steps, list):
                process_steps(next_steps, chat)
            else:
                process_steps([next_steps], chat)
            return
            
        elif step_type == "OUTPUT":
            print(f"\n✅ OUTPUT: {step_obj.get('content')}\n")
            return True
    
    return False

def main():
    print("\n" + "="*60)
    print("🤖 Agentic AI Assistant (Rate-Limited)")
    print("="*60 + "\n")
    
    # Create chat session
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config={
            **config,
            "system_instruction": MODEL_PROMPT
        }
    )
    
    print("💡 Tip: Free tier = 20 requests/day. Use wisely!\n")
    
    while True:
        user_query = input("User: ").strip()
        
        if not user_query:
            continue
        
        if user_query.lower() in ['exit', 'quit', 'bye']:
            print("👋 Goodbye!")
            break
        
        try:
            # Send user query and get response
            response = safe_api_call(chat.send_message, user_query)
            steps = json.loads(response.text)
            
            # Handle both single object and array responses
            if isinstance(steps, dict):
                steps = [steps]
            
            # Process all steps
            process_steps(steps, chat)
            
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            break
        
        print("\n" + "-"*60 + "\n")

if __name__ == "__main__":
    main()