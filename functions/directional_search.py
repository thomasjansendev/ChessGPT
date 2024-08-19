#Directional array search implementation
from main import BOARD_REF

ARRAY_CARDINALS = { "N":  (-1,0),
                    "NE": (-1,1),
                    "E":  (0,1),
                    "SE": (1,1),
                    "S":  (1,0),
                    "SO": (1,-1),
                    "O":  (0,-1),
                    "NO": (-1,-1) }

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