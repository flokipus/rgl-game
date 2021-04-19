from pygame import Surface

from utils.utils import Vec2i


class Sprite:
    def __init__(self, surface: Surface):
        self.surface = surface

    def draw_at_pos(self, surface_where: Surface, pixel_offset: Vec2i) -> None:
        surface_where.blit(self.surface, (pixel_offset.x, pixel_offset.y))
