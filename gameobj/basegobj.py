import pygame
from typing import Union, overload

from utils.utils import Vec2i


class GameObject:
    """Base class for all game objects (objects that represents something visible (or not) in game)
    """
    def __init__(self, pos: Vec2i, sprite: Union[None, pygame.Surface] = None):
        self.pos = pos
        self.sprite = sprite

    @overload
    def update(self) -> None: ...

    @overload
    def get_pos(self) -> Vec2i: ...

    @overload
    def set_pos(self, new_pos: Vec2i) -> None: ...

    """Implementation block   
    """

    def update(self) -> None:
        pass

    def get_pos(self) -> Vec2i:
        return self.pos

    def set_pos(self, new_pos: Vec2i) -> None:
        self.pos = new_pos
