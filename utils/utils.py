from __future__ import annotations
from typing import NamedTuple, overload, Union
from numpy import ndarray

from settings.screen import *


class Vec2:
    def __init__(self, x: Union[int, float], y: Union[int, float]):
        self.xy = (x, y)

    @property
    def x(self) -> int:
        return self.xy[0]

    @property
    def y(self) -> int:
        return self.xy[1]

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(x=self.x + other.x, y=self.y + other.y)

    def __truediv__(self, other: Union[int, float, Vec2]) -> Union[Vec2, int]:
        if isinstance(other, int) or isinstance(other, float):
            return Vec2(x=self.x / other, y=self.y / other)
        elif isinstance(other, Vec2):
            return Vec2(x=self.x / other.x, y=self.y / other.y)
        else:
            raise AttributeError('Wrong type of other! Expected Union[int, Vec2i], given is {}'.format(type(other)))

    def __mul__(self, other: Union[int, float, Vec2]) -> Union[Vec2, int]:
        if isinstance(other, int) or isinstance(other, float):
            return Vec2(x=self.x * other, y=self.y * other)
        elif isinstance(other, Vec2):
            return self.x * other.x + self.y * other.y
        else:
            raise AttributeError('Wrong type of other! Expected Union[int, Vec2i], given is {}'.format(type(other)))

    def dot(self, other: Vec2) -> Vec2:
        return Vec2(x=self.x * other.x, y=self.y * other.y)

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(x=self.x - other.x, y=self.y - other.y)

    def __floordiv__(self, other: int) -> Vec2:
        return Vec2(x=self.x // other, y=self.y // other)

    def __getitem__(self, index: int) -> int:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise AttributeError('index >= 1 !')

    def __str__(self) -> str:
        return '({},{})'.format(self.x, self.y)

    def __hash__(self):
        return hash(self.xy)

    def __eq__(self, other: Vec2):
        return self.xy == other.xy


def pixel_pos_to_descartes(pixel_pos: Vec2) -> Vec2:
    x = pixel_pos.x
    y = MAP_HEIGHT - pixel_pos.y
    return Vec2(x=x, y=y)


def pixel_pos_to_cell(pixel_pos: Vec2) -> Vec2:
    descartes_pos = pixel_pos_to_descartes(pixel_pos)
    cell_i = descartes_pos.x // CELL_WIDTH
    cell_j = descartes_pos.y // CELL_HEIGHT
    return Vec2(x=cell_i, y=cell_j)


if __name__ == '__main__':
    v1 = Vec2(x=15, y=16)
    v2 = Vec2(x=10, y=20)
    print(v1)
    print(v1+v2)
    print(v1[0])
    print(v1 * v2)
    print(v1.dot(v2))
