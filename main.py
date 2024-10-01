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
    possible_moves = None
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                for key in board:
                    square_dict = board[key]
                    if square_dict["piece"] != None and square_dict["piece"].rect.collidepoint(event.pos):
                        dragging = True
                        grabbed_piece = square_dict["piece"] 
                        grabbed_piece.rect.center = (event.pos[0],event.pos[1]) #snap piece to mouse
                        possible_moves = grabbed_piece.calc_possible_moves(board_dict_to_array(board))
                        print(f"Possible moves: {possible_moves}")
                        square_of_origin = square_dict #used to return piece to square in case move is invalid 
                        square_dict["piece"] = None #removes piece from square
                        break
                        
            elif event.type == pygame.MOUSEMOTION and grabbed_piece != None:
                if dragging:
                    grabbed_piece.rect.center = (event.pos[0],event.pos[1])
                    
            elif event.type == pygame.MOUSEBUTTONUP and grabbed_piece != None:
                #TODO: update board_dictionary with new piece location
                for key in board: #TODO: find a more efficient way to do find the square a mouse is hovering over -> .collidedict perhaps
                    square_rect = board[key]["rect"]
                    square_piece = board[key]["piece"]
                    if square_rect.collidepoint(event.pos):
                        if square_piece == None:
                            grabbed_piece.rect.topleft = (square_rect.x,square_rect.y)
                            board[key]["piece"] = grabbed_piece #add piece to square
                            print_algebraic_notation(grabbed_piece,key)
                        else:
                            grabbed_piece.rect.topleft = (square_of_origin["rect"].x,square_of_origin["rect"].y)  
                            square_of_origin["piece"] = grabbed_piece  
                        break
                dragging = False
                grabbed_piece = None
                possible_moves = None
                
                
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
        #draw possible moves
        if possible_moves != None:
            for move in possible_moves:
                pygame.draw.circle(screen, (0,0,0), board[move]['rect'].center, 10)

        if grabbed_piece != None:
            screen.blit(grabbed_piece.img,grabbed_piece.rect) #drawn last to stay on top of other sprites
        
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