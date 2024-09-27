import os

def load_sprites() -> dict:
    #Initialize dictionary to store filepaths to sprites
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
    
    #Get the directory containing the sprites and the filenames
    sprites_dir = os.path.join('.','sprites','png')
    try:
        _, _, sprites_filenames = next(os.walk(sprites_dir))
    except StopIteration:
        print(f"Initialization: Directory {sprites_dir} not found or empty.")
        return sprites_dict

    #Assign filepath to each sprite in the sprite dictionary for future reference
    for key in sprites_dict:
        for filename in sprites_filenames:
            if key in filename:
                sprites_dict[key] = os.path.join(sprites_dir,filename)
                # print(f"{key}: {sprites_dict[key]}")
    
    return sprites_dict

SPRITES_DICT = load_sprites()