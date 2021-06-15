from __future__ import annotations
import pygame
from typing import Union

from common.utils.utils import Vec2i


class GameObject:
    """Base class for all game objects (objects that represents something visible (or not) in game)
    """

    __slots__ = ('_pos', '_sprite', '_name', '__id')

    __class_id_counter = 0

    def __init__(self, *, pos: Vec2i, name: str = '', sprite: Union[None, pygame.Surface] = None):
        self._pos = pos
        self._sprite = sprite
        self._name = name
        self.__id = GameObject.__class_id_counter
        GameObject.__class_id_counter += 1

    def __hash__(self) -> int:
        return hash(self.__id)

    def __eq__(self, other: GameObject) -> bool:
        return self.__id == other.__id

    @property
    def id(self) -> int:
        return self.__id

    """Implementation block
    """
    def update(self) -> None:
        pass

    def get_pos(self) -> Vec2i:
        return self._pos

    def set_pos(self, new_pos: Vec2i) -> None:
        self._pos = new_pos

    def get_sprite(self) -> pygame.Surface:
        return self._sprite

    def set_sprite(self, new_sprite: pygame.Surface) -> None:
        self._sprite = new_sprite

    def get_name(self) -> str:
        return self._name

    def set_name(self, new_name):
        self._name = new_name


if __name__ == '__main__':
    from sys import getsizeof
    sp = pygame.Surface(size=(15, 155))
    test_gobj1 = GameObject(pos=Vec2i(1, 2), name='Monster', sprite=sp)
    print(getsizeof(test_gobj1))
    test_gobj2 = GameObject(pos=Vec2i(1, 2), name='Monster2', sprite=None)
    print(getsizeof(test_gobj2))
    test_gobj3 = GameObject(pos=Vec2i(1, 2), name='Monster3', sprite=None)
    print(getsizeof(test_gobj3))
    print(getsizeof(test_gobj3))
