from constants import *

# ======= UTILITY FUNCTIONS =======

def get_index(pos_str: str):
    #TODO (later): cache indicies into a dict and call get_index during initialization 
    #to avoid searching for index each time
    for r in range(0,len(BOARD_REF)):
        if pos_str in BOARD_REF[r]:
            index = (r, BOARD_REF[r].index(pos_str))
            return index

def get_pos_name(pos_idx: tuple):
    return BOARD_REF[pos_idx[0]][pos_idx[1]]

def print_board(board):
    for row in board:
        print(row)

def debug_move(board,old_pos_str,new_pos_str): #used for testing
    old_pos_index = get_index(old_pos_str)
    new_pos_index = get_index(new_pos_str)
    board[new_pos_index[0]][new_pos_index[1]] = board[old_pos_index[0]][old_pos_index[1]]
    board[old_pos_index[0]][old_pos_index[1]] = " "
