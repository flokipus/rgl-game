from pygame import Surface


class Sprite:
    def __init__(self, surface: Surface, offset_xy: tuple = (0, 0)):
        self.surface = surface
        self.offset_xy = offset_xy
