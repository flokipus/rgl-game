from typing import overload, Union

from command.command import Command


class AIProcessor:
    @overload
    def process_context(self) -> Union[None, Command]: ...

    def process_context(self) -> Union[None, Command]:
        return None


class SimpleAgressiveAI(AIProcessor):
    def __init__(self, context):
        self.__context = context
