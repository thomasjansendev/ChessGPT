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
    grabbed_piece = None
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                for key in board:
                    if board[key]["piece"] != None and board[key]["piece"].rect.collidepoint(event.pos):
                        dragging = True
                        grabbed_piece = board[key]["piece"]
                        grabbed_piece.rect.center = (event.pos[0],event.pos[1])
                        board[key]["piece"] = None #remove piece from square
                        print(grabbed_piece)
                        print(f"{grabbed_piece.id}.{key}")
                        break
                        
            elif event.type == pygame.MOUSEMOTION and grabbed_piece != None:
                if dragging:
                    grabbed_piece.rect.center = (event.pos[0],event.pos[1])
                    
            elif event.type == pygame.MOUSEBUTTONUP and grabbed_piece != None:
                #TODO: update board_dictionary with new piece location
                for key in board: #TODO: find a more efficient way to do find the square a mouse is hovering over -> .collidedict perhaps
                    square_rect = board[key]["rect"]
                    if square_rect.collidepoint(event.pos):
                        grabbed_piece.rect.topleft = (square_rect.x,square_rect.y)
                        board[key]["piece"] = grabbed_piece #add piece to square
                        print(key)
                        break
                dragging = False
                grabbed_piece = None
                
                
        screen.fill("black")
        
        #TODO: make it so that you draw board only once
        #TODO: only update the piece being moved (instead of redrawing every piece)
        for key in board:
            #draw squares
            img, rect = board[key]['img'], board[key]['rect']
            screen.blit(img,rect)
            #draw pieces
            piece = board[key]['piece']
            if piece != None and piece != grabbed_piece:
                screen.blit(piece.img,piece.rect)
        if grabbed_piece != None:
            screen.blit(grabbed_piece.img,grabbed_piece.rect)#drawn last to stay on top of other sprites
        
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