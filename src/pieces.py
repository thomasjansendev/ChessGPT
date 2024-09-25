from enum import Enum
from src.constants import ARRAY_CARDINALS

Color = Enum('Color', ['WHITE', 'BLACK'])

class Piece:
    def __init__(self, color: Color) -> None:
        self.color = color
        self.id = None
        self.moveset = None
        self.movedepth = None
        
    def get_position(self, board: list) -> tuple:
        for i in range(0,len(board)):
            if self in board[i]:
                return (i, board[i].index(self))
            
    def calc_possible_moves(self,board) -> list:
        possible_moves = []
        position = self.get_position(board)
        moves_dict = cardinal_array_search(board,position,self.moveset,self.movedepth)
        for key in moves_dict:
            possible_moves += moves_dict[key]
        return possible_moves
    
    
class Queen(Piece): # can move in any direction => 8 DOF
    def __init__(self, color: Color) -> None:
        super().__init__(color)
        self.id = "Q"
        self.moveset = ["N","E","S","O","NE","SE","SO","NO"]
        
        
class King(Piece): # can move to any adjacent square by 1 => 8 DOF
    def __init__(self, color: Color) -> None:
        super().__init__(color)
        self.id = "K"
        self.moveset = ["N","E","S","O","NE","SE","SO","NO"]
        self.movedepth = 1
        
    #TODO in possible moves don't include spaces that are threatened by an enemy piece <= need a way to determine that
        
        
class Knight(Piece): # can jump in L shape => 8 DOF
    def __init__(self, color: Color) -> None:
        super().__init__(color)
        self.id = "N"
        self.moveset = [(-2,+1),(-1,+2),(+1,+2),(+2,+1),(+2,-1),(+1,-2),(-1,-2),(-2,-1)]

    def calc_possible_moves(self,board) -> list:
        possible_moves = []
        position = self.get_position(board)
        for move in self.moveset:
            new_move = (position[0]+move[0],position[1]+move[1]) #add move vector from moveset to the piece's current position
            if 0 <= new_move[0] <= 7 and 0 <= new_move[1] <= 7: #only accept positions that are within board boundaries
                possible_moves.append(new_move)
        return possible_moves


class Bishop(Piece): # can move diagonally => 4 DOF
    def __init__(self, color: Color) -> None:
        super().__init__(color)
        self.id = "B"
        self.moveset = ["NE","SE","SO","NO"]


class Rook(Piece): # can move horizontally and vertically => 4 DOF
    def __init__(self, color: Color) -> None:
        super().__init__(color)
        self.id = "R"
        self.moveset = ["N","E","S","O"]


class Pawn(Piece): # 1.5 DOF
    def __init__(self, color: Color) -> None:
        super().__init__(color)
        self.id = "p"
        if color == Color.WHITE:
            self.moveset = ["N","NE","NO"]
            self.starting_rank = 6
        elif color == Color.BLACK:
            self.moveset = ["S","SE","SO"]
            self.starting_rank = 1
        else:
            raise Exception("Color value should be WHITE or BLACK")
        
    def calc_possible_moves(self,board) -> list:
        #TODO: move diagonally one if it is capturing a piece
        #TODO: en-passant
        possible_moves = []
        position = self.get_position(board)
        
        #TODO: fix later once playing as black is possible (starting row for black is 1)
        if position[0] == self.starting_rank: 
            move_depth = 2 #can move up-two if on starting position
        else:  
            move_depth = 1 #move up one
        
        moves_dict = cardinal_array_search(board,position,self.moveset[0],move_depth)
        for key in moves_dict:
            possible_moves += moves_dict[key]
        
        return possible_moves
        

def cardinal_array_search(array: list, origin: tuple, directions: list, depth: int = None):
    #TODO: snip the last element of possible moves if it is a piece of the same colour
    #TODO: Optimize full search: figure out shortest length needed instead of searching the whole length of array

    #check depth is well defined
    if depth == None: depth = len(array) #default to searching whole array
    elif depth < 0: depth = 0
    elif depth < len(array): depth += 1 #+1 because range() excludes the upper bound
    elif depth >= len(array): depth = len(array) #caping the value of depth

    results = {}
    for direction in directions: #enables multidirectional search    
        
        for i in range(1,depth): #only works for square arrays such as a chess board
            
            p = ( origin[0] + ARRAY_CARDINALS[direction][0] * i,
                origin[1] + ARRAY_CARDINALS[direction][1] * i ) 
            
            if 0 <= p[0] < len(array) and 0 <= p[1] < len(array): #check if within boundaries of board
                #r = BOARD_REF[p[0]][p[1]] # to return square name (e.g. 'a1' 'g8')
                r = p # to return indices 
                #r = array[p[0]][p[1]] # to return board contents
                
                if direction in results: results[direction].append(r)
                else: results[direction] = [r]
                
                if array[p[0]][p[1]] != None: #true: piece is hit
                    break
    
    return results