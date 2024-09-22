from src.constants import *
from src.core import *
from src.utilities import *

def main():
    # board = BOARD_INIT
    board = init_board()
    print_board(board)
    
    # from_pos = "a1"
    # to_pos = "a4"
    # if from_pos != to_pos:
    #     debug_move(board, from_pos, to_pos)
    # print(board[get_index(to_pos)[0]][get_index(to_pos)[1]]) 
    # calc_possible_moves(board,to_pos)
    
    # result = None
    # while result is None:
    #     try:
    #         result = new_move(board)
    #         board = result
    #     except Exception as e:
    #         print(e)

if __name__ == "__main__":
    main()