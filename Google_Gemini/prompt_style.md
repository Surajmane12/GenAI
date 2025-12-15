# PROMPT STYLES


## Alpaca PROMPT TEMPLATE

### Instruction:
{instruction}

### Input:
{input}

### Response:
{response}


# EXAMPLE 
### Instruction:
Write a Python function to check if a number is prime.

### Input:
The function should return True or False.

### Response:
def is_prime(n):
    ...


# CHATML PROMPT STYLE
ChatML is the role-based message format used by modern chat models (system / user / assistant).

# EXAMPLE
[
  { "role": "system", "content": "You are a helpful assistant." },
  { "role": "user", "content": "Hello!" },
  { "role": "assistant", "content": "Hi! How can I help you?" }
]


# INST PROMPT STYLE
(This is the format used by LLaMA / Mistral / Vicuna / Alpaca-INST style models.)

INST (Instruction) prompt style wraps user instructions inside special tokens:

<s>[INST] ... [/INST] ... </s>

### Key Components

#### [INST] ... [/INST]
-> Contains the user instruction and optional input

#### <<SYS>> ... <</SYS>>
Optional system prompt to define role, behavior, or constraints

#### Content outside [/INST]
Represents the assistant’s response


#### FORMAT

<s>[INST]
<<SYS>>
{system_prompt}
<</SYS>>

{instruction_and_input}
[/INST]
{assistant_response}
</s>


#### EXAMPLE:

<s>[INST]
<<SYS>>
You are a senior Python developer.
<</SYS>>

Write a Python function to check if a number is prime.
[/INST]
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
</s>
