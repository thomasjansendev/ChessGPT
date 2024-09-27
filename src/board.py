import pygame
from src.sprites import SPRITES_DICT

rows, cols = 8, 8
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512
SPRITE_WIDTH = SCREEN_WIDTH / cols
SPRITE_HEIGHT = SCREEN_HEIGHT / rows
CELL_WIDTH, CELL_HEIGHT = SPRITE_WIDTH, SPRITE_HEIGHT

square_dark_image = pygame.image.load(SPRITES_DICT["square_dark"])
square_dark_image = pygame.transform.scale(square_dark_image, (SPRITE_WIDTH, SPRITE_HEIGHT))

square_light_image = pygame.image.load(SPRITES_DICT["square_light"])
square_light_image = pygame.transform.scale(square_light_image, (SPRITE_WIDTH, SPRITE_HEIGHT))

