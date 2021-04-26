from typing import Union, overload
import random

from . import command
from common.utils import utils as utils


class ModelCommandChannel:
    """
    Base class for command channel
    """
    @overload
    def request_command(self) -> Union[None, command.ModelCommand]: ...

    @overload
    def put_command(self, command: command.ModelCommand) -> None: ...

    def request_command(self) -> Union[None, command.ModelCommand]:
        pass

    def put_command(self, command: command.ModelCommand) -> None:
        pass


class UserCommandChannel(ModelCommandChannel):
    """TODO: Гибкая настройка key_map -> command, обработка gui + mouse"""
    def __init__(self) -> None:
        self.command_buffer = list()
        self.max_buffer_len = 2

    def request_command(self) -> Union[None, command.ModelCommand]:
        if len(self.command_buffer) == 0:
            return None
        else:
            command = self.command_buffer[0]
            self.command_buffer.pop(0)
            return command

    def put_command(self, command: command.ModelCommand) -> None:
        if len(self.command_buffer) == self.max_buffer_len:
            self.command_buffer.pop(0)
        self.command_buffer.append(command)


class AIRandMoveCC(ModelCommandChannel):
    __moves = [
        command.GobjWaitCommand(),  # Stand
        command.MoveGobjCommand(utils.Vec2i(1, 0)),  # Move right
        command.MoveGobjCommand(utils.Vec2i(-1, 0)),  # Move left
        command.MoveGobjCommand(utils.Vec2i(0, 1)),  # Move top
        command.MoveGobjCommand(utils.Vec2i(0, -1)),  # Move bot
    ]

    def request_command(self) -> Union[None, command.ModelCommand]:
        move_num = random.randint(0, 4)
        return self.__moves[move_num]
