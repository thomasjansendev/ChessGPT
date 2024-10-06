from src.pieces import *
from src.utilities import *

# ======= CORE FUNCTIONS =======

def new_move(board,current_player):

    #get input
    old_pos_str = input("from: ").strip()
    old_pos_index = name_to_idx(old_pos_str)
    
    piece = board[old_pos_index[0]][old_pos_index[1]]
    possible_moves = piece.get_possible_moves(board)
    possible_moves = list(map(lambda x: idx_to_name(x),possible_moves))
    
    #check if valid piece for current player
    if piece == None:
        raise Exception("No piece available to move at this location.")
    if piece.colour != current_player:
        raise Exception("Please chose a piece of your own colour")
    
    #debug info
    print(f"Selected: {piece}")
    print(f"Possible moves: {possible_moves}")
    
    #get input
    new_pos_str = input("to: ").strip()
    new_pos_index = name_to_idx(new_pos_str)

    #check if input string is valid
    if (old_pos_index == None or new_pos_index == None):
        raise Exception("Invalid input. Please provide a letter between a-h combined with a number between 1-8. Example 'a6','g1' etc.")
    elif old_pos_str == new_pos_str:
        raise Exception("Must move piece to a different square than starting square.")

    #check if move is legal -> error is raised if not
    if new_pos_str not in possible_moves: 
        raise Exception(f"Illegal move. Possible moves for selected piece are {possible_moves}")

    #update board
    board[new_pos_index[0]][new_pos_index[1]] = piece
    board[old_pos_index[0]][old_pos_index[1]] = None
    
    return board