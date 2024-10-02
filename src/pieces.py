from src.constants import ARRAY_CARDINALS, BOARD_REF, Color
from src.sprites import SPRITES_DICT
from src.utilities import idx_to_name, name_to_idx

class Piece:
    def __init__(self, color: Color) -> None:
        self.color = color
        self.id = None
        self.moveset = None
        self.movedepth = None        
            
    def calc_possible_moves(self,board: list) -> list:
        position = self.get_position(board)
        possible_moves = []
        possible_moves_dict = cardinal_array_search(board,position,self.moveset,self.color,depth=self.movedepth)
        for direction in possible_moves_dict:
            possible_moves += possible_moves_dict[direction]
        return possible_moves

    def get_position(self, board: list) -> tuple:
        for i in range(0,len(board)):
            if self in board[i]:
                return (i, board[i].index(self))
    
    
class Queen(Piece): # can move in any direction => 8 DOF
    def __init__(self, color: Color, rect) -> None:
        super().__init__(color)
        self.id = "Q"
        self.moveset = ["N","E","S","O","NE","SE","SO","NO"]
        if color == Color.WHITE:
            self.img = SPRITES_DICT["w_queen"]
        elif color == Color.BLACK:
            self.img = SPRITES_DICT["b_queen"]
        self.rect = self.img.get_rect(topleft=(rect.x, rect.y))
        
        
class King(Piece): # can move to any adjacent square by 1 => 8 DOF
    def __init__(self, color: Color, rect) -> None:
        super().__init__(color)
        self.id = "K"
        self.moveset = ["N","E","S","O","NE","SE","SO","NO"]
        self.movedepth = 1
        if color == Color.WHITE:
            self.img = SPRITES_DICT["w_king"]
        elif color == Color.BLACK:
            self.img = SPRITES_DICT["b_king"]
        self.rect = self.img.get_rect(topleft=(rect.x, rect.y))
        
    #TODO in possible moves don't include spaces that are threatened by an enemy piece <= need a way to determine that
    # option 1: calculate all the possible moves of enemy pieces then check if kings possible moves are part of that list
    #           - need a reference to all active pieces of the opposite colour
    #           
    
        
        
class Knight(Piece): # can jump in L shape => 8 DOF
    def __init__(self, color: Color, rect) -> None:
        super().__init__(color)
        self.id = "N"
        self.moveset = [(-2,+1),(-1,+2),(+1,+2),(+2,+1),(+2,-1),(+1,-2),(-1,-2),(-2,-1)]
        if color == Color.WHITE:
            self.img = SPRITES_DICT["w_knight"]
        elif color == Color.BLACK:
            self.img = SPRITES_DICT["b_knight"]
        self.rect = self.img.get_rect(topleft=(rect.x, rect.y))

    def calc_possible_moves(self,board) -> list:
        possible_moves = []
        position = self.get_position(board)
        for move in self.moveset:
            new_move = (position[0]+move[0],position[1]+move[1]) #add move vector from moveset to the piece's current position
            if 0 <= new_move[0] <= 7 and 0 <= new_move[1] <= 7: #only accept positions that are within board boundaries
                content = board[new_move[0]][new_move[1]]
                if content != None and content.color != self.color:
                    possible_moves.append(idx_to_name(new_move))
                elif content == None:
                    possible_moves.append(idx_to_name(new_move))   
        return possible_moves


class Bishop(Piece): # can move diagonally => 4 DOF
    def __init__(self, color: Color, rect) -> None:
        super().__init__(color)
        self.id = "B"
        self.moveset = ["NE","SE","SO","NO"]
        if color == Color.WHITE:
            self.img = SPRITES_DICT["w_bishop"]
        elif color == Color.BLACK:
            self.img = SPRITES_DICT["b_bishop"]
        self.rect = self.img.get_rect(topleft=(rect.x, rect.y))


class Rook(Piece): # can move horizontally and vertically => 4 DOF
    def __init__(self, color: Color, rect) -> None:
        super().__init__(color)
        self.id = "R"
        self.moveset = ["N","E","S","O"]
        if color == Color.WHITE:
            self.img = SPRITES_DICT["w_rook"]
        elif color == Color.BLACK:
            self.img = SPRITES_DICT["b_rook"]
        self.rect = self.img.get_rect(topleft=(rect.x, rect.y))


class Pawn(Piece): # 1.5 DOF
    def __init__(self, color: Color, rect) -> None:
        super().__init__(color)
        self.id = "p"
        if color == Color.WHITE:
            self.moveset = ["N","NE","NO"]
            self.starting_row = 6
            self.img = SPRITES_DICT["w_pawn"]
        elif color == Color.BLACK:
            self.moveset = ["S","SE","SO"]
            self.starting_row = 1
            self.img = SPRITES_DICT["b_pawn"]
        else:
            raise Exception("Color value should be WHITE or BLACK")
        self.rect = self.img.get_rect(topleft=(rect.x, rect.y))
        
    def calc_possible_moves(self,board) -> list:
        #TODO: move diagonally one if it is capturing a piece
        #TODO: en-passant
        position = self.get_position(board)
        if position[0] == self.starting_row: 
            move_depth = 2 #can move up-two if on starting position
        else:  
            move_depth = 1 #move up one
        
        possible_moves = []
        possible_moves_dict = cardinal_array_search(board,position,self.moveset,self.color,depth=move_depth)        
        
        #TODO: since the move depth of pawns is just one we can remove the for loop and
        #filter moves on vertical 'N' or 'S'
        for move in possible_moves_dict[self.moveset[0]]: 
            content = board[name_to_idx(move)[0]][name_to_idx(move)[1]]
            if content == None:
                possible_moves.append(move)
        #filter moves on first diagonal 'NE' or 'SE'
        for move in possible_moves_dict[self.moveset[1]]:
            content = board[name_to_idx(move)[0]][name_to_idx(move)[1]]
            if content != None and content.color != self.color:
                possible_moves.append(move)
        #filter moves on second diagonal 'NO' or 'SO'
        for move in possible_moves_dict[self.moveset[2]]:
            content = board[name_to_idx(move)[0]][name_to_idx(move)[1]]
            if content != None and content.color != self.color:
                possible_moves.append(move)
        
        return possible_moves
        

def cardinal_array_search(board: list, origin: tuple, directions: list, color, depth: int = None) -> dict:
    #check depth is well defined
    if depth == None: depth = len(board) #default to searching whole array
    elif depth < len(board): depth += 1 #+1 because range() excludes the upper bound
    elif depth >= len(board): depth = len(board) #caping the value of depth

    results = {}
    for direction in directions: #enables multidirectional search    
        results[direction] = []
        for i in range(1,depth):
            
            position = ( origin[0] + ARRAY_CARDINALS[direction][0] * i,
                         origin[1] + ARRAY_CARDINALS[direction][1] * i ) 
            
            if 0 <= position[0] < len(board) and 0 <= position[1] < len(board): #check if within boundaries of board
                result = BOARD_REF[position[0]][position[1]] # to return square name (e.g. 'a1' 'g8')
                content = board[position[0]][position[1]]
                #r = p # to return indices 
                #r = board[p[0]][p[1]] # to return board contents
                if content != None and content.color == color: #ignore pieces of the same color
                    break
                elif content != None and content.color != color:
                    results[direction].append(result)
                    break
                else:
                    results[direction].append(result)
    
    return results

def capture_piece(piece,piece_dict):
    if piece.color == Color.WHITE:
        piece_dict["active_white"].remove(piece)
        piece_dict["captured_white"].append(piece)
    elif piece.color == Color.BLACK:
        piece_dict["active_black"].remove(piece)
        piece_dict["captured_black"].append(piece)     
    return piece_dict
    