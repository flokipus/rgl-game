from typing import overload, Union

from command.command import Command, MOVE_ONE_TILE


class AIProcessor:
    @overload
    def process_context(self) -> Union[None, Command]: ...

    def process_context(self) -> Union[None, Command]:
        return MOVE_ONE_TILE['UP']


class SimpleAgressiveAI(AIProcessor):
    def __init__(self, context):
        self.__context = context
