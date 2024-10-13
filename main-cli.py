from src.utilities import clear
from src.board import Board
from src.ai import *

def main():
    
    board = Board()
    prompt = [system_prompt, user_prompt]

    while not board.checkmate:
        
        # Get move from user
        invalid_output = True
        while invalid_output:
            try:
                user_move = input("\nInput from user: ")
                board.update(user_move)
                invalid_output = False
            except Exception as e:
                print(e)
        
        # Print current state
        print(f"Gamelog:\n{board.gamelog}\n")
        board.print()
        
        # Update game state
        board.active_colour = 'b'
        
        # Get move from LLM
        user_prompt["content"] = board.gamelog
        invalid_output = True
        while invalid_output:
            try:
                # Try getting output from LLM
                ai_move, ai_move_raw = get_llm_move(prompt)
                print("Log: ai_move format is valid")
                # Reset prompt to remove any error prompts that might have been appended by ValueErrors
                prompt = [system_prompt,user_prompt]
                # Try updating board with move request
                board.update(ai_move)
                print("Log: ai_move request is valid")
                invalid_output = False
            except ValueError as e:
                message, ai_move_raw = e.args
                # assistant_prompt = new_assistant_prompt(ai_move_raw)
                # error_prompt = new_user_prompt(message)
                # prompt = [system_prompt,user_prompt,assistant_prompt,error_prompt]
                prompt.append(new_assistant_prompt(ai_move_raw))
                prompt.append(new_user_prompt(message))
                print("--- ERROR ---")
                print(e)
                print(f"New prompt: {prompt[1:]}")
                print("-------------")
            except Exception as e:
                # assistant_prompt = new_assistant_prompt(ai_move_raw)
                # error_prompt = new_user_prompt(str(e))
                # prompt = [system_prompt,user_prompt,assistant_prompt,error_prompt]
                prompt.append(new_assistant_prompt(ai_move))
                prompt.append(new_user_prompt(str(e)))
                print("--- ERROR ---")
                print(e)
                print(f"New prompt: {prompt[1:]}")
                print("-------------")
        
        # Print current state
        print(f"Gamelog:\n{board.gamelog}\n")
        board.print()
        
        # Update game state
        board.active_colour = 'w'
        board.fullmove_number += 1
        
        # Reset prompt to remove any error prompts that might have been appended
        prompt = [system_prompt, user_prompt]

if __name__ == "__main__":
    main()