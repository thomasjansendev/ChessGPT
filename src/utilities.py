from os import system, name
from src.constants import *
# from src.pieces import *

# ======= UTILITY FUNCTIONS =======

def name_to_idx(pos_str: str) -> tuple: #converts a chess board location into an an array index location (e.g. "a8" -> (0,0))
    #TODO (later): cache indicies into a dict during initialization 
    #to avoid searching for index each time
    for i in range(0,len(BOARD_REF)):
        if pos_str in BOARD_REF[i]:
            index = (i, BOARD_REF[i].index(pos_str))
            return index

def idx_to_name(pos_idx: tuple) -> str: #converts an array index location to a chess board location (e.g. (0,0) -> "a8")
    return BOARD_REF[pos_idx[0]][pos_idx[1]]

def print_board(board_array: list,mode="--clean"):
    match mode:
        case "--clean":
            for row in board_array:
                row = list(map(lambda x: x.id if issubclass(type(x), Piece) else x, row))
                row = list(map(lambda x: ' ' if x == None else x, row))
                print(row)
        case "--raw":
            for row in board_array: print(row)

def mark_moves_on_board(board,moves:tuple):
    new_board = board.copy()
    for move in moves:
        board[move[0]][move[1]] = 'o'
    return new_board

def debug_move(board,old_pos_str,new_pos_str): #used for testing to move a piece freely without checking if it is a valid move
    old_pos_index = name_to_idx(old_pos_str)
    new_pos_index = name_to_idx(new_pos_str)
    board[new_pos_index[0]][new_pos_index[1]] = board[old_pos_index[0]][old_pos_index[1]]
    board[old_pos_index[0]][old_pos_index[1]] = " "

def print_gamelog(gamelog) -> None:
    clear()
    for key in gamelog:
        print(f"{key}. {gamelog[key]}")
    
def update_gamelog(gamelog: dict, turn_number: int, piece, square: str) -> dict:
    if piece.id == 'p': id = ''
    else: id = piece.id
    if piece.color == Color.WHITE:
        gamelog[turn_number] = f"{id}{square}"
    elif piece.color == Color.BLACK:
        gamelog[turn_number] += f" {id}{square}"
        turn_number += 1
    return gamelog, turn_number
    
def board_dict_to_array(board: dict) -> list:
    board_array = [[None for _ in range(8)] for _ in range(8)] #initialize empty board
    # Could be optimized to not reset the board_array each time get
    # _possible_moves is called 
    # but then we would need to maintain two sources of truth: board_dict and board_array
    # I chose to prioritize data integrity before trying to optimize for the time being
    for key in board:
        piece = board[key]["piece"]
        row = board[key]["index"][0]
        col = board[key]["index"][1]
        board_array[row][col] = piece
    
    return board_array

def change_current_player(current_player) -> Color:
    if current_player == Color.WHITE:
        return Color.BLACK
    elif current_player == Color.BLACK:
        return Color.WHITE
    
def clear(): #clears the console line
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
    