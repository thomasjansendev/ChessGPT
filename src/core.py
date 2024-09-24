from src.pieces import *
from src.utilities import *

# ======= CORE FUNCTIONS =======

def new_move(board,white_turn):

    #get input
    old_pos_str = input("from: ").strip()
    old_pos_index = name_to_idx(old_pos_str)
    
    #check if piece is available
    piece = board[old_pos_index[0]][old_pos_index[1]]
    if piece == None:
        raise Exception("No piece available to move at this location.")
    possible_moves = piece.calc_possible_moves(board)
    possible_moves = list(map(lambda x: idx_to_name(x),possible_moves))
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

def init_board():
    board = [[None for _ in range(8)] for _ in range(8)]
    # Queen Q
    board[name_to_idx("d8")[0]][name_to_idx("d8")[1]] = Queen(Color.BLACK)
    board[name_to_idx("d1")[0]][name_to_idx("d1")[1]] = Queen(Color.WHITE)
    # King K
    board[name_to_idx("e8")[0]][name_to_idx("e8")[1]] = King(Color.BLACK)
    board[name_to_idx("e1")[0]][name_to_idx("e1")[1]] = King(Color.WHITE)
    # Knights N
    board[name_to_idx("b8")[0]][name_to_idx("b8")[1]] = Knight(Color.BLACK)
    board[name_to_idx("g8")[0]][name_to_idx("g8")[1]] = Knight(Color.BLACK)
    board[name_to_idx("b1")[0]][name_to_idx("b1")[1]] = Knight(Color.WHITE)
    board[name_to_idx("g1")[0]][name_to_idx("g1")[1]] = Knight(Color.WHITE)
    # Bishop B
    board[name_to_idx("c8")[0]][name_to_idx("c8")[1]] = Bishop(Color.BLACK)
    board[name_to_idx("f8")[0]][name_to_idx("f8")[1]] = Bishop(Color.BLACK)
    board[name_to_idx("c1")[0]][name_to_idx("c1")[1]] = Bishop(Color.WHITE)
    board[name_to_idx("f1")[0]][name_to_idx("f1")[1]] = Bishop(Color.WHITE)
    # Rook R
    board[name_to_idx("a8")[0]][name_to_idx("a8")[1]] = Rook(Color.BLACK)
    board[name_to_idx("h8")[0]][name_to_idx("h8")[1]] = Rook(Color.BLACK)
    board[name_to_idx("a1")[0]][name_to_idx("a1")[1]] = Rook(Color.WHITE)
    board[name_to_idx("h1")[0]][name_to_idx("h1")[1]] = Rook(Color.WHITE)
    # Pawns p
    board[1] = [Pawn(Color.BLACK) for _ in range(len(board[0]))]
    board[6] = [Pawn(Color.WHITE) for _ in range(len(board[0]))]
    return board

def init_pieces(color: Color):
    piece_dict = {}
    match color:
        case Color.WHITE:
            pass
        case Color.BLACK:
            pass
        case _:
            raise Exception("Invalid color. Either black or white")
    return piece_dict

def init_empty_board() -> list:
    board = [[None for _ in range(8)] for _ in range(8)]
    return board