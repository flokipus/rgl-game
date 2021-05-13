# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Union
import random

# from gamelogic.model.command import ModelCommand, MOVE_ONE_TILE
#
#
# class AIProcessor(ABC):
#     @abstractmethod
#     def process_context(self) -> Union[None, ModelCommand]: ...
#
#
# class RandomMoveAI(AIProcessor):
#     def __init__(self):
#         self.__moves = ['UP', 'DOWN', 'LEFT', 'RIGHT']
#
#     def process_context(self) -> Union[None, ModelCommand]:
#         move = self.__moves[random.randint(0, 3)]
#         return MOVE_ONE_TILE[move]
