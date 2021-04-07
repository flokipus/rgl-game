from typing import overload, Union
import random

from command.command import Command, MOVE_ONE_TILE


class AIProcessor:
    @overload
    def process_context(self) -> Union[None, Command]: ...


class SimpleAgressiveAI(AIProcessor):
    def __init__(self, context):
        self.__context = context


class RandomMoveAI(AIProcessor):
    def __init__(self):
        self.__moves = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    def process_context(self) -> Union[None, Command]:
        move = self.__moves[random.randint(0, 3)]
        return MOVE_ONE_TILE[move]
