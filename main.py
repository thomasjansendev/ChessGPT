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
    debug_move(board, "e1","e4")
    calc_possible_moves(board,"e4")

    # idx = get_index("h7")
    # print(idx)
    # str = get_pos_name(idx)
    # print(str)
    
    # result = None
    # while result is None:
    #     try:
    #         result = new_move(board)
    #         board = result
    #     except Exception as e:
    #         print(e)


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

def get_index(pos_str: str):
    #TODO (later): cache indicies into a dict and call get_index during initialization 
    #to avoid searching for index each time
    for r in range(0,len(board_ref)):
        if pos_str in board_ref[r]:
            index = (r, board_ref[r].index(pos_str))
            return index

def get_pos_name(pos_idx: tuple):
    return board_ref[pos_idx[0]][pos_idx[1]]

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

    #check if move is legal -> error is raised if not
    if new_pos_str not in calc_possible_moves(board,old_pos_str): 
        raise Exception(f"Illegal move. Possible moves for selected piece are {calc_possible_moves(board,old_pos_str)}")

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
    #TODO check if another piece is blocking the movement of that piece
    possible_moves_str = []
    possible_moves_idx = []
    match piece_id:
        
        case "Q": # can move in any direction => 8 DOF - :
            pass


        case "K": # can move to any adjacent square by 1 => 8 DOF - 1
            king_moveset = [(-1,0),(-1,+1),(0,+1),(+1,+1),(+1,0),(+1,-1),(0,-1),(-1,-1)]
            for move in king_moveset:
                new_move = (piece_idx[0]+move[0],piece_idx[1]+move[1]) #add moveset to the piece's current position
                if 0 <= new_move[0] <= 7 and 0 <= new_move[1] <= 7: #only accept positions that are within board boundaries
                    possible_moves_str.append(get_pos_name(new_move))


        case "N": # can jump in L shape => 8 DOF - N/A
            knight_moveset = [(-2,+1),(-1,+2),(+1,+2),(+2,+1),(+2,-1),(+1,-2),(-1,-2),(-2,-1)]
            for move in knight_moveset:
                new_move = (piece_idx[0]+move[0],piece_idx[1]+move[1]) #add moveset to the piece's current position
                if 0 <= new_move[0] <= 7 and 0 <= new_move[1] <= 7: #only accept positions that are within board boundaries
                    possible_moves_str.append(get_pos_name(new_move))

        case "B": # can move diagonally => 4 DOF - :
            pass


        case "R": # can move horizontally and vertically => 4 DOF - :
            possible_moves_str += [rank[piece_file] for rank in board_ref] # vertical movement
            possible_moves_str += board_ref[piece_rank][:] # horizontal movement
            possible_moves_str = list(dict.fromkeys(possible_moves_str)) # removes duplicate values
            possible_moves_str.remove(position_str) # removes current piece position
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

def debug_move(board,old_pos_str,new_pos_str):
    old_pos_index = get_index(old_pos_str)
    new_pos_index = get_index(new_pos_str)
    board[new_pos_index[0]][new_pos_index[1]] = board[old_pos_index[0]][old_pos_index[1]]
    board[old_pos_index[0]][old_pos_index[1]] = " "


main()