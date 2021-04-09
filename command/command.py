from typing import overload, Union
from enum import Enum

from utils.utils import Vec2


class Command:
    pass


class ExitCommand(Command):
    pass


class SaveAndExitCommand(Command):
    pass


class MoveCommand(Command):
    def __init__(self, dij: Vec2):
        self.dij = dij


MOVE_ONE_TILE = {
    'UP': MoveCommand(Vec2(0, 1)),
    'DOWN': MoveCommand(Vec2(0, -1)),
    'LEFT': MoveCommand(Vec2(-1, 0)),
    'RIGHT': MoveCommand(Vec2(1, 0)),
    'WAIT': MoveCommand(Vec2(0, 0))
}


if __name__ == '__main__':
    pass
