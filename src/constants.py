ROWS, COLS = 8, 8
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512
SPRITE_WIDTH = SCREEN_WIDTH / COLS
SPRITE_HEIGHT = SCREEN_HEIGHT / ROWS
CELL_WIDTH, CELL_HEIGHT = SPRITE_WIDTH, SPRITE_HEIGHT

from enum import Enum
colour = Enum('colour', ['WHITE', 'BLACK'])

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