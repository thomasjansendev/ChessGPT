from src.constants import ARRAY_CARDINALS, BOARD_REF, colour
from src.sprites import SPRITES_DICT
from src.utilities import idx_to_name, name_to_idx, move_dict_to_list

class Piece:
    def __init__(self, colour: colour) -> None:
        self.colour = colour
        self.id = None
        self.moveset = None
        self.movedepth = None    

    # Return the position of the piece in a 8x8 array representing the board
    def get_position(self, board: list) -> tuple:
        for i in range(0,len(board)):
            if self in board[i]:
                return (i, board[i].index(self))

    # Returns a list of square names that the piece can move to
    def get_legal_moves(self, board: list, pieces: dict):
        position = self.get_position(board)
        possible_moves = move_search(board, position, self, filtered=True, format='-list')
        return possible_moves
    
    # Returns a list of squares that are threatened by this piece
    def get_attacking_squares(self,board,pieces) -> list:
        return self.get_legal_moves(board,pieces)

    
class Queen(Piece): # can move in any direction => 8 DOF
    def __init__(self, colour: colour, rect) -> None:
        super().__init__(colour)
        self.id = "Q"
        self.moveset = ["N","E","S","O","NE","SE","SO","NO"]
        if colour == colour.WHITE:
            self.img = SPRITES_DICT["w_queen"]
        elif colour == colour.BLACK:
            self.img = SPRITES_DICT["b_queen"]
        self.rect = self.img.get_rect(topleft=(rect.x, rect.y))
        
        
class King(Piece): # can move to any adjacent square by 1 => 8 DOF
    def __init__(self, colour: colour, rect) -> None:
        super().__init__(colour)
        self.id = "K"
        self.moveset = ["N","E","S","O","NE","SE","SO","NO"]
        self.movedepth = 1
        if colour == colour.WHITE:
            self.img = SPRITES_DICT["w_king"]
        elif colour == colour.BLACK:
            self.img = SPRITES_DICT["b_king"]
        self.rect = self.img.get_rect(topleft=(rect.x, rect.y))    
    
    def get_legal_moves(self, board: list, pieces: dict):
        position = self.get_position(board)
        
        possible_moves = move_search(board, position, self, filtered=True, format='-list')
        squares_under_threat = get_squares_under_threat(board,pieces,self.colour)
        
        legal_moves = []
        for move in possible_moves:
            if move not in squares_under_threat:
                legal_moves.append(move)
        return legal_moves
        
    def get_attacking_squares(self, board: list, pieces: dict) -> list:
        position = self.get_position(board)
        possible_moves = move_search(board, position, self, filtered=False, format='-list')
        return possible_moves
        
class Knight(Piece): # can jump in L shape => 8 DOF
    def __init__(self, colour: colour, rect) -> None:
        super().__init__(colour)
        self.id = "N"
        self.moveset = [(-2,+1),(-1,+2),(+1,+2),(+2,+1),(+2,-1),(+1,-2),(-1,-2),(-2,-1)]
        if colour == colour.WHITE:
            self.img = SPRITES_DICT["w_knight"]
        elif colour == colour.BLACK:
            self.img = SPRITES_DICT["b_knight"]
        self.rect = self.img.get_rect(topleft=(rect.x, rect.y))

    def get_legal_moves(self,board,pieces) -> list:
        possible_moves = []
        position = self.get_position(board)
        for move in self.moveset:
            # Add move vector from moveset to the piece's current position
            new_move = (position[0]+move[0],position[1]+move[1])
            # Check if new_move is within board boundaries
            if 0 <= new_move[0] <= 7 and 0 <= new_move[1] <= 7: 
                content = board[new_move[0]][new_move[1]]
                if content != None and content.colour != self.colour:
                    possible_moves.append(idx_to_name(new_move))
                elif content == None:
                    possible_moves.append(idx_to_name(new_move))   
        return possible_moves
    
    def get_attacking_squares(self, board: list, pieces: dict):
        return self.get_legal_moves(board,pieces)


class Bishop(Piece): # can move diagonally => 4 DOF
    def __init__(self, colour: colour, rect) -> None:
        super().__init__(colour)
        self.id = "B"
        self.moveset = ["NE","SE","SO","NO"]
        if colour == colour.WHITE:
            self.img = SPRITES_DICT["w_bishop"]
        elif colour == colour.BLACK:
            self.img = SPRITES_DICT["b_bishop"]
        self.rect = self.img.get_rect(topleft=(rect.x, rect.y))


class Rook(Piece): # can move horizontally and vertically => 4 DOF
    def __init__(self, colour: colour, rect) -> None:
        super().__init__(colour)
        self.id = "R"
        self.moveset = ["N","E","S","O"]
        if colour == colour.WHITE:
            self.img = SPRITES_DICT["w_rook"]
        elif colour == colour.BLACK:
            self.img = SPRITES_DICT["b_rook"]
        self.rect = self.img.get_rect(topleft=(rect.x, rect.y))


class Pawn(Piece): # 1.5 DOF
    def __init__(self, colour: colour, rect) -> None:
        super().__init__(colour)
        self.id = "p"
        if colour == colour.WHITE:
            self.moveset = ["N","NE","NO"]
            self.starting_row = 6
            self.img = SPRITES_DICT["w_pawn"]
        elif colour == colour.BLACK:
            self.moveset = ["S","SE","SO"]
            self.starting_row = 1
            self.img = SPRITES_DICT["b_pawn"]
        else:
            raise Exception("colour value should be WHITE or BLACK")
        self.rect = self.img.get_rect(topleft=(rect.x, rect.y))
        
    def get_legal_moves(self, board: list, pieces: dict):
        #TODO: add en-passant
        position = self.get_position(board)
        self.movedepth = 2 if position[0] == self.starting_row else 1
        
        possible_moves_dict = move_search(board,position,self,filtered=True,format='-dict')
        possible_moves_list = []
        
        # Add vertical squares to possible moves if square is empty
        vertical_moves = possible_moves_dict[self.moveset[0]]
        for move in vertical_moves:
            content = board[name_to_idx(move)[0]][name_to_idx(move)[1]]
            if content == None:
                possible_moves_list.append(move)
        
        # Get the first square of each diagonal <- needed when pawn is on starting rank and has a movedepth of 2
        diagonal_moves = []
        for i in [1,2]: # <- these correspond to the indices of the diagonals in self.moveset
            diagonal_squares = possible_moves_dict[self.moveset[i]]
            if len(diagonal_squares) != 0:
                diagonal_moves.append(diagonal_squares[0])
            
        # Add square of each diagonal ONLY if square is occupied by enemy        
        for move in diagonal_moves:
            content = board[name_to_idx(move)[0]][name_to_idx(move)[1]]
            if content != None and content.colour != self.colour:
                possible_moves_list.append(move)
        
        return possible_moves_list
    
    def get_attacking_squares(self, board: list, pieces: dict) -> list:
        position = self.get_position(board)
        self.movedepth = 1 # because pawns only threaten the first diagonal squares
        
        possible_moves_dict = move_search(board,position,self,filtered=False,format='-dict')
        
        diagonal_moves = possible_moves_dict[self.moveset[1]] + possible_moves_dict[self.moveset[2]] 
        return diagonal_moves
        

def move_search(board: list, origin: tuple, piece: Piece, filtered: bool=False, format: str='-list'):
    # Get parameters from piece object
    moveset = piece.moveset
    depth = piece.movedepth
    colour = piece.colour
    
    # Ensure depth is well defined
    if depth == None: depth = len(BOARD_REF) #default to searching whole array
    elif depth < len(BOARD_REF): depth += 1 #+1 because range() excludes the upper bound
    elif depth >= len(BOARD_REF): depth = len(BOARD_REF) #caping the value of depth

    moves_dict = {}
    # Search squares in every direction of the piece's moveset
    for direction in moveset:  
        # Initialize the direction as a key in the move_dict
        moves_dict[direction] = []
        
        for i in range(1,depth):
            # Move by 1 element in the current direction
            search_pos = ( origin[0] + i * ARRAY_CARDINALS[direction][0],
                           origin[1] + i * ARRAY_CARDINALS[direction][1]) 
            
            # Skip current search position if NOT within boundaries of BOARD_REF
            if search_pos[0] < 0 or search_pos[0] >= len(board) or search_pos[1] < 0 or search_pos[1] >= len(board):
                continue

            # Convert array position to square name (e.g. 'a1', 'g8')
            square = BOARD_REF[search_pos[0]][search_pos[1]]

            if filtered:
                # Check content of current square in search
                content = board[search_pos[0]][search_pos[1]]
                # Stop search in this direction if ENEMY piece is hit and append square to move_dict
                if content != None and content.colour != colour:
                    moves_dict[direction].append(square)
                    break
                # Stop search in this direction if FIRENDLY piece is hit but DO NOT append square to move_dict
                elif content != None and content.colour == colour:
                    break
                
            moves_dict[direction].append(square)
    
    # Return dictionary if specified
    if format == '-dict':
        return moves_dict
    # Return list as default
    elif format == '-list':
        return move_dict_to_list(moves_dict)
    else:
        raise Exception("move_search: 'format' argument is invalid. Should either be '-dict' or '-list'")


def capture_piece(piece,piece_dict):
    if piece.colour == colour.WHITE:
        piece_dict["active_white"].remove(piece)
        piece_dict["captured_white"].append(piece)
    elif piece.colour == colour.BLACK:
        piece_dict["active_black"].remove(piece)
        piece_dict["captured_black"].append(piece)     
    return piece_dict

def get_squares_under_threat(board: list, pieces: dict, piece_colour: colour):
    # Used by king to identify squares it shouldn't move to
    
    if piece_colour == colour.WHITE:
            enemy_pieces = pieces["active_black"]
    elif piece_colour == colour.BLACK:
            enemy_pieces = pieces["active_white"]
            
    possible_moves = []
    for piece in enemy_pieces:
        possible_moves += piece.get_attacking_squares(board,pieces)

    return list(set(possible_moves)) #convert to set to remove duplicate values
    