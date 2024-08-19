#script to TEST the directional array search
from main import BOARD_REF
from main import get_index
from functions.directional_search import * 

board_example = [['R_b', 'N_b', 'B_b', 'Q_b', 'K_b', 'B_b', 'N_b', 'R_b'],
                 ['p_b', 'p_b', 'p_b', 'p_b', 'p_b', 'p_b', 'p_b', 'p_b'],
                 ['___', '___', '___', '___', '___', '___', '___', '___'],
                 ['___', '___', '___', '___', '___', '___', '___', '___'],
                 ['___', '___', '___', '___', '___', '___', '___', '___'],
                 ['___', '___', '___', '___', '___', '___', '___', '___'],
                 ['p_w', 'p_w', 'p_w', 'p_w', 'p_w', 'p_w', 'p_w', 'p_w'],
                 ['R_w', 'N_w', 'B_w', 'Q_w', 'K_w', 'B_w', 'N_w', 'R_w']]

def test():
    origin = input("Origin of search (e.g. a1, e4 etc.): ")

    origin_idx = get_index(origin)
    depth = None
    search_directions = ["N","E","S","O","NE","SE","SO","NO"]
    results = search(board_example,origin_idx,search_directions,depth)

    for result in results:
        print(f"{result}: {results[result]}")
    
test()
