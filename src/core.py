from src.pieces import *
from src.utilities import *

# ======= CORE FUNCTIONS =======

def new_move(board):

    #get input
    old_pos_str = input("Move from: ")
    new_pos_str = input("To: ")

    #check if input is valid
    if (get_index(old_pos_str) == None or get_index(old_pos_str) == None):
        raise Exception("Invalid input. Please provide a letter between a-h combined with a number between 1-8. Example 'a6','g1' etc.")
    elif old_pos_str == new_pos_str:
        raise Exception("Must move piece to a different square than starting square.")

    # #check if move is legal -> error is raised if not
    # possible_moves = calc_possible_moves(board,old_pos_str)
    # if new_pos_str not in possible_moves: 
    #     raise Exception(f"Illegal move. Possible moves for selected piece are {possible_moves}")

    #update board & print new state
    old_pos_index = get_index(old_pos_str)
    new_pos_index = get_index(new_pos_str)
    board[new_pos_index[0]][new_pos_index[1]] = board[old_pos_index[0]][old_pos_index[1]]
    board[old_pos_index[0]][old_pos_index[1]] = " "
    print_board(board)

    return board

def init_board() -> list:
    board = [[None for _ in range(8)] for _ in range(8)]
    # Queen Q
    board[get_index("d8")[0]][get_index("d8")[1]] = Queen("black")
    board[get_index("d1")[0]][get_index("d1")[1]] = Queen("white")
    # King K
    board[get_index("e8")[0]][get_index("e8")[1]] = King("black")
    board[get_index("e1")[0]][get_index("e1")[1]] = King("white")
    # Knights N
    board[get_index("b8")[0]][get_index("b8")[1]] = Knight("black")
    board[get_index("g8")[0]][get_index("g8")[1]] = Knight("black")
    board[get_index("b1")[0]][get_index("b1")[1]] = Knight("white")
    board[get_index("g1")[0]][get_index("g1")[1]] = Knight("white")
    # Bishop B
    board[get_index("c8")[0]][get_index("c8")[1]] = Bishop("black")
    board[get_index("f8")[0]][get_index("f8")[1]] = Bishop("black")
    board[get_index("c1")[0]][get_index("c1")[1]] = Bishop("white")
    board[get_index("f1")[0]][get_index("f1")[1]] = Bishop("white")
    # Rook R
    board[get_index("a8")[0]][get_index("a8")[1]] = Rook("black")
    board[get_index("h8")[0]][get_index("h8")[1]] = Rook("black")
    board[get_index("a1")[0]][get_index("a1")[1]] = Rook("white")
    board[get_index("h1")[0]][get_index("h1")[1]] = Rook("white")
    # Pawns p
    board[1] = [Pawn("black") for _ in range(len(board[0]))]
    board[6] = [Pawn("white") for _ in range(len(board[0]))]
    return board

def init_empty_board() -> list:
    board = [[None for _ in range(8)] for _ in range(8)]
    return board