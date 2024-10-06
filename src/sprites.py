import os
import pygame
from src.constants import *

def load_sprites() -> dict: #returns a dictionary of filepaths
    # Initialize dictionary to store filepaths to sprites
    # The name of each key needs to appear in the title of the corresponding file
    sprites_dict = {
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
    
    #TODO: Ensure the current directory is the project's working directory -> possibly in main ?
    project_dir = os.getcwd()
    print(f"Current working directory: {project_dir}")
    
    # Set the directory path containing the sprites
    sprites_dir = os.path.join('.','sprites','png')
    
    # Get the filenames of all files in that dir
    try:
        _, _, sprites_filenames = next(os.walk(sprites_dir))
    except StopIteration:
        print(f"Initialization: Directory {sprites_dir} not found or empty.")
        return sprites_dict

    #Use filepaths to load sprites as pygame images for the corresponding sprite in the sprites dictionary
    for key in sprites_dict:
        for filename in sprites_filenames:
            if key in filename:
                sprite_filepath = os.path.join(sprites_dir,filename)
                sprite_image = pygame.image.load(sprite_filepath)
                #TODO: fix scaling of sprites for the pieces (need to be slightly smaller + something wrong with the look)
                sprite_image = pygame.transform.scale(sprite_image,(SPRITE_WIDTH,SPRITE_HEIGHT))
                sprites_dict[key] = sprite_image
                break
    
    return sprites_dict

SPRITES_DICT = load_sprites()