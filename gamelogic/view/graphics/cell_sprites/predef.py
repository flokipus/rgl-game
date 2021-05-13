# -*- coding: utf-8 -*-

import pygame

from . import sprite_ascii
from gamelogic.view.settings import screen
from gamelogic.view.settings import colors

pygame.init()
FONT = pygame.font.Font(None, screen.FONT_SIZE)
CELL_CREATOR = sprite_ascii.AsciiCellCreator(FONT, screen.CELL_SIZE)

wall = CELL_CREATOR.create('#', colors.DEFAULT_SYMBOL_COLOR, colors.TRANSPARENT_COLOR)
human = CELL_CREATOR.create('@', colors.DEFAULT_SYMBOL_COLOR, colors.TRANSPARENT_COLOR)
dot = CELL_CREATOR.create('.', colors.DEFAULT_SYMBOL_COLOR, colors.TRANSPARENT_COLOR)
dragon = CELL_CREATOR.create('D', colors.BLUE, colors.TRANSPARENT_COLOR)
shadow = pygame.draw.ellipse(CELL_CREATOR.create_empty_cell(), (80, 80, 80, 200), (0, 20, 0, 20))

if __name__ == '__main__':
    print(wall.get_size())
    print(dot.get_size())
    pass
