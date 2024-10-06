from src.constants import ARRAY_CARDINALS, BOARD_REF, Color
from src.sprites import SPRITES_DICT
from src.utilities import idx_to_name, name_to_idx

class Piece:
    def __init__(self, color: Color) -> None:
        self.color = color
        self.id = None
        self.moveset = None
        self.movedepth = None    

    # Return the position of the piece in a 8x8 array representing the board
    def get_position(self, board: list) -> tuple:
        for i in range(0,len(board)):
            if self in board[i]:
                return (i, board[i].index(self))

    # Calculate the possible moves for a piece irrespective of board state
    # idea: add filter parameter to determine whether user wants to filter or not
    def get_possible_moves(self, board: list, pieces: dict) -> list:
        position = self.get_position(board)
        possible_moves = cardinal_array_search(position,self.moveset,depth=self.movedepth,mode='-list')
        return possible_moves
    
    # Filter possible moves to take into account board state
    def get_legal_moves(self, board, possible_moves):
        pass
    
    
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
    
    def get_possible_moves(self, board: list, pieces: dict) -> list:
        possible_moves = super().get_possible_moves(board,pieces)
        enemy_moves = get_possible_moves_enemy(board,pieces,self.color)
        filtered_possible_moves = []
        for move in possible_moves:
            if move not in enemy_moves:
                filtered_possible_moves.append(move)
        return filtered_possible_moves
        
        
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

    def get_possible_moves(self,board,pieces) -> list:
        possible_moves = []
        position = self.get_position(board)
        for move in self.moveset:
            # Add move vector from moveset to the piece's current position
            new_move = (position[0]+move[0],position[1]+move[1])
            # Check if new_move is within board boundaries
            if 0 <= new_move[0] <= 7 and 0 <= new_move[1] <= 7: 
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
        
    def get_possible_moves(self, board: list, pieces: dict) -> list:
        #TODO: move diagonally one if it is capturing a piece
        #TODO: en-passant
        position = self.get_position(board)
        if position[0] == self.starting_row: 
            move_depth = 2 #can move up-two if on starting position
        else:  
            move_depth = 1 #move up one
        
        possible_moves = []
        possible_moves_dict = cardinal_array_search(position,self.moveset,depth=move_depth,mode='-dict')        
        
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
        

def cardinal_array_search(origin: tuple, directions: list, depth: int = None, mode: str='-list'):
    # Ensure depth is well defined
    if depth == None: depth = len(BOARD_REF) #default to searching whole array
    elif depth < len(BOARD_REF): depth += 1 #+1 because range() excludes the upper bound
    elif depth >= len(BOARD_REF): depth = len(BOARD_REF) #caping the value of depth

    results_dict = {}
    for direction in directions: #enables multidirectional search    
        # Initialize cardinal direction key in output dictionary
        results_dict[direction] = []
        
        for i in range(1,depth):
            # Store the current array position of the search
            position = ( origin[0] + ARRAY_CARDINALS[direction][0] * i,
                         origin[1] + ARRAY_CARDINALS[direction][1] * i ) 
            
            # Check if position is within boundaries of BOARD_REF
            if 0 <= position[0] < len(BOARD_REF) and 0 <= position[1] < len(BOARD_REF): 
                # Convert array position to square name (e.g. 'a1', 'g8')
                result = BOARD_REF[position[0]][position[1]]
                results_dict[direction].append(result)

                #Check if hit a piece
                # content = board[position[0]][position[1]]
                # #r = p # to return indices 
                # #r = board[p[0]][p[1]] # to return board contents
                # if content != None and content.color == color: #ignore pieces of the same color
                #     break
                # elif content != None and content.color != color:
                    
                #     results[direction].append(result)
                #     break
                # else:
                #     results[direction].append(result)
    
    # Output dictionary if specified
    if mode == '-dict':
        return results_dict
    # Output list as default
    else:
        results_list = []
        for direction in results_dict:
            results_list += results_dict[direction]
        return results_list


def capture_piece(piece,piece_dict):
    if piece.color == Color.WHITE:
        piece_dict["active_white"].remove(piece)
        piece_dict["captured_white"].append(piece)
    elif piece.color == Color.BLACK:
        piece_dict["active_black"].remove(piece)
        piece_dict["captured_black"].append(piece)     
    return piece_dict

def get_possible_moves_enemy(board: list, pieces: dict, piece_color: Color):
    # Used by king to identify squares it shouldn't move to
    
    if piece_color == Color.WHITE:
            enemy_pieces = pieces["active_black"]
    elif piece_color == Color.BLACK:
            enemy_pieces = pieces["active_white"]
            
    all_possible_moves = []
    for piece in enemy_pieces:
        if type(piece) == King:
            continue
        #TODO: fix infinite recursion when enemy king is inccluded
        possible_moves = piece.get_possible_moves(board,pieces)
        all_possible_moves += possible_moves
        
    return list(set(all_possible_moves)) #convert to set to remove duplicate values
    