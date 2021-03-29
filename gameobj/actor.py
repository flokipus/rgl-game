from queue import Queue
import pygame

from states.basic import BaseState
from utils import Vec2i
from .base import GameObject


class Actor(GameObject):
    def __init__(self, pos: Vec2i, base_state: BaseState, command_channel: Queue, sprite: pygame.Surface):
        GameObject.__init__(self, pos, sprite)
        self._state = base_state
        self._action_channel = command_channel
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
        self._state.handle_command(gobj=self, command=self._current_command)

    def request_command(self) -> None:
        if not self._action_channel.empty():
            self._current_command = self._action_channel.get()
        else:
            self._current_command = None

    def has_command(self) -> bool:
        return self._current_command is None

    def ready_to_move(self) -> bool:
        return self._state.ready()
