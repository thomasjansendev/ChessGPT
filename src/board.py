import pygame
from src.sprites import SPRITES_DICT
from src.utilities import *
from src.constants import *
from src.pieces import *

def init_board_array() -> list:
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

def init_empty_board() -> list:
    board = [[None for _ in range(8)] for _ in range(8)]
    return board

def init_board_dict(): 
    # Returns a dictionary containing a key for each square on the board
    # Initiliazes an empty board -> set_pieces() is used to fill board with starting piece positions 
    board_dict = dict()
    
    is_light = False
    for row in range(0,len(BOARD_REF)):
        is_light = not is_light
        for col in range(0,len(BOARD_REF[row])):
            square_name = BOARD_REF[row][col]
            if is_light:
                square_img = SPRITES_DICT["square_light"]
            else:
                square_img = SPRITES_DICT["square_dark"]
            
            x = col * CELL_WIDTH
            y = row * CELL_HEIGHT
            square_img_rect = square_img.get_rect(topleft=(x,y))
            
            board_dict[square_name] = {'index': (row,col), # Used to convert to array to get_possible_moves
                                       'img': square_img, # Used to store sprite to draw to screen
                                       'rect': square_img_rect, # Used to store the square's hitbox
                                       'piece': None # used to store the current piece on the square
                                       }
            is_light = not is_light
            
    return board_dict

def init_pieces(board_dict: dict):
    # Fills the board dictionary with the pieces at their starting position
    # & initializes a dictionary to keep track of the active/captured pieces
    
    pieces_dict = {
        "active_white": [],
        "active_black": [],
        "captured_white": [],
        "captured_black": []
    }
    
    #WHITE PIECES
    board_dict, pieces_dict = set_piece(Rook, Color.WHITE, "a1", board_dict, pieces_dict)
    board_dict, pieces_dict = set_piece(Knight, Color.WHITE, "b1", board_dict, pieces_dict)
    board_dict, pieces_dict = set_piece(Bishop, Color.WHITE, "c1", board_dict, pieces_dict)
    board_dict, pieces_dict = set_piece(Queen, Color.WHITE, "d1", board_dict, pieces_dict)
    board_dict, pieces_dict = set_piece(King, Color.WHITE, "e1", board_dict, pieces_dict)
    board_dict, pieces_dict = set_piece(Bishop, Color.WHITE, "f1", board_dict, pieces_dict)
    board_dict, pieces_dict = set_piece(Knight, Color.WHITE, "g1", board_dict, pieces_dict)
    board_dict, pieces_dict = set_piece(Rook, Color.WHITE, "h1", board_dict, pieces_dict)
    
    #BLACK PIECES
    board_dict, pieces_dict = set_piece(Rook, Color.BLACK, "a8", board_dict, pieces_dict)
    board_dict, pieces_dict = set_piece(Knight, Color.BLACK, "b8", board_dict, pieces_dict)
    board_dict, pieces_dict = set_piece(Bishop, Color.BLACK, "c8", board_dict, pieces_dict)
    board_dict, pieces_dict = set_piece(Queen, Color.BLACK, "d8", board_dict, pieces_dict)
    board_dict, pieces_dict = set_piece(King, Color.BLACK, "e8", board_dict, pieces_dict)
    board_dict, pieces_dict = set_piece(Bishop, Color.BLACK, "f8", board_dict, pieces_dict)
    board_dict, pieces_dict = set_piece(Knight, Color.BLACK, "g8", board_dict, pieces_dict)
    board_dict, pieces_dict = set_piece(Rook, Color.BLACK, "h8", board_dict, pieces_dict)
    
    #PAWNS
    white_pawn_squares = ["a2","b2","c2","d2","e2","f2","g2","h2"]
    for square in white_pawn_squares:
        board_dict, pieces_dict = set_piece(Pawn, Color.WHITE, square, board_dict, pieces_dict)
    black_pawn_squares = ["a7","b7","c7","d7","e7","f7","g7","h7"]
    for square in black_pawn_squares:
        board_dict, pieces_dict = set_piece(Pawn, Color.BLACK, square, board_dict, pieces_dict)
    
    return board_dict, pieces_dict

def set_piece(new_piece: Piece, color: Color, square: str, board_dict: dict, pieces_dict: dict):
    # Initialize new piece
    new_piece = new_piece(color,board_dict[square]["rect"])
    # Update board with new piece at specified square
    board_dict[square]["piece"] = new_piece
    # Update piece dictionary with new piece
    if color == color.WHITE:
        pieces_dict["active_white"].append(new_piece)
    elif color == color.BLACK:
        pieces_dict["active_black"].append(new_piece)
    return board_dict, pieces_dict
    
    
        