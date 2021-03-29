from __future__ import annotations
from typing import NamedTuple, overload, Union
from numpy import ndarray

from settings.screen import *


class Vec2i:
    def __init__(self, x: int, y: int):
        self.xy = (x, y)

    @property
    def x(self) -> int:
        return self.xy[0]

    @property
    def y(self) -> int:
        return self.xy[1]

    def __add__(self, other: Vec2i) -> Vec2i:
        return Vec2i(x=self.x + other.x, y=self.y + other.y)

    def __mul__(self, other: Union[int, float, Vec2i]) -> Union[Vec2i, int]:
        if isinstance(other, int) or isinstance(other, float):
            return Vec2i(x=int(self.x * other), y=int(self.y * other))
        elif isinstance(other, Vec2i):
            return self.x * other.x + self.y * other.y
        else:
            raise AttributeError('Wrong type of other! Expected Union[int, Vec2i], given is {}'.format(type(other)))

    def dot(self, other: Vec2i) -> Vec2i:
        return Vec2i(x=self.x * other.x, y=self.y * other.y)

    def __sub__(self, other: Vec2i) -> Vec2i:
        return Vec2i(x=self.x - other.x, y=self.y - other.y)

    def __floordiv__(self, other: int) -> Vec2i:
        return Vec2i(x=self.x // other, y=self.y // other)

    def __getitem__(self, index: int) -> int:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise AttributeError('index >= 1 !')

    def __str__(self) -> str:
        return '({},{})'.format(self.x, self.y)


def pixel_pos_to_descartes(pixel_pos: Vec2i) -> Vec2i:
    x = pixel_pos.x
    y = MAP_HEIGHT - pixel_pos.y
    return Vec2i(x=x, y=y)


def pixel_pos_to_cell(pixel_pos: Vec2i) -> Vec2i:
    descartes_pos = pixel_pos_to_descartes(pixel_pos)
    cell_i = descartes_pos.x // CELL_WIDTH
    cell_j = descartes_pos.y // CELL_HEIGHT
    return Vec2i(x=cell_i, y=cell_j)


if __name__ == '__main__':
    v1 = Vec2i(x=15, y=16)
    v2 = Vec2i(x=10, y=20)
    print(v1)
    print(v1+v2)
    print(v1[0])
    print(v1 * v2)
    print(v1.dot(v2))
