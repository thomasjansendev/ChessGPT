from src.constants import *
from src.pieces import *

# ======= UTILITY FUNCTIONS =======

def get_index(pos_str: str):
    #TODO (later): cache indicies into a dict and call get_index during initialization 
    #to avoid searching for index each time
    for i in range(0,len(BOARD_REF)):
        if pos_str in BOARD_REF[i]:
            index = (i, BOARD_REF[i].index(pos_str))
            return index

def get_pos_name(pos_idx: tuple):
    return BOARD_REF[pos_idx[0]][pos_idx[1]]

def print_board(board,mode="--clean"):
    match mode:
        case "--clean":
            for row in board:
                row = list(map(lambda x: x.id if issubclass(type(x), Piece) else x, row))
                row = list(map(lambda x: ' ' if x == None else x, row))
                print(row)
        case "--raw":
            for row in board: print(row)

def mark_moves_on_board(board,moves:tuple):
    new_board = board.copy()
    for move in moves:
        board[move[0]][move[1]] = 'o'
    return new_board

def debug_move(board,old_pos_str,new_pos_str): #used for testing to move a piece freely without checking if it is a valid move
    old_pos_index = get_index(old_pos_str)
    new_pos_index = get_index(new_pos_str)
    board[new_pos_index[0]][new_pos_index[1]] = board[old_pos_index[0]][old_pos_index[1]]
    board[old_pos_index[0]][old_pos_index[1]] = " "
