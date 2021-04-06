import pygame
from typing import Union, overload

from gameobj.states import BaseState
from gameobj.basegobj import GameObject
from utils.utils import Vec2i
from command.command_channel import Command, CommandChannel


class Actor(GameObject):
    def __init__(self, pos: Vec2i, base_state: BaseState,
                 command_channel: CommandChannel, sprite: pygame.Surface) -> None:
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
        self._current_command = self._command_channel.request_command()
        return self._current_command

    def has_command(self) -> bool:
        return self._current_command is not None

    def set_command_channel(self, command_channel) -> CommandChannel:
        prev_ch = self._command_channel
        self._command_channel = command_channel
        return prev_ch

    @property
    def get_current_command(self):
        return self._current_command

    def ready_to_move(self) -> bool:
        return self._state.ready()
