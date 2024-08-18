board_spaces = [["a8","b8","c8","d8","e8","f8","g8","h8"],
                ["a7","b7","c7","d7","e7","f7","g7","h7"],
                ["a6","b6","c6","d6","e6","f6","g6","h6"],
                ["a5","b5","c5","d5","e5","f5","g5","h5"],
                ["a4","b4","c4","d4","e4","f4","g4","h4"],
                ["a3","b3","c3","d3","e3","f3","g3","h3"],
                ["a2","b2","c2","d2","e2","f2","g2","h2"],
                ["a1","b1","c1","d1","e1","f1","g1","h1"]]

def main():
    board = init_board()
    result = None
    while result is None:
        try:
            result = new_move(board)
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
    #TODO (later): cache the board_space indicies into a dict
    for r in range(0,len(board_spaces)):
        if pos in board_spaces[r]:
            index = (r, board_spaces[r].index(pos))
            return index

def print_board(board):
    for row in board:
        print(row)

def new_move(board): #get input from user and update with selected move

    #get input
    print("Move from: ")
    old_pos_str = input()
    print("To: ")
    new_pos_str = input()

    #check if input is valid
    if len(old_pos_str) != 2 or len(new_pos_str) != 2:
        raise Exception("Error: Invalid input. Please provide a letter between a-h combined with a number between 1-8. Example 'a6','g1' etc.")

    old_pos_index = get_index(old_pos_str)
    new_pos_index = get_index(new_pos_str)
    
    #TODO: check whether input is valid (part of squares str "e1" etc.)
    #TODO: check whether move is legal: ask for input again if not

    board[new_pos_index[0]][new_pos_index[1]] = board[old_pos_index[0]][old_pos_index[1]]
    board[old_pos_index[0]][old_pos_index[1]] = " "
    
    print_board(board)
    return board

def is_move_legal(board,old_pos_str,new_pos_str):
    
    old_pos_index = get_index(old_pos_str)
    new_pos_index = get_index(new_pos_str)

    #Check for available piece
    if board[old_pos_index[0]][old_pos_index[1]] == " ":
        print("No piece is available to move on {old_pos_str} ")
        return False
           
    return True



class Board:
    def __init__(self):
        pass


class Pawn:
    def __init__(self,colour):
        self.__init__ = colour
        self.position = ""



main()