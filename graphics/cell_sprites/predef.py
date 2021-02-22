import pygame
from . import sprite_ascii
from settings import screen
from settings import colors

pygame.init()
__FONT = pygame.font.Font(None, screen.FONT_SIZE)
__cell_creator = sprite_ascii.AsciiCellCreator(__FONT, screen.CELL_SIZE)

wall = __cell_creator.create('#', colors.DEFAULT_SYMBOL_COLOR, colors.TRANSPARENT_COLOR)
human = __cell_creator.create('@', colors.DEFAULT_SYMBOL_COLOR, colors.TRANSPARENT_COLOR)
dot = __cell_creator.create('.', colors.DEFAULT_SYMBOL_COLOR, colors.TRANSPARENT_COLOR)
dragon = __cell_creator.create('D', colors.BLUE, colors.TRANSPARENT_COLOR)

shadow = pygame.draw.ellipse(__cell_creator.create_empty_cell(), (80, 80, 80, 200), (0, 20, 0, 20))

