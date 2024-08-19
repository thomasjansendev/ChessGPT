#SCRIPT TO BUILD & TEST AN ARRAY SEARCH FUNCTION

BOARD_REF = [["a8","b8","c8","d8","e8","f8","g8","h8"],
             ["a7","b7","c7","d7","e7","f7","g7","h7"],
             ["a6","b6","c6","d6","e6","f6","g6","h6"],
             ["a5","b5","c5","d5","e5","f5","g5","h5"],
             ["a4","b4","c4","d4","e4","f4","g4","h4"],
             ["a3","b3","c3","d3","e3","f3","g3","h3"],
             ["a2","b2","c2","d2","e2","f2","g2","h2"],
             ["a1","b1","c1","d1","e1","f1","g1","h1"]]

ARRAY_CARDINALS = { "N":  (-1,0),
                    "NE": (-1,1),
                    "E":  (0,1),
                    "SE": (1,1),
                    "S":  (1,0),
                    "SO": (1,-1),
                    "O":  (0,-1),
                    "NO": (-1,-1) }

board_example = [['R_b', 'N_b', 'B_b', 'Q_b', 'K_b', 'B_b', 'N_b', 'R_b'],
                 ['p_b', 'p_b', 'p_b', 'p_b', 'p_b', 'p_b', 'p_b', 'p_b'],
                 ['___', '___', '___', '___', '___', '___', '___', '___'],
                 ['___', '___', '___', '___', '___', '___', '___', '___'],
                 ['___', '___', '___', '___', '___', '___', '___', '___'],
                 ['___', '___', '___', '___', '___', '___', '___', '___'],
                 ['p_w', 'p_w', 'p_w', 'p_w', 'p_w', 'p_w', 'p_w', 'p_w'],
                 ['R_w', 'N_w', 'B_w', 'Q_w', 'K_w', 'B_w', 'N_w', 'R_w']]

def main():
    origin = input("Origin: ")
    origin_idx = get_index(origin)
    depth = None
    # search_directions = ["N","E","S","O","NE","SE","SO","NO"]
    search_directions = ["N","E","S","O"]
    results = search(board_example,origin_idx,search_directions,depth)

    for result in results:
        print(f"{result}: {results[result]}")


def search(array: list, origin: tuple, directions: list, depth = None):
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
    
def get_index(pos_str: str):
    for r in range(0,len(BOARD_REF)):
        if pos_str in BOARD_REF[r]:
            index = (r, BOARD_REF[r].index(pos_str))
            return index
    
main()

# for i in range(1,depth): #works for square or rectangular arrays
    
#     p = (origin[0]+ARRAY_CARDINALS[direction][0]*i,
#             origin[1]+ARRAY_CARDINALS[direction][1]*i ) 
    
#     if 0 <= p[0] < len(array) and 0 <= p[1] < len(array):
#         result.append(BOARD_REF[p[0]][p[1]])
