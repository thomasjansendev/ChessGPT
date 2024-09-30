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
    rect = pygame.Rect(center_x,center_y,CELL_WIDTH,CELL_HEIGHT)     
    test_piece = Queen(Color.WHITE,rect)
    
    dragging = False
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if test_piece.rect.collidepoint(event.pos):
                    dragging = True
                    test_piece.rect.center = (event.pos[0],event.pos[1])
            
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    test_piece.rect.center = (event.pos[0],event.pos[1])
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                #TODO: fix bug moving piece on release
                dragging = False
                for square in board: #TODO: find a more efficient way to do get the rect a mouse is hovering over
                    square_rect = board[square]["rect"]
                    if square_rect.collidepoint(event.pos):
                        test_piece.rect.topleft = (square_rect.x,square_rect.y)
                
                
        screen.fill("black")
        
        #TODO: make it so that you draw board only once
        #TODO: only update the piece being moved (instead of redrawing every piece)
        for key in board:
            img, rect, piece = board[key]['img'], board[key]['rect'], board[key]['piece']
            screen.blit(img,rect)
            if piece != None:
                screen.blit(piece.img,rect)
        
        screen.blit(test_piece.img, test_piece.rect)

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