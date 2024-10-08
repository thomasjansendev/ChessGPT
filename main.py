import pygame
from src.utilities import *
from src.constants import *
from src.move import *
from src.pieces import *
from src.sprites import *
from src.board import *

def main():
    
    # Pygame Initialization
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    dt = 0
    
    # Chess Initialization
    board, pieces = init_pieces(init_board_dict())
    current_player = colour.WHITE
    
    # Game state variables
    dragging = False
    grabbed_piece = None
    possible_moves = None
    turn_number = 1
    gamelog = {}
    
    while running:

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT: 
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                for square in board:
                    square_dict = board[square]
                    if square_dict["piece"] != None and square_dict["piece"].colour == current_player and square_dict["piece"].rect.collidepoint(event.pos):
                        dragging = True
                        grabbed_piece = square_dict["piece"]
                        grabbed_piece.rect.center = (event.pos[0],event.pos[1]) #snap piece to mouse
                        
                        possible_moves = grabbed_piece.get_legal_moves(board_dict_to_array(board), pieces)
                        
                        print(possible_moves)
                        square_of_origin = square_dict #used to return piece to square in case move is invalid 
                        square_dict["piece"] = None #removes piece from square
                        break
                    
            elif event.type == pygame.MOUSEMOTION and grabbed_piece != None:
                if dragging:
                    grabbed_piece.rect.center = (event.pos[0],event.pos[1])
            
            elif event.type == pygame.MOUSEBUTTONUP and grabbed_piece != None:
                #TODO: find a more efficient way to do find the square a mouse is hovering over -> .collidedict perhaps
                #TODO: solution: only check the squares corresponding to the possible moves
                piece_moved_successfuly = False
                for square in possible_moves:
                    square_rect = board[square]["rect"]
                    square_content = board[square]["piece"]
                    if square_rect.collidepoint(event.pos):
                        # check if an enemy piece is on the square and capture it  
                        if square_content != None and square_content.colour != grabbed_piece.colour:
                            pieces = capture_piece(square_content,pieces)
                        # update board square with new piece
                        board[square]["piece"] = grabbed_piece
                        grabbed_piece.rect.center = square_rect.center
                        # update game state since move is succesful
                        piece_moved_successfuly = True
                        current_player = change_current_player(current_player)
                        gamelog, turn_number = update_gamelog(gamelog,turn_number,grabbed_piece,square)              
                        print_gamelog(gamelog)
                        break
                    
                if not piece_moved_successfuly:
                    grabbed_piece.rect.center = square_of_origin["rect"].center  
                    square_of_origin["piece"] = grabbed_piece
                           
                dragging = False
                grabbed_piece = None
                possible_moves = None
                
                
        screen.fill("black")
        

        #TODO: make it so that you draw board only once
        #TODO: only update the piece being moved (instead of redrawing every piece)
        for square in board:
            #draw squares
            img, rect = board[square]['img'], board[square]['rect']
            screen.blit(img,rect)
            #draw pieces
            piece = board[square]['piece']
            if piece != None and piece != grabbed_piece:
                screen.blit(piece.img,piece.rect)
        #draw possible moves
        if possible_moves != None:
            for move in possible_moves:
                pygame.draw.circle(screen, (0,0,0), board[move]['rect'].center, 10)
        #draw new position of grabbed_piece
        if grabbed_piece != None:
            screen.blit(grabbed_piece.img,grabbed_piece.rect) #drawn last to stay on top of other sprites
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()