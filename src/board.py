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
        self.sprites = init_board_sprites()
        init_piece_sprites(self)
        # Games state attributes
        self.active_colour = 'w' # or 'b'
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
    
    def update(self,move:str): #TODO: add legal_moves to method signature as kwarg to avoid calculating twice
        # Assuming move is given in UCI format 'e2e4' (long algebraic notation)
        origin_square = move[:2]
        origin_square_idx = name_to_idx(origin_square)
        destination_square = move[2:4]
        destination_square_idx = name_to_idx(destination_square)
        
        # Check if piece is valid
        piece = self.array[origin_square_idx[0]][origin_square_idx[1]]
        if piece == None:
            raise Exception(f"No piece is available on {origin_square}.")
        elif piece.colour != self.active_colour:
            raise Exception(f"The piece you are trying to move does not belong to you.")
        
        # Check if requested move is valid
        legal_moves = piece.get_legal_moves(self.array)
        if destination_square not in legal_moves:
            raise Exception(f"{move} is an illegal move. Please try again.")
        
        # Verify capture
        destination_content = self.array[destination_square_idx[0]][destination_square_idx[1]]
        if destination_content != None and destination_content.colour != piece.colour:
            self.capture_piece(destination_content)
            capture = True
        else:
            capture = False
        
        # Verify castling 
        castling = verify_castling()
        
        # Verify promotion (currently based on LLM output length -> deeply flawed xD to be changed later)
        promotion = move[4] if len(move) == 5 else ''
        
        # Update board state
        self.array[destination_square_idx[0]][destination_square_idx[1]] = piece
        self.array[origin_square_idx[0]][origin_square_idx[1]] = None
        piece.rect.center = self.sprites[destination_square]["rect"].center
        
        # Verify check given new board state
        check = verify_check_after_move(self)
        if check:
            verify_checkmate(self)
        
        # Update gamelog
        self.update_gamelog(piece,origin_square,destination_square,capture,check,castling,promotion)
        
        self.swap_active_colour()
        if piece.colour == "b": self.fullmove_number += 1
            
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
        return self.array[index[0]][index[1]]
    
    def capture_piece(self,piece):
        if piece.colour == 'w':
            self.active_pieces["w"].remove(piece)
            self.captured_pieces["w"].append(piece)
        elif piece.colour == 'b':
            self.active_pieces["b"].remove(piece)
            self.captured_pieces["b"].append(piece)
    
    def swap_active_colour(self):
        if self.active_colour == 'w':
            self.active_colour = 'b'
        elif self.active_colour == 'b':
            self.active_colour = 'w'
    
    def update_gamelog(self, piece:Piece, origin_square:str, destination_square:str, capture:bool=False, check:bool=False, castling:str='', promotion:str=''):
        
        piece_str = piece.id.upper() if type(piece) != Pawn else ''
        check_str = ''
        if self.checkmate == True:
            check_str = '#'
        elif check == True:
            check_str = '+'
        
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

def verify_check_after_move(board: Board):
    # Verifies whether a succesful move results to a check
    
    # Step 0: Find position of enemy king -> to be replaced later with a better implementation
    opposite_king_id = 'k' if board.active_colour == 'w' else 'K'
    opposite_king_pos = None
    for rank in range(0,len(board.array)):
        for file in range(0,len(board.array[rank])):
            piece = board.array[rank][file]
            if piece != None and piece.id == opposite_king_id:
                opposite_king_pos = idx_to_name((rank,file))
    
    # Step 1: calculate squares under threat
    pieces = board.active_pieces[board.active_colour]
    squares_under_threat = []
    for piece in pieces:
        squares_under_threat += piece.get_attacking_squares(board.array)
    
    # Step 2: verify check
    if opposite_king_pos in squares_under_threat:
        return True
        
    return False

def verify_checkmate(board:Board):
    opposite_colour = 'b' if board.active_colour == 'w' else 'w'
    
    possible_moves_for_opposite_colour = []
    for piece in board.active_pieces[opposite_colour]:
        possible_moves_for_opposite_colour += piece.get_legal_moves(board.array)
    
    if len(possible_moves_for_opposite_colour) == 0:
        board.checkmate = True


def verify_castling():
    return ''

def init_empty_board() -> list:
    return [[None for _ in range(8)] for _ in range(8)]

def fill_board(board: list) -> None:
    
    # WHITE PIECES
    set_piece(Rook, 'w', "a1", board)
    set_piece(Knight, 'w', "b1", board)
    set_piece(Bishop, 'w', "c1", board)
    set_piece(Queen, 'w', "d1", board)
    set_piece(King, 'w', "e1", board)
    set_piece(Bishop, 'w', "f1", board)
    set_piece(Knight, 'w', "g1", board)
    set_piece(Rook, 'w', "h1", board)
    
    # WHITE PAWNS
    white_pawn_squares = ["a2","b2","c2","d2","e2","f2","g2","h2"]
    for square in white_pawn_squares:
        set_piece(Pawn, 'w', square, board)
    
    # BLACK PIECES
    set_piece(Rook, 'b', "a8", board)
    set_piece(Knight, 'b', "b8", board)
    set_piece(Bishop, 'b', "c8", board)
    set_piece(Queen, 'b', "d8", board)
    set_piece(King, 'b', "e8", board)
    set_piece(Bishop, 'b', "f8", board)
    set_piece(Knight, 'b', "g8", board)
    set_piece(Rook, 'b', "h8", board)
    
    # BLACK PAWNS
    black_pawn_squares = ["a7","b7","c7","d7","e7","f7","g7","h7"]
    for square in black_pawn_squares:
        set_piece(Pawn, 'b', square, board)

def set_piece(piece_type: Piece, colour: str, square: str, board: Board) -> None:
    # Initialize new piece
    new_piece = piece_type(colour)
    # Update board with new piece at specified square
    index_loc = name_to_idx(square)
    board.array[index_loc[0]][index_loc[1]] = new_piece
    # Update active piece dictionary with new piece
    if colour == 'w':
        board.active_pieces["w"].append(new_piece)
    elif colour == 'b':
        board.active_pieces["b"].append(new_piece)

def init_board_sprites() -> dict:
    # Creates a dictionary used by pygame to draw to screen:
    #   - key = square on the board 
    #   - value = data needed for pygame to draw a GUI (image, rect)
    
    gui_dict = {}
    
    is_light = False # simple bool to alternate between light/dark squares
    for row in range(0,len(BOARD_REF)):
        is_light = not is_light
        for col in range(0,len(BOARD_REF[row])):
            square_name = BOARD_REF[row][col]
            square_img = SPRITES_DICT["square_light"] if is_light else SPRITES_DICT["square_dark"]
            
            x = col * CELL_WIDTH
            y = row * CELL_HEIGHT
            square_rect = square_img.get_rect(topleft=(x,y))
            
            gui_dict[square_name] = {
                'img': square_img, # Used to store sprite to draw to screen
                'rect': square_rect, # Used to store the square's hitbox
                }
            is_light = not is_light
    
    return gui_dict

def init_piece_sprites(board: Board):
    # Initializes the rect of pieces to their corresponding square
    # Inneficient because this could be done when calling fill_board() and set_piece()
    # but at least the backend and frontend operations are decoupled and I can more easily swap to a different frontend when needed 
    # + it is an operation done a initialization and not at runtime
    for piece in board.active_pieces["w"] + board.active_pieces["b"]:
        square = idx_to_name(piece.get_position(board.array))
        square_rect = board.sprites[square]["rect"]
        piece.rect = piece.img.get_rect(topleft=(square_rect.x, square_rect.y))