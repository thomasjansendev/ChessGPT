from utilities import *
from constants import *

# ======= CORE FUNCTIONS =======

def init_board():
    #TODO: differentiate between black and white pieces
    board = [[" " for _ in range(8)] for _ in range(8)]
    
    # Queen Q
    board[get_index("d8")[0]][get_index("d8")[1]] = "Q" #black
    board[get_index("d1")[0]][get_index("d1")[1]] = "Q" #white

    # King K
    board[get_index("e8")[0]][get_index("e8")[1]] = "K" #black
    board[get_index("e1")[0]][get_index("e1")[1]] = "K" #white

    # Knights N
    board[get_index("b8")[0]][get_index("b8")[1]] = "N" #black
    board[get_index("g8")[0]][get_index("g8")[1]] = "N" #black
    board[get_index("b1")[0]][get_index("b1")[1]] = "N" #white
    board[get_index("g1")[0]][get_index("g1")[1]] = "N" #white

    # Bishop B
    board[get_index("c8")[0]][get_index("c8")[1]] = "B" #black
    board[get_index("f8")[0]][get_index("f8")[1]] = "B" #black
    board[get_index("c1")[0]][get_index("c1")[1]] = "B" #white
    board[get_index("f1")[0]][get_index("f1")[1]] = "B" #white

    # Rook R
    board[get_index("a8")[0]][get_index("a8")[1]] = "R" #black
    board[get_index("h8")[0]][get_index("h8")[1]] = "R" #black
    board[get_index("a1")[0]][get_index("a1")[1]] = "R" #white
    board[get_index("h1")[0]][get_index("h1")[1]] = "R" #white

    # Pawns p
    board[1] = ["p" for _ in range(len(board[1]))]
    board[6] = ["p" for _ in range(len(board[1]))]

    # print_board(board)        
    return board

def new_move(board):

    #get input
    old_pos_str = input("Move from: ")
    new_pos_str = input("To: ")

    #check if input is valid
    if (get_index(old_pos_str) == None or get_index(old_pos_str) == None):
        raise Exception("Invalid input. Please provide a letter between a-h combined with a number between 1-8. Example 'a6','g1' etc.")
    elif old_pos_str == new_pos_str:
        raise Exception("Must move piece to a different square than starting square.")

    #check if move is legal -> error is raised if not
    # if new_pos_str not in calc_possible_moves(board,old_pos_str): 
    #     raise Exception(f"Illegal move. Possible moves for selected piece are {calc_possible_moves(board,old_pos_str)}")

    #update board & print new state
    old_pos_index = get_index(old_pos_str)
    new_pos_index = get_index(new_pos_str)
    board[new_pos_index[0]][new_pos_index[1]] = board[old_pos_index[0]][old_pos_index[1]]
    board[old_pos_index[0]][old_pos_index[1]] = " "
    print_board(board)

    return board

def calc_possible_moves(board: list,position_str: str):
    piece_idx = get_index(position_str)
    piece_rank = get_index(position_str)[0]
    piece_file = get_index(position_str)[1]
    piece_id = board[piece_rank][piece_file]

    if piece_id == " ": raise Exception(f"No piece is available to move on {position_str}")
    
    #TODO calculate legal moves for piece type
    possible_moves_str = []
    possible_moves_idx = []
    match piece_id:
        
        case "Q": # can move in any direction => 8 DOF - :
            moves_dict = search(board,piece_idx,["N","E","S","O","NE","SE","SO","NO"])
            for key in moves_dict:
                possible_moves_str += moves_dict[key]

        case "K": # can move to any adjacent square by 1 => 8 DOF - 1 || cannot move to a space threatened by an opponent piece
            #TODO remove spaces that are threatened by an enemy piece <= need a way to determine that
            moves_dict = search(board,piece_idx,["N","E","S","O","NE","SE","SO","NO"],depth=1)
            for key in moves_dict:
                possible_moves_str += moves_dict[key]

        case "N": # can jump in L shape => 8 DOF - N/A
            knight_moveset = [(-2,+1),(-1,+2),(+1,+2),(+2,+1),(+2,-1),(+1,-2),(-1,-2),(-2,-1)]
            for move in knight_moveset:
                new_move = (piece_idx[0]+move[0],piece_idx[1]+move[1]) #add moveset to the piece's current position
                if 0 <= new_move[0] <= 7 and 0 <= new_move[1] <= 7: #only accept positions that are within board boundaries
                    possible_moves_str.append(get_pos_name(new_move))

        case "B": # can move diagonally => 4 DOF - :
            moves_dict = search(board,piece_idx,["NE","SE","SO","NO"])
            for key in moves_dict:
                possible_moves_str += moves_dict[key]


        case "R": # can move horizontally and vertically => 4 DOF - :
            moves_dict = search(board,piece_idx,["N","E","S","O"])
            for key in moves_dict:
                possible_moves_str += moves_dict[key]
            pass


        case "p": # 1.5 DOF - 2->1
            #move up one
            #move up-two if on starting position
            #move diagonally one if it is capturing a piece
            pass


        case _:
            raise Exception(f"Invalid piece_id")
    
    
    print(possible_moves_str)
    return possible_moves_str

def search(array: list, origin: tuple, directions: list, depth: int = None):
    #TODO: snip the last element of possible moves if it is a piece of the same colour
    #TODO: Optimize full search: figure out shortest length needed instead of searching the whole length of array
    #TODO: integrate search with possible moves -> main()

    #make sure depth is well defined
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
                r = BOARD_REF[p[0]][p[1]] #'= p' to return indices #'= array[p[0]][p[1]]' to return board contents
                
                if direction in results: results[direction].append(r)
                else: results[direction] = [r]
                
                if array[p[0]][p[1]] != '___': #true: piece is hit
                    break
    
    return results