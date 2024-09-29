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
    #board = init_board_array()
    board = set_pieces(init_board_dict())
    current_player = Color.WHITE
    
    #temporary variable to help with dev
    center_x, center_y = SCREEN_WIDTH/2, SCREEN_HEIGHT/2               
    piece = Queen(Color.WHITE)
    piece_img = piece.sprite
    piece_img_rect = piece_img.get_rect(topleft=(center_x, center_y))
    dragging = False
    
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if piece_img_rect.collidepoint(event.pos):
                    dragging = True
                    piece_img_rect.center = (event.pos[0],event.pos[1])
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    piece_img_rect.center = (event.pos[0],event.pos[1])
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                for square in board:
                    square_rect = board[square]["rect"]
                    if square_rect.collidepoint(event.pos):
                        piece_img_rect.topleft = (square_rect.x,square_rect.y)
                
                
        screen.fill("black")
        
        #TODO: make this a onetime operation instead of drawing each cell individually each frame -> input to screen.fill ?
        for key in board:
            img = board[key]['img']
            rect = board[key]['rect']
            screen.blit(img,rect)
        
        screen.blit(square_img,square_img_rect)
        screen.blit(piece_img, piece_img_rect)

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