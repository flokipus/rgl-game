from typing import overload, Union
from enum import Enum

from utils.utils import Vec2i


class Command:
    pass


class MoveCommand(Command):
    def __init__(self, dij: Vec2i):
        self.dij = dij


MOVE_ONE_TILE = {
    'UP': MoveCommand(Vec2i(0, 1)),
    'DOWN': MoveCommand(Vec2i(0, -1)),
    'LEFT': MoveCommand(Vec2i(-1, 0)),
    'RIGHT': MoveCommand(Vec2i(1, 0))
}


if __name__ == '__main__':
    pass
