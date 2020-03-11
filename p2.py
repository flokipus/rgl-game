import pygame
from CellCreator import *


pygame.init()


class GraphicSettings:
    FPS = 30


class GameMapConsts:
    WIDTH = 840
    HEIGHT = 620
    SIZE = (WIDTH, HEIGHT)


class AsciiConsts:
    FONT_SIZE = 40
    CELL_WIDTH = 25
    CELL_HEIGHT = 25
    CELL_SIZE = (CELL_WIDTH, CELL_HEIGHT)
    # DEFAULT_BACKGROUND_COLOR = pygame.Color(50, 50, 50)
    # DEFAULT_SYMBOL_COLOR = pygame.Color(255, 255, 255)
    DEFAULT_BACKGROUND_COLOR = pygame.Color(50, 50, 50)
    SAND_BACKGROUND_COLOR = pygame.Color(205, 150, 60)
    DEFAULT_SYMBOL_COLOR = pygame.Color(255, 255, 255)
    ANTIALIAS = True
    DEFAULT_FONT = pygame.font.Font(None, FONT_SIZE)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLACK_GREY = (20, 20, 20)
    GREY = (100, 100, 100)
    BLUE = (0, 0, 255)
    YARN_BLUE = (100, 100, 255)


cell_creator = AsciiCellCreator(AsciiConsts.DEFAULT_FONT, AsciiConsts.CELL_SIZE)


def empty_background():
    return cell_creator.create('.', AsciiConsts.WHITE, AsciiConsts.BLACK)


def sand_background():
    return cell_creator.create('.', AsciiConsts.DEFAULT_SYMBOL_COLOR, AsciiConsts.SAND_BACKGROUND_COLOR)


def wall_background():
    return cell_creator.create('#', AsciiConsts.DEFAULT_SYMBOL_COLOR, AsciiConsts.BLACK)


def player_empty():
    return cell_creator.create('@', AsciiConsts.BLUE, AsciiConsts.BLACK)


def symbol_over_transparent():
    return cell_creator.create('F', AsciiConsts.BLUE, (0, 0, 0, 0))


def sand_background():
    return cell_creator.create('', (0, 0, 0), AsciiConsts.SAND_BACKGROUND_COLOR)


def empty_cell():
    return cell_creator.create('.', AsciiConsts.DEFAULT_SYMBOL_COLOR, (0, 0, 0, 0))


layer0 = []
sand_cell0 = sand_background()
for i in range(25):
    hor_line = []
    for j in range(20):
        hor_line.append(sand_cell0)
    layer0.append(hor_line)

layer1 = []
def_back0 = empty_cell()
for i in range(25):
    hor_line = []
    for j in range(20):
        hor_line.append(def_back0)
    layer1.append(hor_line)

class GameObject:
    def __init__(self, visualisation=None, xy=None, interaction=None, *args, **kwargs):
        self._visualisation = visualisation
        self._xy = xy
        self._interaction = interaction

    def interact(self, *args, **kwargs):
        pass


class MapCell(GameObject):
    def __init__(self, visualisation, xy, interaction):
        GameObject.__init__(self, visualisation, xy, interaction)


class MapCell:
    def __init__(self, default_symbol, default_color):
        self._default_symbol = default_symbol
        self._default_color = default_color


def main():
    empty = empty_background()
    sand = sand_background()
    wall = wall_background()
    player = player_empty()
    ss = symbol_over_transparent()
    pygame.init()
    clock = pygame.time.Clock()
    game_display = pygame.display.set_mode(GameMapConsts.SIZE)
    screen = pygame.Surface(GameMapConsts.SIZE)
    screen.fill(AsciiConsts.BLACK)

    running = True
    x, y = float(250), float(250)
    key_pressed = -1
    press_left = 0
    press_right = 1
    press_up = 2
    press_down = 3

    character = AsciiConsts.DEFAULT_FONT.render('@', 1, AsciiConsts.YARN_BLUE)
    character_pos = [20, 20]
    character_old_pos = character_pos.copy()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("User quit the game")
                running = False
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    key_pressed = press_up
                    character_pos[1] -= AsciiConsts.CELL_HEIGHT
                elif event.key == pygame.K_DOWN:
                    key_pressed = press_down
                    character_pos[1] += AsciiConsts.CELL_HEIGHT
                elif event.key == pygame.K_LEFT:
                    key_pressed = press_left
                    character_pos[0] -= AsciiConsts.CELL_WIDTH
                elif event.key == pygame.K_RIGHT:
                    key_pressed = press_right
                    character_pos[0] += AsciiConsts.CELL_WIDTH
                # cell_i, cell_j = pos_to_cell_index(character_old_pos)
                # cells[count_y * cell_i + cell_j].set_letter(letter_in_cell, letter_in_cell_pos)
                # character_old_pos = character_pos.copy()
            elif event.type == pygame.KEYUP:
                key_pressed = -1

        # 0 level
        game_display.fill(AsciiConsts.BLACK)
        screen.fill(AsciiConsts.BLACK_GREY)

        # 2 level: fill prev cell

        for i in range(25):
            for j in range(20):
                screen.blit(layer0[i][j], (i*AsciiConsts.CELL_WIDTH, j*AsciiConsts.CELL_HEIGHT))

        for i in range(25):
            for j in range(20):
                screen.blit(layer1[i][j], (i*AsciiConsts.CELL_WIDTH, j*AsciiConsts.CELL_HEIGHT))

        screen.blit(empty, (AsciiConsts.CELL_WIDTH, AsciiConsts.CELL_HEIGHT))
        screen.blit(wall, (3*AsciiConsts.CELL_WIDTH, 3*AsciiConsts.CELL_HEIGHT))

        screen.blit(player, (5 * AsciiConsts.CELL_WIDTH, 5 * AsciiConsts.CELL_HEIGHT))
        screen.blit(empty, (6 * AsciiConsts.CELL_WIDTH, 6 * AsciiConsts.CELL_HEIGHT))
        screen.blit(player, (6 * AsciiConsts.CELL_WIDTH, 6 * AsciiConsts.CELL_HEIGHT))
        screen.blit(ss, (7 * AsciiConsts.CELL_WIDTH, 6 * AsciiConsts.CELL_HEIGHT))
        # # 1 level: lines of greed
        # for i in range(1, count_x):
        #     startpos = (i * cell_width, 0)
        #     endpos = (i * cell_width, HEIGHT)
        #     pygame.draw.aaline(screen, GREY, startpos, endpos)
        # for i in range(1, count_y):
        #     startpos = (0, i * cell_height)
        #     endpos = (WIDTH, i * cell_height)
        #     pygame.draw.aaline(screen, GREY, startpos, endpos)


        for i in range(5, 10):
            for j in range(10, 14):
                screen.blit(wall, (i * AsciiConsts.CELL_WIDTH, j * AsciiConsts.CELL_HEIGHT))

        game_display.blit(screen, (0, 0))
        pygame.display.update()
        clock.tick(GraphicSettings.FPS)


main()