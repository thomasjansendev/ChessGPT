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

def main():
    origin = input("Origin: ")
    origin_idx = get_index(origin)
    depth = None
    r_n = search(BOARD_REF,origin_idx,"N",depth)
    r_e = search(BOARD_REF,origin_idx,"E",depth)
    r_s = search(BOARD_REF,origin_idx,"S",depth)
    r_o = search(BOARD_REF,origin_idx,"O",depth)
    r_ne = search(BOARD_REF,origin_idx,"NE",depth)
    r_se = search(BOARD_REF,origin_idx,"SE",depth)
    r_so = search(BOARD_REF,origin_idx,"SO",depth)
    r_no = search(BOARD_REF,origin_idx,"NO",depth)
        
    print("=== VERT/HORI ===")
    print(f"North: {r_n}")
    print(f"Est: {r_e}")
    print(f"South: {r_s}")
    print(f"Ouest: {r_o}")
    
    print("=== DIAGONAL ===")
    print(f"North East: {r_ne}")
    print(f"South East: {r_se}")
    print(f"South Ouest: {r_so}")
    print(f"North Ouest: {r_no}")
    
    print("================")


def search(array: list, origin: tuple, direction: str, depth = None):
    #TODO: interupt if intercept a piece 
    #TODO: Optimize full search: need calculate shortest length needed instead of searching the whole length of array 
    
    if depth == None: depth = max(len(array),len(array[0])) #to manage none square matrices
    elif depth < 0: depth = 0
    elif depth < len(array): depth += 1
    elif depth >= len(array): depth = len(array)

    result = []
    for i in range(1,depth): #works for square or rectangular arrays
        
        p = (origin[0]+ARRAY_CARDINALS[direction][0]*i,
             origin[1]+ARRAY_CARDINALS[direction][1]*i ) 
        
        if 0 <= p[0] < len(array) and 0 <= p[1] < len(array):
            result.append(BOARD_REF[p[0]][p[1]])
    
    return result    
    
def get_index(pos_str: str):
    for r in range(0,len(BOARD_REF)):
        if pos_str in BOARD_REF[r]:
            index = (r, BOARD_REF[r].index(pos_str))
            return index
    
main()


