from os import system, name
from src.constants import *
# from src.pieces import *

# ======= UTILITY FUNCTIONS =======

def name_to_idx(pos_str: str) -> tuple: #converts a chess board location into an an array index location (e.g. "a8" -> (0,0))
    return BOARD_REF_DICT[pos_str]

def idx_to_name(pos_idx: tuple) -> str: #converts an array index location to a chess board location (e.g. (0,0) -> "a8")
    return BOARD_REF[pos_idx[0]][pos_idx[1]]

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
    if piece.colour == colour.WHITE:
        gamelog[turn_number] = f"{id}{square}"
    elif piece.colour == colour.BLACK:
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

def change_current_player(current_player) -> colour:
    if current_player == colour.WHITE:
        return colour.BLACK
    elif current_player == colour.BLACK:
        return colour.WHITE
    
def clear(): #clears the console line
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
        
def move_dict_to_list(move_dict) -> list:
    # Concatenates the list stored in each key of a dictionary
    # Used to convert output of the move_search function from a dictionary to a list
    moves = []
    for direction in move_dict:
        moves += move_dict[direction]
    return moves

def capture_piece(piece,piece_dict):
    if piece.colour == colour.WHITE:
        piece_dict["active_white"].remove(piece)
        piece_dict["captured_white"].append(piece)
    elif piece.colour == colour.BLACK:
        piece_dict["active_black"].remove(piece)
        piece_dict["captured_black"].append(piece)     
    return piece_dict