import pygame
from src.sprites import SPRITES_DICT
from src.utilities import *
from src.constants import *
from src.pieces import *

class Board:
    def __init__(self) -> None:
        # Board state attributes
        self.array = init_empty_board()
        self.active_pieces = { "w": [], "b": []}
        self.captured_pieces = { "w": [], "b": []}
        fill_board(self)
        # GUI attributes
        self.sprites = {} #TODO: use this to store {'square': {'img': _}, {'rect': _} } to draw the GUI
        # Games state attributes
        self.active_colour = 'w'
        self.castling_availability = {
            "white_kingside": True,
            "white_queenside": True,
            "black_kingside": True,
            "black_queenside": True
        }
        self.enpassant_target_square = '-' 
        self.halfmove_clock = 0 # This is the number of halfmoves since the last capture or pawn move.
        self.fullmove_number = 1
        self.checkmate = False
        self.gamelog = "" # To keep track of turns in PGN format
        
        
    def update(self,move:str):
        # Assuming move is given in UCI format 'e2e4' (long algebraic notation)
        origin_square = move[:2]
        origin_square_idx = name_to_idx(origin_square)
        destination_square = move[2:4]
        destination_square_idx = name_to_idx(destination_square)
        
        # Get list of legal moves if piece is available on selected square
        piece = self.array[origin_square_idx[0]][origin_square_idx[1]]
        if piece != None:
            legal_moves = piece.get_legal_moves(self)
        else:
            raise Exception(f"No piece is available on {origin_square}.")
        
        destination_content = self.array[destination_square_idx[0]][destination_square_idx[1]]
        if destination_square in legal_moves:
            # Check special movement conditions (check, capture, castling, promotion)
            if destination_content != None and destination_content.colour != piece.colour:
                capture = True
                self.capture_piece(destination_content)
            else:
                capture = False
            check = verify_check()
            castling = verify_castling()
            promotion = move[4] if len(move) == 5 else ''
            
            # Update board state & gamelog
            self.array[destination_square_idx[0]][destination_square_idx[1]] = piece
            self.array[origin_square_idx[0]][origin_square_idx[1]] = None
            self.update_gamelog(piece,origin_square,destination_square,capture,check,castling,promotion)
        else:
            raise Exception(f"{move} is an illegal move. Please try again.")
            
    def draw():
        pass
        
    def print(self,mode="-clean"):
        board = self.array
        if mode == '-clean':
            for row in board:
                row = list(map(lambda x: x.id if issubclass(type(x), Piece) else x, row))
                row = list(map(lambda x: ' ' if x == None else x, row))
                print(row)
        elif mode == "-FEN":
            pass
        elif mode == "-raw":
            for row in board: print(row)
        else:
            raise Exception("Board.print(): valid arguments for 'mode' are '-clean', '-FEN' or '-raw'.")
    
    def get_piece(self,square: str) -> Piece:
        index = name_to_idx(square)
        piece = self.array[index[0]][index[1]]
        return piece
    
    def capture_piece(self,piece):
        if piece.colour == colour.WHITE:
            self.active_pieces["w"].remove(piece)
            self.captured_pieces["w"].append(piece)
        elif piece.colour == colour.BLACK:
            self.active_pieces["b"].remove(piece)
            self.captured_pieces["b"].append(piece)
    
    def update_gamelog(self, piece:Piece, origin_square:str, destination_square:str, capture:bool=False, check:bool=False, castling:str='', promotion:str=''):
        
        piece_str = piece.id.upper() if type(piece) != Pawn else ''
        check_str = '+' if check == True else ''
        
        if capture and type(piece) != Pawn:
            capture_str = 'x'
        elif capture and type(piece) == Pawn:
            capture_str = f'{origin_square[0]}x' #add column origin file if piece is a pawn
        else:
            capture_str = ''
        
        if castling == '':
            move_str = f"{piece_str}{capture_str}{destination_square}{promotion}{check_str}"
        elif castling == 'queenside':
            move_str = "0-0-0"
        elif castling == 'kingside':
            move_str = "0-0"
        
        if self.active_colour == 'w':
            self.gamelog += f'{self.fullmove_number}. {move_str} '
        elif self.active_colour == 'b':
            self.gamelog += f'{move_str} '
         
    
# Helper functions

def verify_check():
    return False

def verify_castling():
    return ''

def init_empty_board():
    return [[None for _ in range(8)] for _ in range(8)]

def fill_board(board):
    
    # WHITE PIECES
    set_piece(Rook, colour.WHITE, "a1", board)
    set_piece(Knight, colour.WHITE, "b1", board)
    set_piece(Bishop, colour.WHITE, "c1", board)
    set_piece(Queen, colour.WHITE, "d1", board)
    set_piece(King, colour.WHITE, "e1", board)
    set_piece(Bishop, colour.WHITE, "f1", board)
    set_piece(Knight, colour.WHITE, "g1", board)
    set_piece(Rook, colour.WHITE, "h1", board)
    
    # WHITE PAWNS
    white_pawn_squares = ["a2","b2","c2","d2","e2","f2","g2","h2"]
    for square in white_pawn_squares:
        set_piece(Pawn, colour.WHITE, square, board)
    
    # BLACK PIECES
    set_piece(Rook, colour.BLACK, "a8", board)
    set_piece(Knight, colour.BLACK, "b8", board)
    set_piece(Bishop, colour.BLACK, "c8", board)
    set_piece(Queen, colour.BLACK, "d8", board)
    set_piece(King, colour.BLACK, "e8", board)
    set_piece(Bishop, colour.BLACK, "f8", board)
    set_piece(Knight, colour.BLACK, "g8", board)
    set_piece(Rook, colour.BLACK, "h8", board)
    
    # BLACK PAWNS
    black_pawn_squares = ["a7","b7","c7","d7","e7","f7","g7","h7"]
    for square in black_pawn_squares:
        set_piece(Pawn, colour.BLACK, square, board)

def set_piece(piece_type: Piece, colour: colour, square: str, board: Board):
    # Initialize new piece
    new_piece = piece_type(colour)
    # Update board with new piece at specified square
    index_loc = name_to_idx(square)
    board.array[index_loc[0]][index_loc[1]] = new_piece
    # Update piece dictionary with new piece
    if colour == colour.WHITE:
        board.active_pieces["w"].append(new_piece)
    elif colour == colour.BLACK:
        board.active_pieces["b"].append(new_piece)
    
# TODO: refactor to create self.sprites dictionary instead {'square': {'img': _}, {'rect': _} } 
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
