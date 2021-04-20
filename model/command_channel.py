from typing import Union, overload

from .command import ModelCommand


class ModelCommandChannel:
    """
    Base class for command channel
    """
    @overload
    def request_command(self) -> Union[None, ModelCommand]: ...

    @overload
    def put_command(self, command: ModelCommand) -> None: ...

    def request_command(self) -> Union[None, ModelCommand]:
        return None


class UserCommandChannel(ModelCommandChannel):
    """TODO: Гибкая настройка key_map -> command, обработка gui + mouse"""
    def __init__(self) -> None:
        self.command_buffer = list()

    def request_command(self) -> Union[None, ModelCommand]:
        if len(self.command_buffer) == 0:
            return None
        else:
            command = self.command_buffer[0]
            self.command_buffer.pop(0)
            return command

    def put_command(self, command: ModelCommand) -> None:
        self.command_buffer.append(command)


class AIRandMoveCC(ModelCommandChannel):
    def request_command(self) -> Union[None, ModelCommand]:
        return MOVE_ONE_TILE[move]
