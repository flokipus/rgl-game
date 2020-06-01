import pygame


class AsciiCellCreator:
    def __init__(self, font, default_background_size: tuple):
        self._font = font
        self._background_size = default_background_size

    def create(self, symbol: str, symb_color: pygame.Color, back_color: pygame.Color,
               antialias: bool = True, symbol_pos=None):
        letter = self._font.render(symbol, antialias, symb_color)
        surface = pygame.Surface(self._background_size, pygame.SRCALPHA)
        surface.fill(back_color)
        if symbol_pos is None:
            symsize = letter.get_size()
            surfsize = surface.get_size()
            x = (surfsize[0] - symsize[0])//2
            y = (surfsize[1] - symsize[1])//2
            symbol_pos = (x, y)
        surface.blit(letter, symbol_pos)
        return surface

    @property
    def get_back_size(self):
        return self._background_size

    @property
    def get_font(self):
        return self._font

    def set_size(self, size: tuple):
        self._background_size = size

    def set_font(self, font: pygame.font):
        self._font = font


class BackgroundCreator:
    def __init__(self, default_background_size: tuple):
        self._back_size = default_background_size

    @property
    def get_size(self):
        return self._back_size
