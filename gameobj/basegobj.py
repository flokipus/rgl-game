from __future__ import annotations
import pygame
from typing import Union, overload

from utils.utils import Vec2


class GameObject:
    """Base class for all game objects (objects that represents something visible (or not) in game)
    """

    __class_id_counter = 0

    def __init__(self, *, pos: Vec2, name: str = '', sprite: Union[None, pygame.Surface] = None):
        self.pos = pos
        self.sprite = sprite
        self.name = name
        self.__id = GameObject.__class_id_counter
        GameObject.__class_id_counter += 1

    def __hash__(self) -> int:
        return hash(self.__id)

    def __eq__(self, other: GameObject) -> bool:
        return self.__id == other.__id

    @property
    def id(self) -> int:
        return self.__id

    @overload
    def update(self) -> None: ...

    @overload
    def get_pos(self) -> Vec2: ...

    @overload
    def set_pos(self, new_pos: Vec2) -> None: ...

    @overload
    def get_sprite(self) -> pygame.Surface: ...

    """Implementation block
    """
    def update(self) -> None:
        pass

    def get_pos(self) -> Vec2:
        return self.pos

    def set_pos(self, new_pos: Vec2) -> None:
        self.pos = new_pos

    def get_sprite(self) -> pygame.Surface:
        return self.sprite
