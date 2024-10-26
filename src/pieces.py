from src.constants import ARRAY_CARDINALS, BOARD_REF
from src.sprites import SPRITES_DICT
from src.utilities import idx_to_name, name_to_idx, move_dict_to_list
# from src.board import Board

class Piece:
    def __init__(self, colour: str) -> None:
        self.colour = colour
        self.id = None
        self.moveset = None
        self.movedepth = None
        self.rect = None

    # Return the position of the piece in a 8x8 array representing the board
    def get_position(self, board_array: list) -> tuple:
        # this could be removed if the piece's position was tracked as a class attribute -> TODO: Later
        for i in range(0,len(board_array)):
            if self in board_array[i]:
                return (i, board_array[i].index(self))

    # Returns a list of square names that the piece can legally move to
    def get_legal_moves(self, board, position:tuple=None) -> list: #TODO: (perf) add position as method parameter
        board_array = board.array
        if position == None: # temp check until position parameter is fully utilized
            position = self.get_position(board_array)
        possible_moves = move_search(board_array, position, self, mode='-legal', format='-list')
        return possible_moves
    
    # Returns a list of squares that are threatened by this piece
    def get_attacking_squares(self, board) -> list:
        board_array = board.array
        position = self.get_position(board_array)
        possible_moves = move_search(board_array, position, self, mode='-attacking', format='-list')
        return possible_moves

    
class Queen(Piece): # can move in any direction => 8 DOF
    def __init__(self, colour: str) -> None:
        super().__init__(colour)
        self.moveset = ["N","E","S","O","NE","SE","SO","NO"]
        if colour == 'w':
            self.id = "Q"
            self.img = SPRITES_DICT["w_queen"]
        elif colour == 'b':
            self.id = "q"
            self.img = SPRITES_DICT["b_queen"]
        # self.rect = self.img.get_rect(topleft=(rect.x, rect.y))
        
        
class King(Piece): # can move to any adjacent square by 1 => 8 DOF
    def __init__(self, colour: str) -> None:
        super().__init__(colour)
        self.moveset = ["N","E","S","O","NE","SE","SO","NO"]
        self.movedepth = 1
        if colour == 'w':
            self.id = "K"     
            self.img = SPRITES_DICT["w_king"]
        elif colour == 'b':
            self.id = "k"
            self.img = SPRITES_DICT["b_king"]
        # self.rect = self.img.get_rect(topleft=(rect.x, rect.y))    
    
    def get_legal_moves(self, board, position=None) -> list:
        board_array = board.array
        if position == None: # temp check until position parameter is fully utilized
            position = self.get_position(board_array)
        possible_moves = move_search(board_array, position, self, mode='-legal', format='-list')
        squares_under_threat = get_squares_under_threat(board,self.colour)
        
        legal_moves = []
        for move in possible_moves:
            if move not in squares_under_threat:
                legal_moves.append(move)
        return legal_moves
        
    def get_attacking_squares(self, board) -> list:
            board_array = board.array
            position = self.get_position(board_array)
            possible_moves = move_search(board_array, position, self, mode='-attacking', format='-list')
            return possible_moves
        
class Knight(Piece): # can jump in L shape => 8 DOF
    def __init__(self, colour: str) -> None:
        super().__init__(colour)
        self.moveset = [(-2,+1),(-1,+2),(+1,+2),(+2,+1),(+2,-1),(+1,-2),(-1,-2),(-2,-1)]
        if colour == 'w':
            self.id = "N"
            self.img = SPRITES_DICT["w_knight"]
        elif colour == 'b':
            self.id = "n"
            self.img = SPRITES_DICT["b_knight"]
        # self.rect = self.img.get_rect(topleft=(rect.x, rect.y))

    def get_legal_moves(self, board, position=None) -> list:
        board_array = board.array
        if position == None: # temp check until position parameter is fully utilized
            position = self.get_position(board_array)
        possible_moves = []
        for move in self.moveset:
            # Add move vector from moveset to the piece's current position
            new_move = (position[0]+move[0],position[1]+move[1])
            # Check if new_move is within board boundaries
            if 0 <= new_move[0] <= 7 and 0 <= new_move[1] <= 7: 
                content = board_array[new_move[0]][new_move[1]]
                if content != None and content.colour != self.colour:
                    possible_moves.append(idx_to_name(new_move))
                elif content == None:
                    possible_moves.append(idx_to_name(new_move))   
        return possible_moves
    
    def get_attacking_squares(self, board):
        return self.get_legal_moves(board)


class Bishop(Piece): # can move diagonally => 4 DOF
    def __init__(self, colour: str) -> None:
        super().__init__(colour)
        self.moveset = ["NE","SE","SO","NO"]
        if colour == 'w':
            self.id = "B"
            self.img = SPRITES_DICT["w_bishop"]
        elif colour == 'b':
            self.id = "b"
            self.img = SPRITES_DICT["b_bishop"]
        # self.rect = self.img.get_rect(topleft=(rect.x, rect.y))


class Rook(Piece): # can move horizontally and vertically => 4 DOF
    def __init__(self, colour: str) -> None:
        super().__init__(colour)
        self.moveset = ["N","E","S","O"]
        if colour == 'w':
            self.id = "R"
            self.img = SPRITES_DICT["w_rook"]
        elif colour == 'b':
            self.id = "r"
            self.img = SPRITES_DICT["b_rook"]
        # self.rect = self.img.get_rect(topleft=(rect.x, rect.y))


class Pawn(Piece): # 1.5 DOF
    def __init__(self, colour: str) -> None:
        super().__init__(colour)
        if colour == 'w':
            self.id = "P"
            self.moveset = ["N","NE","NO"]
            self.starting_row = 6
            self.img = SPRITES_DICT["w_pawn"]
        elif colour == 'b':
            self.id = "p"
            self.moveset = ["S","SE","SO"]
            self.starting_row = 1
            self.img = SPRITES_DICT["b_pawn"]
        else:
            raise Exception("Colour value should be 'w' or 'b'")
        # self.rect = self.img.get_rect(topleft=(rect.x, rect.y))
        
    def get_legal_moves(self, board, position=None) -> list:
        #TODO: add en-passant
        board_array = board.array 
        if position == None: # temp check until position parameter is fully utilized
            position = self.get_position(board_array)
        self.movedepth = 2 if position[0] == self.starting_row else 1
        
        possible_moves_dict = move_search(board_array,position,self,mode='-legal',format='-dict')
        possible_moves_list = []
        
        # Add vertical squares to possible moves if square is empty
        vertical_moves = possible_moves_dict[self.moveset[0]]
        for move in vertical_moves:
            content = board_array[name_to_idx(move)[0]][name_to_idx(move)[1]]
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
            content = board_array[name_to_idx(move)[0]][name_to_idx(move)[1]]
            if content != None and content.colour != self.colour:
                possible_moves_list.append(move)
        
        return possible_moves_list
    
    def get_attacking_squares(self, board) -> list:
        board_array = board.array
        position = self.get_position(board_array)
        self.movedepth = 1 # because pawns only threaten the first diagonal squares
        
        possible_moves_dict = move_search(board_array,position,self,mode='-attacking',format='-dict')
        
        diagonal_moves = possible_moves_dict[self.moveset[1]] + possible_moves_dict[self.moveset[2]]
        return diagonal_moves
        

def move_search(board: list, origin: tuple, piece: Piece, mode: str='-legal', format: str='-list'):
    # mode = '-legal' returns legal moves for piece
    # mode = '-attacking' returns squares that are threatened by piece ignoring the king
    
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
            square = idx_to_name(search_pos)
            # Check content of current square in search
            content = board[search_pos[0]][search_pos[1]]

            # When user wants to return the legal moves of piece
            if mode == '-legal':
                # Stop search in this direction if ENEMY piece is hit and append square to move_dict
                if content != None and content.colour != colour:
                    moves_dict[direction].append(square)
                    break
                # Stop search in this direction if FIRENDLY piece is hit but DO NOT append square to move_dict
                elif content != None and content.colour == colour:
                    break
            
            # When user wants to return the squares that are threatened by piece ignoring the king -> used by King to calculate its legal moves
            if mode == '-attacking':
                # Stop search in this direction if piece is hit and append square to move_dict
                if content != None and type(content) != King: #TODO: this might lead to situations in which the 
                    moves_dict[direction].append(square)
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

def get_squares_under_threat(board, piece_colour: str):
    # Used by king to identify squares it shouldn't move to
    
    if piece_colour == 'w':
        enemy_pieces = board.active_pieces["b"]
    elif piece_colour == 'b':
        enemy_pieces = board.active_pieces["w"]
            
    possible_moves = []
    for piece in enemy_pieces:
        possible_moves += piece.get_attacking_squares(board)

    return list(set(possible_moves)) #convert to set to remove duplicate values
    