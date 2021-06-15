from __future__ import annotations
from typing import Union, Tuple


class Vec2i:
    __slots__ = ('xy', )

    def __init__(self, x: Union[int, float], y: Union[int, float]):
        self.xy = (int(x), int(y))

    @property
    def x(self) -> int:
        return self.xy[0]

    @property
    def y(self) -> int:
        return self.xy[1]

    def to_tuple(self) -> Tuple[int, int]:
        return self.xy

    def copy(self) -> Vec2i:
        return Vec2i(self.x, self.y)

    def __add__(self, other: Vec2i) -> Vec2i:
        return Vec2i(x=self.x + other.x, y=self.y + other.y)

    def __truediv__(self, other: Union[int, float, Vec2i]) -> Union[Vec2i, int]:
        if isinstance(other, int) or isinstance(other, float):
            return Vec2i(x=int(self.x / other), y=int(self.y / other))
        elif isinstance(other, Vec2i):
            return Vec2i(x=int(self.x / other.x), y=int(self.y / other.y))
        else:
            raise AttributeError('Wrong type of other! Expected Union[int, Vec2i], given is {}'.format(type(other)))

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

    def __setitem__(self, index: int, value: int) -> None:
        if isinstance(index, int):
            if index == 0:
                old_y = self.xy[1]
                self.xy = int(value), old_y
                return
            if index == 1:
                old_x = self.xy[0]
                self.xy = old_x, int(value)
                return
        raise AttributeError('index error!')

    def __str__(self) -> str:
        return '({},{})'.format(self.x, self.y)

    def __hash__(self):
        return hash(self.xy)

    def __eq__(self, other: Vec2i):
        return self.xy == other.xy


if __name__ == '__main__':
    v1 = Vec2i(x=15, y=16)
    v2 = Vec2i(x=10, y=20)
    print(v1)
    print(v1+v2)
    print(v1[0])
    print(v1 * v2)
    print(v1.dot(v2))

    import sys
    print(sys.getsizeof(v1))
