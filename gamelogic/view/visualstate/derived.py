from __future__ import annotations
from typing import Union
from time import time
import math

from ..visualisation import Visualisation
from .basic import VisualState
from common.utils import utils


class Moving(VisualState):
    def __init__(self,
                 dxy: utils.Vec2i,
                 time_to_move: float,
                 fps: int):
        self.dxy = dxy
        self.time_to_move = time_to_move
        self.initial_offset_xy = None
        self.time_begin = 0.0
        self.fps = fps

    def update(self, *, owner: Visualisation) -> Union[None, VisualState]:
        current_time = time()
        elapsed_time = current_time - self.time_begin
        r = min(1.0, elapsed_time / self.time_to_move)
        owner.set_pixel_xy_offset((self.initial_offset_xy + self.dxy * r))
        if elapsed_time > self.time_to_move:
            return VisualState()
        else:
            return None

    def enter(self, *, owner: Visualisation, old_state: VisualState) -> None:
        self.time_begin = time() - 1/self.fps
        self.initial_offset_xy = owner.get_pixel_offset()

    def exit(self, *, owner: Visualisation, next_state: VisualState) -> None:
        owner.set_pixel_xy_offset(self.initial_offset_xy + self.dxy)


class MeleeAttacking(VisualState):
    def __init__(self, dxy: utils.Vec2i, time_to_attack: float, max_amplitude_ratio: float, fps: int) -> None:
        self.dxy = dxy
        self.time_to_attack = time_to_attack
        self.max_amplitude_ratio = max_amplitude_ratio
        self.fps = fps
        self.time_begin = None
        self.initial_offset_xy = None

    def enter(self, *, owner: Visualisation, old_state: VisualState) -> None:
        self.time_begin = time() - 1/self.fps
        self.initial_offset_xy = owner.get_pixel_offset()

    def exit(self, *, owner: Visualisation, next_state: VisualState) -> None:
        owner.set_pixel_xy_offset(self.initial_offset_xy)

    @staticmethod
    def amplitude(r: float) -> float:
        return math.sin(2 * math.pi * r)

    def update(self, *, owner: Visualisation) -> Union[None, VisualState]:
        current_time = time()
        elapsed_time = current_time - self.time_begin
        r = min(1.0, elapsed_time / self.time_to_attack)
        if r < 1.0:
            delta_offset = self.dxy * MeleeAttacking.amplitude(r) * self.max_amplitude_ratio
            print('delta_offset: {}'.format(delta_offset))
            old_offset = owner.get_pixel_offset()
            owner.set_pixel_xy_offset(old_offset + delta_offset)
            return None
        else:
            return VisualState()
