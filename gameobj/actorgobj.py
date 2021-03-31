from queue import Queue
import pygame
from typing import Union

from gameobj.states import BaseState
from gameobj.basegobj import GameObject
from utils.utils import Vec2i
from command.command import Command


class Actor(GameObject):
    def __init__(self, pos: Vec2i, base_state: BaseState, command_channel: list, sprite: pygame.Surface):
        GameObject.__init__(self, pos, sprite)
        self._state = base_state
        self._command_channel = command_channel
        self._current_command = None

    def update(self) -> None:
        return_state = self._state.update(gobj=self)
        if return_state is not None:
            self.set_new_state(return_state)

    def set_new_state(self, new_state: BaseState) -> None:
        self._state.exit(gobj=self, next_state=new_state)
        old_state = self._state
        self._state = new_state
        self._state.enter(gobj=self, old_state=old_state)

    def handle_command(self) -> None:
        return_state = self._state.handle_command(gobj=self, command=self._current_command)
        if return_state is not None:
            self.set_new_state(return_state)

    def request_command(self) -> Union[None, Command]:
        if not len(self._command_channel) == 0:
            self._current_command = self._command_channel[0]
            self._command_channel.pop(0)
        else:
            self._current_command = None
        return self._current_command

    def has_command(self) -> bool:
        return self._current_command is not None

    @property
    def get_current_command(self):
        return self._current_command

    def ready_to_move(self) -> bool:
        return self._state.ready()
