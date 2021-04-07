from __future__ import annotations
from typing import Union, overload
import pygame

from command.command import Command, MoveCommand
from gameobj.basegobj import GameObject
from utils.utils import Vec2


class BaseState:
    @overload
    def update(self, *, gobj: GameObject) -> Union[None, BaseState]: ...

    @overload
    def handle_command(self, *, gobj: GameObject, command: Command) -> Union[None, BaseState]: ...

    @overload
    def enter(self, *, gobj: GameObject, old_state: BaseState) -> None: ...

    @overload
    def exit(self, *, gobj: GameObject, next_state: BaseState) -> None: ...

    @overload
    def ready(self) -> bool: ...

    """Empty implementations
    """
    def update(self, *, gobj: GameObject) -> Union[None, BaseState]:
        pass

    def handle_command(self, *, gobj: GameObject, command: Command) -> Union[None, BaseState]:
        pass

    def enter(self, *, gobj: GameObject, old_state: BaseState) -> None:
        pass

    def exit(self, *, gobj: GameObject, next_state: BaseState) -> None:
        pass

    def ready(self) -> bool:
        return True


class Standing(BaseState):
    def __init__(self):
        pass

    def update(self, *, gobj: GameObject) -> Union[None, BaseState]:
        return None

    def handle_command(self, *, gobj: GameObject, command: Command) -> Union[None, BaseState]:
        if isinstance(command, MoveCommand):
            return Moving(command.dij)
        else:
            return None

    def enter(self, *, gobj: GameObject, old_state: BaseState) -> None:
        return None

    def exit(self, *, gobj: GameObject, next_state: BaseState) -> None:
        return None


class Moving(BaseState):
    def __init__(self, dij: Vec2, time_to_move: float = 0.3):
        self.ij_from = None
        self.dij = dij
        self.time_to_move = time_to_move
        self.time_begin = 0.0

    def enter(self, *, gobj: GameObject, old_state: BaseState) -> None:
        self.time_begin = pygame.time.get_ticks()
        self.ij_from = gobj.get_pos()

    def update(self, *, gobj: GameObject) -> Union[None, BaseState]:
        cur_time = pygame.time.get_ticks()  # in seconds
        delta_time = min((cur_time - self.time_begin) / 1000, self.time_to_move)
        new_pos = self.ij_from + self.dij * delta_time / self.time_to_move
        gobj.set_pos(new_pos)
        if delta_time == self.time_to_move:
            return Standing()
        else:
            return None

    def handle_command(self, *, gobj: GameObject, command: Command) -> Union[None, BaseState]:
        return None

    def ready(self) -> bool:
        return False
