board_ref = [["a8","b8","c8","d8","e8","f8","g8","h8"],
             ["a7","b7","c7","d7","e7","f7","g7","h7"],
             ["a6","b6","c6","d6","e6","f6","g6","h6"],
             ["a5","b5","c5","d5","e5","f5","g5","h5"],
             ["a4","b4","c4","d4","e4","f4","g4","h4"],
             ["a3","b3","c3","d3","e3","f3","g3","h3"],
             ["a2","b2","c2","d2","e2","f2","g2","h2"],
             ["a1","b1","c1","d1","e1","f1","g1","h1"]]

def main():
    board = init_board()
    # calc_possible_moves(board,"a1")
    result = None
    while result is None:
        try:
            result = new_move(board)
            board = result
        except Exception as e:
            print(e)


def init_board():
    
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

def get_index(pos: str):
    #TODO (later): cache indicies into a dict and call get_index during initialization 
    #to avoid searching for index each time
    for r in range(0,len(board_ref)):
        if pos in board_ref[r]:
            index = (r, board_ref[r].index(pos))
            return index

def print_board(board):
    for row in board:
        print(row)

def new_move(board):

    #get input
    old_pos_str = input("Move from: ")
    new_pos_str = input("To: ")

    #check if input is valid
    if (get_index(old_pos_str) == None or get_index(old_pos_str) == None):
        raise Exception("Invalid input. Please provide a letter between a-h combined with a number between 1-8. Example 'a6','g1' etc.")
    elif old_pos_str == new_pos_str:
        raise Exception("Must move piece to a different square than starting square.")

    #check if move is legal
    is_move_legal(board,old_pos_str,new_pos_str)

    #update board & print new state
    old_pos_index = get_index(old_pos_str)
    new_pos_index = get_index(new_pos_str)
    board[new_pos_index[0]][new_pos_index[1]] = board[old_pos_index[0]][old_pos_index[1]]
    board[old_pos_index[0]][old_pos_index[1]] = " "
    print_board(board)

    return board

def is_move_legal(board,old_pos_str,new_pos_str):
    
    if new_pos_str not in calc_possible_moves(board,old_pos_str): 
        raise Exception("Illegal move")
    
    #TODO check if another piece is blocking the movement of that piece

    return True

def calc_possible_moves(board: list,position_str: str):
    piece_rank = get_index(position_str)[0]
    piece_file = get_index(position_str)[1]
    piece_id = board[piece_rank][piece_file]

    if piece_id == " ": raise Exception(f"No piece is available to move on {position_str}")
    
    #TODO calculate legal moves for piece type
    possible_moves = []
    match piece_id:
        case "Q":
            #move diagonally, up and across
            pass
        case "K":
            #move up by one
            #move across by one
            pass
        case "N":
            #jump in an L shape
            pass
        case "B":
            #move diagonally
            pass
        case "R":
            #move up
            possible_moves += [rank[piece_file] for rank in board_ref]
            #move across
            possible_moves += board_ref[piece_rank][:]
            pass
        case "p":
            #move up one
            #move up-two if on starting position
            #move diagonally one if it is capturing a piece
            pass
        case _:
            raise Exception(f"Invalid piece_id")
    
    possible_moves = list(dict.fromkeys(possible_moves)) #removes duplicate values
    possible_moves.remove(position_str) #removes current piece position
    
    # print(possible_moves)
    return possible_moves

class Board:
    def __init__(self):
        pass


class Pawn:
    def __init__(self,colour):
        self.__init__ = colour
        self.position = ""



main()