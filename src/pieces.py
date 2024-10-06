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

    # Calculate the possible moves for a piece irrespective of board state
    def get_possible_moves(self, board: list, pieces: dict) -> list:
        position = self.get_position(board)
        possible_moves = move_search(board, position, self, filtered=False, format='-list')
        return possible_moves
    
    # Filter possible moves to take into account board state
    def get_legal_moves(self, board: list, pieces: dict):
        position = self.get_position(board)
        possible_moves = move_search(board, position, self, filtered=True, format='-list')
        return possible_moves

    
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
        
    #TODO in possible moves don't include spaces that are threatened by an enemy piece <= need a way to determine that
    # option 1: calculate all the possible moves of enemy pieces then check if kings possible moves are part of that list
    #           - need a reference to all active pieces of the opposite colour     
    
    def get_possible_moves(self, board: list, pieces: dict) -> list:
        return super().get_possible_moves(board, pieces)
    
    def get_legal_moves(self, board: list, pieces: dict):
        possible_moves = super().get_possible_moves(board,pieces)
        
        return super().get_legal_moves(board, pieces)
        # possible_moves = super().get_possible_moves(board,pieces)
        # enemy_moves = get_possible_moves_enemy(board,pieces,self.colour)
        # filtered_possible_moves = []
        # for move in possible_moves:
        #     if move not in enemy_moves:
        #         filtered_possible_moves.append(move)
        # return filtered_possible_moves
        
        
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

    def get_possible_moves(self,board,pieces) -> list:
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
    
    def get_legal_moves(self, board: list, pieces: dict):
        return self.get_possible_moves(board,pieces)


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
        
    def get_possible_moves(self, board: list, pieces: dict) -> list:
        #TODO: move diagonally one if it is capturing a piece
        #TODO: en-passant
        position = self.get_position(board)
        self.movedepth = 2 if position[0] == self.starting_row else 1
        
        possible_moves_list = []
        possible_moves_dict = move_search(board,position,self,filtered=False,format='-dict')
        
        # Add vertical squares to possible moves
        vertical_moves = possible_moves_dict[self.moveset[0]]
        possible_moves_list += vertical_moves
        
        # Only include first square in diagonals
        diagonals = [1,2] # <- corresponds to indices in self.moveset that are diagonals (e.g. index 1 = 'NE' for white, 'SE' for black)
        for i in diagonals:
            diagonal_moves = possible_moves_dict[self.moveset[i]]
            possible_moves_list.append(diagonal_moves[0])
        
        return possible_moves_list
    
    def get_legal_moves(self, board: list, pieces: dict):
        position = self.get_position(board)
        self.movedepth = 2 if position[0] == self.starting_row else 1
        
        possible_moves_list = []
        possible_moves_dict = move_search(board,position,self,filtered=True,format='-dict')
        
        # Add vertical squares to possible moves
        vertical_moves = possible_moves_dict[self.moveset[0]]
        possible_moves_list += vertical_moves
        
        # Add diagonal movement ONLY if square is occupied by enemy
        diagonal_moves = possible_moves_dict[self.moveset[1]] + possible_moves_dict[self.moveset[2]]
        for move in diagonal_moves:
            content = board[name_to_idx(move)[0]][name_to_idx(move)[1]]
            if content != None and content.colour != self.colour:
                possible_moves_list.append(move)
        
        return possible_moves_list
        
        
        

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

def get_possible_moves_enemy(board: list, pieces: dict, piece_colour: colour):
    # Used by king to identify squares it shouldn't move to
    
    if piece_colour == colour.WHITE:
            enemy_pieces = pieces["active_black"]
    elif piece_colour == colour.BLACK:
            enemy_pieces = pieces["active_white"]
            
    all_possible_moves = []
    for piece in enemy_pieces:
        if type(piece) == King:
            continue
        #TODO: fix infinite recursion when enemy king is inccluded
        possible_moves = piece.get_possible_moves(board,pieces)
        all_possible_moves += possible_moves
        
    return list(set(all_possible_moves)) #convert to set to remove duplicate values
    