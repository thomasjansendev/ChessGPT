from src.board import Board
from src.ai import *


def main():
    board = Board()
    prompt = [system_prompt, user_prompt]

    while not board.checkmate and board.halfmove_clock <= 50:
        # Get move from user
        user_move = input("\nInput from user: ")
        board.update(user_move)

        # Print current state
        print(f"Gamelog:\n{board.gamelog}\n")
        board.print()

        # Update game state
        board.active_colour = "b"

        # Get move from user
        user_move = input("\nInput from user: ")
        board.update(user_move)

        # Print current state
        print(f"Gamelog:\n{board.gamelog}\n")
        board.print()

        # Update game state
        board.active_colour = "w"
        board.fullmove_number += 1

        # Reset prompt to remove any error prompts that might have been appended
        prompt = [system_prompt, user_prompt]


if __name__ == "__main__":
    main()
