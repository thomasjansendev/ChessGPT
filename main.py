from src.constants import *
from src.core import *
from src.pieces import *

def main():
    board = init_board()
    # board = init_empty_board()
    # piece = Queen(Color.WHITE)
    # pos = (2,2)
    # board[pos[0]][pos[1]] = piece
    
    # piece_pos = piece.get_position(board)
    # piece_moves = piece.calc_possible_moves(board)
    # board = mark_moves_on_board(board,piece_moves)
    # print_board(board,mode="--clean")
    # print(f"Position: {piece_pos}")
    # print(f"Possible moves: {piece_moves}")
    
    running = True
    current_player = Color.WHITE
    while running:
        print(f"{current_player} to move: ")
        result = None
        while result is None:
            try:
                result = new_move(board,current_player)
                board = result
                print_board(board)
            except Exception as e:
                print(e)
        
        if current_player == Color.WHITE: current_player = Color.BLACK
        elif current_player == Color.BLACK: current_player = Color.WHITE
        
    
    # print_board(board,mode="--clean")

if __name__ == "__main__":
    main()