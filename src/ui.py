import pygame

SCREEN_WIDTH = 768
SCREEN_HEIGHT = 768

def load_sprites() -> dict:
    sprite_dir = "./sprites/png/"
    sprites_filepaths = {
        "square_dark": "",
        "square_light": "",
        "w_bishop": "",
        "w_king": "",
        "w_knight": "",     
        "w_pawn": "",  
        "w_queen": "",
        "w_rook": "",
        "b_bishop": "",
        "b_king": "",
        "b_knight": "",     
        "b_pawn": "",  
        "b_queen": "",
        "b_rook": "",
    }
    
    return sprites_filepaths

