from openai import OpenAI
from src.constants import RANKS, FILES, PIECES

# Initialize OpenAI client

# api_key_path = r"C:\MyData\tmp\openai_api_key.txt"
api_key_path = "/Users/thomasjansen/Workspace/api_keys/openai.txt"
with open(api_key_path, 'r', encoding="utf-8") as file:
    api_key = file.read()
    
client = OpenAI(
  organization='org-vMsEVjzqSbKcnzeMxc9JOnGX',
  project='proj_T7hKH2TdFoBlLemrv118jBjL',
  api_key=api_key,
)

# Initialize system prompt -> used to parametrize the output from the model
with open("./src/sys_prompt.txt", 'r', encoding="utf-8") as file:
    system_prompt_content = file.read()

system_prompt = {
    "role": "system",
    "content": system_prompt_content
}

# Initialize user prompt
user_prompt = {
    "role": "user",
    "content": ""
}

# Initialize user prompt
assistant_prompt = {
    "role": "user",
    "content": ""
}

def get_llm_move(prompt,model="gpt-4o"):
    chat_completion = client.chat.completions.create(
        messages=prompt,
        model=model,
    )
    raw_output_str = chat_completion.choices[0].message.content
    print(f"\nRaw output from LLM: {raw_output_str}")
    output_str = format_move(raw_output_str)
    print(f"Filtered output from LLM: {output_str}")
    
    if len(output_str) == 4:
        if output_str[0] in FILES and output_str[2] in FILES:
            if output_str[1] in RANKS and output_str[3] in RANKS:
                return output_str, raw_output_str
    else:
        error_str = "Output should be in long algebraic notation: '<origin_square><destination_square>'."
        raise ValueError(error_str,raw_output_str)
        
def format_move(move_str:str):
    # search for first and second occurence of letter/number pair
    new_move_str = ''
    # start from end of message because LLM often adds unnecessary text before
    for i in range(len(move_str)-2,-1,-1):
        char_pair = move_str[i:i+2]
        if char_pair[0] in FILES and char_pair[1] in RANKS:
            new_move_str = char_pair + new_move_str
    return new_move_str

def new_user_prompt(content:str):
    return {"role": "user", "content": content}

def new_assistant_prompt(content:str):
    return {"role": "assistant", "content": content}
    
    