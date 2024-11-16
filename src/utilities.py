from os import system, name
from src.constants import BOARD_REF, BOARD_REF_DICT

# ======= UTILITY FUNCTIONS =======

def name_to_idx(pos_str: str) -> tuple: #converts a chess board location into an an array index location (e.g. "a8" -> (0,0))
    return BOARD_REF_DICT[pos_str]

def idx_to_name(pos_idx: tuple) -> str: #converts an array index location to a chess board location (e.g. (0,0) -> "a8")
    return BOARD_REF[pos_idx[0]][pos_idx[1]]

def clear(): #clears the console line
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')