import pygame
from typing import Union, overload

from .command import Command, MoveOneTile
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


class UICommandChannel(CommandChannel):
    """TODO: Гибкая настройка key_map -> command, обработка gui + mouse"""
    def __init__(self, kb_processor: UserKeyboardProcessor) -> None:
        self._kb_proc = kb_processor
        self._key_map = {pygame.K_UP: MoveOneTile.UP, pygame.K_w: MoveOneTile.UP,
                         pygame.K_DOWN: MoveOneTile.DOWN, pygame.K_s: MoveOneTile.DOWN,
                         pygame.K_LEFT: MoveOneTile.LEFT, pygame.K_a: MoveOneTile.LEFT,
                         pygame.K_RIGHT: MoveOneTile.RIGHT, pygame.K_d: MoveOneTile.RIGHT,
                         None: None}

    def request_command(self) -> Union[None, Command]:
        input = self._kb_proc.process_input()
        try:
            return self._key_map[input]
        except KeyError as e:
            return None


class AICommandChannel(CommandChannel):
    """TODO: Это просто заглушка"""
    def __init__(self, ai_processor: AIProcessor) -> None:
        self._ai_proc = ai_processor

    def request_command(self) -> Union[None, Command]:
        return self._ai_proc.process_context()
