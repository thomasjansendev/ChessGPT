from openai import OpenAI
from os import system, name

# Get API key
api_key_path = r"C:\MyData\tmp\openai_api_key.txt"
with open(api_key_path, 'r', encoding="utf-8") as file:
    api_key = file.read()
    
# Initialize OpenAI client
client = OpenAI(
  organization='org-vMsEVjzqSbKcnzeMxc9JOnGX',
  project='proj_T7hKH2TdFoBlLemrv118jBjL',
  api_key=api_key,
)

# Initialize system prompt -> used to parametrize the output from the model
system_prompt = {
    "role": "system",
    "content": "You are a chess grandmaster playing black, and your goal is to win as quickly as possible. I will provide the current game score before each of your moves, and your reply should just be your next move in algebraic notation with no other commentary. The desired output should follow this format: '<your_move>' and should NOT ressemble this format: '<turn_number>... <your_move>'."
}

# Initialize game_log to track the history of moves
game_log = {
    "role": "user",
    "content": ""
}

# Initialize prompt which will be updated every turn
prompt = [system_prompt, game_log]

turn_number = 1

while True:

    # Get user input
    user_input = input("User: ")
    
    # Update game_log with White move
    game_log["content"] += f"{turn_number}. {user_input.strip()} "
    
    # Submit prompt to model
    chat_completion = client.chat.completions.create(
        messages=prompt,
        model="gpt-4o",
    )
    
    # Update game_log with Black move
    model_response_raw = chat_completion.choices[0].message.content
    
    # Check if input is in correct format since model sometimes provides moves as '3... d5'
    if '...' in model_response_raw: 
        model_response = model_response_raw.split()[1]
    else:
        model_response = model_response_raw
    
    game_log["content"] += f"{model_response} "
    
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
    
    print(game_log["content"])
    
    turn_number += 1
    
    