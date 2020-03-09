import pygame

pygame.init()


class AsciiCell:
    """

    """
    def __init__(self, ascii_symbol, font: pygame.font.Font, ascii_symbol_color: pygame.Color,
                 antialias: bool, symbol_pos, cell_background_color: pygame.Color,
                 cell_size: tuple):
        self.ascii_symbol = ascii_symbol
        self.font = font
        self.ascii_symbol_color = ascii_symbol_color
        self.antialias = antialias
        self.symbol_pos = symbol_pos
        self.cell_background_color = cell_background_color
        self.cell_size = cell_size
        self.draw_self()

    def draw_self(self):
        surface_letter = self.font.render(self.ascii_symbol, self.antialias, self.ascii_symbol_color)
        surface_background = pygame.Surface(self.cell_size)
        surface_background.fill(self.cell_background_color)
        surface_background.blit(surface_letter, self.symbol_pos)


def AsciiCell(ascii_symbol, font: pygame.font.Font, ascii_symbol_color: pygame.Color,
                 antialias: bool, symbol_pos, cell_background_color: pygame.Color,
                 cell_size: tuple):
    letter = font.render(ascii_symbol, antialias, ascii_symbol_color)
    surface = pygame.Surface(cell_size)
    surface.fill(cell_background_color)
    surface.blit(letter, symbol_pos)
    return surface

class GraphicSettings:
    FPS = 30


class GameMapConsts:
    WIDTH = 840
    HEIGHT = 620
    SIZE = (WIDTH, HEIGHT)


class AsciiConsts:
    FONT_SIZE = 30
    CELL_WIDTH = 25
    CELL_HEIGHT = 25
    CELL_SIZE = (CELL_WIDTH, CELL_HEIGHT)
    # DEFAULT_BACKGROUND_COLOR = pygame.Color(50, 50, 50)
    # DEFAULT_SYMBOL_COLOR = pygame.Color(255, 255, 255)
    DEFAULT_BACKGROUND_COLOR = (50, 50, 50)
    DEFAULT_SYMBOL_COLOR = (255, 255, 255)
    ANTIALIAS = True
    DEFAULT_FONT = pygame.font.Font(None, FONT_SIZE)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLACK_GREY = (20, 20, 20)
    GREY = (100, 100, 100)
    BLUE = (0, 0, 255)
    YARN_BLUE = (100, 100, 255)


def empty_background():
    symbol = '.'
    symbol_pos = (AsciiConsts.CELL_WIDTH//2, 0)
    return AsciiCell(symbol, AsciiConsts.DEFAULT_FONT, AsciiConsts.DEFAULT_SYMBOL_COLOR,
                     AsciiConsts.ANTIALIAS, symbol_pos, AsciiConsts.DEFAULT_BACKGROUND_COLOR, AsciiConsts.CELL_SIZE)


def wall_background():
    symbol = '#'
    symbol_pos = (AsciiConsts.CELL_WIDTH // 2, AsciiConsts.CELL_HEIGHT // 4)
    return AsciiCell(symbol, AsciiConsts.DEFAULT_FONT, AsciiConsts.DEFAULT_SYMBOL_COLOR,
                     AsciiConsts.ANTIALIAS, symbol_pos, AsciiConsts.DEFAULT_BACKGROUND_COLOR, AsciiConsts.CELL_SIZE)


def main():
    empty = empty_background()
    wall = wall_background()
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
                screen.blit(empty, (i*AsciiConsts.CELL_WIDTH, j*AsciiConsts.CELL_HEIGHT))
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