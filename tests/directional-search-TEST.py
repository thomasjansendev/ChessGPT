#script to TEST the directional array search
from constants import *
from core import search

def test():
    origin = input("Origin of search (e.g. a1, e4 etc.): ")

    origin_idx = get_index(origin)
    depth = None
    search_directions = ["N","E","S","O","NE","SE","SO","NO"]
    results = search(BOARD_INIT_W,origin_idx,search_directions,depth)

    for result in results:
        print(f"{result}: {results[result]}")

def get_index(pos_str: str):
    #TODO (later): cache indicies into a dict and call get_index during initialization 
    #to avoid searching for index each time
    for r in range(0,len(BOARD_REF)):
        if pos_str in BOARD_REF[r]:
            index = (r, BOARD_REF[r].index(pos_str))
            return index

test()
