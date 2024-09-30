import pygame
from src.sprites import SPRITES_DICT
from src.utilities import *
from src.constants import *

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
    # Each square/key stores the image and rect used to display the square
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
            
            board_dict[square_name] = {'img': square_img, 
                                       'rect': square_img_rect, 
                                       'piece': None}
            is_light = not is_light
            
    return board_dict

def set_pieces(board_dict: dict) -> dict:
    
    #WHITE PIECES
    board_dict["a1"]["piece"] = Rook(Color.WHITE,board_dict["a1"]["rect"])
    board_dict["b1"]["piece"] = Knight(Color.WHITE,board_dict["b1"]["rect"])
    board_dict["c1"]["piece"] = Bishop(Color.WHITE,board_dict["c1"]["rect"])
    board_dict["d1"]["piece"] = Queen(Color.WHITE,board_dict["d1"]["rect"])
    board_dict["e1"]["piece"] = King(Color.WHITE,board_dict["e1"]["rect"])
    board_dict["f1"]["piece"] = Bishop(Color.WHITE,board_dict["f1"]["rect"])
    board_dict["g1"]["piece"] = Knight(Color.WHITE,board_dict["g1"]["rect"])
    board_dict["h1"]["piece"] = Rook(Color.WHITE,board_dict["h1"]["rect"])
    
    #BLACK PIECES
    board_dict["a8"]["piece"] = Rook(Color.BLACK,board_dict["a8"]["rect"])
    board_dict["b8"]["piece"] = Knight(Color.BLACK,board_dict["b8"]["rect"])
    board_dict["c8"]["piece"] = Bishop(Color.BLACK,board_dict["c8"]["rect"])
    board_dict["d8"]["piece"] = Queen(Color.BLACK,board_dict["d8"]["rect"])
    board_dict["e8"]["piece"] = King(Color.BLACK,board_dict["e8"]["rect"])
    board_dict["f8"]["piece"] = Bishop(Color.BLACK,board_dict["f8"]["rect"])
    board_dict["g8"]["piece"] = Knight(Color.BLACK,board_dict["g8"]["rect"])
    board_dict["h8"]["piece"] = Rook(Color.BLACK,board_dict["h8"]["rect"])
    
    #PAWNS
    white_pawn_squares = ["a2","b2","c2","d2","e2","f2","g2","h2"]
    for square in white_pawn_squares:
        board_dict[square]["piece"] = Pawn(Color.WHITE,board_dict[square]["rect"])
    black_pawn_squares = ["a7","b7","c7","d7","e7","f7","g7","h7"]
    for square in black_pawn_squares:
        board_dict[square]["piece"] = Pawn(Color.BLACK,board_dict[square]["rect"])
    
    return board_dict
    
        