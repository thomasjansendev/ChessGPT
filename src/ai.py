from openai import OpenAI
from os import system, name
from src.board import *

# Get API key
# api_key_path = r"C:\MyData\tmp\openai_api_key.txt"
api_key_path = "/Users/thomasjansen/Workspace/api_keys/openai.txt"
with open(api_key_path, 'r', encoding="utf-8") as file:
    api_key = file.read()
    
# Initialize OpenAI client
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

# Initialize game_log to track the history of moves
game_log = {
    "role": "user",
    "content": ""
}

# Initialize prompt which will be updated every turn
prompt = [system_prompt, game_log]

board = Board()
playing = True
while playing:

    # Get user input
    user_input = input("User: ")
    board.update(user_input)
    # board.print()
    
    # Update game_log with White move
    # game_log["content"] += f"{turn_number}. {user_input.strip()} "
    game_log["content"] = user_input
    
    # Submit prompt to model
    chat_completion = client.chat.completions.create(
        messages=prompt,
        model="gpt-4o",
    )
    
    # Update game_log with Black move
    model_response_raw = chat_completion.choices[0].message.content
    # print(model_response_raw)
    board.update(model_response_raw)
    board.print()
    
    # # Check if input is in correct format since model sometimes provides moves as '3... d5'
    # if '...' in model_response_raw: 
    #     model_response = model_response_raw.split()[1]
    # else:
    #     model_response = model_response_raw
    
    # game_log["content"] += f"{model_response} "
    
    # # for windows
    # if name == 'nt':
    #     _ = system('cls')
    # # for mac and linux(here, os.name is 'posix')
    # else:
    #     _ = system('clear')
    
    # print(game_log["content"])
    
    board.fullmove_number += 1
    playing = False
    
    