from settings import screen
from settings import colors
from generators import asciicell
import pygame


pygame.init()
FONT = pygame.font.Font(None, screen.FONT_SIZE)
cell_creator = asciicell.AsciiCellCreator(FONT, screen.CELL_SIZE)


def empty_background():
    return cell_creator.create('.', colors.WHITE, colors.BLACK)


def sand_background():
    return cell_creator.create('.', colors.DEFAULT_SYMBOL_COLOR, colors.SAND_BACKGROUND_COLOR)


def wall_background():
    return cell_creator.create('#', colors.DEFAULT_SYMBOL_COLOR, colors.BLACK)


def player_empty():
    return cell_creator.create('@', colors.BLUE, colors.BLACK)


def symbol_over_transparent(symbol):
    return cell_creator.create(symbol, colors.BLUE, (0, 0, 0, 0))


def sand_background():
    return cell_creator.create('', (0, 0, 0), colors.SAND_BACKGROUND_COLOR)


def empty_cell():
    return cell_creator.create('.', colors.DEFAULT_SYMBOL_COLOR, (0, 0, 0, 0))
