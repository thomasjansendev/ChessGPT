import pygame
from src.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from src.board import Board
from src.utilities import idx_to_name

def main():
    
    # Pygame Initialization
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    dt = 0
    
    # Chess initialization
    board = Board()
    
    # GUI state variables
    dragging = False
    grabbed_piece = None
    possible_moves = None
    
    while running and not board.checkmate:
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT: 
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                for piece in board.active_pieces[board.active_colour]:
                    if piece.rect.collidepoint(event.pos):
                        grabbed_piece = piece
                        grabbed_piece.rect.center = (event.pos[0],event.pos[1]) #snap piece to mouse
                        origin_square = idx_to_name(piece.get_position(board.array)) #calling get_position negates the performance improvement of looping through active pieces of current player -> consider changing this
                        origin_rect = board.sprites[origin_square]["rect"]
                        possible_moves = grabbed_piece.get_legal_moves(board) #called here and in board.update() <- TODO: make this better
                        dragging = True
                        break
            
            elif event.type == pygame.MOUSEMOTION and dragging:
                grabbed_piece.rect.center = (event.pos[0],event.pos[1])                
            
            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                succesful_move = False
                
                for square in possible_moves:
                    if board.sprites[square]["rect"].collidepoint(event.pos):
                        destination_square = square
                        destination_rect = board.sprites[square]["rect"]
                        user_move = origin_square + destination_square
                        try: 
                            board.update(user_move) # In theory, this should never raise an exception since we only loop through possible moves
                            succesful_move = True
                        except Exception as e:
                            print(e)
                        break
                
                if succesful_move:
                    print(board.gamelog)
                else: #if move is not valid then reset position of piece to origin
                    grabbed_piece.rect.center = origin_rect.center
                
                dragging = False
                grabbed_piece = None
                possible_moves = None
                            
                
        screen.fill("black")
        
        # Draw squares
        for square in board.sprites:
            screen.blit(board.sprites[square]["img"],board.sprites[square]["rect"])
        
        # Draw pieces except for grabbed_piece
        for piece in board.active_pieces["w"] + board.active_pieces["b"]:
            if piece == grabbed_piece:
                continue
            screen.blit(piece.img,piece.rect)
        
        # Draw possible_moves
        if possible_moves != None: 
            for square in possible_moves:
                pygame.draw.circle(screen, (0,0,0), board.sprites[square]['rect'].center, 10)
        
        # Draw new position of grabbed_piece
        if grabbed_piece != None:
            screen.blit(grabbed_piece.img,grabbed_piece.rect)
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()