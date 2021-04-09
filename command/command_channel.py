import pygame
from typing import Union, overload

from .command import Command, MOVE_ONE_TILE
from user_input.keyboard_processor import UserKeyboardProcessor
from ai.aiprocessor import AIProcessor


class CommandChannel:
    """
    Base class for command channel
    """
    @overload
    def request_command(self) -> Union[None, Command]: ...

    def request_command(self) -> Union[None, Command]:
        return None


class UserCommandChannel(CommandChannel):
    """TODO: Гибкая настройка key_map -> command, обработка gui + mouse"""
    def __init__(self) -> None:
        self.command_buffer = list()

    def request_command(self) -> Union[None, Command]:
        if len(self.command_buffer) == 0:
            return None
        else:
            command = self.command_buffer[0]
            self.command_buffer.pop(0)
            return command

    def put_command(self, command: Command) -> None:
        self.command_buffer.append(command)


class AICommandChannel(CommandChannel):
    """TODO: Это просто заглушка"""
    def __init__(self, ai_processor: AIProcessor) -> None:
        self._ai_proc = ai_processor

    def request_command(self) -> Union[None, Command]:
        return self._ai_proc.process_context()
