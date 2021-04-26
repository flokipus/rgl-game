from __future__ import annotations
from typing import Union, overload
from time import time
import math

from .visualisation import Visualisation
from common.utils import utils


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
                 time_to_move: float,
                 fps: int):
        self.dxy = dxy
        self.time_to_move = time_to_move
        self.initial_offset_xy = None
        self.time_begin = 0.0
        self.fps = fps

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
        self.time_begin = time() - 1/self.fps
        self.initial_offset_xy = visual.get_pixel_offset()

    def exit(self, *, visual: Visualisation, next_state: BaseState) -> None:
        visual.set_pixel_xy_offset(self.initial_offset_xy + self.dxy)

    def ready(self) -> bool:
        return False


class MeleeAttacking(BaseState):
    def __init__(self, dxy: utils.Vec2i, time_to_attack: float, max_amplitude_ratio: float, fps: int) -> None:
        self.dxy = dxy
        self.time_to_attack = time_to_attack
        self.max_amplitude_ratio = max_amplitude_ratio
        self.fps = fps
        self.time_begin = None
        self.initial_offset_xy = None

    def enter(self, *, visual: Visualisation, old_state: BaseState) -> None:
        self.time_begin = time() - 1/self.fps
        self.initial_offset_xy = visual.get_pixel_offset()

    def exit(self, *, visual: Visualisation, next_state: BaseState) -> None:
        visual.set_pixel_xy_offset(self.initial_offset_xy)

    @staticmethod
    def amplitude(r: float) -> float:
        return math.sin(2 * math.pi * r)

    def update(self, *, visual: Visualisation) -> Union[None, BaseState]:
        current_time = time()
        elapsed_time = current_time - self.time_begin
        r = min(1.0, elapsed_time / self.time_to_attack)
        if r < 1.0:
            delta_offset = self.dxy * MeleeAttacking.amplitude(r) * self.max_amplitude_ratio
            print('delta_offset: {}'.format(delta_offset))
            old_offset = visual.get_pixel_offset()
            visual.set_pixel_xy_offset(old_offset + delta_offset)
            return None
        else:
            return BaseState()
