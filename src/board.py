import pygame
from src.sprites import SPRITES_DICT
from src.utilities import *
from src.constants import *

def init_board() -> list:
    board = [[None for _ in range(8)] for _ in range(8)]
    # Queen Q
    board[name_to_idx("d8")[0]][name_to_idx("d8")[1]] = Queen(Color.BLACK)
    board[name_to_idx("d1")[0]][name_to_idx("d1")[1]] = Queen(Color.WHITE)
    # King K
    board[name_to_idx("e8")[0]][name_to_idx("e8")[1]] = King(Color.BLACK)
    board[name_to_idx("e1")[0]][name_to_idx("e1")[1]] = King(Color.WHITE)
    # Knights N
    board[name_to_idx("b8")[0]][name_to_idx("b8")[1]] = Knight(Color.BLACK)
    board[name_to_idx("g8")[0]][name_to_idx("g8")[1]] = Knight(Color.BLACK)
    board[name_to_idx("b1")[0]][name_to_idx("b1")[1]] = Knight(Color.WHITE)
    board[name_to_idx("g1")[0]][name_to_idx("g1")[1]] = Knight(Color.WHITE)
    # Bishop B
    board[name_to_idx("c8")[0]][name_to_idx("c8")[1]] = Bishop(Color.BLACK)
    board[name_to_idx("f8")[0]][name_to_idx("f8")[1]] = Bishop(Color.BLACK)
    board[name_to_idx("c1")[0]][name_to_idx("c1")[1]] = Bishop(Color.WHITE)
    board[name_to_idx("f1")[0]][name_to_idx("f1")[1]] = Bishop(Color.WHITE)
    # Rook R
    board[name_to_idx("a8")[0]][name_to_idx("a8")[1]] = Rook(Color.BLACK)
    board[name_to_idx("h8")[0]][name_to_idx("h8")[1]] = Rook(Color.BLACK)
    board[name_to_idx("a1")[0]][name_to_idx("a1")[1]] = Rook(Color.WHITE)
    board[name_to_idx("h1")[0]][name_to_idx("h1")[1]] = Rook(Color.WHITE)
    # Pawns p
    board[1] = [Pawn(Color.BLACK) for _ in range(len(board[0]))]
    board[6] = [Pawn(Color.WHITE) for _ in range(len(board[0]))]
    return board

def init_empty_board() -> list:
    board = [[None for _ in range(8)] for _ in range(8)]
    return board