import pygame
from src.constants import *
from src.move import *
from src.pieces import *
from src.sprites import *
from src.board import *

def main():
    #Pygame Initialization
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    dt = 0
    
    #Chess Initialization
    board = init_board()
    current_player = Color.WHITE
    
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
                
        screen.fill("black")
        
        #TODO: make this a onetime operation instead of drawing each cell individually each frame -> input to screen.fill ?
        is_light = False
        for row in range(ROWS):
            is_light = not is_light
            for col in range(COLS):
                x = col * CELL_WIDTH
                y = row * CELL_HEIGHT
                if is_light: screen.blit(SPRITES_DICT["square_dark"], (x, y))
                else: screen.blit(SPRITES_DICT["square_light"], (x, y))
                is_light = not is_light
                                
        

        pygame.display.flip()
        dt = clock.tick(60) / 1000
    
        

def handle_move() -> None: #temporarily putting code here
    print(f"{current_player.name} to move: ")
    result = None
    while result is None:
        try:
            result = new_move(board,current_player)
            board = result
            print_board(board)
        except Exception as e:
            print(e)
    if current_player == Color.WHITE: current_player = Color.BLACK
    elif current_player == Color.BLACK: current_player = Color.WHITE


if __name__ == "__main__":
    main()