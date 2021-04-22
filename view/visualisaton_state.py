from __future__ import annotations
from typing import Union, overload
from time import time

from .visualisation import Visualisation
from utils import utils


class BaseState:
    @overload
    def update(self, *, visual: Visualisation) -> Union[None, BaseState]: ...

    @overload
    def enter(self, *, visual: Visualisation, old_state: BaseState) -> None: ...

    @overload
    def exit(self, *, visual: Visualisation, next_state: BaseState) -> None: ...

    @overload
    def ready(self) -> bool: ...

    """Empty implementations
    """
    def update(self, *, visual: Visualisation) -> Union[None, BaseState]:
        pass

    def enter(self, *, visual: Visualisation, old_state: BaseState) -> None:
        pass

    def exit(self, *, visual: Visualisation, next_state: BaseState) -> None:
        pass

    def ready(self) -> bool:
        return True


class Moving(BaseState):
    def __init__(self,
                 dxy: utils.Vec2i,
                 time_to_move: float = 0.3):
        self.dxy = dxy
        self.time_to_move = time_to_move
        self.initial_offset_xy = None
        self.time_begin = 0.0

    def update(self, *, visual: Visualisation) -> Union[None, BaseState]:
        current_time = time()
        elapsed_time = current_time - self.time_begin
        r = min(1.0, elapsed_time / self.time_to_move)
        visual.set_pixel_xy_offset((self.initial_offset_xy + self.dxy * r))
        if elapsed_time > self.time_to_move:
            return BaseState()
        else:
            return None

    def enter(self, *, visual: Visualisation, old_state: BaseState) -> None:
        self.time_begin = time()
        self.initial_offset_xy = visual.get_pixel_offset()

    def exit(self, *, visual: Visualisation, next_state: BaseState) -> None:
        visual.set_pixel_xy_offset(self.initial_offset_xy + self.dxy)

    def ready(self) -> bool:
        return False
