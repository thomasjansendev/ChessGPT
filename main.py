from src.constants import *
from src.core import *
from src.pieces import *

def main():
    # board = init_board()
    board = init_empty_board()
    piece = Queen("white")
    pos = (2,2)
    board[pos[0]][pos[1]] = piece
    
    piece_pos = piece.get_position(board)
    piece_moves = piece.calc_possible_moves(board)
    board = mark_moves_on_board(board,piece_moves)
    print_board(board,mode="--clean")
    print(f"Position: {piece_pos}")
    # print(f"Possible moves: {piece_moves}")
    
    # result = None
    # while result is None:
    #     try:
    #         result = new_move(board)
    #         board = result
    #     except Exception as e:
    #         print(e)

if __name__ == "__main__":
    main()