from typing import overload, Union
import random

from ..command import ModelCommand, MOVE_ONE_TILE


class AIProcessor:
    @overload
    def process_context(self) -> Union[None, ModelCommand]: ...


class RandomMoveAI(AIProcessor):
    def __init__(self):
        self.__moves = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    def process_context(self) -> Union[None, ModelCommand]:
        move = self.__moves[random.randint(0, 3)]
        return MOVE_ONE_TILE[move]
